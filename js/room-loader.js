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

  onSceneChange(sceneId) {
    // Scene-specific logic if needed
  }
};


