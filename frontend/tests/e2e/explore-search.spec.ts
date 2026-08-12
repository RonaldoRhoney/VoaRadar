import { expect, test } from "@playwright/test";

test("explore flow: Home -> results -> offer detail", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });

  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Voa Radar" })).toBeVisible();

  await page.fill('input[placeholder="Belém"]', "Belém");
  await page.selectOption("select", "Outubro");
  await page.click('button:has-text("Encontrar viagens")');

  await expect(page.getByText(/Encontramos \d+ possibilidade/)).toBeVisible();
  await expect(page.getByText("Recife")).toBeVisible();
  await expect(page.getByText("⭐ Melhor oportunidade")).toBeVisible();

  await page.click('a:has-text("Ver oportunidade")');
  await expect(page.getByText("Companhia")).toBeVisible();
  await expect(page.getByText("Duração")).toBeVisible();

  expect(consoleErrors).toEqual([]);
});

test("explore flow: budget too low shows near-budget suggestion", async ({ page }) => {
  await page.goto("/resultados?orcamento=350&origem=Bel%C3%A9m&mes=Outubro");

  await expect(page.getByText(/Não encontramos oportunidades/)).toBeVisible();
  await expect(page.getByText(/Encontramos opções a partir de/)).toBeVisible();

  await page.click('button:has-text("Ver opções")');
  await expect(page.getByText("Recife")).toBeVisible();
});
