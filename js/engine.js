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
    document.getElementById('btn-back').addEventListener('click', () => this.goBack());
    
    // Debug Mode Toggle (Hotspot Outlines)
    window.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'd') {
        SpriteManager.debugMode = !SpriteManager.debugMode;
        console.log('Debug Mode:', SpriteManager.debugMode ? 'ON' : 'OFF');
      }
    });

    await this.loadRoom(1);
  },

  async loadRoom(roomNumber) {
    try {
      this.roomData = await RoomLoader.loadRoom(roomNumber);
      this.sceneHistory = [];
      this.updateBackButton();

      if (roomNumber === 1) {
        this.roomState = await RoomLoader.setupRoom1(this.roomData);
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
    text.textContent = I18n.currentLang === 'zh' ? 
      '你已经解开了大堂的所有谜题。电梯正在上升...' : 
      'You have solved all puzzles in the Lobby. The elevator is ascending...';
    modal.classList.remove('hidden');
    
    document.getElementById('btn-next-room').onclick = () => {
      modal.classList.add('hidden');
      Dialog.showFeedback('Level 2 Coming Soon!', 3000);
    };
  }
};

// ---- Boot ----
window.addEventListener('DOMContentLoaded', () => Engine.init());
