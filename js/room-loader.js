/* ============================================
   room-loader.js — Loads room JSON and sets up scene
   ============================================ */
const RoomLoader = {

  async loadRoom(roomNumber) {
    const padded = String(roomNumber).padStart(2, '0');
    
    // 1. Load Room JSON
    const response = await fetch(`data/rooms/room_${padded}.json`);
    const roomData = await response.json();

    // 2. Dynamic Script and CSS Loading
    await this.loadScript(`js/rooms/Room${padded}.js`);
    this.loadCSS(`css/rooms/room_${padded}.css`);

    document.getElementById('room-title').textContent = I18n.t(roomData.room_name);

    return roomData;
  },

  loadScript(src) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.body.appendChild(script);
    });
  },

  loadCSS(href) {
    if (document.querySelector(`link[href="${href}"]`)) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    document.head.appendChild(link);
  }
};


