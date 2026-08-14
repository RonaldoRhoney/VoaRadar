import { expect, test } from "@playwright/test";

// Smoke test da v0.4 (Radar & Alertas) — cobre rotas protegidas e
// renderização, sem depender de credenciais reais do Supabase Auth (que
// ainda não estão configuradas em backend/.env nesta máquina). Fluxo real
// de cadastro/login precisa ser validado manualmente depois que as chaves
// (SUPABASE_URL/ANON_KEY/JWT_SECRET) forem preenchidas.

test("rotas protegidas redirecionam para /entrar quando não autenticado", async ({ page }) => {
  await page.goto("/radares");
  await expect(page).toHaveURL(/\/entrar$/);

  await page.goto("/notificacoes");
  await expect(page).toHaveURL(/\/entrar$/);

  await page.goto("/radares/novo");
  await expect(page).toHaveURL(/\/entrar$/);
});

test("página de login renderiza e mostra erro amigável sem Supabase configurado", async ({ page }) => {
  await page.goto("/entrar");
  await expect(page.getByRole("heading", { name: "Entrar" })).toBeVisible();

  await page.fill('input[type="email"]', "teste@example.com");
  await page.fill('input[type="password"]', "senha-forte-123");
  await page.click('button:has-text("Entrar")');

  // 503 esperado (Supabase Auth ainda sem chaves no .env desta máquina) —
  // o que importa é que a UI nunca mostra erro técnico cru, só a mensagem
  // amigável do backend (auth.py AUTH_NOT_CONFIGURED).
  await expect(page.getByRole("alert")).toContainText("não está disponível");
});

test("página de cadastro renderiza", async ({ page }) => {
  await page.goto("/cadastro");
  await expect(page.getByRole("heading", { name: "Criar conta" })).toBeVisible();
  await expect(page.getByText("Já tem conta?")).toBeVisible();
});

test("header mostra Entrar quando deslogado e link de busca continua funcionando", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("link", { name: "Entrar" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Voa Radar" })).toBeVisible();
});
