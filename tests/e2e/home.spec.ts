import { test, expect } from '@playwright/test';

test.describe('Homepage Critical Path Audit', () => {
  
  test.beforeEach(async ({ page }) => {
    console.log('🔍 Running Homepage Audit...');
    await page.goto('/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
  });

  test('Protocol loads successfully @smoke', async ({ page }) => {
    console.log('🔍 Auditing: Protocol initialization...');
    await expect(page.locator('.stApp')).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(/Plainview Protocol/i).first()).toBeVisible({ timeout: 10000 });
  });

  test('Debt Ticker module loads and displays data', async ({ page }) => {
    console.log('🔍 Auditing: Debt Ticker module...');
    
    await page.getByRole('link', { name: /National Lens/i }).click();
    await page.waitForTimeout(2000);
    
    await expect(page.getByText(/National Debt/i).first()).toBeVisible({ timeout: 15000 });
    
    const debtDisplay = page.locator('text=/\\$[0-9,]+/').first();
    await expect(debtDisplay).toBeVisible({ timeout: 10000 });
  });

  test('Force Continuum module loads with content', async ({ page }) => {
    console.log('🔍 Auditing: Force Continuum module...');
    
    await page.goto('/Force_Continuum', { waitUntil: 'networkidle' });
    await page.waitForTimeout(4000);
    
    await expect(page.locator('.stApp')).toBeVisible({ timeout: 20000 });
    
    await page.waitForFunction(() => {
      const body = document.body.innerText;
      return body.includes('Impact') || body.includes('Cost') || body.includes('Legal') || body.includes('Force') || body.includes('Continuum');
    }, { timeout: 15000 });
  });

  test('Navigation sidebar displays core modules', async ({ page }) => {
    console.log('🔍 Auditing: Navigation integrity...');
    
    await expect(page.getByRole('link', { name: /Mission Control/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('link', { name: /National Lens/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('link', { name: /Corruption Heatmap/i })).toBeVisible({ timeout: 10000 });
  });
});
