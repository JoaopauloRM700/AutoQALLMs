const { test, expect } = require('@playwright/test');

test('Test 1: Navigate to Register Page', async ({ page }) => {
  await page.goto('https://demo.automationtesting.in/Register.html');
  const url = page.url();
  expect(url).toBe('https://demo.automationtesting.in/Register.html');
});

test('Test 2: Check Title', async ({ page }) => {
  const title = await page.title();
  expect(title).toBe('Register');
});

test('Test 3: Check H1 Heading', async ({ page }) => {
  const heading = await page.locator('h1').textContent();
  expect(heading).toBe('Automation Demo Site');
});

test('Test 4: Check H2 Heading', async ({ page }) => {
  const heading = await page.locator('h2').textContent();
  expect(heading).toBe('Register');
});

test('Test 5: Check First Name Input', async ({ page }) => {
  const input = await page.locator('input[placeholder="First Name"]');
  expect(input).toBeTruthy();
});

test('Test 6: Check Last Name Input', async ({ page }) => {
  const input = await page.locator('input[placeholder="Last Name"]');
  expect(input).toBeTruthy();
});

test('Test 7: Check Email Input', async ({ page }) => {
  const input = await page.locator('input[type="email"]');
  expect(input).toBeTruthy();
});

test('Test 8: Check Phone Input', async ({ page }) => {
  const input = await page.locator('input[type="tel"]');
  expect(input).toBeTruthy();
});

test('Test 9: Check Radio Options', async ({ page }) => {
  const radio = await page.locator('input[name="radiooptions"]');
  expect(radio).toBeTruthy();
});

test('Test 10: Fill First Name', async ({ page }) => {
  await page.fill('input[placeholder="First Name"]', 'John');
  const value = await page.locator('input[placeholder="First Name"]').inputValue();
  expect(value).toBe('John');
});

test('Test 11: Fill Last Name', async ({ page }) => {
  await page.fill('input[placeholder="Last Name"]', 'Doe');
  const value = await page.locator('input[placeholder="Last Name"]').inputValue();
  expect(value).toBe('Doe');
});

test('Test 12: Fill Email', async ({ page }) => {
  await page.fill('input[type="email"]', 'john.doe@example.com');
  const value = await page.locator('input[type="email"]').inputValue();
  expect(value).toBe('john.doe@example.com');
});

test('Test 13: Fill Phone', async ({ page }) => {
  await page.fill('input[type="tel"]', '1234567890');
  const value = await page.locator('input[type="tel"]').inputValue();
  expect(value).toBe('1234567890');
});

test('Test 14: Select Radio Option', async ({ page }) => {
  await page.click('input[name="radiooptions"]');
  const checked = await page.locator('input[name="radiooptions"]').isChecked();
  expect(checked).toBe(true);
});

test('Test 15: Check Form Submission', async ({ page }) => {
  await page.click('button[type="submit"]');
  const url = page.url();
  expect(url).not.toBe('https://demo.automationtesting.in/Register.html');
});

// Continue with the rest of the tests...