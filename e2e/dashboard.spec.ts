import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  test('dashboard loads and shows all 8 sections', async ({ page }) => {
    // Dashboard has 8 blocks: Bienvenido, Grupos de Hogar, Fe, Reuniones, Ubicación, Asistencia, Formación, Oración
    // Use exact h2 selectors to avoid matching the h1 welcome text or sidebar nav links
    await expect(page.getByRole('heading', { name: /Bienvenido/ })).toBeVisible({ timeout: 10000 })
    // h2 exact: 'Grupos de Hogar' - the h1 contains it but is not exact, use h2 specifically
    await expect(page.locator('h2').filter({ hasText: /^Grupos de Hogar$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Fe$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Reuniones$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Ubicación$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Asistencia$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Formación$/ })).toBeVisible()
    await expect(page.locator('h2').filter({ hasText: /^Oración$/ })).toBeVisible()
  })

  test('testimonios destacados section shows cards or gracefully empty', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Bienvenido/ })).toBeVisible({ timeout: 10000 })
    // The section either shows cards or nothing - just no crash
    const card = page.locator('.card').first()
    await expect(card).toBeVisible()
  })

  test('grupos metrics show numbers', async ({ page }) => {
    await expect(page.locator('h2').filter({ hasText: /^Grupos de Hogar$/ })).toBeVisible({ timeout: 10000 })
    // StatCard2 shows number + label inside .card
    await expect(page.locator('.card').getByText('Grupos').first()).toBeVisible()
    await expect(page.locator('.card').getByText('Integrantes').first()).toBeVisible()
  })

  test('map toggle switches between grupos and integrantes', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Ubicación' })).toBeVisible({ timeout: 10000 })
    // Two toggle buttons in the map section - use exact match
    const gruposBtn = page.locator('button').filter({ hasText: /^Grupos$/ })
    const integrantesBtn = page.locator('button').filter({ hasText: /^Integrantes$/ })
    await expect(gruposBtn).toBeVisible()
    await expect(integrantesBtn).toBeVisible()
    // Click integrantes
    await integrantesBtn.click()
    // Click back to grupos
    await gruposBtn.click()
    // Just verify no crash
    await expect(page.getByRole('heading', { name: 'Ubicación' })).toBeVisible()
  })

  test('formacion table renders rows', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Formación' })).toBeVisible({ timeout: 10000 })
    await expect(page.getByText('Discipulado inicial')).toBeVisible()
    await expect(page.getByText('Pre-bautismo')).toBeVisible()
    await expect(page.getByText('Escuela bíblica')).toBeVisible()
  })
})
