import type { ExploreParams, ExploreResult, Offer, Destination, PriceCalendar } from "../types/flight";
import type { PriceHistoryPoint, PriceIntelligence } from "../types/priceIntelligence";
import type { Session } from "../types/auth";
import type { Airport, Radar } from "../types/radar";
import type { AppNotification } from "../types/notification";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {}

const FRIENDLY_NETWORK_ERROR = "Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.";

async function fetchJson(path: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(`${API_BASE_URL}${path}`, init);
  } catch {
    throw new ApiError(FRIENDLY_NETWORK_ERROR);
  }
}

// O backend fala snake_case (contrato em docs/v0.2/ARCHITECTURE.md); o
// frontend trabalha em camelCase. Este arquivo é a única fronteira entre
// os dois formatos — nada fora daqui deve conhecer o snake_case da API.

interface OfferWire {
  id: string;
  price: number;
  departure_date: string;
  return_date: string | null;
  duration_minutes: number;
  stops: number;
  airline: string;
}

interface DestinationWire {
  id: string;
  city: string;
  uf: string;
  budget_status: "within_budget" | "near_budget";
  highlight: "best_price" | null;
  best_offer: OfferWire;
  offers: OfferWire[];
}

interface ExploreResponseWire {
  search: {
    origin_city: string;
    budget: number;
    month: string;
    flexible: boolean;
    passengers: number;
  };
  destinations: DestinationWire[];
  near_budget: DestinationWire[];
  metadata: {
    result_count: number;
    cheapest_price: number | null;
  };
}

function mapOffer(offer: OfferWire): Offer {
  return {
    id: offer.id,
    price: offer.price,
    departureDate: offer.departure_date,
    returnDate: offer.return_date,
    durationMinutes: offer.duration_minutes,
    stops: offer.stops,
    airline: offer.airline,
  };
}

function mapDestination(destination: DestinationWire): Destination {
  return {
    id: destination.id,
    city: destination.city,
    uf: destination.uf,
    budgetStatus: destination.budget_status,
    highlight: destination.highlight,
    bestOffer: mapOffer(destination.best_offer),
    offers: destination.offers.map(mapOffer),
  };
}

