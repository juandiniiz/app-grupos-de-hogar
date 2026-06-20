import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

const TS = Date.now()

test.describe('Ministerios', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  test('ministerios list loads', async ({ page }) => {
    await page.goto('/ministerios')
    // Use heading role to avoid matching the sidebar nav link
    await expect(page.getByRole('heading', { name: 'Ministerios' })).toBeVisible({ timeout: 8000 })
    await page.waitForTimeout(1000)
    // No crash
    await expect(page.locator('.card').first()).toBeVisible()
  })

  test('create new ministerio', async ({ page }) => {
    await page.goto('/ministerios')
    await expect(page.getByRole('heading', { name: 'Ministerios' })).toBeVisible({ timeout: 8000 })
    await page.locator('button').filter({ hasText: 'NUEVO MINISTERIO' }).click()
    // Modal h3 heading - use role heading to avoid matching the button text
    await expect(page.getByRole('heading', { name: 'Nuevo Ministerio' })).toBeVisible({ timeout: 3000 })
    await page.getByPlaceholder('Nombre del ministerio').fill(`MinTest${TS}`)
    await page.getByPlaceholder('Descripción opcional...').fill('Descripción de prueba')
    await page.locator('button').filter({ hasText: /^Crear$/ }).click()
    await page.waitForTimeout(1500)
    // Modal closes and list reloads - verify new ministerio appears
    await expect(page.getByText(`MinTest${TS}`)).toBeVisible({ timeout: 8000 })
  })

  test('ministerio detail shows tarefas', async ({ page }) => {
    await page.goto('/ministerios')
    await page.waitForTimeout(1500)
    const firstMin = page.locator('a[href^="/ministerios/"]').first()
    if (await firstMin.isVisible()) {
      await firstMin.click()
      await expect(page).toHaveURL(/\/ministerios\/\d+/, { timeout: 5000 })
      await expect(page.getByRole('heading', { name: 'Tareas' })).toBeVisible({ timeout: 5000 })
    } else {
      test.skip()
    }
  })

  test('add tarefa to ministerio', async ({ page }) => {
    await page.goto('/ministerios')
    await page.waitForTimeout(1500)
    const firstMin = page.locator('a[href^="/ministerios/"]').first()
    if (await firstMin.isVisible()) {
      await firstMin.click()
      await expect(page).toHaveURL(/\/ministerios\/\d+/, { timeout: 5000 })
      await expect(page.getByRole('heading', { name: 'Tareas' })).toBeVisible({ timeout: 5000 })
      const tarefaInput = page.getByPlaceholder('Nueva tarea...')
      await tarefaInput.fill(`TarefaTest${TS}`)
      await page.locator('button').filter({ hasText: /^Añadir$/ }).click()
      await page.waitForTimeout(1500)
      await expect(page.getByText(`TarefaTest${TS}`)).toBeVisible({ timeout: 5000 })
    } else {
      test.skip()
    }
  })
})
