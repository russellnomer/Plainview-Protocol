import { test, expect } from '@playwright/test';

test.describe('Homepage Critical Path Audit', () => {
  
  test.beforeEach(async ({ page }) => {
    console.log('🔍 Running Homepage Audit...');
    await page.goto('/');
  });

  test('Protocol loads successfully @smoke', async ({ page }) => {
    console.log('🔍 Auditing: Protocol initialization...');
    await expect(page.locator('body')).toBeVisible();
    await expect(page.getByText(/Plainview Protocol/i).first()).toBeVisible();
  });

  test('Debt Ticker module loads and displays data', async ({ page }) => {
    console.log('🔍 Auditing: Debt Ticker module...');
    
    await page.getByText(/National Lens/i).first().click();
    
    await expect(page.getByText(/National Debt/i).first()).toBeVisible({ timeout: 10000 });
    
    const debtDisplay = page.locator('text=/\\$[0-9,]+/').first();
    await expect(debtDisplay).toBeVisible();
  });

  test('Force Continuum module loads with tabs', async ({ page }) => {
    console.log('🔍 Auditing: Force Continuum module...');
    
    await page.getByText(/Force Continuum/i).first().click();
    
    await expect(page.getByText(/Impact Calculator/i).first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/Legal Framework/i).first()).toBeVisible();
    await expect(page.getByText(/Cost Ticker/i).first()).toBeVisible();
    await expect(page.getByText(/Narrative Shield/i).first()).toBeVisible();
  });

  test('Navigation sidebar displays all modules', async ({ page }) => {
    console.log('🔍 Auditing: Navigation integrity...');
    
    const navItems = [
      'Mission Control',
      'Force Continuum',
      'ICE Shield'
    ];
    
    for (const item of navItems) {
      await expect(page.getByText(item).first()).toBeVisible();
    }
  });
});
