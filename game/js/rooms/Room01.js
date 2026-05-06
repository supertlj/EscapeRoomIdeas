class Room01 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    
    // Clear all scenes and initialize 'main'
    SpriteManager.scenes = {};
    await SpriteManager.setScene('main', `assets/rooms/room_${padded}/background.png`);
    
    this.state = {
      guestBookZoomed: false,
      guestBookRead: false,
      brassKeyFound: false,
      safeOpened: false,
      noteFound: false,
      elevatorOpen: false,
      escaped: false
    };

    this.setupLobby();
    this.setupGuestbook();
    this.setupSafe();
    this.setupChandelier();
    this.setupElevator();
    this.initInspectModal();

    HintSystem.setCurrentPuzzle(0);
    return this.state;
  }

  setupLobby() {
    // Guest Book
    SpriteManager.addSprite('main', {
      id: 'guest_book_tap', x: 140, y: 580, w: 300, h: 140,
      onClick: async () => {
        await Engine.switchScene('zoom_guestbook', 'assets/rooms/room_01/zoom_guestbook.png');
      }
    });

    // Safe
    SpriteManager.addSprite('main', {
      id: 'safe_entrance', x: 80, y: 730, w: 200, h: 250,
      onClick: async () => {
        let bg = 'assets/rooms/room_01/zoom_safe_closed.png';
        if (this.state.safeOpened) {
          bg = this.state.noteFound ? 
            'assets/rooms/room_01/zoom_safe_open.png' : 
            'assets/rooms/room_01/zoom_safe_with_note.png';
        }
        await Engine.switchScene('zoom_safe', bg);
      }
    });

    // Chandelier
    SpriteManager.addSprite('main', {
      id: 'chandelier', x: 400, y: 0, w: 400, h: 380,
      onClick: async () => {
        if (!this.state.guestBookRead) return;
        const bg = this.state.brassKeyFound ? 
          'assets/rooms/room_01/zoom_chandelier_empty.png' : 
          'assets/rooms/room_01/zoom_chandelier.png';
        await Engine.switchScene('zoom_chandelier', bg);
      }
    });

    // Elevator
    SpriteManager.addSprite('main', {
      id: 'elevator', x: 620, y: 380, w: 220, h: 280,
      onClick: async () => {
        if (this.state.elevatorOpen) {
          Engine.completeRoom();
          return;
        }
        await Engine.switchScene('zoom_elevator', 'assets/rooms/room_01/zoom_elevator.png');
      }
    });
  }

  setupGuestbook() {
    SpriteManager.addSprite('zoom_guestbook', {
      id: 'guest_book_read', x: 200, y: 200, w: 624, h: 624,
      onClick: () => {
        if (this.state.guestBookRead) return;
        this.state.guestBookRead = true;
        Dialog.showStory(this.roomData.story_fragment, () => {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '登记簿提到吊灯...' : 'The book mentions the chandelier...', 2500);
        });
      }
    });
  }

  setupChandelier() {
    SpriteManager.addSprite('zoom_chandelier', {
      id: 'brass_key_item', x: 440, y: 550, w: 160, h: 160,
      blendMode: 'screen',
      glint: true,
      onClick: async () => {
        if (this.state.brassKeyFound) return;
        
        this.state.brassKeyFound = true;
        
        const keyData = { 
          id: 'brass_key', 
          name: this.roomData.items[0].name,
          icon: 'assets/items/room_01/brass_key.png'
        };
        
        Engine.pickupItem(keyData, 520, 630, () => {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '找到黄铜钥匙！' : 'Found the Brass Key!', 2000);
        });
        
        SpriteManager.updateSprite('zoom_chandelier', 'brass_key_item', { visible: false });
      }
    });

    SpriteManager.updateSprite('zoom_chandelier', 'brass_key_item', { visible: !this.state.brassKeyFound });
    SpriteManager.loadSpriteImage('zoom_chandelier', 'brass_key_item', 'assets/items/room_01/brass_key.png');
  }

  setupSafe() {
    // Safe door/mechanism
    SpriteManager.addSprite('zoom_safe', {
      id: 'safe_mechanism', x: 200, y: 200, w: 624, h: 624,
      onClick: async () => {
        if (this.state.safeOpened) return;

        if (PuzzleEngine.checkItemUse('brass_key')) {
          this.state.safeOpened = true;
          Inventory.removeItem('brass_key');
          Audio.playSFX('door_open');
          
          // Disable the mechanism hitbox so it doesn't block the note
          SpriteManager.updateSprite('zoom_safe', 'safe_mechanism', { visible: false });
          
          await SpriteManager.setScene('zoom_safe', 'assets/rooms/room_01/zoom_safe_with_note.png');
          // Update main background to open safe (with note)
          SpriteManager.scenes['main'].background.src = 'assets/rooms/room_01/background_safe_open.png';
          SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: true });
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '保险箱已打开' : 'Safe opened');
        } else {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '它被锁住了，需要一把钥匙。' : 'It is locked. You need a key.');
        }
      }
    });

    // Initialize visibility
    SpriteManager.updateSprite('zoom_safe', 'safe_mechanism', { visible: !this.state.safeOpened });

    // Note inside safe - defined AFTER so it is on TOP
    SpriteManager.addSprite('zoom_safe', {
      id: 'safe_note_item', x: 230, y: 640, w: 350, h: 250,
      onClick: async () => {
        if (this.state.noteFound || !this.state.safeOpened) return;
        
        Dialog.inspectItem('assets/rooms/room_01/zoom_note.png');

        this.state.noteFound = true;
        
        const noteData = { 
          id: 'reception_note', 
          name: this.roomData.items[1].name,
          icon: 'assets/items/room_01/note_folded.png',
          examineBg: 'assets/rooms/room_01/zoom_note.png'
        };

        Engine.pickupItem(noteData, 405, 825, () => {
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '便条已加入物品栏' : 'Note added to inventory');
        }, 'paper_pickup');
        
        await SpriteManager.setScene('zoom_safe', 'assets/rooms/room_01/zoom_safe_open.png');
        // Update main background to empty safe
        SpriteManager.scenes['main'].background.src = 'assets/rooms/room_01/background_safe_empty.png';
        SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: false });
      }
    });

    SpriteManager.updateSprite('zoom_safe', 'safe_note_item', { visible: this.state.safeOpened && !this.state.noteFound });
  }

  setupElevator() {
    SpriteManager.addSprite('zoom_elevator', {
      id: 'elevator_keypad_zoom', x: 745, y: 475, w: 70, h: 100,
      onClick: () => {
        this.keypad.show();
      }
    });

    this.keypad = new KeypadPuzzle({
      targetCode: '3142',
      onSuccess: async () => {
        this.state.elevatorOpen = true;
        Audio.playSFX('door_open');
        this.keypad.hide();
        
        // Update both backgrounds for consistency
        await SpriteManager.setScene('zoom_elevator', 'assets/rooms/room_01/zoom_elevator_open.png');
        SpriteManager.scenes['main'].background.src = 'assets/rooms/room_01/background_elevator_open.png';
        
        // Add click handler to the open elevator in zoom view to exit
        SpriteManager.addSprite('zoom_elevator', {
          id: 'elevator_exit_click', x: 200, y: 200, w: 624, h: 624,
          onClick: () => Engine.completeRoom()
        });
      },
      onFail: () => {
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '密码错误' : 'Invalid Code');
      }
    });
    this.keypad.init();
  }

  cleanup() {
    if (this.keypad) {
      this.keypad.cleanup();
    }
  }

  initInspectModal() {
    if (document.getElementById('item-inspect-modal')) return;
    
    const modal = document.createElement('div');
    modal.id = 'item-inspect-modal';
    modal.className = 'modal-overlay hidden';
    modal.innerHTML = `
      <div class="zoom-frame">
        <img id="item-inspect-image" src="" alt="Inspecting item">
      </div>
      <div class="zoom-hint-text">TAP ANYWHERE TO CLOSE</div>
    `;
    
    document.getElementById('ui-design-container').appendChild(modal);
    
    modal.onclick = () => {
      modal.classList.add('hidden');
    };
  }
}

window.Room01 = Room01;
