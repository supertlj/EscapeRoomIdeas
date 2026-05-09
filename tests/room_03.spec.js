const { test, expect } = require('@playwright/test');

test('Room 03 Load Test', async ({ page }) => {
  await page.goto('/');

  // Ensure we are in Room 03
  await page.evaluate(() => {
    localStorage.clear();
    Engine.loadRoom(3);
  });
  await page.waitForTimeout(1000);

  // Close story modal if visible
  const storyClose = await page.$('#story-close');
  if (storyClose) {
    await storyClose.click();
  }
  await page.waitForTimeout(500);

  // Verify Room 03 Title
  const roomTitle = await page.textContent('#room-title');
  expect(roomTitle.toLowerCase()).toContain('bar');
});
