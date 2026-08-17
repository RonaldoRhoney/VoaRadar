export type RadarStatus = "ACTIVE" | "PAUSED";
export type ConditionType = "PRICE_BELOW" | "OPPORTUNITY_CLASSIFICATION";

export interface Airport {
  id: string;
  code: string;
  name: string;
  city: string;
}

export interface Radar {
  id: string;
  name: string;
  originAirportId: string;
  destinationAirportId: string;
  departureDate: string | null;
  returnDate: string | null;
  status: RadarStatus;
  conditionType: ConditionType;
  conditionPrice: number | null;
  conditionClassification: string | null;
  createdAt: string;
  updatedAt: string;
}
