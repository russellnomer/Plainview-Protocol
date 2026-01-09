import { test, expect } from '@playwright/test';

test.describe('ICE Shield Contact Audit', () => {
  
  test.beforeEach(async ({ page }) => {
    console.log('🔍 Running ICE Shield Contact Audit...');
    await page.goto('/');
  });

  test('ICE Shield page loads with email form', async ({ page }) => {
    console.log('🔍 Auditing: ICE Shield page structure...');
    
    await page.getByText(/ICE Shield/i).first().click();
    
    await expect(page.getByText(/Stand with ICE/i).first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/Send Official Support/i).first()).toBeVisible();
  });

  test('Email form requires user input before activation', async ({ page }) => {
    console.log('🔍 Auditing: Form validation logic...');
    
    await page.getByText(/ICE Shield/i).first().click();
    
    await expect(page.getByText(/Please complete all fields/i).first()).toBeVisible({ timeout: 10000 });
    
    await page.getByPlaceholder(/John Smith/i).fill('Test User');
    await page.getByPlaceholder(/Plainview/i).fill('New York');
    await page.getByRole('combobox').selectOption('New York');
    
    await expect(page.getByText(/SEND OFFICIAL SUPPORT/i).first()).toBeVisible();
  });

  test('Mailto link contains correct DHS email addresses', async ({ page }) => {
    console.log('🔍 Auditing: Mailto link integrity...');
    
    await page.getByText(/ICE Shield/i).first().click();
    
    await page.getByPlaceholder(/John Smith/i).fill('Test Sentinel');
    await page.getByPlaceholder(/Plainview/i).fill('Plainview');
    await page.getByRole('combobox').selectOption('New York');
    
    const mailtoLink = page.locator('a[href^="mailto:"]');
    const href = await mailtoLink.getAttribute('href');
    
    expect(href).toContain('PublicEngagement@ice.dhs.gov');
    expect(href).toContain('Secretary@dhs.gov');
    expect(href).toContain('THANK%20YOU');
  });

  test('Badge unlock section appears after confirmation', async ({ page }) => {
    console.log('🔍 Auditing: Badge unlock flow...');
    
    await page.getByText(/ICE Shield/i).first().click();
    
    await page.getByPlaceholder(/John Smith/i).fill('Test Sentinel');
    await page.getByPlaceholder(/Plainview/i).fill('Plainview');
    await page.getByRole('combobox').selectOption('New York');
    
    await page.getByRole('button', { name: /Sent My Email/i }).click();
    
    await expect(page.getByText(/Digital Badge/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/Download Your Badge/i).first()).toBeVisible();
  });

  test('Social share buttons are present after unlock', async ({ page }) => {
    console.log('🔍 Auditing: Social share integration...');
    
    await page.getByText(/ICE Shield/i).first().click();
    
    await page.getByPlaceholder(/John Smith/i).fill('Test Sentinel');
    await page.getByPlaceholder(/Plainview/i).fill('Plainview');
    await page.getByRole('combobox').selectOption('New York');
    await page.getByRole('button', { name: /Sent My Email/i }).click();
    
    await expect(page.getByText(/Share on X/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/Share on Facebook/i).first()).toBeVisible();
  });
});
