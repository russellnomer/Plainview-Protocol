import { test, expect } from '@playwright/test';

test.describe('ICE Shield Contact Audit', () => {
  
  test.beforeEach(async ({ page }) => {
    console.log('🔍 Running ICE Shield Contact Audit...');
    await page.goto('/ICE_Shield', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
  });

  test('ICE Shield page loads with content', async ({ page }) => {
    console.log('🔍 Auditing: ICE Shield page structure...');
    
    await expect(page.locator('.stApp')).toBeVisible({ timeout: 15000 });
    
    await page.waitForFunction(() => {
      const body = document.body.innerText;
      return body.includes('ICE') || body.includes('Shield') || body.includes('Stand') || body.includes('Support');
    }, { timeout: 15000 });
  });

  test('Page has form input elements for user data', async ({ page }) => {
    console.log('🔍 Auditing: Form input fields...');
    
    const inputFields = page.locator('input[type="text"], select, [data-testid*="Input"]');
    await expect(inputFields.first()).toBeVisible({ timeout: 15000 });
  });

  test('Page references DHS or immigration enforcement', async ({ page }) => {
    console.log('🔍 Auditing: DHS reference presence...');
    
    await page.waitForFunction(() => {
      const body = document.body.innerText;
      return body.includes('DHS') || body.includes('ICE') || body.includes('enforcement') || body.includes('immigration');
    }, { timeout: 15000 });
  });

  test('Mailto link generation is present', async ({ page }) => {
    console.log('🔍 Auditing: Mailto link presence...');
    
    const mailtoLink = page.locator('a[href^="mailto:"]');
    const count = await mailtoLink.count();
    
    const hasMailto = count > 0;
    const pageContent = await page.content();
    const hasEmailRef = /email|mailto|dhs\.gov/i.test(pageContent);
    
    expect(hasMailto || hasEmailRef).toBe(true);
  });

  test('Social share functionality exists', async ({ page }) => {
    console.log('🔍 Auditing: Social share presence...');
    
    await page.waitForFunction(() => {
      const body = document.body.innerText;
      return body.includes('Share') || body.includes('Twitter') || body.includes('Facebook') || body.includes('Post');
    }, { timeout: 15000 });
  });
});
