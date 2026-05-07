const { test, expect } = require('@playwright/test');

test('Room 02 Walkthrough', async ({ page }) => {
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

  // Ensure we are in Room 02
  await page.evaluate(() => {
    localStorage.clear();
    Engine.loadRoom(2);
  });
  await page.waitForTimeout(1000);

  // 1. Close story modal
  await page.click('#story-close');
  await page.waitForTimeout(500);

  // 1a. Check Chalkboard for prices
  // click_chalkboard: x: 620, y: 310, w: 100, h: 200
  // Abs Center: 698, 810
  await clickDesign(698, 810, "Check Chalkboard");
  await page.waitForTimeout(1000);
  await page.click('#btn-back');
  
  // 1b. Check Chef Note on Table 4
  // click_table_4: x: 20, y: 580, w: 320, h: 220
  // Abs Center: 20 + 28 + 160 = 208, 580 + 400 + 110 = 1090
  await clickDesign(208, 1090, "Zoom Table 4");
  await page.waitForTimeout(1000);
  // table_4_chef_note in zoom: x: 200, y: 550, w: 300, h: 400
  // Abs Zoom Center: 28 + 200 + 150 = 378, 400 + 550 + 200 = 1150
  await clickDesign(378, 1150, "Read Chef Note");
  await page.waitForTimeout(1000);
  await page.click('#btn-back');
  await page.waitForTimeout(500);

  // 2. Click Cabinet to zoom
  // click_cabinet: x: 90, y: 310, w: 120, h: 140
  // Abs: 118, 710 -> Center: 178, 780
  await clickDesign(178, 780, "Zoom Cabinet");
  await page.waitForTimeout(1000);

  // 3. Enter Code 472 on Combination Lock
  // cabinet_lock_target: x: 360, y: 430, w: 350, h: 140
  // Abs: 388, 830 -> Center: 563, 900
  await clickDesign(563, 900, "Click Cabinet Lock Target");
  await page.waitForSelector('#combination-lock-modal:not(.hidden)', { state: 'visible' });
  
  console.log("Entering code 472...");
  for (let i = 0; i < 4; i++) await page.click('#roller-0');
  for (let i = 0; i < 7; i++) await page.click('#roller-1');
  for (let i = 0; i < 2; i++) await page.click('#roller-2');
  await page.waitForTimeout(2000); // Wait for unlock animation

  // 4. Pick up Corkscrew
  // brass_corkscrew_item: x: 330, y: 450, w: 200, h: 300
  // Abs: 358, 850 -> Center: 458, 1000
  await clickDesign(458, 1000, "Pick up Corkscrew");
  await page.waitForTimeout(1500);

  // 5. Go Back
  await page.click('#btn-back');
  await page.waitForTimeout(500);

  // 6. Click Hatch to zoom
  // click_hatch: x: 790, y: 240, w: 200, h: 270
  // Abs: 818, 640 -> Center: 918, 775
  await clickDesign(918, 775, "Zoom Hatch");
  await page.waitForTimeout(1000);

  // 7. Enter Code 51 on Dial
  // hatch_lock_target: x: 350, y: 380, w: 250, h: 250
  // Abs: 378, 780 -> Center: 503, 905
  await clickDesign(503, 905, "Click Hatch Lock Target");
  await page.waitForSelector('#dial-puzzle-container:not(.hidden)', { state: 'visible' });
  
  console.log("Setting dial to 51...");
  for (let i = 0; i < 51; i++) {
    await page.click('#btn-dial-right');
    if (i % 10 === 0) await page.waitForTimeout(50);
  }
  await page.waitForTimeout(2000);

  // 8. Pick up Vintage Bottle
  // vintage_bottle_item: x: 350, y: 400, w: 300, h: 400
  // Abs: 378, 800 -> Center: 528, 1000
  // WAIT: hatch_lock_target is ON TOP (y up to 1028). Click lower at y=1100
  await clickDesign(528, 1100, "Pick up Vintage Bottle");
  await page.waitForTimeout(1500);

  // 9. Go Back
  await page.click('#btn-back');
  await page.waitForTimeout(1000);

  // 10. Examine Bottle and Use Corkscrew
  await page.click('.inv-slot:nth-child(2)'); // Vintage Bottle
  await page.waitForSelector('#item-inspect-modal:not(.hidden)');
  
  // Select Corkscrew
  await page.click('.inv-slot:nth-child(1)');
  // Click bottle in inspection view (safe area: center)
  // Target: 540, 912
  await clickDesign(540, 912, "Use Corkscrew on Bottle");
  await page.waitForTimeout(1500);

  // 11. Pick up Key from open bottle
  // Center of inspect modal: 540, 960
  await clickDesign(540, 960, "Pick up Key from Bottle");
  await page.waitForTimeout(1500);
  
  // 12. Go to Door zoom
  // exit_door: x: 380, y: 220, w: 160, h: 400
  // Abs: 408, 620 -> Center: 488, 820
  await clickDesign(488, 820, "Zoom Door");
  await page.waitForTimeout(1000);
  
  // 13. Use Dining Key on Door
  await page.click('.inv-slot:nth-child(1)'); // Dining Key
  // keyhole: x: 440, y: 350, w: 140, h: 220
  // Abs: 468, 750 -> Center: 538, 860
  await clickDesign(538, 860, "Use Key on Door");
  await page.waitForTimeout(1000);
  
  // 14. Exit Door
  // keyhole again to exit
  await clickDesign(538, 860, "Exit Door");
  await page.waitForTimeout(1000);

  // Click "Next Room" on the completion modal
  console.log("Clicking Next Room button...");
  await page.click('#btn-next-room');
  await page.waitForTimeout(2000);
  
  // 15. Verify Room Complete (Hotel Bar)
  const roomTitle = await page.textContent('#room-title');
  expect(roomTitle.toLowerCase()).toContain('bar');
});
