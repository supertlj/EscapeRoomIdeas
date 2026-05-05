/* ============================================
   room-loader.js — Loads room JSON and sets up scene
   ============================================ */
const RoomLoader = {

  async loadRoom(roomNumber) {
    const padded = String(roomNumber).padStart(2, '0');
    const response = await fetch(`data/rooms/room_${padded}.json`);
    const roomData = await response.json();

    document.getElementById('room-title').textContent = I18n.t(roomData.room_name);

    // Initial scene
    await SpriteManager.setScene('main', `assets/rooms/room_01/background.png`);

    return roomData;
  },

  async setupRoom1(roomData) {
    const padded = String(roomData.room_number).padStart(2, '0');
    
    // Clear all scenes and initialize 'main'
    SpriteManager.scenes = {};
    await SpriteManager.setScene('main', `assets/rooms/room_${padded}/background.png`);
    
    const state = {
      guestBookZoomed: false,
      guestBookRead: false,
      brassKeyFound: false,
      safeOpened: false,
      noteFound: false,
      escaped: false
    };

    // ============================================
    // MAIN LOBBY SCENE (Art Space: 1024x1024)
    // ============================================
    
    // Guest Book (Zoom in) - Accurate to the counter top
    SpriteManager.addSprite('main', {
      id: 'guest_book_tap', x: 150, y: 450, w: 350, h: 200,
      onClick: async () => {
        await Engine.switchScene('zoom_guestbook', 'assets/rooms/room_01/zoom_guestbook.png');
      }
    });

    // Safe (Transition to Zoom View) - Large hitbox under the left counter
    SpriteManager.addSprite('main', {
      id: 'safe_entrance', x: 50, y: 650, w: 450, h: 350,
      onClick: async () => {
        let bg = 'assets/rooms/room_01/zoom_safe_closed.png';
        if (state.safeOpened) {
          bg = state.noteFound ? 
            'assets/rooms/room_01/zoom_safe_open.png' : 
            'assets/rooms/room_01/zoom_safe_with_note.png';
        }
        await Engine.switchScene('zoom_safe', bg);
      }
    });

    // Chandelier (Transition to Zoom View)
    SpriteManager.addSprite('main', {
      id: 'chandelier', x: 400, y: 0, w: 400, h: 400,
      onClick: async () => {
        if (!state.guestBookRead) return;
        const bg = state.brassKeyFound ? 
          'assets/rooms/room_01/zoom_chandelier_empty.png' : 
          'assets/rooms/room_01/zoom_chandelier.png';
        await Engine.switchScene('zoom_chandelier', bg);
      }
    });

    // ============================================
    // ZOOM VIEW: CHANDELIER (Art Space: 1024x1024)
    // ============================================
    
    SpriteManager.addSprite('zoom_chandelier', {
      id: 'brass_key_item', x: 440, y: 550, w: 160, h: 160,
      blendMode: 'screen', // Seamlessly integrates with the crystals
      glint: true,         // Adds a subtle light pulse to make it obvious
      onClick: async () => {
        if (state.brassKeyFound) return;
        
        state.brassKeyFound = true;
        Audio.playSFX('key_pickup');
        
        // Visual Animation: Fly to inventory from the key's location
        Engine.animateItemPickup(520, 630, 'assets/items/brass_key.png');
        
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '找到黄铜钥匙！' : 'Found the Brass Key!', 2000);
        Inventory.addItem({ 
          id: 'brass_key', 
          name: roomData.items[0].name,
          icon: 'assets/items/brass_key.png'
        });
        
        // Hide sprite
        SpriteManager.updateSprite('zoom_chandelier', 'brass_key_item', { visible: false });
      }
    });

    // Initialize key visibility and image
    SpriteManager.updateSprite('zoom_chandelier', 'brass_key_item', { visible: !state.brassKeyFound });
    SpriteManager.loadSpriteImage('zoom_chandelier', 'brass_key_item', 'assets/items/brass_key.png');

    // Keypad on the wall (Goes to Elevator Zoom first)
    SpriteManager.addSprite('main', {
      id: 'keypad_on_wall', x: 770, y: 500, w: 60, h: 100,
      onClick: async () => {
        await Engine.switchScene('zoom_elevator', 'assets/rooms/room_01/zoom_elevator.png');
      }
    });

    // Elevator (Interaction - Goes to Elevator Zoom)
    SpriteManager.addSprite('main', {
      id: 'elevator', x: 620, y: 380, w: 150, h: 280,
      onClick: async () => {
        await Engine.switchScene('zoom_elevator', 'assets/rooms/room_01/zoom_elevator.png');
      }
    });

    // ============================================
    // ZOOM VIEW: ELEVATOR FRONT (Art Space: 1024x1024)
    // ============================================
    
    // Hitbox for the keypad on the zoomed-in elevator wall
    SpriteManager.addSprite('zoom_elevator', {
      id: 'elevator_keypad_zoom', x: 745, y: 475, w: 70, h: 100,
      onClick: async () => {
        await Engine.switchScene('zoom_keypad', 'assets/rooms/room_01/zoom_keypad.png');
        this.updateKeypadDisplay();
      }
    });

    // ============================================
    // ZOOM VIEW: GUEST BOOK (Art Space: 1024x1024)
    // ============================================
    
    SpriteManager.addSprite('zoom_guestbook', {
      id: 'guest_book_read', x: 200, y: 200, w: 624, h: 624,
      onClick: () => {
        if (state.guestBookRead) return;
        state.guestBookRead = true;
        Dialog.showStory(roomData.story_fragment, () => {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '登记簿提到吊灯...' : 'The book mentions the chandelier...', 2500);
        });
      }
    });

    // ============================================
    // ZOOM VIEW: SAFE (Art Space: 1024x1024)
    // ============================================
    
    // Invisible hitbox for the baked-in note
    SpriteManager.addSprite('zoom_safe', {
      id: 'safe_note_item', x: 230, y: 700, w: 350, h: 250,
      onClick: async () => {
        if (state.noteFound) return;
        
        // Show the handwritten detail view in the new overlay modal
        Dialog.inspectItem('assets/rooms/room_01/zoom_note.png');

        // Logic for taking the note
        state.noteFound = true;
        Audio.playSFX('paper_pickup');
        Inventory.addItem({ 
          id: 'reception_note', 
          name: roomData.items[1].name,
          icon: 'assets/items/note_folded.png',
          examineBg: 'assets/rooms/room_01/zoom_note.png'
        });
        
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '便条已加入物品栏' : 'Note added to inventory');
        
        // Swap the safe background to the empty version
        await SpriteManager.setScene('zoom_safe', 'assets/rooms/room_01/zoom_safe_open.png');
        SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: false });
      }
    });

    // The safe door/mechanism interaction
    SpriteManager.addSprite('zoom_safe', {
      id: 'safe_mechanism', x: 200, y: 200, w: 624, h: 624,
      onClick: async () => {
        if (state.safeOpened) return; 

        if (PuzzleEngine.checkItemUse('brass_key')) {
          state.safeOpened = true;
          Inventory.removeItem('brass_key');
          Audio.playSFX('door_open');
          // Switch to the background with the note baked in
          await SpriteManager.setScene('zoom_safe', 'assets/rooms/room_01/zoom_safe_with_note.png');
          SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: true });
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '保险箱已打开' : 'Safe opened');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '它被锁住了，需要一把钥匙。' : 'It is locked. You need a key.');
        }
      }
    });

    // Initialize visibility
    SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: state.safeOpened && !state.noteFound });

    // ============================================
    // ZOOM VIEW: KEYPAD (Art Space: 1024x1024)
    // ============================================
    
    this.currentKeypadCode = '';
    
    const keypadConfig = [
      { id: 'key_1', x: 330, y: 310, val: '1' },
      { id: 'key_2', x: 460, y: 310, val: '2' },
      { id: 'key_3', x: 590, y: 310, val: '3' },
      { id: 'key_4', x: 330, y: 440, val: '4' },
      { id: 'key_5', x: 460, y: 440, val: '5' },
      { id: 'key_6', x: 590, y: 440, val: '6' },
      { id: 'key_7', x: 330, y: 570, val: '7' },
      { id: 'key_8', x: 460, y: 570, val: '8' },
      { id: 'key_9', x: 590, y: 570, val: '9' },
      { id: 'key_0', x: 460, y: 700, val: '0' },
      { id: 'key_clear', x: 320, y: 700, val: 'CLEAR', w: 120 },
      { id: 'key_enter', x: 580, y: 700, val: 'ENTER', w: 120 }
    ];

    keypadConfig.forEach(cfg => {
      SpriteManager.addSprite('zoom_keypad', {
        id: cfg.id, x: cfg.x, y: cfg.y, w: cfg.w || 100, h: 100,
        onClick: () => {
          Audio.playSFX('button_click');
          if (cfg.val === 'CLEAR') {
            this.currentKeypadCode = '';
          } else if (cfg.val === 'ENTER') {
            if (this.currentKeypadCode === '3142') {
              Audio.playSFX('door_open');
              Dialog.showStory({
                en: "The elevator dings and the doors slide open. You've escaped the lobby!",
                zh: "电梯发出叮的一声，门缓缓打开。你成功离开了大堂！"
              }, () => {
                Engine.completeRoom();
              });
            } else {
              Dialog.showFeedback(I18n.currentLang === 'zh' ? '密码错误' : 'Invalid Code');
              this.currentKeypadCode = '';
            }
          } else {
            if (this.currentKeypadCode.length < 4) {
              this.currentKeypadCode += cfg.val;
            }
          }
          this.updateKeypadDisplay();
        }
      });
    });

    HintSystem.setCurrentPuzzle(0);
    return state;
  },

  updateKeypadDisplay() {
    const display = document.getElementById('keypad-display');
    const slots = document.querySelectorAll('.digit-slot');
    
    if (SpriteManager.currentSceneId === 'zoom_keypad') {
      display.classList.remove('hidden');
      slots.forEach((slot, i) => {
        const val = this.currentKeypadCode[i] || '';
        slot.textContent = val;
        // Toggle 'has-value' class to show/hide ghost segments
        if (val !== '') {
          slot.classList.add('has-value');
        } else {
          slot.classList.remove('has-value');
        }
      });
    } else {
      display.classList.add('hidden');
    }
  },

  onSceneChange(sceneId) {
    this.updateKeypadDisplay();
  }
};


