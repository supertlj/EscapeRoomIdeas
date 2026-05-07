class Room02 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    const assetPath = `assets/rooms/room_${padded}`;
    
    // Clear old scenes
    SpriteManager.scenes = {};

    this.state = {
      wineCabinetLocked: true,
      wineCabinetOpen: false,
      kitchenHatchLocked: true,
      kitchenHatchOpen: false,
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
    await loadScene('main', `${assetPath}/background.webp`);
    await loadScene('chalkboard', `${assetPath}/chalkboard_zoom.webp`);
    await loadScene('table_2', `${assetPath}/table_2_zoom.webp`);
    await loadScene('table_4', `${assetPath}/table_4_zoom.webp`);
    await loadScene('table_7', `${assetPath}/table_7_zoom.webp`);
    await loadScene('hatch', `${assetPath}/hatch_zoom.webp`);
    await loadScene('service_note', `${assetPath}/servicenote_zoom.webp`);
    await loadScene('door', `${assetPath}/door_zoom.webp`);
    await loadScene('door_open', `${assetPath}/door_open_zoom.webp`);
    
    const cabinetBg = this.state.wineCabinetOpen ? 
      (this.state.hasCorkscrew ? 'assets/rooms/room_02/cabinet_zoom_empty.webp' : 'assets/rooms/room_02/cabinet_zoom_open.webp') : 
      'assets/rooms/room_02/cabinet_zoom.webp';
    await loadScene('cabinet', cabinetBg);
    
    // Preload overlays and Open states
    await AssetLoader.loadImage('hatch_open_patch', `${assetPath}/hatch_open_patch.webp`);
    await AssetLoader.loadImage('hatch_zoom_open', `${assetPath}/hatch_zoom_open.webp`);
    await AssetLoader.loadImage('hatch_zoom_open_with_bottle', `${assetPath}/hatch_zoom_open_with_bottle.webp`);
    await AssetLoader.loadImage('cabinet_open_patch', `${assetPath}/cabinet_open_patch.webp`);
    await AssetLoader.loadImage('door_open_patch', `${assetPath}/door_open_patch.webp`);
    await AssetLoader.loadImage('vintage_bottle_sprite', `assets/items/room_02/vintage_bottle.webp`);
    await AssetLoader.loadImage('bottle_with_key_sprite', `assets/items/room_02/bottle_with_key.webp`);

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
    // Cabinet Open Overlay (Patch)
    // Resolution is 345x1024, sits at the far left (x = 0)
    SpriteManager.addSprite('main', {
      id: 'cabinet_open_overlay', x: 0, y: 0, w: 372, h: 1024,
      image: AssetLoader.images['cabinet_open_patch'],
      visible: this.state.wineCabinetOpen,
      zIndex: 1
    });

    // Hatch Open Overlay (Patch)
    // Resolution is 295x1024, sits at the far right (x = 1024 - 295 = 729)
    SpriteManager.addSprite('main', {
      id: 'hatch_open_overlay', x: 729, y: 0, w: 295, h: 1024,
      image: AssetLoader.images['hatch_open_patch'],
      visible: this.state.kitchenHatchOpen,
      zIndex: 1 // Just above background
    });

    // Door Open Overlay (Patch)
    SpriteManager.addSprite('main', {
      id: 'door_open_overlay', x: 358, y: 0, w: 307, h: 1024,
      image: AssetLoader.images['door_open_patch'],
      visible: this.state.escaped,
      zIndex: 1
    });

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

    // Exit Door (Now transitions to zoom)
    SpriteManager.addSprite('main', {
      id: 'exit_door', x: 380, y: 220, w: 160, h: 400,
      onClick: () => Engine.switchScene('door')
    });

    // Service Note Zoom
    SpriteManager.addSprite('main', {
      id: 'click_service_note', x: 295, y: 300, w: 70, h: 110,
      onClick: () => Engine.switchScene('service_note')
    });
  }

  setupZoomScenes() {
    // Door Zoom interaction
    SpriteManager.addSprite('door', {
      id: 'keyhole', x: 440, y: 350, w: 140, h: 220,
      onClick: () => {
        if (this.state.escaped) {
          // If already open, clicking the corridor completes the room
          Engine.completeRoom();
          return;
        }
        if (Inventory.selectedItem && Inventory.selectedItem.id === 'dining_key') {
          Audio.playSFX('door_open');
          Inventory.removeItem('dining_key');
          this.state.escaped = true;
          
          // Show the open door in main room
          SpriteManager.updateSprite('main', 'door_open_overlay', { visible: true });
          
          // Swap background of the zoom scene too
          SpriteManager.setScene('door', 'assets/rooms/room_02/door_open_zoom.webp');
          
          Dialog.showStory(I18n.currentLang === 'zh' ? '你用钥匙打开了门，离开餐厅进入了走廊。' : 'You use the key to open the door and leave the restaurant into the corridor.');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '门锁着。我需要餐厅钥匙。' : 'The door is locked. I need the Dining Room Key.');
        }
      }
    });

    // Relying on global UI back button for other scenes.
    // Chalkboard details
    SpriteManager.addSprite('chalkboard', {
      id: 'read_menu', x: 200, y: 200, w: 600, h: 600,
      onClick: () => Dialog.showFeedback(I18n.currentLang === 'zh' ? '主厨特供：龙虾浓汤 $14，菲力牛排 $28，焦糖布丁 $9。' : 'Chef\'s Special: Lobster Bisque $14, Filet Mignon $28, Crème Brûlée $9.')
    });

    // The Hatch Zoom - Needs to show the open state and the bottle
    SpriteManager.addSprite('hatch', {
      id: 'hatch_open_zoom_bg', x: 0, y: 0, w: 1024, h: 1024,
      image: this.state.hasVintageBottle ? AssetLoader.images['hatch_zoom_open'] : AssetLoader.images['hatch_zoom_open_with_bottle'], 
      visible: this.state.kitchenHatchOpen,
      zIndex: 1
    });

    SpriteManager.addSprite('hatch', {
      id: 'vintage_bottle_item', x: 350, y: 400, w: 300, h: 400,
      visible: this.state.kitchenHatchOpen && !this.state.hasVintageBottle,
      zIndex: 10,
      onClick: () => {
        if (!this.state.kitchenHatchOpen || this.state.hasVintageBottle) return;
        
        Engine.pickupItem('vintage_bottle', 540, 960, () => {
          this.state.hasVintageBottle = true;
          // Hide the bottle in both views
          SpriteManager.updateSprite('hatch', 'vintage_bottle_item', { visible: false });
          SpriteManager.updateSprite('main', 'hatch_bottle_overlay', { visible: false });
          
          // Swap background to empty version
          SpriteManager.setScene('hatch', 'assets/rooms/room_02/hatch_zoom_open.webp');
          
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '获得陈年酒瓶' : 'Obtained the Vintage Bottle!');
        });
      }
    });

    // The Cabinet Zoom
    // Initial scene background is set in setupZoomScenes if opened
    if (this.state.wineCabinetOpen) {
      SpriteManager.setScene('cabinet', 'assets/rooms/room_02/cabinet_zoom_open.webp');
    }

    // Brass Corkscrew (Inside cabinet)
    SpriteManager.addSprite('cabinet', {
      id: 'brass_corkscrew_item', x: 330, y: 450, w: 200, h: 300,
      glint: true,
      visible: this.state.wineCabinetOpen && !this.state.hasCorkscrew,
      zIndex: 10,
      onClick: () => {
        if (!this.state.wineCabinetOpen || this.state.hasCorkscrew) return;
        
        Engine.pickupItem('corkscrew', 540, 960, () => {
          this.state.hasCorkscrew = true;
          // Swap to empty background in zoom view
          SpriteManager.setScene('cabinet', 'assets/rooms/room_02/cabinet_zoom_empty.webp');
          SpriteManager.updateSprite('cabinet', 'brass_corkscrew_item', { visible: false });
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '获得黄铜开瓶器' : 'Found the Brass Corkscrew!');
        });
      }
    });

    this.initInspectModal();

    this.setupMainScene();
  }

  /**
   * Returns hotspots for interactive item modals
   */
  getInteractiveHotspots(itemId) {
    if (itemId === 'vintage_bottle') {
      if (!this.state.bottleOpened) {
        return [
          {
            id: 'cork',
            x: 250, y: 0, w: 300, h: 800, // Large area covering the whole bottle for easy tool use
            onClick: () => {
              if (Inventory.selectedItem && Inventory.selectedItem.id === 'corkscrew') {
                this.combineBottle();
              } else {
                Dialog.showFeedback(I18n.currentLang === 'zh' ? '这瓶酒封得很严，需要个工具。' : 'This bottle is sealed tight. I need a tool.');
              }
            }
          }
        ];
      } else {
        // Phase 2: Bottle is sideways, key is visible
        return [
          {
            id: 'key_on_floor',
            x: 200, y: 200, w: 500, h: 500, // Large area for picking up the key
            onClick: async () => {
              await Engine.pickupItem('dining_key', 540, 960);
              this.state.hasDiningKey = true;
              Inventory.removeItem('vintage_bottle');
              Dialog.showFeedback(I18n.currentLang === 'zh' ? '你拿到了餐厅钥匙！' : 'You picked up the Dining Room Key!');
              // Close modal after pickup
              document.getElementById('item-inspect-modal').classList.add('hidden');
            }
          }
        ];
      }
    }
    return [];
  }

  setupPuzzles() {
    // Kitchen Hatch Puzzle (Code 51) using the new DialPuzzle
    this.hatchDial = new DialPuzzle({
      targetValue: 51,
      assetPath: 'assets/rooms/room_02/dial.webp',
      bgImage: 'assets/rooms/room_02/hatch_zoom.webp',
      onSuccess: async () => {
        this.state.kitchenHatchLocked = false;
        this.state.kitchenHatchOpen = true;
        Audio.playSFX('door_open');
        this.hatchDial.hide();
        
        // Update the views immediately
        SpriteManager.updateSprite('main', 'hatch_open_overlay', { visible: true });
        SpriteManager.updateSprite('hatch', 'hatch_open_zoom_bg', { visible: true });
        SpriteManager.updateSprite('hatch', 'vintage_bottle_item', { visible: !this.state.hasVintageBottle });

        Dialog.showFeedback(I18n.currentLang === 'zh' ? '传菜窗打开了。里面有一瓶陈年酒。' : 'The hatch opens. There is a vintage bottle inside.');
      }
    });
    this.hatchDial.init();
    SpriteManager.addSprite('hatch', {
      id: 'hatch_lock_target', x: 350, y: 380, w: 250, h: 250,
      onClick: () => { 
        if (this.state.kitchenHatchLocked) {
          this.hatchDial.show(); 
        } else {
          // If already open, let the user pick up the bottle or see it's empty
          if (!this.state.hasVintageBottle) {
            Dialog.showFeedback(I18n.currentLang === 'zh' ? '酒瓶在里面。' : 'The bottle is inside.');
          }
        }
      }
    });

    this.cabinetLock = new CombinationLockPuzzle({
      targetCode: '472',
      bgImage: 'assets/rooms/room_02/cabinet_lock.webp',
      onSuccess: async () => {
        this.state.wineCabinetLocked = false;
        this.state.wineCabinetOpen = true;
        Audio.playSFX('door_open');
        this.cabinetLock.hide();
        
        // Update backgrounds
        await SpriteManager.setScene('cabinet', 'assets/rooms/room_02/cabinet_zoom_open.webp');
        
        // Show the corkscrew in the zoom view
        SpriteManager.updateSprite('cabinet', 'brass_corkscrew_item', { visible: !this.state.hasCorkscrew });
        
        // Also update the main room background to show it open
        SpriteManager.updateSprite('main', 'cabinet_open_overlay', { visible: true });
        
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '小柜子打开了。你发现了一个黄铜开瓶器。' : 'The small cabinet opens. You find a brass corkscrew.', 2000);
      }
    });
    this.cabinetLock.init();
    SpriteManager.addSprite('cabinet', {
      id: 'cabinet_lock_target', x: 360, y: 430, w: 350, h: 140, // Centered on the rolling digits
      onClick: () => { if (this.state.wineCabinetLocked) this.cabinetLock.show(); }
    });
  }

  async handleItemUse(selectedId, targetId) {
    if ((selectedId === 'corkscrew' && targetId === 'vintage_bottle') ||
        (selectedId === 'vintage_bottle' && targetId === 'corkscrew')) {
      await this.combineBottle();
      return true;
    }
    return false;
  }

  async combineBottle() {
    if (this.state.bottleOpened) return;
    this.state.bottleOpened = true;
    
    Inventory.removeItem('corkscrew');
    // We don't remove the bottle yet, we just change its "state" in the modal
    
    Audio.playSFX('door_open'); // Placeholder for cork pop
    
    // Refresh the modal with the new image and new hotspots
    Dialog.inspectItem('assets/items/room_02/bottle_with_key.webp', this.getInteractiveHotspots('vintage_bottle'));
  }

  cleanup() {
    if (this.hatchDial) this.hatchDial.cleanup();
    if (this.cabinetLock) {
      if (this.cabinetLock.modal) this.cabinetLock.modal.remove();
    }
  }
}

window.Room02 = Room02;
