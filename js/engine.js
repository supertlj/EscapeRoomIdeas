/* ============================================
   engine.js — Core Game Engine
   ============================================ */
const Engine = {
  roomData: null,
  roomState: null,
  currentPuzzleIndex: 0,
  sceneHistory: [],

  async init() {
    I18n.init();
    Inventory.init();
    HintSystem.init();
    AdManager.init();

    const canvas = document.getElementById('game-canvas');
    SpriteManager.init(canvas);

    canvas.addEventListener('click', (e) => this.handleTap(e));
    canvas.addEventListener('touchend', (e) => {
      e.preventDefault();
      const touch = e.changedTouches[0];
      this.handleTap({ clientX: touch.clientX, clientY: touch.clientY });
    });

    document.getElementById('btn-menu').addEventListener('click', () => this.showMenu());
    document.getElementById('btn-resume').addEventListener('click', () => this.hideMenu());
    document.getElementById('btn-language').addEventListener('click', () => this.toggleLanguage());
    document.getElementById('btn-restart-room').addEventListener('click', () => this.restartRoom());
    document.getElementById('btn-level-select').addEventListener('click', () => this.openLevelSelect());
    document.getElementById('btn-close-levels').addEventListener('click', () => this.hideLevelSelect());
    document.getElementById('btn-back').addEventListener('click', () => this.goBack());
    
    // Debug Mode Toggle (Hotspot Outlines)
    window.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'd') {
        SpriteManager.debugMode = !SpriteManager.debugMode;
        console.log('Debug Mode:', SpriteManager.debugMode ? 'ON' : 'OFF');
      }
    });

    await this.loadRoom(SaveManager.getSavedRoom());
  },

  async loadRoom(roomNumber) {
    try {
      Inventory.init(); // Clear inventory on room load
      this.roomData = await RoomLoader.loadRoom(roomNumber);
      this.sceneHistory = [];
      this.updateBackButton();

      if (this.currentRoomInstance) {
        this.currentRoomInstance.cleanup();
      }

      const className = `Room${String(roomNumber).padStart(2, '0')}`;
      if (window[className]) {
        this.currentRoomInstance = new window[className](this.roomData);
        this.roomState = await this.currentRoomInstance.setup();
      } else {
        console.warn(`Class ${className} not found, falling back to manual setup if exists.`);
      }

      SpriteManager.resize();
      SpriteManager.startRenderLoop();

      setTimeout(() => {
        Dialog.showStory(this.roomData.room_description, () => {
          Dialog.showFeedback(
            I18n.currentLang === 'zh' ? '点击物品进行互动' : 'Tap objects to interact',
            2500
          );
        });
      }, 500);
    } catch (err) {
      console.error('Failed to load room:', err);
      Dialog.showFeedback('Error loading room data', 3000);
    }
  },

  handleTap(e) {
    const dp = SpriteManager.screenToDesign(e.clientX, e.clientY);
    const hit = SpriteManager.hitTest(dp.x, dp.y);
    if (hit && hit.onClick) {
      hit.onClick();
    }
  },

  async switchScene(sceneId, backgroundSrc) {
    if (SpriteManager.currentSceneId !== sceneId) {
      this.sceneHistory.push(SpriteManager.currentSceneId);
    }
    await SpriteManager.setScene(sceneId, backgroundSrc);
    this.updateBackButton();
    if (RoomLoader.onSceneChange) RoomLoader.onSceneChange(sceneId);
  },

  async goBack() {
    if (this.sceneHistory.length > 0) {
      const prevSceneId = this.sceneHistory.pop();
      await SpriteManager.setScene(prevSceneId);
      this.updateBackButton();
      if (RoomLoader.onSceneChange) RoomLoader.onSceneChange(prevSceneId);
    }
  },

  updateBackButton() {
    const btn = document.getElementById('btn-back');
    if (this.sceneHistory.length > 0) {
      btn.classList.remove('hidden');
    } else {
      btn.classList.add('hidden');
    }
  },

  getCurrentPuzzle() {
    if (!this.roomData || !this.roomData.puzzles) return null;
    return this.roomData.puzzles[this.currentPuzzleIndex] || this.roomData.puzzles[0];
  },

  showMenu() {
    document.getElementById('menu-panel').classList.remove('hidden');
  },

  hideMenu() {
    document.getElementById('menu-panel').classList.add('hidden');
  },

  toggleLanguage() {
    const newLang = I18n.toggle();
    // Refresh room title
    if (this.roomData) {
      document.getElementById('room-title').textContent = I18n.t(this.roomData.room_name);
    }
    Inventory.render();
    this.hideMenu();
    Dialog.showFeedback(newLang === 'zh' ? '语言已切换为中文' : 'Language switched to English', 1500);
  },

  async openLevelSelect() {
    this.hideMenu();
    const panel = document.getElementById('level-select-panel');
    const grid = document.getElementById('level-grid');
    grid.innerHTML = '';

    const maxUnlocked = SaveManager.getSavedRoom();
    
    // Load metadata from rooms.json
    const response = await fetch('data/rooms.json');
    const data = await response.json();

    data.rooms.forEach(room => {
      const card = document.createElement('div');
      card.className = 'level-card';
      if (room.id > maxUnlocked) card.classList.add('locked');
      
      const padded = String(room.id).padStart(2, '0');
      if (room.developed) {
        card.style.backgroundImage = `url('assets/rooms/room_${padded}/background.png')`;
      } else {
        card.classList.add('no-asset');
      }
      
      const displayName = I18n.currentLang === 'zh' ? room.name.zh : room.name.en;

      card.innerHTML = `
        <div class="level-info">
          <span class="level-num">ROOM ${padded}</span>
          <span class="level-name">${displayName}</span>
        </div>
      `;

      if (room.id <= maxUnlocked) {
        card.onclick = () => {
          this.hideLevelSelect();
          this.loadRoom(room.id);
        };
      }
      grid.appendChild(card);
    });

    panel.classList.remove('hidden');
  },

  hideLevelSelect() {
    document.getElementById('level-select-panel').classList.add('hidden');
  },

  animateItemPickup(startX, startY, imgSrc, targetSlotIndex = -1, itemId = null) {
    const fly = document.createElement('img');
    fly.src = imgSrc;
    fly.className = 'fly-item';
    
    const sm = SpriteManager;
    const sx = (startX + sm.ART_X) * sm.scale + sm.offsetX;
    const sy = (startY + sm.ART_Y) * sm.scale + sm.offsetY;

    fly.style.left = `${sx - 50}px`; // Centering the 100px sprite
    fly.style.top = `${sy - 50}px`;
    document.body.appendChild(fly);

    let tx, ty;
    const slots = document.querySelectorAll('.inv-slot');
    
    if (targetSlotIndex >= 0 && slots[targetSlotIndex]) {
      const rect = slots[targetSlotIndex].getBoundingClientRect();
      tx = rect.left + rect.width / 2 - 50;
      ty = rect.top + rect.height / 2 - 50;
    } else {
      const inv = document.getElementById('inventory-bar').getBoundingClientRect();
      tx = inv.left + inv.width / 2 - 50;
      ty = inv.top + inv.height / 2 - 50;
    }

    requestAnimationFrame(() => {
      fly.style.left = `${tx}px`;
      fly.style.top = `${ty}px`;
      fly.classList.add('animating');
    });

    setTimeout(() => {
      fly.remove();
      if (itemId) {
        Inventory.revealItem(itemId);
      }
    }, 850);
  },

  pickupItem(itemData, startX, startY, onComplete, sfx = 'key_pickup') {
    Audio.playSFX(sfx);
    const slotIdx = Inventory.addItem(itemData, true); // Add silently
    this.animateItemPickup(startX, startY, itemData.icon, slotIdx, itemData.id);
    if (onComplete) {
      setTimeout(onComplete, 850); // trigger callback when animation finishes
    }
  },

  async restartRoom() {
    this.hideMenu();
    Inventory.init();
    HintSystem.hintsRevealed = {};
    if (this.roomData) {
      await this.loadRoom(this.roomData.room_number);
    }
  },


  completeRoom() {
    const modal = document.getElementById('room-complete');
    const text = document.getElementById('complete-text');
    text.textContent = I18n.t(this.roomData.final_action);
    modal.classList.remove('hidden');
    
    document.getElementById('btn-next-room').onclick = () => {
      AdManager.showInterstitialAd(() => {
        modal.classList.add('hidden');
        const nextRoom = this.roomData.room_number + 1;
        SaveManager.saveProgress(nextRoom);
        this.loadRoom(nextRoom);
      });
    };
  }
};

// ---- Boot ----
window.addEventListener('DOMContentLoaded', () => Engine.init());
