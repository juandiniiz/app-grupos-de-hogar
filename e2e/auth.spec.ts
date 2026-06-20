import { test, expect } from '@playwright/test'
import { ADMIN, loginAs } from './helpers'

test.describe('Auth', () => {
  test('login with valid credentials navigates to dashboard', async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
    await expect(page).toHaveURL('/')
    // dashboard should render something meaningful
    await expect(page.locator('h1, h2').first()).toBeVisible({ timeout: 8000 })
  })

  test('login with wrong password shows error message', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', ADMIN.email)
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')
    // Should stay on login and show error
    await expect(page).toHaveURL('/login')
    const err = page.locator('p.text-red, p[class*="text-red"]')
    await expect(err).toBeVisible({ timeout: 5000 })
    const text = await err.textContent()
    expect(text).toBeTruthy()
  })

  test('login with wrong email shows error message', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'noexiste@fake.com')
    await page.fill('input[type="password"]', 'whatever')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/login')
    const err = page.locator('p.text-red, p[class*="text-red"]')
    await expect(err).toBeVisible({ timeout: 5000 })
  })

  test('error message does not say "conectar" (not a network error)', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', ADMIN.email)
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/login')
    const err = page.locator('p.text-red, p[class*="text-red"]')
    await expect(err).toBeVisible({ timeout: 5000 })
    const text = await err.textContent()
    expect(text).not.toContain('conectar')
  })

  test('logout via side menu works', async ({ page }) => {
    await loginAs(page, ADMIN.email, ADMIN.password)
    // Open side menu via hamburger button (aria-label="Abrir menú")
    await page.locator('button[aria-label="Abrir menú"]').click()
    // Click Cerrar Sesión
    await page.getByText('Cerrar Sesión').click()
    await expect(page).toHaveURL('/login', { timeout: 5000 })
  })

  test('accessing / without token redirects to /login', async ({ page }) => {
    // Clear storage first
    await page.goto('/login')
    await page.evaluate(() => { localStorage.removeItem('token'); localStorage.removeItem('user') })
    await page.goto('/')
    await expect(page).toHaveURL('/login', { timeout: 5000 })
  })
})
