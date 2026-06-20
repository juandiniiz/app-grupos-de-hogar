import { Page } from '@playwright/test'

export const ADMIN = { email: 'admin@puntodeencuentro.es', password: 'admin1234' }
export const BASE = 'http://localhost:5173'
export const API = 'http://localhost:8000/api'

export async function loginAs(page: Page, email: string, password: string) {
  await page.goto('/login')
  await page.fill('input[type="email"]', email)
  await page.fill('input[type="password"]', password)
  await page.click('button[type="submit"]')
  await page.waitForURL('/', { timeout: 10000 })
}
