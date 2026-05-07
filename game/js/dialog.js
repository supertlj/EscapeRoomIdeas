/* ============================================
   dialog.js — Story & Text Display System
   ============================================ */
const Dialog = {
  typewriterTimer: null,

  showStory(textObj, onClose) {
    const modal = document.getElementById('story-modal');
    const textEl = document.getElementById('story-text');
    const closeBtn = document.getElementById('story-close');

    const text = I18n.t(textObj);
    textEl.textContent = text;
    modal.classList.remove('hidden');

    closeBtn.onclick = () => {
      modal.classList.add('hidden');
      if (onClose) onClose();
    };
  },

  showFeedback(text, duration = 1500) {
    const overlay = document.getElementById('feedback-overlay');
    const textEl = document.getElementById('feedback-text');
    textEl.textContent = text;
    overlay.classList.remove('hidden');
    setTimeout(() => overlay.classList.add('hidden'), duration);
  },

  showRoomComplete(roomData, onNext) {
    const modal = document.getElementById('room-complete');
    const title = document.getElementById('complete-title');
    const text = document.getElementById('complete-text');
    const btn = document.getElementById('btn-next-room');

    title.textContent = I18n.currentLang === 'zh' ? '成功逃脱！' : 'Room Escaped!';
    text.textContent = I18n.t(roomData.final_action);
    modal.classList.remove('hidden');

    btn.onclick = () => {
      modal.classList.add('hidden');
      if (onNext) onNext();
    };
  },

  inspectItem(imgSrc, hotspots = []) {
    const modal = document.getElementById('item-inspect-modal');
    const img = document.getElementById('item-inspect-image');
    const container = document.getElementById('item-inspect-hotspots');
    
    if (!modal || !img) {
      console.error('item-inspect-modal or item-inspect-image not found in DOM.');
      return;
    }
    
    img.src = imgSrc;
    
    // Clear old hotspots
    if (container) {
      container.innerHTML = '';
      container.style.pointerEvents = 'none'; // Container is pass-through
      container.style.zIndex = '9000'; // Above image
      hotspots.forEach(hs => {
        const div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.left = hs.x + 'px';
        div.style.top = hs.y + 'px';
        div.style.width = hs.w + 'px';
        div.style.height = hs.h + 'px';
        div.style.pointerEvents = 'auto';
        div.style.cursor = 'pointer';
        div.style.zIndex = '9999';
        
        const trigger = (e) => {
          e.stopPropagation();
          if (hs.onClick) hs.onClick();
        };

        div.onclick = trigger;
        div.addEventListener('mousedown', trigger);
        
        container.appendChild(div);
      });
    }
    
    modal.classList.remove('hidden');
  }
};