export async function exploreDestinations(params: ExploreParams): Promise<ExploreResult> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/flights/explore`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        budget: params.budget,
        origin_city: params.originCity,
        month: params.month,
        flexible: params.flexible,
        passengers: params.passengers,
      }),
    });
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos encontrar destinos neste momento. Tente novamente em instantes.");
  }

  const body: ExploreResponseWire = await response.json();

  return {
    search: {
      originCity: body.search.origin_city,
      budget: body.search.budget,
      month: body.search.month,
      flexible: body.search.flexible,
      passengers: body.search.passengers,
    },
    destinations: body.destinations.map(mapDestination),
    nearBudget: body.near_budget.map(mapDestination),
    metadata: {
      resultCount: body.metadata.result_count,
      cheapestPrice: body.metadata.cheapest_price,
    },
  };
}

interface PriceHistoryPointWire {
  price: number;
  observed_at: string;
}

interface PriceIntelligenceWire {
  current_price: number;
  sample_size: number;
  confidence: "LOW" | "MEDIUM" | "HIGH";
  has_sufficient_data: boolean;
  minimum: number | null;
  maximum: number | null;
  mean: number | null;
  median: number | null;
  percentage_vs_mean: number | null;
  percentage_vs_min: number | null;
  score: number | null;
  classification: "EXCELLENT" | "GOOD" | "NORMAL" | "EXPENSIVE" | "VERY_EXPENSIVE" | null;
  history: PriceHistoryPointWire[];
}

function mapPriceIntelligence(body: PriceIntelligenceWire): PriceIntelligence {
  const mapPoint = (point: PriceHistoryPointWire): PriceHistoryPoint => ({
    price: point.price,
    observedAt: point.observed_at,
  });

  return {
    currentPrice: body.current_price,
    sampleSize: body.sample_size,
    confidence: body.confidence,
    hasSufficientData: body.has_sufficient_data,
    minimum: body.minimum,
    maximum: body.maximum,
    mean: body.mean,
    median: body.median,
    percentageVsMean: body.percentage_vs_mean,
    percentageVsMin: body.percentage_vs_min,
    score: body.score,
    classification: body.classification,
    history: body.history.map(mapPoint),
  };
}

/** `null` = a oferta ainda não tem histórico coletado (404 da API) — não é
 * erro, é um estado válido que a UI trata separado ("ainda sem dados"). */
export async function fetchPriceIntelligence(
  offerId: string,
  currentPrice: number,
): Promise<PriceIntelligence | null> {
  let response: Response;
  try {
    response = await fetch(
      `${API_BASE_URL}/flights/price-intelligence/${encodeURIComponent(offerId)}?price=${currentPrice}`,
    );
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos analisar esse preço agora. Tente novamente em instantes.");
  }

  return mapPriceIntelligence(await response.json());
}

interface PriceCalendarWire {
  destination_id: string;
  month: string;
  days: { date: string; price: number }[];
  cheapest_date: string | null;
}

export async function fetchPriceCalendar(destinationId: string, month: string): Promise<PriceCalendar> {
  let response: Response;
  try {
    response = await fetch(
      `${API_BASE_URL}/flights/calendar?destination_id=${encodeURIComponent(destinationId)}&month=${encodeURIComponent(month)}`,
    );
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos carregar o calendário de preços agora. Tente novamente em instantes.");
  }

  const body: PriceCalendarWire = await response.json();
  return {
    destinationId: body.destination_id,
    month: body.month,
    days: body.days,
    cheapestDate: body.cheapest_date,
  };
}

// --- Auth (v0.4) ---------------------------------------------------------

interface TokenResponseWire {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

function isTokenResponse(body: unknown): body is TokenResponseWire {
  return typeof body === "object" && body !== null && "access_token" in body;
}

function toSession(body: TokenResponseWire): Session {
  return {
    accessToken: body.access_token,
    refreshToken: body.refresh_token,
    expiresAt: Date.now() + body.expires_in * 1000,
  };
}

const FRIENDLY_AUTH_ERROR = "Não foi possível completar essa ação. Confira o e-mail e a senha e tente de novo.";

/** O backend sempre devolve `detail` amigável (nunca stack trace cru,
 * CLAUDE.md §15) — usa direto quando presente, com fallback só por segurança. */
async function authErrorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json();
    return typeof body.detail === "string" ? body.detail : FRIENDLY_AUTH_ERROR;
  } catch {
    return FRIENDLY_AUTH_ERROR;
  }
}

/** `null` = cadastro recebido mas aguardando confirmação por e-mail — não é
 * erro, é um estado válido (o backend pode exigir confirmação). */
export async function signup(email: string, password: string): Promise<Session | null> {
  const response = await fetchJson("/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new ApiError(await authErrorMessage(response));
  const body = await response.json();
  return isTokenResponse(body) ? toSession(body) : null;
}

export async function login(email: string, password: string): Promise<Session> {
  const response = await fetchJson("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new ApiError(await authErrorMessage(response));
  return toSession(await response.json());
}

export async function logout(accessToken: string): Promise<void> {
  await fetchJson("/auth/logout", {
    method: "POST",
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

// --- Chamadas autenticadas (Radares, notificações) ------------------------

class AuthRequiredError extends ApiError {}

async function authFetch(path: string, accessToken: string, init?: RequestInit): Promise<Response> {
  const response = await fetchJson(path, {
    ...init,
    headers: { ...init?.headers, Authorization: `Bearer ${accessToken}` },
  });
  if (response.status === 401) throw new AuthRequiredError("Sua sessão expirou. Entre novamente.");
  return response;
}

export { AuthRequiredError };

export interface Me {
  id: string;
  email: string | null;
  role: string;
}

export async function getMe(accessToken: string): Promise<Me> {
  const response = await authFetch("/auth/me", accessToken);
  if (!response.ok) throw new ApiError("Não conseguimos confirmar sua sessão.");
  return response.json();
}

export interface PlatformMetrics {
  totalUsers: number;
  totalRadars: number;
  activeRadars: number;
  totalRadarEvents: number;
  totalNotifications: number;
  newUsers7d: number;
  newRadars7d: number;
}

export async function getPlatformMetrics(accessToken: string): Promise<PlatformMetrics> {
  const response = await authFetch("/admin/metrics", accessToken);
  if (!response.ok) throw new ApiError("Não conseguimos carregar as métricas.");
  const body = await response.json();
  return {
    totalUsers: body.total_users,
    totalRadars: body.total_radars,
    activeRadars: body.active_radars,
    totalRadarEvents: body.total_radar_events,
    totalNotifications: body.total_notifications,
    newUsers7d: body.new_users_7d,
    newRadars7d: body.new_radars_7d,
  };
}

// --- Airports (v0.4 — só pro seletor de origem/destino do Radar) ----------

interface AirportWire {
  id: string;
  code: string;
  name: string;
  city: string;
}

export async function listAirports(): Promise<Airport[]> {
  const response = await fetchJson("/airports");
  if (!response.ok) throw new ApiError("Não conseguimos carregar a lista de aeroportos.");
  const body: AirportWire[] = await response.json();
  return body;
}

// --- Radares (v0.4) --------------------------------------------------------

interface RadarWire {
  id: string;
  name: string;
  origin_airport_id: string;
  destination_airport_id: string;
  status: "ACTIVE" | "PAUSED";
  condition_type: "PRICE_BELOW" | "OPPORTUNITY_CLASSIFICATION";
  condition_price: number | null;
  condition_classification: string | null;
  created_at: string;
  updated_at: string;
}

function mapRadar(radar: RadarWire): Radar {
  return {
    id: radar.id,
    name: radar.name,
    originAirportId: radar.origin_airport_id,
    destinationAirportId: radar.destination_airport_id,
    status: radar.status,
    conditionType: radar.condition_type,
    conditionPrice: radar.condition_price,
    conditionClassification: radar.condition_classification,
    createdAt: radar.created_at,
    updatedAt: radar.updated_at,
  };
}

export interface RadarInput {
  name: string;
  originAirportId: string;
  destinationAirportId: string;
  conditionType: "PRICE_BELOW" | "OPPORTUNITY_CLASSIFICATION";
  conditionPrice?: number | null;
  conditionClassification?: string | null;
}

function radarInputToWire(input: RadarInput) {
  return {
    name: input.name,
    origin_airport_id: input.originAirportId,
    destination_airport_id: input.destinationAirportId,
    condition_type: input.conditionType,
    condition_price: input.conditionPrice ?? null,
    condition_classification: input.conditionClassification ?? null,
  };
}

const FRIENDLY_RADAR_ERROR = "Não conseguimos salvar o Radar agora. Confira os dados e tente de novo.";

export async function createRadar(accessToken: string, input: RadarInput): Promise<Radar> {
  const response = await authFetch("/radars", accessToken, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(radarInputToWire(input)),
  });
  if (!response.ok) throw new ApiError(FRIENDLY_RADAR_ERROR);
  return mapRadar(await response.json());
}

export async function listRadars(accessToken: string): Promise<Radar[]> {
  const response = await authFetch("/radars", accessToken);
  if (!response.ok) throw new ApiError("Não conseguimos carregar seus Radares agora.");
  const body: RadarWire[] = await response.json();
  return body.map(mapRadar);
}

export async function updateRadar(
  accessToken: string,
  radarId: string,
  patch: Partial<RadarInput> & { status?: "ACTIVE" | "PAUSED" },
): Promise<Radar> {
  const body: Record<string, unknown> = {};
  if (patch.name !== undefined) body.name = patch.name;
  if (patch.originAirportId !== undefined) body.origin_airport_id = patch.originAirportId;
  if (patch.destinationAirportId !== undefined) body.destination_airport_id = patch.destinationAirportId;
  if (patch.status !== undefined) body.status = patch.status;
  if (patch.conditionType !== undefined) body.condition_type = patch.conditionType;
  if (patch.conditionPrice !== undefined) body.condition_price = patch.conditionPrice;
  if (patch.conditionClassification !== undefined) body.condition_classification = patch.conditionClassification;

  const response = await authFetch(`/radars/${radarId}`, accessToken, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (response.status === 404) throw new ApiError("Radar não encontrado.");
  if (!response.ok) throw new ApiError(FRIENDLY_RADAR_ERROR);
  return mapRadar(await response.json());
}

export async function deleteRadar(accessToken: string, radarId: string): Promise<void> {
  const response = await authFetch(`/radars/${radarId}`, accessToken, { method: "DELETE" });
  if (response.status === 404) throw new ApiError("Radar não encontrado.");
  if (!response.ok) throw new ApiError(FRIENDLY_RADAR_ERROR);
}

// --- Notificações (v0.4) ----------------------------------------------------

interface NotificationWire {
  id: string;
  radar_id: string;
  type: string;
  title: string;
  message: string;
  read_at: string | null;
  created_at: string;
}

function mapNotification(notification: NotificationWire): AppNotification {
  return {
    id: notification.id,
    radarId: notification.radar_id,
    type: notification.type,
    title: notification.title,
    message: notification.message,
    readAt: notification.read_at,
    createdAt: notification.created_at,
  };
}

export async function listNotifications(accessToken: string): Promise<AppNotification[]> {
  const response = await authFetch("/notifications", accessToken);
  if (!response.ok) throw new ApiError("Não conseguimos carregar suas notificações agora.");
  const body: NotificationWire[] = await response.json();
  return body.map(mapNotification);
}

export async function markNotificationRead(accessToken: string, notificationId: string): Promise<AppNotification> {
  const response = await authFetch(`/notifications/${notificationId}/read`, accessToken, { method: "PATCH" });
  if (!response.ok) throw new ApiError("Não conseguimos marcar essa notificação como lida.");
  return mapNotification(await response.json());
}
