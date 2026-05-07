const { test, expect } = require('@playwright/test');

test('Room 01 Walkthrough', async ({ page }) => {
  const drawClickDot = async (x, y) => {
    await page.evaluate((p) => {
      const dot = document.createElement('div');
      dot.style.position = 'fixed';
      dot.style.left = (p.x - 10) + 'px';
      dot.style.top = (p.y - 10) + 'px';
      dot.style.width = '20px';
      dot.style.height = '20px';
      dot.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';
      dot.style.border = '2px solid white';
      dot.style.borderRadius = '50%';
      dot.style.zIndex = '999999';
      dot.style.pointerEvents = 'none';
      document.body.appendChild(dot);
      setTimeout(() => dot.remove(), 1000);
    }, { x, y });
  };

  const clickDesign = async (x, y, label = "click") => {
    const start = Date.now();
    const timeout = 10000;
    
    while (Date.now() - start < timeout) {
      const busy = await page.evaluate(() => Engine.busyCount);
      const hitId = await page.evaluate((p) => {
        const s = SpriteManager.hitTest(p.x, p.y);
        return s ? s.id : 'none';
      }, { x, y });
      
      console.log(`[${label}] Busy: ${busy}, Hit: ${hitId} at ${x}, ${y}`);
      
      if (busy === 0) {
        await drawClickDot(x, y);
        await page.mouse.click(x, y);
        await page.waitForTimeout(500);
        return;
      }
      await page.waitForTimeout(500);
    }
    throw new Error(`Failed to click ${label}: Engine stayed busy or click failed to trigger.`);
  };

  await page.goto('/');

  // Ensure we are in Room 01 and state is reset
  await page.evaluate(() => {
    localStorage.clear();
    Engine.loadRoom(1);
  });
  await page.waitForTimeout(1000);

  // 1. Close story modal
  await page.click('#story-close');
  await page.waitForTimeout(500);

  // 1b. Read Guestbook
  await clickDesign(318, 1050, "Open Guestbook");
  await page.waitForTimeout(500);
  await clickDesign(540, 912, "Read Guestbook");
  await page.waitForTimeout(500);
  await page.click('#story-close');
  await page.waitForTimeout(500);
  await page.click('#btn-back');
  await page.waitForTimeout(500);

  // 2. Click Chandelier to zoom
  await clickDesign(628, 590, "Zoom Chandelier");
  await page.waitForTimeout(1000);

  // 3. Pick up Brass Key
  await page.waitForTimeout(1000);
  await clickDesign(548, 1030, "Pick up Key");
  await page.waitForTimeout(1500);

  // 4. Go Back
  await page.click('#btn-back');
  await page.waitForTimeout(500);

  // 5. Click Safe to zoom
  await clickDesign(208, 1255, "Zoom Safe");
  await page.waitForTimeout(500);

  // 6. Use Key on Safe
  await page.click('.inv-slot:nth-child(1)');
  await clickDesign(540, 912, "Use Key on Safe");
  await page.waitForTimeout(1000);

  // 7. Pick up Note
  await page.waitForTimeout(500);
  await clickDesign(433, 1165, "Pick up Note");
  await page.waitForTimeout(1500);
  // CLOSE inspection modal
  await drawClickDot(100, 300);
  await page.click('#item-inspect-modal', { position: { x: 100, y: 300 } });
  await page.waitForTimeout(1000);

  // 8. Go Back
  await page.click('#btn-back');
  await page.waitForTimeout(1000);

  // 9. Click Elevator to zoom
  await clickDesign(758, 920, "Zoom Elevator");
  await page.waitForTimeout(2000);

  // 10. Click Keypad
  await clickDesign(808, 925, "Click Keypad");
  
  // Wait for keypad to appear (it uses ID #keypad-modal)
  await page.waitForSelector('#keypad-modal:not(.hidden)', { state: 'visible', timeout: 5000 });
  await page.waitForTimeout(500);

  // 11. Enter Code 3142
  console.log("Entering code 3142...");
  
  for (const val of ['3', '1', '4', '2']) {
    console.log(`Clicking Keypad Button: ${val}`);
    await page.click(`#keypad-modal .key-btn[data-val="${val}"]`, { force: true });
    await page.waitForTimeout(200);
  }
  await page.waitForTimeout(1000);

  // 12. Click to complete room
  // We are still in zoom_elevator, need to click the open elevator sprite
  await clickDesign(540, 912, "Exit Elevator");
  await page.waitForTimeout(1000);
  
  // Click "Next Room" on the completion modal
  console.log("Clicking Next Room button...");
  await page.click('#btn-next-room');
  await page.waitForTimeout(2000);

  // 13. Verify Room 02
  const roomTitle = await page.textContent('#room-title');
  expect(roomTitle.toLowerCase()).toContain('restaurant');
});
