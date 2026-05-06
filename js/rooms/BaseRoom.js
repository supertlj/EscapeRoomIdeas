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
    modal.className = 'modal-overlay hidden';
    modal.innerHTML = `
      <div class="zoom-frame">
        <img id="item-inspect-image" src="" alt="Inspecting item">
      </div>
      <div class="zoom-hint-text">TAP ANYWHERE TO CLOSE</div>
    `;
    
    const container = document.getElementById('ui-design-container');
    if (container) container.appendChild(modal);
    
    modal.onclick = () => {
      modal.classList.add('hidden');
    };
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
