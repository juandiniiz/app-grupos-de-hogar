import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

const TS = Date.now()

test.describe('Grupos', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  test('grupos list loads', async ({ page }) => {
    await page.goto('/grupos')
    await expect(page.locator('input[type="search"]')).toBeVisible({ timeout: 8000 })
    await page.waitForTimeout(1000)
    // No crash - either shows groups or empty
    await expect(page.locator('.card').first()).toBeVisible()
  })

  test('create new grupo', async ({ page }) => {
    await page.goto('/grupos/nuevo')
    await expect(page.getByPlaceholder('Nombre del grupo')).toBeVisible({ timeout: 8000 })
    await page.getByPlaceholder('Nombre del grupo').fill(`GrupoTest${TS}`)
    await page.locator('button[type="submit"]').click()
    await expect(page).toHaveURL(/\/grupos\/\d+/, { timeout: 8000 })
  })

  test('grupo detail shows all blocks', async ({ page }) => {
    await page.goto('/grupos')
    await page.waitForTimeout(1500)
    const firstGrupo = page.locator('a[href^="/grupos/"]').first()
    if (await firstGrupo.isVisible()) {
      await firstGrupo.click()
      await expect(page).toHaveURL(/\/grupos\/\d+$/, { timeout: 5000 })
      // Block 1: Info - grupo name as h2
      await expect(page.locator('h2').first()).toBeVisible({ timeout: 5000 })
      // Block 2: Horario
      await expect(page.getByRole('heading', { name: 'Horario y lugar' })).toBeVisible()
      // Block 3: Integrantes
      await expect(page.getByRole('heading', { name: /^Integrantes/ })).toBeVisible()
      // Block 4: Estadísticas
      await expect(page.getByRole('heading', { name: 'Estadísticas' })).toBeVisible()
      // Block 6: Reuniones
      await expect(page.getByRole('heading', { name: /^Reuniones/ })).toBeVisible()
      // Block 8: Testimonios (use heading to avoid sidebar)
      await expect(page.getByRole('heading', { name: 'Testimonios' })).toBeVisible()
    } else {
      test.skip()
    }
  })

  test('grupo detail shows integrantes list', async ({ page }) => {
    await page.goto('/grupos')
    await page.waitForTimeout(1500)
    const firstGrupo = page.locator('a[href^="/grupos/"]').first()
    if (await firstGrupo.isVisible()) {
      await firstGrupo.click()
      await expect(page).toHaveURL(/\/grupos\/\d+$/, { timeout: 5000 })
      // Integrantes block is always rendered
      await expect(page.getByRole('heading', { name: /^Integrantes/ })).toBeVisible({ timeout: 5000 })
    } else {
      test.skip()
    }
  })

  test('create new reunion from grupo detail', async ({ page }) => {
    // First navigate to a grupo
    await page.goto('/grupos')
    await page.waitForTimeout(1500)
    const firstGrupo = page.locator('a[href^="/grupos/"]').first()
    if (await firstGrupo.isVisible()) {
      await firstGrupo.click()
      await expect(page).toHaveURL(/\/grupos\/\d+$/, { timeout: 5000 })
      // Click + REUNIÓN button
      await page.locator('button').filter({ hasText: '+ REUNIÓN' }).click()
      await expect(page.getByText('Nueva Reunión')).toBeVisible({ timeout: 3000 })
      // Fill and create
      await page.locator('button').filter({ hasText: /^Crear$/ }).click()
      // Should navigate to reunion detail
      await expect(page).toHaveURL(/\/grupos\/\d+\/reuniones\/\d+/, { timeout: 8000 })
    } else {
      test.skip()
    }
  })

  test('filter grupos by frecuencia', async ({ page }) => {
    await page.goto('/grupos')
    await page.locator('button').filter({ hasText: 'FILTRAR' }).click()
    await expect(page.getByText('Filtros')).toBeVisible({ timeout: 5000 })
    await page.locator('select').first().selectOption('semanal')
    await page.locator('button').filter({ hasText: 'APLICAR' }).click()
    await page.waitForTimeout(1000)
    await expect(page.locator('input[type="search"]')).toBeVisible()
  })
})
