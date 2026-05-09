const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  workers: 1,
  timeout: 120000,
  use: {
    baseURL: 'http://localhost:8000',
    viewport: { width: 1080, height: 1920 },
    headless: false,
    launchOptions: {
      slowMo: 100,
    },
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
});
