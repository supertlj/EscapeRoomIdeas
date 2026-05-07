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
      mixingProgress: { blue: 0, red: 0, gold: 0 }
    };

    // Scene loading with placeholders
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
    await loadScene('bottles', `${assetPath}/bottles_zoom.webp`);
    await loadScene('register', `${assetPath}/register_zoom.webp`);
    await loadScene('jukebox', `${assetPath}/jukebox_zoom.webp`);
    await loadScene('door', `${assetPath}/door_zoom.webp`);
    
    SpriteManager.currentSceneId = 'main';

    this.initInspectModal();
    this.setupMainScene();
    this.setupZoomScenes();
    this.setupPuzzles();
  }

  setupMainScene() {
    // Mirror Zoom
    SpriteManager.addSprite('main', {
      id: 'click_mirror', x: 200, y: 150, w: 600, h: 300,
      onClick: () => Engine.switchScene('mirror')
    });

    // Bottles Zoom
    SpriteManager.addSprite('main', {
      id: 'click_bottles', x: 250, y: 450, w: 500, h: 200,
      onClick: () => Engine.switchScene('bottles')
    });

    // Register Zoom
    SpriteManager.addSprite('main', {
      id: 'click_register', x: 750, y: 550, w: 150, h: 150,
      onClick: () => Engine.switchScene('register')
    });

    // Jukebox Zoom
    SpriteManager.addSprite('main', {
      id: 'click_jukebox', x: 50, y: 600, w: 180, h: 300,
      onClick: () => Engine.switchScene('jukebox')
    });

    // Exit Door
    SpriteManager.addSprite('main', {
      id: 'click_door', x: 450, y: 200, w: 120, h: 350,
      onClick: () => Engine.switchScene('door')
    });
  }

  setupZoomScenes() {
    // 1. Mirror Scene
    SpriteManager.addSprite('mirror', {
      id: 'mirror_napkin_reflected', x: 400, y: 300, w: 200, h: 200,
      onClick: () => Dialog.showFeedback(I18n.currentLang === 'zh' ? '餐厅纸上的数字在镜子里是反转的：5831' : 'The numbers on the napkin are reversed in the mirror: 5831')
    });

    // 2. Bottles & Mixing Scene
    // Blue Bottle
    SpriteManager.addSprite('bottles', {
      id: 'bottle_blue', x: 200, y: 200, w: 100, h: 300,
      onClick: () => this.pourDrink('blue')
    });
    // Red Bottle
    SpriteManager.addSprite('bottles', {
      id: 'bottle_red', x: 450, y: 200, w: 100, h: 300,
      onClick: () => this.pourDrink('red')
    });
    // Gold Bottle
    SpriteManager.addSprite('bottles', {
      id: 'bottle_gold', x: 700, y: 200, w: 100, h: 300,
      onClick: () => this.pourDrink('gold')
    });

    // Crystal Glass / Coaster
    SpriteManager.addSprite('bottles', {
      id: 'crystal_glass_coaster', x: 430, y: 700, w: 150, h: 150,
      onClick: () => {
        if (this.state.cocktailMixed && !this.state.glassPlaced) {
          this.state.glassPlaced = true;
          Audio.playSFX('mechanical_click');
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '调好的酒杯放在了4号杯垫上。吧台下弹出了一个面板！' : 'Placed the mixed glass on coaster 4. A panel opened under the bar!');
          SpriteManager.updateSprite('bottles', 'small_brass_key', { visible: true });
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '标有"4"的黄铜杯垫。' : 'A brass coaster marked "4".');
        }
      }
    });

    // Small Brass Key (Reward from Mixing)
    SpriteManager.addSprite('bottles', {
      id: 'small_brass_key', x: 480, y: 880, w: 80, h: 80,
      visible: false,
      onClick: () => {
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '这把钥匙看起来太小，打不开大门。也许是给点唱机准备的。' : 'This key looks too small for the main door. Maybe for the jukebox.');
        // Actually the design says the coin is in the register. 
        // Let's assume this key unlocks the back of the jukebox if needed, or just a story item.
      }
    });

    // 3. Register Scene
    SpriteManager.addSprite('register', {
      id: 'register_keypad_target', x: 350, y: 350, w: 300, h: 300,
      onClick: () => this.cashRegisterKeypad.show()
    });

    // 4. Jukebox Scene
    SpriteManager.addSprite('jukebox', {
      id: 'jukebox_coin_slot', x: 450, y: 400, w: 100, h: 100,
      onClick: () => {
        if (Inventory.selectedItem && Inventory.selectedItem.id === 'jukebox_coin') {
          Inventory.removeItem('jukebox_coin');
          Audio.playSFX('coin_insert');
          this.state.hasCoin = true;
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '投币成功。请选择曲目。' : 'Coin inserted. Please select a track.');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '需要一枚点唱机硬币。' : 'Needs a jukebox coin.');
        }
      }
    });

    SpriteManager.addSprite('jukebox', {
      id: 'jukebox_button_b7', x: 480, y: 600, w: 80, h: 80,
      onClick: () => {
        if (!this.state.hasCoin) {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '先投币。' : 'Insert coin first.');
          return;
        }
        Audio.playSFX('mechanical_tick');
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '播放：B7 —— 告别格兰德维尤' : 'Playing: B7 - Farewell to the Grandview');
        this.playJukebox();
      }
    });

    // 5. Door Scene
    SpriteManager.addSprite('door', {
      id: 'bar_keyhole', x: 450, y: 450, w: 120, h: 120,
      onClick: () => {
        if (this.state.escaped) {
          Engine.completeRoom();
          return;
        }
        if (Inventory.selectedItem && Inventory.selectedItem.id === 'bar_exit_key') {
          Audio.playSFX('door_open');
          Inventory.removeItem('bar_exit_key');
          this.state.escaped = true;
          SpriteManager.setScene('door', 'assets/rooms/room_03/door_open_zoom.webp');
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '储物间门已打开。' : 'Storage door opened.');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '门锁着。我需要酒吧储物间钥匙。' : 'The door is locked. I need the Bar Storage Key.');
        }
      }
    });
  }

  setupPuzzles() {
    this.cashRegisterKeypad = new KeypadPuzzle({
      targetCode: '1385',
      onSuccess: () => {
        Audio.playSFX('cash_register');
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '收银机打开了！' : 'Cash register opened!');
        this.state.registerOpened = true;
        
        // Collect items
        Engine.pickupItem('cocktail_recipe', 540, 960);
        Engine.pickupItem('jukebox_coin', 540, 960);
      }
    });
    this.cashRegisterKeypad.init();
  }

  pourDrink(color) {
    if (this.state.cocktailMixed) return;
    
    this.state.mixingProgress[color]++;
    Audio.playSFX('liquid_pour');
    
    // Check Recipe: 2 Blue, 1 Red, 3 Gold
    const p = this.state.mixingProgress;
    if (p.blue === 2 && p.red === 1 && p.gold === 3) {
      this.state.cocktailMixed = true;
      Audio.playSFX('unlock');
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '鸡尾酒调制完成！' : 'Cocktail mixed!');
    } else if (p.blue > 2 || p.red > 1 || p.gold > 3) {
      // Reset if overshoot
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '配方不对。重倒一杯。' : 'Wrong mix. Starting over.');
      this.state.mixingProgress = { blue: 0, red: 0, gold: 0 };
    }
  }

  async playJukebox() {
    if (this.state.jukeboxPlaying) return;
    this.state.jukeboxPlaying = true;
    
    // Simulate song playing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    Audio.playSFX('mechanical_click');
    Dialog.showFeedback(I18n.currentLang === 'zh' ? '歌曲结束了。点唱机背面弹出了一个小格！' : 'Song finished. A panel popped open on the back of the jukebox!');
    
    // Pickup Exit Key
    Engine.pickupItem('bar_exit_key', 540, 960);
  }

  cleanup() {
    if (this.cashRegisterKeypad) this.cashRegisterKeypad.cleanup();
  }
}

window.Room03 = Room03;
