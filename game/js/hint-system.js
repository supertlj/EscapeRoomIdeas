/* ============================================
   hint-system.js — 3-Tier Hint System with Ad Gate
   ============================================ */
const HintSystem = {
  currentPuzzleIndex: 0,
  hintsRevealed: {},  // { puzzleName: tierRevealed (0,1,2) }

  init() {
    this.hintsRevealed = {};
    document.getElementById('btn-hint').addEventListener('click', () => this.showHintModal());
    document.getElementById('hint-close').addEventListener('click', () => this.hideHintModal());
    document.getElementById('hint-watch-ad').addEventListener('click', () => this.watchAdForHint());
  },

  /** Set which puzzle the player is currently working on */
  setCurrentPuzzle(puzzleIndex) {
    this.currentPuzzleIndex = puzzleIndex;
  },

  /** Get the current hint tier revealed for a puzzle */
  getTierRevealed(puzzleName) {
    return this.hintsRevealed[puzzleName] || 0;
  },

  showHintModal() {
    const puzzle = Engine.getCurrentPuzzle();
    if (!puzzle) return;

    const puzzleName = I18n.t(puzzle.puzzle_name);
    const tier = this.getTierRevealed(puzzleName);
    const hints = puzzle.hints || [];

    const modal = document.getElementById('hint-modal');
    const tierLabel = document.getElementById('hint-tier-label');
    const hintText = document.getElementById('hint-text');
    const watchBtn = document.getElementById('hint-watch-ad');

    if (tier >= hints.length) {
      // All hints revealed
      tierLabel.textContent = I18n.currentLang === 'zh' ? '所有提示已揭示' : 'All Hints Revealed';
      hintText.textContent = I18n.t(hints[hints.length - 1]);
      watchBtn.style.display = 'none';
    } else if (tier === 0) {
      // No hints yet — show ad prompt
      tierLabel.textContent = I18n.currentLang === 'zh' ? `提示 1 / ${hints.length}` : `Hint 1 of ${hints.length}`;
      hintText.textContent = I18n.currentLang === 'zh' ? '观看广告获取提示' : 'Watch an ad to get a hint';
      watchBtn.style.display = 'block';
      watchBtn.textContent = I18n.currentLang === 'zh' ? '观看广告获取提示' : 'Watch Ad for Hint';
    } else {
      // Show current tier hint, offer next
      tierLabel.textContent = I18n.currentLang === 'zh' ? `提示 ${tier} / ${hints.length}` : `Hint ${tier} of ${hints.length}`;
      hintText.textContent = I18n.t(hints[tier - 1]);
      if (tier < hints.length) {
        watchBtn.style.display = 'block';
        watchBtn.textContent = I18n.currentLang === 'zh' ? '观看广告获取下一条提示' : 'Watch Ad for Next Hint';
      } else {
        watchBtn.style.display = 'none';
      }
    }

    modal.classList.remove('hidden');
  },

  hideHintModal() {
    document.getElementById('hint-modal').classList.add('hidden');
  },

  watchAdForHint() {
    const watchBtn = document.getElementById('hint-watch-ad');
    watchBtn.disabled = true;

    AdManager.showRewardedAd(
      () => {
        // Success: Award the hint
        const puzzle = Engine.getCurrentPuzzle();
        if (puzzle) {
          const puzzleName = I18n.t(puzzle.puzzle_name);
          const tier = this.getTierRevealed(puzzleName);
          this.hintsRevealed[puzzleName] = tier + 1;
        }
        watchBtn.disabled = false;
        this.showHintModal();
      },
      () => {
        // Fail/Skip: No hint
        watchBtn.disabled = false;
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '广告未看完' : 'Ad not finished', 2000);
      }
    );
  }
};
