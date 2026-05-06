/* ============================================
   SaveManager.js — Simplified Checkpoint System
   ============================================ */
const SaveManager = {
  SAVE_KEY: 'grandview_hotel_checkpoint',

  /** Save the current room number (Checkpoint) */
  saveProgress(roomNumber) {
    localStorage.setItem(this.SAVE_KEY, roomNumber);
    console.log(`Progress saved: Room ${roomNumber}`);
  },

  /** Get the furthest unlocked room number */
  getSavedRoom() {
    const saved = localStorage.getItem(this.SAVE_KEY);
    return saved ? parseInt(saved, 10) : 1;
  },

  /** Full reset - start from Room 1 */
  resetGame() {
    localStorage.removeItem(this.SAVE_KEY);
    window.location.reload();
  }
};
