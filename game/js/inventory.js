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

  addItem(item) {
    if (this.items.find(i => i.id === item.id)) return false;
    this.items.push(item);
    Audio.playSFX('item_pickup');
    this.render();
    return true;
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
      if (item) {
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
        
        slot.addEventListener('click', () => {
          if (item.examineBg) {
            Dialog.inspectItem(item.examineBg);
          } else {
            this.selectItem(item.id);
          }
        });
      } else {
        slot.classList.add('empty');
      }
      container.appendChild(slot);
    }
  }
};
