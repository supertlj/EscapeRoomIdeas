/* ============================================
   CombinationLockPuzzle.js — Mechanical Roller Lock
   ============================================ */
class CombinationLockPuzzle {
  constructor(options = {}) {
    this.targetCode = options.targetCode || '472';
    this.bgImage = options.bgImage || 'assets/rooms/room_02/cabinet_zoom.png';
    this.onSuccess = options.onSuccess || (() => {});
    
    this.currentDigits = [0, 0, 0];
    this.visualOffsets = [0, 0, 0]; // Track visual position for continuous rolling
    this.isSolved = false;
    
    this.isVisible = false;
    this.createDOM();
  }

  createDOM() {
    this.modal = document.createElement('div');
    this.modal.className = `modal zoom-mode hidden mechanical-lock`;
    this.modal.id = 'combination-lock-modal';

    this.modal.innerHTML = `
      <div class="zoom-overlay-container">
        <div class="zoom-inner-box centered-layout" id="combo-lock-overlay-inner">
          <div id="combo-lock-wrapper" style="position: relative; width: 800px; height: 800px; overflow: hidden;">
            <img src="${this.bgImage}" id="combo-lock-bg" style="width: 100%; height: 100%; object-fit: contain;">
            
            <!-- Feedback Message Overlay -->
            <div id="combo-feedback" class="puzzle-feedback-overlay"></div>

            <!-- The Knob (The Enter Button) -->
            <div id="combo-knob" class="lock-target" style="position: absolute; left: 135px; top: 326px; width: 145px; height: 145px;"></div>
            
            <!-- The Rolling Digit Reels (Mask Overlays) -->
            <div class="roller-column" id="roller-0" style="position: absolute; left: 313px; top: 285px; width: 78px; height: 227px;"></div>
            <div class="roller-column" id="roller-1" style="position: absolute; left: 437px; top: 285px; width: 79px; height: 227px;"></div>
            <div class="roller-column" id="roller-2" style="position: absolute; left: 559px; top: 285px; width: 81px; height: 227px;"></div>
          </div>
        </div>
        <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
      </div>
    `;
    
    document.getElementById('ui-design-container').appendChild(this.modal);
    
    // Close on overlay click
    this.modal.addEventListener('click', (e) => {
      // If we clicked the modal background or the hint, close it
      if (e.target === this.modal || e.target.classList.contains('zoom-overlay-container') || e.target.classList.contains('zoom-hint')) {
        this.hide();
      }
    });

    this.modal.querySelector('#combo-knob').addEventListener('click', (e) => {
      e.stopPropagation();
      this.checkCode();
    });
    
    [0, 1, 2].forEach(index => {
      this.modal.querySelector(`#roller-${index}`).addEventListener('click', (e) => {
        e.stopPropagation();
        this.incrementDigit(index);
      });
    });
  }

  async incrementDigit(index) {
    if (Engine.isBusy || this.isSolved) return;
    Engine.isBusy = true;

    try {
      this.visualOffsets[index]++;
      this.currentDigits[index] = this.visualOffsets[index] % 10;
      Audio.playSFX('click');
      this.updateDisplay();

      // Auto-check for success
      const code = this.currentDigits.join('');
      if (code === this.targetCode) {
        this.isSolved = true; // Lock the puzzle immediately so fast clicks don't overshoot
        await new Promise(resolve => setTimeout(resolve, 500));
        await this.checkCode();
      }
    } finally {
      Engine.isBusy = false;
    }
  }

  updateDisplay() {
    [0, 1, 2].forEach(index => {
      const roller = this.modal.querySelector(`#roller-${index}`);
      if (!roller) return;
      
      const digitHeight = 227 / 3;
      const visualIdx = this.visualOffsets[index] + 0.7;
      const offsetPxl = visualIdx * digitHeight;
      
      roller.style.backgroundPosition = `center -${offsetPxl}px`;
    });
  }

  async checkCode() {
    const code = this.currentDigits.join('');
    if (code === this.targetCode) {
      this.isSolved = true;
      await this.showSuccess();
    } else {
      this.isSolved = false; // Allow retrying if manual knob was used wrongly
      Audio.playSFX('error');
      Dialog.showFeedback(I18n.currentLang === 'zh' ? '密码错误' : 'INVALID CODE', 2000);
    }
  }

  async showSuccess() {
    Audio.playSFX('puzzle_solve');
    Dialog.showFeedback(I18n.currentLang === 'zh' ? '已解锁' : 'UNLOCKED', 2000);
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.hide();
    if (this.onSuccess) await this.onSuccess();
  }

  show() {
    this.modal.classList.remove('hidden');
    this.isVisible = true;
    this.updateDisplay();
  }

  hide() {
    this.modal.classList.add('hidden');
    this.isVisible = false;
  }

  init() {
    this.currentDigits = [0, 0, 0];
    this.visualOffsets = [0, 0, 0];
    this.isSolved = false;
    this.updateDisplay();
  }
}

window.CombinationLockPuzzle = CombinationLockPuzzle;
