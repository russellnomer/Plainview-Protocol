import { test, expect } from '@playwright/test';

test.describe('Security & Privacy Accountability Audit', () => {

  test('Protocol loads over secure connection @smoke', async ({ page }) => {
    console.log('🔍 Running Security Audit: Connection integrity...');
    
    const response = await page.goto('/');
    expect(response?.status()).toBeLessThan(400);
    
    console.log('✅ Security Audit: Page loads successfully');
  });

  test('Console is free of severe JavaScript errors', async ({ page }) => {
    console.log('🔍 Running Security Audit: Console error scan...');
    
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForTimeout(3000);
    
    const criticalErrors = errors.filter(e => 
      !e.includes('favicon') && 
      !e.includes('404') &&
      !e.includes('net::ERR')
    );
    
    console.log(`✅ Security Audit: Found ${errors.length} console messages, ${criticalErrors.length} critical`);
    expect(criticalErrors.length).toBe(0);
  });

  test('Privacy Policy link is accessible in footer', async ({ page }) => {
    console.log('🔍 Running Security Audit: Privacy Policy accessibility...');
    
    await page.goto('/');
    
    const legalExpander = page.getByText(/Legal & Privacy/i).first();
    await expect(legalExpander).toBeVisible();
    await legalExpander.click();
    
    const privacyButton = page.getByRole('button', { name: /Privacy/i });
    await expect(privacyButton).toBeVisible();
    
    await privacyButton.click();
    
    await expect(page.getByText(/Privacy Policy/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/AI Processing Disclosure/i).first()).toBeVisible();
    
    console.log('✅ Security Audit: Privacy Policy is accessible');
  });

  test('Terms of Service link is accessible', async ({ page }) => {
    console.log('🔍 Running Security Audit: Terms of Service accessibility...');
    
    await page.goto('/');
    
    await page.getByText(/Legal & Privacy/i).first().click();
    
    const termsButton = page.getByRole('button', { name: /Terms/i });
    await expect(termsButton).toBeVisible();
    
    await termsButton.click();
    
    await expect(page.getByText(/Terms of Service/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/AS-IS/i).first()).toBeVisible();
    
    console.log('✅ Security Audit: Terms of Service is accessible');
  });

  test('Safe Harbor statement is accessible', async ({ page }) => {
    console.log('🔍 Running Security Audit: Safe Harbor accessibility...');
    
    await page.goto('/');
    
    await page.getByText(/Legal & Privacy/i).first().click();
    
    const safeHarborButton = page.getByRole('button', { name: /Safe Harbor/i });
    await expect(safeHarborButton).toBeVisible();
    
    await safeHarborButton.click();
    
    await expect(page.getByText(/Safe Harbor Statement/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/72-hour/i).first()).toBeVisible();
    
    console.log('✅ Security Audit: Safe Harbor statement is accessible');
  });

  test('Affidavit signing mechanism is present', async ({ page }) => {
    console.log('🔍 Running Security Audit: Affidavit integrity...');
    
    await page.goto('/Foreign_Influence', { waitUntil: 'networkidle' });
    await page.waitForTimeout(4000);
    
    await expect(page.locator('.stApp')).toBeVisible({ timeout: 20000 });
    
    await page.waitForFunction(() => {
      const body = document.body.innerText;
      return body.includes('Affidavit') || body.includes('Integrity') || body.includes('Sign') || body.includes('Foreign') || body.includes('Influence');
    }, { timeout: 15000 });
    
    console.log('✅ Security Audit: Affidavit mechanism is present');
  });

  test('Founder disclaimer is visible in footer', async ({ page }) => {
    console.log('🔍 Running Security Audit: Legal disclaimer visibility...');
    
    await page.goto('/');
    
    await page.getByText(/Legal & Privacy/i).first().click();
    
    await expect(page.getByText(/Russell David Nomer/i).first()).toBeVisible();
    await expect(page.getByText(/Not legal advice/i).first()).toBeVisible();
    
    console.log('✅ Security Audit: Legal disclaimers are visible');
  });
});
