class Room02 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    const assetPath = `assets/rooms/room_${padded}`;
    
    // Clear old scenes
    SpriteManager.scenes = {};

    this.state = {
      wineCabinetLocked: true,
      kitchenHatchLocked: true,
      hasVintageBottle: false,
      hasCorkscrew: false,
      hasDiningKey: false,
      bottleOpened: false
    };

    // Helper to load background and INITIALIZE sprites array
    const loadScene = async (sceneId, src) => {
      const img = new Image();
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = src;
      });
      // CRITICAL: Must have sprites array for addSprite to work!
      SpriteManager.scenes[sceneId] = { background: img, sprites: [] };
    };

    // Load everything silently
    await loadScene('main', `${assetPath}/background.png`);
    await loadScene('chalkboard', `${assetPath}/chalkboard_zoom.png`);
    await loadScene('table_2', `${assetPath}/table_2_zoom.png`);
    await loadScene('table_4', `${assetPath}/table_4_zoom.png`);
    await loadScene('table_7', `${assetPath}/table_7_zoom.png`);
    await loadScene('hatch', `${assetPath}/hatch_zoom.png`);
    await loadScene('cabinet', `${assetPath}/cabinet_zoom.png`);
    
    // Set the starting scene correctly
    SpriteManager.currentSceneId = 'main';

    // IMPORTANT: Call these AFTER all scenes are loaded and initialized
    this.setupMainScene();
    this.setupZoomScenes();
    this.setupPuzzles();

    HintSystem.setCurrentPuzzle(0);
    return this.state;
  }

  setupMainScene() {
    // Zoom to Chalkboard
    SpriteManager.addSprite('main', {
      id: 'click_chalkboard', x: 580, y: 310, w: 160, h: 360,
      onClick: () => Engine.switchScene('chalkboard')
    });

    // Zoom to Tables
    SpriteManager.addSprite('main', {
      id: 'click_table_4', x: 20, y: 580, w: 320, h: 220,
      onClick: () => Engine.switchScene('table_4')
    });
    SpriteManager.addSprite('main', {
      id: 'click_table_7', x: 250, y: 760, w: 500, h: 260,
      onClick: () => Engine.switchScene('table_7')
    });
    SpriteManager.addSprite('main', {
      id: 'click_table_2', x: 740, y: 640, w: 280, h: 280,
      onClick: () => Engine.switchScene('table_2')
    });

    // Zoom to Puzzles
    SpriteManager.addSprite('main', {
      id: 'click_hatch', x: 790, y: 240, w: 200, h: 270,
      onClick: () => Engine.switchScene('hatch')
    });
    SpriteManager.addSprite('main', {
      id: 'click_cabinet', x: 90, y: 310, w: 120, h: 140,
      onClick: () => Engine.switchScene('cabinet')
    });

    // Exit Door
    SpriteManager.addSprite('main', {
      id: 'exit_door', x: 380, y: 220, w: 160, h: 400,
      onClick: () => {
        if (this.state.hasDiningKey) {
          Audio.playSFX('door_open');
          Dialog.showStory(I18n.currentLang === 'zh' ? '你用钥匙打开了门，离开餐厅进入了走廊。' : 'You use the key to open the door and leave the restaurant into the corridor.', () => {
            Engine.completeRoom();
          });
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '门锁着。我需要餐厅钥匙。' : 'The door is locked. I need the Dining Room Key.');
        }
      }
    });
  }

  setupZoomScenes() {
    // Relying on global UI back button. No local hotspots needed.
    // Chalkboard details
    SpriteManager.addSprite('chalkboard', {
      id: 'read_menu', x: 200, y: 200, w: 600, h: 600,
      onClick: () => Dialog.showFeedback(I18n.currentLang === 'zh' ? '主厨特供：龙虾浓汤 $14，菲力牛排 $28，焦糖布丁 $9。' : 'Chef\'s Special: Lobster Bisque $14, Filet Mignon $28, Crème Brûlée $9.')
    });
  }

  setupPuzzles() {
    // Kitchen Hatch Puzzle (Code 51) using the new DialPuzzle
    this.hatchDial = new DialPuzzle({
      targetValue: 51,
      assetPath: 'assets/rooms/room_02/dial.png',
      onSuccess: async () => {
        this.state.kitchenHatchLocked = false;
        Audio.playSFX('door_open');
        this.hatchDial.hide();
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '传菜窗打开了。里面有一瓶陈年酒。' : 'The hatch opens. There is a vintage bottle inside.');
        
        const bottleData = { 
          id: 'vintage_bottle', 
          name: this.roomData.items[0].name,
          icon: 'assets/items/room_02/vintage_bottle.png'
        };
        Engine.pickupItem(bottleData, 512, 512);
        this.state.hasVintageBottle = true;
      }
    });
    this.hatchDial.init();
    SpriteManager.addSprite('hatch', {
      id: 'hatch_lock_target', x: 400, y: 350, w: 250, h: 250,
      onClick: () => { if (this.state.kitchenHatchLocked) this.hatchDial.show(); }
    });

    // Wine Cabinet Puzzle (Code 472)
    this.cabinetKeypad = new KeypadPuzzle({
      targetCode: '472',
      cssClass: 'keypad-room02',
      onSuccess: async () => {
        this.state.wineCabinetLocked = false;
        Audio.playSFX('door_open');
        this.cabinetKeypad.hide();
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '小柜子打开了。你发现了一个黄铜开瓶器。' : 'The small cabinet opens. You find a brass corkscrew.');
        
        const corkscrewData = { 
          id: 'corkscrew', 
          name: this.roomData.items[1].name,
          icon: 'assets/items/room_02/corkscrew.png'
        };
        Engine.pickupItem(corkscrewData, 512, 512);
        this.state.hasCorkscrew = true;
      }
    });
    this.cabinetKeypad.init();
    SpriteManager.addSprite('cabinet', {
      id: 'cabinet_lock_target', x: 380, y: 350, w: 250, h: 250,
      onClick: () => { if (this.state.wineCabinetLocked) this.cabinetKeypad.show(); }
    });
  }

  handleItemUse(itemId) {
    if ((itemId === 'corkscrew' && Inventory.selectedItem?.id === 'vintage_bottle') ||
        (itemId === 'vintage_bottle' && Inventory.selectedItem?.id === 'corkscrew')) {
      this.combineBottle();
      return true;
    }
    return false;
  }

  combineBottle() {
    if (this.state.bottleOpened) return;
    this.state.bottleOpened = true;
    Inventory.removeItem('corkscrew');
    Inventory.removeItem('vintage_bottle');
    const keyData = { 
      id: 'dining_key', 
      name: this.roomData.items[2].name,
      icon: 'assets/items/room_02/dining_key.png'
    };
    Audio.playSFX('item_pickup');
    Engine.pickupItem(keyData, 540, 960);
    this.state.hasDiningKey = true;
    Dialog.showFeedback(I18n.currentLang === 'zh' ? '你用开瓶器打开了酒瓶，在里面发现了一把走廊钥匙！' : 'You used the corkscrew to open the bottle and found a corridor key inside!');
  }

  cleanup() {
    if (this.hatchDial) this.hatchDial.cleanup();
    if (this.cabinetKeypad) this.cabinetKeypad.cleanup();
  }
}

window.Room02 = Room02;
