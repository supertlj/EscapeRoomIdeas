/* ============================================
   puzzle-engine.js — Puzzle Logic Handler
   ============================================ */
const PuzzleEngine = {

  /** Show numeric code entry modal and validate input */
  showCodeEntry(expectedCode, onSuccess, onFail) {
    const modal = document.getElementById('code-modal');
    const digits = document.getElementById('code-digits');
    let currentInput = '';

    digits.textContent = '';
    modal.classList.remove('hidden');

    // Remove old listeners by replacing buttons
    const keypad = document.getElementById('code-keypad');
    const newKeypad = keypad.cloneNode(true);
    keypad.parentNode.replaceChild(newKeypad, keypad);

    newKeypad.addEventListener('click', (e) => {
      const btn = e.target.closest('.key-btn');
      if (!btn) return;
      const key = btn.dataset.key;

      Audio.playSFX('click');

      if (key === 'clear') {
        currentInput = '';
      } else if (key === 'enter') {
        if (currentInput === String(expectedCode)) {
          modal.classList.add('hidden');
          Audio.playSFX('puzzle_solve');
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '✓ 正确！' : '✓ Correct!');
          if (onSuccess) onSuccess();
        } else {
          Audio.playSFX('wrong_code');
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '✗ 密码错误' : '✗ Wrong Code', 1000);
          currentInput = '';
          digits.textContent = '';
          if (onFail) onFail();
        }
        return;
      } else {
        if (currentInput.length < String(expectedCode).length + 2) {
          currentInput += key;
        }
      }
      digits.textContent = currentInput;
    });
  },

  /** Close code modal */
  closeCodeEntry() {
    document.getElementById('code-modal').classList.add('hidden');
  },

  /** Check if an item-use puzzle can be solved */
  checkItemUse(requiredItemId) {
    const selected = Inventory.getSelected();
    if (selected && selected.id === requiredItemId) {
      return true;
    }
    return false;
  },

  /** Validate sequence input (e.g., pressing buttons in order) */
  createSequenceChecker(expectedSequence, onSuccess) {
    let currentIndex = 0;
    return {
      input(value) {
        if (value === expectedSequence[currentIndex]) {
          currentIndex++;
          Audio.playSFX('click');
          if (currentIndex >= expectedSequence.length) {
            Audio.playSFX('puzzle_solve');
            Dialog.showFeedback(I18n.currentLang === 'zh' ? '✓ 正确！' : '✓ Correct!');
            if (onSuccess) onSuccess();
            return true;
          }
        } else {
          currentIndex = 0;
          Audio.playSFX('wrong_code');
          Dialog.showFeedback(I18n.currentLang === 'zh' ? '✗ 顺序错误' : '✗ Wrong Order', 1000);
        }
        return false;
      },
      reset() { currentIndex = 0; }
    };
  }
};
