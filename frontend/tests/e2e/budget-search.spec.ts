import { expect, test } from "@playwright/test";

test("budget search flow: Home -> results -> opportunity detail", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });

  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Voa Radar" })).toBeVisible();

  await page.fill('input[placeholder="Belém"]', "Belém");
  await page.selectOption("select", "Outubro");
  await page.click('button:has-text("Encontrar viagens")');

  await expect(page.getByText("Encontramos destinos")).toBeVisible();
  await expect(page.getByText("Recife")).toBeVisible();

  await page.click('a:has-text("Ver oportunidade")');
  await expect(page.getByText("por pessoa, ida")).toBeVisible();

  expect(consoleErrors).toEqual([]);
});
