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
   * Called when the engine switches scenes within this room.
   * Useful for updating scene-specific UI or logic.
   */
  onSceneChange(sceneId) {}

  /**
   * Called when leaving this room to clean up listeners and DOM changes.
   */
  cleanup() {}
}
