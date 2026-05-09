class Room03 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    const assetPath = `assets/rooms/room_${padded}`;
    
    // Clear old scenes
    SpriteManager.scenes = {};

    this.state = {
      registerOpened: false,
      cocktailMixed: false,
      glassPlaced: false,
      jukeboxPlaying: false,
      hasRecipe: false,
      hasCoin: false,
      hasKey: false,
      escaped: false,
      jukeboxUnlocked: false,
      mixingProgress: { blue: 0, red: 0, gold: 0 },
      coinPickedUp: false
    };

    // Helper to load background and INITIALIZE sprites array
    const loadScene = async (sceneId, src) => {
      const img = new Image();
      try {
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = src;
        });
        SpriteManager.scenes[sceneId] = { background: img, sprites: [] };
      } catch (e) {
        console.warn(`Room03: Could not load ${src}. Using black background.`);
        SpriteManager.scenes[sceneId] = { background: null, sprites: [] };
      }
    };

    await loadScene('main', `${assetPath}/background.webp`);
    await loadScene('mirror', `${assetPath}/mirror_zoom.webp`);
    await loadScene('bottles', `${assetPath}/mirror_zoom.webp`);
    await loadScene('register', `${assetPath}/register_zoom.png`);
    await loadScene('jukebox', `${assetPath}/jukebox_zoom.webp`);
    await loadScene('jukebox_keyboard', `${assetPath}/jukebox_keyboard_zoom.webp`);
    await loadScene('diary', `${assetPath}/diary_zoom.webp`);
    await loadScene('door', `${assetPath}/door_zoom.webp`);
    
    SpriteManager.currentSceneId = 'main';
    SpriteManager.debugMode = false;



    this.mirrorOpenEmptyImg = new Image();
    await new Promise((resolve) => {
      this.mirrorOpenEmptyImg.onload = resolve;
      this.mirrorOpenEmptyImg.onerror = resolve;
      this.mirrorOpenEmptyImg.src = 'assets/rooms/room_03/mirror_zoom_brassdooropen_empty.webp';
    });

    this.mirrorOpenWithCoinImg = new Image();
    await new Promise((resolve) => {
      this.mirrorOpenWithCoinImg.onload = resolve;
      this.mirrorOpenWithCoinImg.onerror = resolve;
      this.mirrorOpenWithCoinImg.src = 'assets/rooms/room_03/mirror_zoom_brassdooropen.webp';
    });

    this.backgroundOpenImg = new Image();
    await new Promise((resolve) => {
      this.backgroundOpenImg.onload = resolve;
      this.backgroundOpenImg.onerror = resolve;
      this.backgroundOpenImg.src = 'assets/rooms/room_03/background_open.webp';
    });

    this.doorOpenZoomImg = new Image();
    await new Promise((resolve) => {
      this.doorOpenZoomImg.onload = resolve;
      this.doorOpenZoomImg.onerror = resolve;
      this.doorOpenZoomImg.src = 'assets/rooms/room_03/door_open_zoom.webp';
    });

    this.backgroundDoorOpenImg = new Image();
    await new Promise((resolve) => {
      this.backgroundDoorOpenImg.onload = resolve;
      this.backgroundDoorOpenImg.onerror = resolve;
      this.backgroundDoorOpenImg.src = 'assets/rooms/room_03/background_door_open.webp';
    });

    this.initInspectModal();
    this.setupMainScene();
    this.setupZoomScenes();
    await this.setupPuzzles();

    return this.state;
  }

  setupMainScene() {
    // 1. Exit Door (Far Left)
    SpriteManager.addSprite('main', {
      id: 'click_door', x: 0, y: 280, w: 120, h: 450,
      onClick: () => {
        if (this.state.escaped) {
          Engine.completeRoom();
        } else {
          Engine.switchScene('door');
        }
      }
    });

    // 2. Jukebox (Mid Left)
    SpriteManager.addSprite('main', {
      id: 'click_jukebox', x: 150, y: 420, w: 160, h: 340,
      onClick: () => Engine.switchScene('jukebox')
    });

    // 3. Mirror & Bottles (Combined Hotspot)
    SpriteManager.addSprite('main', {
      id: 'click_mirror', x: 510, y: 100, w: 410, h: 460,
      onClick: () => Engine.switchScene('mirror')
    });

    // 5. Cash Register (Far Right)
    SpriteManager.addSprite('main', {
      id: 'click_register', x: 780, y: 460, w: 220, h: 320,
      onClick: () => Engine.switchScene('register')
    });

    // 6. Bartender's Diary (On Counter Foreground)
    SpriteManager.addSprite('main', {
      id: 'click_diary', x: 560, y: 600, w: 200, h: 150,
      onClick: () => Engine.switchScene('diary')
    });

    // 7. Coaster '4' (On Counter Foreground)
    SpriteManager.addSprite('main', {
      id: 'click_coaster', x: 346, y: 572, w: 98, h: 77,
      onClick: () => Engine.switchScene('bottles') // Go to bottle/counter zoom
    });


  }

  setupZoomScenes() {
    // 1. Mirror Scene (Now handles bottles interaction)
    SpriteManager.addSprite('mirror', {
      id: 'cocktail_station_target', x: 250, y: 500, w: 500, h: 250,
      onClick: () => {
        if (this.state.coinPickedUp) {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '吧台下面的面板已经空了。' : 'The panel under the bar is empty.');
        } else if (this.state.cocktailMixed) {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '面板已经打开了。' : 'The panel is already open.');
        } else {
          this.showBottlesPuzzle();
        }
      }
    });

    SpriteManager.addSprite('mirror', {
      id: 'pickup_coin_from_door', x: 400, y: 750, w: 200, h: 150,
      onClick: () => {
        if (this.state.cocktailMixed && !this.state.coinPickedUp) {
          this.state.coinPickedUp = true;
          Engine.pickupItem('jukebox_coin', window.innerWidth/2, window.innerHeight/2);
          SpriteManager.scenes['mirror'].background = this.mirrorOpenEmptyImg;
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '获得点唱机硬币。' : 'Obtained a jukebox coin.');
        }
      }
    });



    SpriteManager.addSprite('bottles', {
      id: 'small_brass_key_item', x: 470, y: 900, w: 80, h: 80,
      visible: false,
      glint: true,
      onClick: () => {
        this.state.hasKey = true;
        SpriteManager.updateSprite('bottles', 'small_brass_key_item', { visible: false });
        Engine.pickupItem('bar_exit_key', window.innerWidth/2, window.innerHeight/2);
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '获得酒吧储物间钥匙。' : 'Obtained the Bar Storage Key.');
      }
    });


    // 4. Diary Scene
    SpriteManager.addSprite('diary', {
      id: 'read_diary', x: 100, y: 100, w: 824, h: 824,
      onClick: () => Dialog.showStory(this.roomData.story_fragment)
    });

    // 5. Door Scene
    SpriteManager.addSprite('door', {
      id: 'door_keyhole', x: 340, y: 550, w: 80, h: 160,
      onClick: () => {
        if (this.state.escaped) {
          Engine.completeRoom();
          return;
        }
        if (Inventory.selectedItem && Inventory.selectedItem.id === 'bar_exit_key') {
          this.state.escaped = true;
          Audio.playSFX('door_open');
          Inventory.removeItem('bar_exit_key');
          
          // Update backgrounds for both zoom and main view
          SpriteManager.scenes['door'].background = this.doorOpenZoomImg;
          SpriteManager.scenes['main'].background = this.backgroundDoorOpenImg;
          
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '储物间门已打开。' : 'Storage door opened.');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '门锁着。我需要酒吧储物间钥匙。' : 'The door is locked. I need the Bar Storage Key.');
        }
      }
    });
  }

  async setupPuzzles() {
    // Custom SVG Cash Register Keypad (Dial Zoom View Style)
    this.showRegisterPuzzle = async () => {
      const modal = document.createElement('div');
      modal.id = 'custom-register-modal';
      modal.className = 'modal zoom-mode';
      modal.style.position = 'absolute';
      modal.style.top = '0';
      modal.style.left = '0';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
      modal.style.display = 'flex';
      modal.style.justifyContent = 'center';
      modal.style.alignItems = 'center';
      modal.style.zIndex = '2000';

      // Load SVG from file
      let svgText = "";
      try {
        const response = await fetch('assets/ui/register_keypad.svg');
        svgText = await response.text();
      } catch (e) {
        console.error("Failed to load register SVG", e);
        return;
      }

      modal.innerHTML = `
        <div class="zoom-overlay-container">
          <div class="zoom-inner-box centered-layout" id="register-overlay-inner">
            <div id="dial-wrapper" style="position: relative; width: 800px; height: 800px; overflow: hidden;">
              <img src="assets/rooms/room_03/register_zoom.png" id="dial-bg" style="width: 100%; height: 100%; object-fit: contain; filter: blur(4px) brightness(0.8); transform: scale(1.05);">
              
              <div class="dial-frame" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 750px; height: 750px; pointer-events: auto;">
                ${svgText}
              </div>
            </div>
          </div>
          <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
        </div>
      `;

      document.getElementById('ui-design-container').appendChild(modal);

      // Force SVG to fill the container
      const svgEl = modal.querySelector('svg');
      if (svgEl) {
        svgEl.style.width = '100%';
        svgEl.style.height = '100%';
      }

      // We need to query buttons from the modal now
      const container = modal;

      // Logic: Array of 4 digits
      let currentInput = ["-", "-", "-", "-"];
      const updateDisplay = () => {
        for (let i = 1; i <= 4; i++) {
          const el = document.getElementById(`digit-${i}`);
          if (el) el.textContent = currentInput[i-1];
        }
      };

      const buttons = container.querySelectorAll('.svg-btn');
      buttons.forEach(btn => {
        btn.style.cursor = 'pointer';
        btn.addEventListener('click', (e) => {
          e.stopPropagation(); // Prevent modal close
          const col = parseInt(btn.getAttribute('data-col'));
          const val = btn.getAttribute('data-val');
          Audio.playSFX('button_press');
          
          // Update the specific column
          currentInput[col-1] = val;
          updateDisplay();
          
          // Check win condition
          if (currentInput.join('') === "1385") {
            Audio.playSFX('cash_register');
            this.state.registerOpened = true;
            Dialog.showFeedback(I18n.currentLang === 'zh' ? '收银机打开了！' : 'Cash register opened!');
            Engine.pickupItem('cocktail_recipe', 540, 960);
            setTimeout(() => modal.remove(), 1000);
          }
        });
      });

      // Close on clicking outside the inner box
      modal.onclick = (e) => {
        if (e.target === modal || e.target.id === 'dial-wrapper') {
          modal.remove();
        }
      };
    };

    this.showJukeboxPuzzle = async () => {
      const modal = document.createElement('div');
      modal.id = 'custom-jukebox-modal';
      modal.className = 'modal zoom-mode';
      modal.style.position = 'absolute';
      modal.style.top = '0';
      modal.style.left = '0';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
      modal.style.display = 'flex';
      modal.style.justifyContent = 'center';
      modal.style.alignItems = 'center';
      modal.style.zIndex = '2000';

      let svgText = "";
      try {
        const response = await fetch('assets/ui/jukebox_keyboard.svg');
        svgText = await response.text();
      } catch (e) {
        console.error("Failed to load jukebox SVG", e);
        return;
      }

      modal.innerHTML = `
        <div class="zoom-overlay-container">
          <div class="zoom-inner-box centered-layout">
            <div id="dial-wrapper" style="position: relative; width: 800px; height: 800px; overflow: hidden;">
              <img src="assets/rooms/room_03/jukebox_zoom.webp" id="dial-bg" style="width: 100%; height: 100%; object-fit: contain; filter: blur(4px) brightness(0.8);">
              
              <div class="dial-frame" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 600px; height: 600px; pointer-events: auto;">
                ${svgText}
              </div>
            </div>
          </div>
          <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
        </div>
      `;

      document.getElementById('ui-design-container').appendChild(modal);

      const svgEl = modal.querySelector('svg');
      if (svgEl) {
        svgEl.style.width = '100%';
        svgEl.style.height = '100%';
      }

      let currentInput = "";
      const displayEl = modal.querySelector('#jukebox-display');

      const buttons = modal.querySelectorAll('.svg-btn');
      buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const val = btn.getAttribute('data-val');
          Audio.playSFX('button_press');

          if (val === "SELECT") {
            if (currentInput === "B7") {
              Dialog.showFeedback(I18n.currentLang === 'zh' ? '播放：B7 —— 告别格兰德维尤' : 'Playing: B7 - Farewell to the Grandview');
              this.playJukebox();
              setTimeout(() => modal.remove(), 1000);
            } else {
              Dialog.showFeedback(I18n.currentLang === 'zh' ? '无效的选择。' : 'Invalid selection.');
              currentInput = "";
              if (displayEl) displayEl.textContent = "__";
            }
          } else {
            if (currentInput.length === 0 && isNaN(val)) {
              currentInput = val;
            } else if (currentInput.length === 1 && !isNaN(val)) {
              currentInput += val;
            } else {
              currentInput = val;
            }
            if (displayEl) displayEl.textContent = currentInput.padEnd(2, '_');
          }
        });
      });

      modal.onclick = (e) => {
        if (e.target === modal || e.target.className === 'zoom-overlay-container') {
          modal.remove();
        }
      };
    };

    SpriteManager.addSprite('register', {
      id: 'register_keypad_target', x: 350, y: 350, w: 300, h: 300,
      onClick: () => {
        if (!this.state.registerOpened) this.showRegisterPuzzle();
      }
    });

    SpriteManager.addSprite('jukebox', {
      id: 'jukebox_target', x: 800, y: 500, w: 200, h: 400, // Placeholder coordinates
      onClick: () => {
        if (this.state.jukeboxPlaying) return;
        if (Inventory.selectedItem && Inventory.selectedItem.id === 'jukebox_coin') {
          Inventory.removeItem('jukebox_coin');
          this.showJukeboxPuzzle();
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '需要使用点唱机硬币。' : 'Need to use the jukebox coin.');
        }
      }
    });

    this.showBottlesPuzzle = async () => {
      const modal = document.createElement('div');
      modal.id = 'custom-bottles-modal';
      modal.className = 'modal zoom-mode';
      modal.style.position = 'absolute';
      modal.style.top = '0';
      modal.style.left = '0';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
      modal.style.display = 'flex';
      modal.style.justifyContent = 'center';
      modal.style.alignItems = 'center';
      modal.style.zIndex = '2000';

      // Load SVG from file
      let svgText = "";
      try {
        const response = await fetch('assets/ui/cocktail_station.svg');
        svgText = await response.text();
      } catch (e) {
        console.error("Failed to load cocktail SVG", e);
        return;
      }

      modal.innerHTML = `
        <div class="zoom-overlay-container">
          <div class="zoom-inner-box centered-layout">
            <div id="dial-wrapper" style="position: relative; width: 800px; height: 800px; overflow: hidden;">
              <img src="assets/rooms/room_03/mirror_zoom.webp" id="dial-bg" style="width: 100%; height: 100%; object-fit: contain; filter: blur(4px) brightness(0.8);">
              
              <div class="dial-frame" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 750px; height: 750px; pointer-events: auto;">
                ${svgText}
              </div>
            </div>
          </div>
          <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
        </div>
      `;

      document.getElementById('ui-design-container').appendChild(modal);

      // Force SVG to fill the container
      const svgEl = modal.querySelector('svg');
      if (svgEl) {
        svgEl.style.width = '100%';
        svgEl.style.height = '100%';
      }


      const buttons = modal.querySelectorAll('.svg-btn');
      let selectedGlass = false;

      buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const type = btn.getAttribute('data-type');
          
          if (type === 'bottle') {
            const color = btn.getAttribute('data-color');
            this.pourDrink(color);
          } else if (type === 'glass') {
            selectedGlass = true;
            btn.classList.add('selected-glass');
            Dialog.showFeedback(I18n.currentLang === 'zh' ? '水晶杯已选中。' : 'Glass selected.');
          } else if (type === 'coaster') {
            const num = parseInt(btn.getAttribute('data-num'));
            if (selectedGlass) {
              if (this.state.cocktailMixed) {
                modal.remove(); // Close zoom view
                this.placeOnCoaster(num);
              } else {
                Dialog.showFeedback(I18n.currentLang === 'zh' ? '杯子里还是空的。' : 'The glass is empty.');
              }
            } else {
              Dialog.showFeedback(I18n.currentLang === 'zh' ? '先选中杯子。' : 'Select the glass first.');
            }
          }
        });
      });

      modal.onclick = (e) => {
        if (e.target === modal || e.target.id === 'dial-wrapper') {
          modal.remove();
        }
      };
    };

    this.openDrawerModal = () => {
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;

      Dialog.inspectItem('assets/rooms/room_03/drawer_open_patch.png', [
        {
          x: centerX - 100, y: centerY - 180, w: 200, h: 200,
          onClick: () => {
            if (!this.state.coinPickedUp) {
              this.state.coinPickedUp = true;
              Engine.pickupItem('jukebox_coin', window.innerWidth / 2, window.innerHeight / 2);
              const img = document.getElementById('item-inspect-image');
              if (img) img.src = 'assets/rooms/room_03/drawer_open_empty_patch.png';
            }
          }
        }
      ]);
    };



    SpriteManager.addSprite('diary', {
      id: 'diary_target', x: 500, y: 700, w: 150, h: 100, // Placeholder coordinates
      onClick: () => {
        Dialog.inspectItem('assets/rooms/room_03/diary_zoom.webp');
      }
    });
  }

  pourDrink(color) {
    if (this.state.cocktailMixed) return;
    this.state.mixingProgress[color]++;
    Audio.playSFX('liquid_pour');
    
    // Update SVG liquid layer
    const modal = document.getElementById('custom-bottles-modal');
    if (modal) {
      const p = this.state.mixingProgress;
      const totalParts = p.blue + p.red + p.gold;
      const layerId = `liquid-layer-${totalParts}`;
      const layer = modal.querySelector(`#${layerId}`);
      if (layer) {
        const colors = {
          blue: '#0055a5',
          red: '#c00000',
          gold: '#d4af37'
        };
        layer.setAttribute('fill', colors[color]);
      }
    }
    
    const p = this.state.mixingProgress;
    const totalParts = p.blue + p.red + p.gold;
    
    if (totalParts === 6) {
      if (p.blue === 2 && p.red === 1 && p.gold === 3) {
        this.state.cocktailMixed = true;
        Audio.playSFX('unlock');
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '鸡尾酒调制完成！现在把它放在杯垫上。' : 'Cocktail mixed! Now place it on the coaster.');
      } else {
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '配方不对。重倒一杯。' : 'Wrong mix. Starting over.');
        this.state.mixingProgress = { blue: 0, red: 0, gold: 0 };
        // Reset liquid level in SVG
        if (modal) {
          for (let i = 1; i <= 6; i++) {
            const layer = modal.querySelector(`#liquid-layer-${i}`);
            if (layer) {
              layer.setAttribute('fill', 'none');
            }
          }
        }
      }
    }
  }

  placeOnCoaster(coasterNumber) {
    if (!this.state.cocktailMixed) {
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '杯子里还是空的。' : 'The glass is empty.');
      return;
    }
    
    if (coasterNumber === 4) {
      Audio.playSFX('mechanical_click');
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '吧台下面的隐藏面板打开了，里面有一枚硬币！' : 'A hidden panel under the bar opened, revealing a coin!');
      
      SpriteManager.scenes['main'].background = this.backgroundOpenImg;
      SpriteManager.scenes['mirror'].background = this.mirrorOpenWithCoinImg;
      Engine.switchScene('mirror');
    } else {
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '什么也没发生。酒洒了，需要重新调制。' : 'Nothing happened. The drink spilled and you need to start over.');
      this.state.cocktailMixed = false;
      this.state.mixingProgress = { blue: 0, red: 0, gold: 0 };
    }
  }

  async playJukebox() {
    if (this.state.jukeboxPlaying) return;
    this.state.jukeboxPlaying = true;
    await new Promise(res => setTimeout(res, 2000));
    Audio.playSFX('mechanical_click');
    Dialog.showFeedback(I18n.currentLang === 'zh' ? '歌曲结束。点唱机背面弹出了酒吧储物间钥匙！' : 'Song finished. The Bar Storage Key popped out of the back!');
    Engine.pickupItem('bar_exit_key', 540, 960);
  }

  cleanup() {
    if (this.cashRegisterKeypad) this.cashRegisterKeypad.cleanup();
  }
}

window.Room03 = Room03;
