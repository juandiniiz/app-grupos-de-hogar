import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

test.describe('Reuniones', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  // Helper: navigate to any reunion detail page (creates one if needed)
  async function getToReunion(page: any): Promise<boolean> {
    await page.goto('/grupos')
    await page.waitForTimeout(1500)
    const firstGrupo = page.locator('a[href^="/grupos/"]').first()
    if (!await firstGrupo.isVisible()) return false
    await firstGrupo.click()
    await expect(page).toHaveURL(/\/grupos\/\d+$/, { timeout: 5000 })

    // If there's already a reunion link, use it
    const reunionLink = page.locator('a[href*="/reuniones/"]').first()
    if (await reunionLink.isVisible()) {
      await reunionLink.click()
      await expect(page).toHaveURL(/\/grupos\/\d+\/reuniones\/\d+/, { timeout: 5000 })
      return true
    }
    // Otherwise create one
    await page.locator('button').filter({ hasText: '+ REUNIÓN' }).click()
    await expect(page.getByText('Nueva Reunión')).toBeVisible({ timeout: 3000 })
    await page.locator('button').filter({ hasText: /^Crear$/ }).click()
    await expect(page).toHaveURL(/\/grupos\/\d+\/reuniones\/\d+/, { timeout: 8000 })
    return true
  }

  test('reunion detail loads from grupo', async ({ page }) => {
    const ok = await getToReunion(page)
    if (!ok) { test.skip(); return }
    // Use heading role to avoid strict mode issues
    await expect(page.getByRole('heading', { name: 'Datos de la reunión' })).toBeVisible({ timeout: 5000 })
    await expect(page.getByRole('heading', { name: 'Asistencia' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Oraciones' })).toBeVisible()
  })

  test('toggle asistencia checkbox', async ({ page }) => {
    const ok = await getToReunion(page)
    if (!ok) { test.skip(); return }
    await expect(page.getByRole('heading', { name: 'Datos de la reunión' })).toBeVisible({ timeout: 5000 })
    // Find checkboxes in asistencia block - they have accent-primary
    const checkboxes = page.locator('label').filter({ has: page.locator('input[type="checkbox"]') })
    const count = await checkboxes.count()
    if (count > 0) {
      const firstCheckbox = checkboxes.first().locator('input[type="checkbox"]')
      const before = await firstCheckbox.isChecked()
      await firstCheckbox.click()
      const after = await firstCheckbox.isChecked()
      expect(after).toBe(!before)
    }
    // No crash
    await expect(page.getByRole('heading', { name: 'Asistencia' })).toBeVisible()
  })

  test('add oracao to reunion', async ({ page }) => {
    const ok = await getToReunion(page)
    if (!ok) { test.skip(); return }
    await expect(page.getByRole('heading', { name: 'Oraciones' })).toBeVisible({ timeout: 5000 })
    // Click + AÑADIR ORACIÓN link
    await page.getByText('+ AÑADIR ORACIÓN').click()
    // The textarea for oracion text - use placeholder
    const oracaoTextarea = page.getByPlaceholder('Texto de la oración...')
    await expect(oracaoTextarea).toBeVisible({ timeout: 3000 })
    await oracaoTextarea.fill('Oración de prueba E2E')
    // Click the Añadir button inside the add oracao panel
    await page.locator('button').filter({ hasText: /^Añadir$/ }).click()
    await page.waitForTimeout(1500)
    await expect(page.getByText('Oración de prueba E2E')).toBeVisible({ timeout: 5000 })
  })

  test('save reunion', async ({ page }) => {
    const ok = await getToReunion(page)
    if (!ok) { test.skip(); return }
    await expect(page.getByRole('heading', { name: 'Datos de la reunión' })).toBeVisible({ timeout: 5000 })
    await page.locator('button').filter({ hasText: 'GUARDAR REUNIÓN' }).click()
    // Should navigate back to grupo
    await expect(page).toHaveURL(/\/grupos\/\d+$/, { timeout: 8000 })
  })
})
