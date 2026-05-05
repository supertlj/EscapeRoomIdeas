class Room02 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    
    SpriteManager.scenes = {};
    // await SpriteManager.setScene('main', `assets/rooms/room_${padded}/background.png`);
    
    this.state = {};

    // Initialize Room 2 specific hotspots here
    
    HintSystem.setCurrentPuzzle(0);
    return this.state;
  }

  cleanup() {
    // Clean up room 2 resources
  }
}

window.Room02 = Room02;
