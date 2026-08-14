import { expect, test } from "@playwright/test";

// Smoke test da v0.4 (Radar & Alertas) — cobre rotas protegidas,
// renderização e o caminho de erro do login contra o Supabase Auth real
// (backend/.env já configurado). O fluxo feliz completo (cadastro →
// confirmar e-mail → login → criar Radar) não dá pra automatizar aqui
// porque a confirmação de e-mail exige clicar num link fora do navegador
// do teste — validado manualmente via curl, ver docs/v0.4/ROADMAP.md.

test("rotas protegidas redirecionam para /entrar quando não autenticado", async ({ page }) => {
  await page.goto("/radares");
  await expect(page).toHaveURL(/\/entrar$/);

  await page.goto("/notificacoes");
  await expect(page).toHaveURL(/\/entrar$/);

  await page.goto("/radares/novo");
  await expect(page).toHaveURL(/\/entrar$/);
});

test("página de login renderiza e mostra erro amigável com credenciais inválidas", async ({ page }) => {
  await page.goto("/entrar");
  await expect(page.getByRole("heading", { name: "Entrar" })).toBeVisible();

  await page.fill('input[type="email"]', "conta-que-nao-existe@example.com");
  await page.fill('input[type="password"]', "senha-qualquer-123");
  await page.click('button:has-text("Entrar")');

  // Credenciais inválidas contra o Supabase Auth real — nunca erro técnico
  // cru, só a mensagem amigável do backend (auth.py FRIENDLY_AUTH_ERROR).
  await expect(page.getByRole("alert")).toContainText("Não foi possível completar essa ação");
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
