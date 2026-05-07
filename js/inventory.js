/* ============================================
   inventory.js — Player Inventory System
   ============================================ */
const Inventory = {
  items: [],
  selectedItem: null,
  persistentItems: [],
  maxSlots: 6,

  init() {
    this.items = [];
    this.selectedItem = null;
    this.render();
  },

  addItem(item, silent = false) {
    if (this.items.find(i => i.id === item.id)) return -1;
    const index = this.items.length;
    item.pendingReveal = silent; // Mark as pending if silent
    this.items.push(item);
    Audio.playSFX('item_pickup');
    this.render();
    return index;
  },

  revealItem(itemId) {
    const item = this.items.find(i => i.id === itemId);
    if (item) {
      item.pendingReveal = false;
      this.render();
      // Optional: Add a small 'pop' animation effect here if desired
    }
  },

  removeItem(itemId) {
    this.items = this.items.filter(i => i.id !== itemId);
    if (this.selectedItem && this.selectedItem.id === itemId) {
      this.selectedItem = null;
    }
    this.render();
  },

  hasItem(itemId) {
    return this.items.some(i => i.id === itemId);
  },

  selectItem(itemId) {
    if (this.selectedItem && this.selectedItem.id === itemId) {
      this.selectedItem = null;
    } else {
      this.selectedItem = this.items.find(i => i.id === itemId) || null;
    }
    this.render();
  },

  getSelected() {
    return this.selectedItem;
  },

  addPersistent(item) {
    if (!this.persistentItems.find(i => i.id === item.id)) {
      this.persistentItems.push(item);
    }
  },

  render() {
    const container = document.getElementById('inventory-slots');
    container.innerHTML = '';
    
    // Always render 6 slots
    for (let i = 0; i < this.maxSlots; i++) {
      const item = this.items[i];
      const slot = document.createElement('div');
      slot.className = 'inv-slot';
      
      // If item exists but is pending reveal, treat slot as empty visually
      if (item && !item.pendingReveal) {
        if (this.selectedItem && this.selectedItem.id === item.id) {
          slot.classList.add('active');
        }
        
        if (item.icon) {
          const img = document.createElement('img');
          img.src = item.icon;
          img.className = 'item-icon';
          slot.appendChild(img);
        } else {
          slot.innerHTML = `<span class="item-label">${I18n.t(item.name)}</span>`;
        }
        
        slot.addEventListener('click', () => this.handleItemClick(item));
      } else {
        slot.classList.add('empty');
      }
      container.appendChild(slot);
    }
  },

  async handleItemClick(item) {
    if (Engine.isBusy) return;

    // 1. Try Combination Logic first if an item is already selected
    if (this.selectedItem && this.selectedItem.id !== item.id) {
      if (window.Engine && Engine.currentRoomInstance && Engine.currentRoomInstance.handleItemUse) {
        Engine.setBusy(true);
        try {
          if (await Engine.currentRoomInstance.handleItemUse(this.selectedItem.id, item.id)) {
            return; // Room handled the combination
          }
        } finally {
          Engine.setBusy(false);
        }
      }
    }

    // 2. Drive Action by explicit Item Type
    switch (item.type) {
      case 'interactive':
      case 'document':
        // UNIFIED ZOOM VIEW: Uses the same HTML modal for all inspection types
        let hotspots = [];
        if (Engine.currentRoomInstance && Engine.currentRoomInstance.getInteractiveHotspots) {
          hotspots = Engine.currentRoomInstance.getInteractiveHotspots(item.id);
        }
        Dialog.inspectItem(item.examineBg, hotspots);
        break;

      case 'tool':
      default:
        // STANDARD SELECTION: Highlight to use on environment
        this.selectItem(item.id);
        break;
    }
  }
};
