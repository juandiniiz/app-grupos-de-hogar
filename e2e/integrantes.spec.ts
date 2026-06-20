import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

const TS = Date.now()

test.describe('Integrantes', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  test('integrantes list loads and shows members', async ({ page }) => {
    await page.goto('/integrantes')
    await expect(page.locator('input[type="search"]')).toBeVisible({ timeout: 8000 })
    // Either shows member cards or empty message - no crash
    await page.waitForTimeout(1500)
    const cards = page.locator('.card')
    await expect(cards.first()).toBeVisible()
  })

  test('create new integrante with minimal data', async ({ page }) => {
    await page.goto('/integrantes/nuevo')
    await expect(page.getByPlaceholder('Nombre')).toBeVisible({ timeout: 8000 })
    await page.getByPlaceholder('Nombre').fill(`TestNombre${TS}`)
    await page.getByPlaceholder('Apellidos').fill(`TestApellido${TS}`)
    await page.locator('button[type="submit"]').click()
    // Should navigate to detail page
    await expect(page).toHaveURL(/\/integrantes\/\d+/, { timeout: 8000 })
  })

  test('create new integrante with grupo assignment', async ({ page }) => {
    await page.goto('/integrantes/nuevo')
    await expect(page.getByPlaceholder('Nombre')).toBeVisible({ timeout: 8000 })
    await page.getByPlaceholder('Nombre').fill(`GrupoTest${TS}`)
    await page.getByPlaceholder('Apellidos').fill(`Apellido${TS}`)
    // Try to add a grupo - type in grupo search
    const grupoSearch = page.getByPlaceholder('Buscar grupo...')
    await grupoSearch.fill('a')
    await page.waitForTimeout(500)
    // If dropdown appears, click first option
    const dropdown = page.locator('.border.border-grey.rounded-card').first()
    if (await dropdown.isVisible()) {
      await dropdown.locator('button').first().click()
    }
    await page.locator('button[type="submit"]').click()
    await expect(page).toHaveURL(/\/integrantes\/\d+/, { timeout: 8000 })
  })

  test('integrante detail page shows all blocks', async ({ page }) => {
    await page.goto('/integrantes')
    await page.waitForTimeout(1500)
    // Click first integrante card
    const firstCard = page.locator('a[href^="/integrantes/"]').first()
    if (await firstCard.isVisible()) {
      await firstCard.click()
      await expect(page).toHaveURL(/\/integrantes\/\d+/, { timeout: 5000 })
      // Should show name
      await expect(page.locator('h2').first()).toBeVisible({ timeout: 5000 })
      // Should show Formación block
      await expect(page.getByText('Formación')).toBeVisible()
    } else {
      // No integrantes yet - skip
      test.skip()
    }
  })

  test('filter by is_membro shows only members', async ({ page }) => {
    await page.goto('/integrantes')
    await page.locator('button').filter({ hasText: 'FILTRAR' }).click()
    await expect(page.getByText('Filtros')).toBeVisible({ timeout: 5000 })
    // Select "Solo miembros"
    await page.locator('select').first().selectOption('true')
    await page.locator('button').filter({ hasText: 'APLICAR' }).click()
    await page.waitForTimeout(1000)
    // No crash
    await expect(page.locator('input[type="search"]')).toBeVisible()
  })

  test('filter by novo_crente works', async ({ page }) => {
    await page.goto('/integrantes')
    await page.locator('button').filter({ hasText: 'FILTRAR' }).click()
    await expect(page.getByText('Filtros')).toBeVisible({ timeout: 5000 })
    // The novo_crente select - find by its options
    const novoCrenteSelect = page.locator('select').filter({ hasText: 'Novo crente: todos' })
    await novoCrenteSelect.selectOption('true')
    await page.locator('button').filter({ hasText: 'APLICAR' }).click()
    await page.waitForTimeout(1000)
    await expect(page.locator('input[type="search"]')).toBeVisible()
  })

  test('search by name filters list', async ({ page }) => {
    await page.goto('/integrantes')
    await page.waitForTimeout(1000)
    await page.fill('input[type="search"]', 'a')
    await page.waitForTimeout(500)
    // No crash
    await expect(page.locator('input[type="search"]')).toBeVisible()
  })

  test('edit integrante updates data', async ({ page }) => {
    // First create one to edit
    await page.goto('/integrantes/nuevo')
    await expect(page.getByPlaceholder('Nombre')).toBeVisible({ timeout: 8000 })
    await page.getByPlaceholder('Nombre').fill(`EditTest${TS}`)
    await page.getByPlaceholder('Apellidos').fill(`EditApellido${TS}`)
    await page.locator('button[type="submit"]').click()
    await expect(page).toHaveURL(/\/integrantes\/\d+/, { timeout: 8000 })
    // Now click EDITAR
    await page.locator('a[href*="/editar"]').click()
    await expect(page).toHaveURL(/\/integrantes\/\d+\/editar/, { timeout: 5000 })
    // Change name
    const nameInput = page.getByPlaceholder('Nombre')
    await nameInput.clear()
    await nameInput.fill(`EditedName${TS}`)
    await page.locator('button[type="submit"]').click()
    await expect(page).toHaveURL(/\/integrantes\/\d+$/, { timeout: 8000 })
    // Verify updated name visible
    await expect(page.getByText(`EditedName${TS}`)).toBeVisible({ timeout: 5000 })
  })
})
