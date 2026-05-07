class KeypadPuzzle {
  constructor(options = {}) {
    this.targetCode = options.targetCode || '0000';
    this.cssClass = options.cssClass || 'keypad-room01';
    this.bgImage = options.bgImage || 'assets/rooms/room_01/zoom_keypad.png';
    this.onSuccess = options.onSuccess || (() => {});
    this.onFail = options.onFail || (() => {});
    this.onClose = options.onClose || (() => {});
    
    this.currentCode = '';
    
    // Bind methods
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleOutsideClick = this.handleOutsideClick.bind(this);
    
    this.createDOM();
  }

  createDOM() {
    this.modal = document.createElement('div');
    this.modal.className = `modal zoom-mode hidden ${this.cssClass}`;
    this.modal.id = 'keypad-modal';
    
    this.modal.innerHTML = `
      <div class="zoom-overlay-container">
        <div class="zoom-inner-box centered-layout" id="keypad-overlay-inner">
          <div id="keypad-wrapper" style="position: relative; width: 800px; height: 800px;">
            <img src="${this.bgImage}" id="keypad-bg-image" alt="Keypad" style="width: 100%; height: 100%; object-fit: contain;">
            
            <div id="keypad-display-overlay">
              <div id="keypad-digits">
                <span class="digit-slot"></span>
                <span class="digit-slot"></span>
                <span class="digit-slot"></span>
                <span class="digit-slot"></span>
              </div>
            </div>

            <div id="keypad-button-grid">
              <div class="key-row">
                <button class="key-btn" data-val="1"></button>
                <button class="key-btn" data-val="2"></button>
                <button class="key-btn" data-val="3"></button>
              </div>
              <div class="key-row">
                <button class="key-btn" data-val="4"></button>
                <button class="key-btn" data-val="5"></button>
                <button class="key-btn" data-val="6"></button>
              </div>
              <div class="key-row">
                <button class="key-btn" data-val="7"></button>
                <button class="key-btn" data-val="8"></button>
                <button class="key-btn" data-val="9"></button>
              </div>
              <div class="key-row">
                <button class="key-btn" data-val="CLEAR"></button>
                <button class="key-btn" data-val="0"></button>
                <button class="key-btn" data-val="ENTER"></button>
              </div>
            </div>
          </div>
        </div>
        <div class="zoom-hint">TAP ANYWHERE TO CLOSE</div>
      </div>
    `;
    
    document.getElementById('ui-design-container').appendChild(this.modal);
    
    this.buttons = this.modal.querySelectorAll('.key-btn');
    this.slots = this.modal.querySelectorAll('.digit-slot');
  }

  init() {
    this.currentCode = '';
    this.updateDisplay();
    
    this.buttons.forEach(btn => btn.addEventListener('click', this.handleButtonClick));
    this.modal.addEventListener('click', this.handleOutsideClick);
  }

  cleanup() {
    this.buttons.forEach(btn => btn.removeEventListener('click', this.handleButtonClick));
    this.modal.removeEventListener('click', this.handleOutsideClick);
    this.modal.classList.add('hidden');
  }

  show() {
    this.currentCode = '';
    this.updateDisplay();
    this.modal.classList.remove('hidden');
  }

  hide() {
    this.modal.classList.add('hidden');
    this.onClose();
  }

  handleOutsideClick(e) {
    if (!e.target.closest('#keypad-overlay-inner')) {
      this.hide();
    }
  }

  async handleButtonClick(e) {
    if (Engine.isBusy) return;
    Engine.isBusy = true;

    try {
      const btn = e.currentTarget;
      const val = btn.dataset.val;
      Audio.playSFX('button_click');

      if (val === 'CLEAR') {
        this.currentCode = '';
      } else if (val === 'ENTER') {
        if (this.currentCode === this.targetCode) {
          await this.onSuccess();
        } else {
          this.onFail();
          this.currentCode = '';
        }
      } else {
        if (this.currentCode.length < this.targetCode.length) {
          this.currentCode += val;
          
          // Auto-check when max length is reached
          if (this.currentCode.length === this.targetCode.length) {
            this.updateDisplay(); // Show the last digit first
            await new Promise(resolve => setTimeout(resolve, 300));
            
            if (this.currentCode === this.targetCode) {
              await this.onSuccess();
            } else {
              this.onFail();
              this.currentCode = '';
              this.updateDisplay();
            }
            return;
          }
        }
      }
      this.updateDisplay();
    } finally {
      Engine.isBusy = false;
    }
  }

  updateDisplay() {
    this.slots.forEach((slot, i) => {
      const val = this.currentCode[i] || '';
      slot.textContent = val;
      if (val !== '') {
        slot.classList.add('has-value');
      } else {
        slot.classList.remove('has-value');
      }
    });
  }
}
