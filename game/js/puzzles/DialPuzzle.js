/* ============================================
   DialPuzzle.js — Dual-Layer Mechanical Safe Dial
   ============================================ */
class DialPuzzle {
  constructor({ targetValue, onSuccess, assetPath, bgImage }) {
    this.targetValue = targetValue;
    this.onSuccess = onSuccess;
    this.bgImage = bgImage || 'assets/rooms/room_02/hatch_zoom.png';
    // Derive basePath from assetPath (e.g., 'assets/rooms/room_02/')
    this.basePath = assetPath.substring(0, assetPath.lastIndexOf('/') + 1);
    this.currentValue = 0;
    this.rotation = 0;
    this.isVisible = false;
    this.container = null;
  }

  init() {
    this.container = document.createElement('div');
    this.container.id = 'dial-puzzle-container';
    this.container.className = 'modal zoom-mode hidden';
    
    this.container.innerHTML = `
      <div class="zoom-overlay-container">
        <div class="zoom-inner-box centered-layout" id="dial-overlay-inner">
          <div id="dial-wrapper" style="position: relative; width: 800px; height: 800px; overflow: hidden;">
            <img src="${this.bgImage}" id="dial-bg" style="width: 100%; height: 100%; object-fit: contain; filter: blur(4px) brightness(0.8); transform: scale(1.05);">
            
            <div class="dial-frame" style="position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%) scale(0.85); filter: drop-shadow(0 20px 40px rgba(0,0,0,0.9));">
              <img src="${this.basePath}dial_outer.png" id="dial-outer" class="dial-layer outer dial-img" style="filter: sepia(0.3) brightness(0.9);">
              <img src="${this.basePath}dial_inner.png" id="dial-inner" class="dial-layer inner dial-img" style="filter: sepia(0.3) brightness(0.95);">
            </div>

            <div class="dial-controls" style="position: absolute; bottom: 100px; left: 0; width: 100%; display: flex; justify-content: center; align-items: center; gap: 40px; pointer-events: none;">
              <button id="btn-dial-left" class="dial-btn" style="pointer-events: auto; background: rgba(40,30,20,0.9); border-color: #c9a84c;"><span>◀</span></button>
              <div class="dial-display" style="background: rgba(20,15,10,0.95); border-color: #c9a84c; color: #ffcc66; text-shadow: 0 0 10px rgba(255, 204, 102, 0.4); font-family: 'Cinzel', serif;">00</div>
              <button id="btn-dial-right" class="dial-btn" style="pointer-events: auto; background: rgba(40,30,20,0.9); border-color: #c9a84c;"><span>▶</span></button>
            </div>
          </div>
        </div>
        <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
      </div>
    `;

    document.getElementById('ui-design-container').appendChild(this.container);

    this.container.querySelector('#btn-dial-left').onclick = () => this.rotate(-1);
    this.container.querySelector('#btn-dial-right').onclick = () => this.rotate(1);
    
    // Clicking anywhere on the background (outside the inner box) closes the modal
    this.container.onclick = (e) => {
      if (!e.target.closest('.zoom-inner-box')) {
        this.hide();
      }
    };
  }

  show() {
    this.container.classList.remove('hidden');
    this.isVisible = true;
    this.updateUI();
  }

  hide() {
    this.container.classList.add('hidden');
    this.isVisible = false;
  }

  async rotate(direction) {
    if (Engine.isBusy || this.isSolved) return;
    Engine.isBusy = true;

    try {
      this.currentValue = (this.currentValue + direction + 60) % 60;
      this.rotation += direction * 6; // 6 degrees per number
      
      Audio.playSFX('mechanical_tick');
      this.updateUI();

      if (this.currentValue === this.targetValue) {
        this.isSolved = true;
        await new Promise(resolve => setTimeout(resolve, 600));
        await this.triggerSuccess();
      }
    } finally {
      Engine.isBusy = false;
    }
  }

  updateUI() {
    const inner = this.container.querySelector('#dial-inner');
    const display = this.container.querySelector('.dial-display');
    
    // Only rotate the inner handle (with the arrow indicator)
    inner.style.transform = `rotate(${this.rotation}deg)`;
    
    display.textContent = String(this.currentValue).padStart(2, '0');
  }

  async triggerSuccess() {
    Audio.playSFX('unlock');
    if (this.onSuccess) await this.onSuccess();
    this.hide();
  }

  cleanup() {
    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
    }
  }
}

window.DialPuzzle = DialPuzzle;
