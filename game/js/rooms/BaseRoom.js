class BaseRoom {
  constructor(roomData) {
    this.roomData = roomData;
    this.state = {};
  }

  /**
   * Called to initialize the room (set up scenes, sprites, etc.)
   */
  async setup() {
    throw new Error('setup() must be implemented by subclass');
  }

  /**
   * Helper to ensure common room UI is present
   */
  initInspectModal() {
    if (document.getElementById('item-inspect-modal')) return;
    
    const modal = document.createElement('div');
    modal.id = 'item-inspect-modal';
    modal.className = 'modal zoom-mode hidden';
    modal.innerHTML = `
      <div class="zoom-overlay-container">
        <div class="zoom-inner-box centered-layout" style="width: 800px; height: 800px;">
          <img id="item-inspect-image" src="" alt="Inspecting item" style="max-width: 90%; max-height: 90%; object-fit: contain;">
          <div id="item-inspect-hotspots" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></div>
        </div>
        <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
      </div>
    `;
    
    const container = document.getElementById('ui-design-container');
    if (container) container.appendChild(modal);
    
    modal.onclick = (e) => {
      if (!e.target.closest('.zoom-inner-box')) {
        modal.classList.add('hidden');
      }
    };
    
    const closeBtn = modal.querySelector('.dial-close');
    if (closeBtn) closeBtn.onclick = () => modal.classList.add('hidden');
  }

  /**
   * Called when the engine switches scenes within this room.
   */
  onSceneChange(sceneId) {}

  /**
   * Called when leaving this room to clean up listeners and DOM changes.
   */
  cleanup() {}
}
