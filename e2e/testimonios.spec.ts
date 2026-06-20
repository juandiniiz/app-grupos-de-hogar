import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

test.describe('Testimonios', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
  })

  test('testimonios list loads', async ({ page }) => {
    await page.goto('/testimonios')
    // Use heading role to avoid matching sidebar nav link
    await expect(page.getByRole('heading', { name: 'Testimonios' })).toBeVisible({ timeout: 8000 })
    await page.waitForTimeout(1000)
    // No crash - either shows testimonios or empty card
    await expect(page.locator('.card').first()).toBeVisible()
  })

  test('testimonio detail shows full content', async ({ page }) => {
    await page.goto('/testimonios')
    await page.waitForTimeout(1500)
    const firstLink = page.locator('a[href^="/testimonios/"]').first()
    if (await firstLink.isVisible()) {
      await firstLink.click()
      await expect(page).toHaveURL(/\/testimonios\/\d+/, { timeout: 5000 })
      // Detail should show content
      await expect(page.locator('h2, h3').first()).toBeVisible({ timeout: 5000 })
    } else {
      test.skip()
    }
  })

  test('navigation between testimonios works', async ({ page }) => {
    await page.goto('/testimonios')
    await page.waitForTimeout(1500)
    const firstLink = page.locator('a[href^="/testimonios/"]').first()
    if (await firstLink.isVisible()) {
      await firstLink.click()
      await expect(page).toHaveURL(/\/testimonios\/\d+/, { timeout: 5000 })
      // Navigate back via button or browser
      const backBtn = page.locator('button').filter({ hasText: 'Volver' })
      if (await backBtn.isVisible()) {
        await backBtn.click()
        await page.waitForTimeout(500)
      } else {
        await page.goBack()
      }
      // Should be back on testimonios list or some other page - no crash
      await page.waitForTimeout(500)
    } else {
      test.skip()
    }
  })
})
