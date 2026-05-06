/* ============================================
   DialPuzzle.js — Dual-Layer Mechanical Safe Dial
   ============================================ */
class DialPuzzle {
  constructor({ targetValue, onSuccess, assetPath }) {
    this.targetValue = targetValue;
    this.onSuccess = onSuccess;
    // We now expect dial_outer.png and dial_inner.png in the same folder
    this.basePath = 'assets/rooms/room_02/';
    this.currentValue = 0;
    this.rotation = 0;
    this.isVisible = false;
    this.container = null;
  }

  init() {
    this.container = document.createElement('div');
    this.container.id = 'dial-puzzle-container';
    this.container.className = 'puzzle-modal hidden';
    
    this.container.innerHTML = `
      <div class="puzzle-overlay"></div>
      <div class="dial-content">
        <div class="dial-frame">
          <img src="${this.basePath}dial_outer.png" id="dial-outer" class="dial-layer outer">
          <img src="${this.basePath}dial_inner.png" id="dial-inner" class="dial-layer inner">
        </div>
        <div class="dial-controls">
          <button id="btn-dial-left" class="dial-btn"><span>◀</span></button>
          <div class="dial-display">00</div>
          <button id="btn-dial-right" class="dial-btn"><span>▶</span></button>
        </div>
        <button id="btn-dial-close" class="dial-close">✕</button>
      </div>
    `;

    document.body.appendChild(this.container);

    this.container.querySelector('#btn-dial-left').onclick = () => this.rotate(-1);
    this.container.querySelector('#btn-dial-right').onclick = () => this.rotate(1);
    this.container.querySelector('#btn-dial-close').onclick = () => this.hide();
    this.container.querySelector('.puzzle-overlay').onclick = () => this.hide();
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

  rotate(direction) {
    this.currentValue = (this.currentValue + direction + 60) % 60;
    this.rotation += direction * 6; // 6 degrees per number
    
    Audio.playSFX('mechanical_tick');
    this.updateUI();

    if (this.currentValue === this.targetValue) {
      setTimeout(() => this.triggerSuccess(), 600);
    }
  }

  updateUI() {
    const inner = this.container.querySelector('#dial-inner');
    const display = this.container.querySelector('.dial-display');
    
    // Only rotate the inner handle (with the arrow indicator)
    inner.style.transform = `rotate(${this.rotation}deg)`;
    
    display.textContent = String(this.currentValue).padStart(2, '0');
  }

  triggerSuccess() {
    Audio.playSFX('unlock');
    if (this.onSuccess) this.onSuccess();
    this.hide();
  }

  cleanup() {
    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
    }
  }
}

window.DialPuzzle = DialPuzzle;
