/* ============================================
   AdManager.js — Monetization Wrapper
   ============================================ */

const AdManager = {
  isSDKLoaded: false,
  
  init() {
    console.log("AdManager: Initializing architecture...");
    // This is where you would load the external SDK script (AdSense, CrazyGames, etc.)
    // For now, we simulate the logic.
    this.isSDKLoaded = true;
  },

  /**
   * Triggers a rewarded video ad.
   * @param {Function} onComplete - Callback if the ad was watched successfully.
   * @param {Function} onFail - Callback if the ad was skipped or failed.
   */
  async showRewardedAd(onComplete, onFail) {
    console.log("AdManager: Requesting rewarded video...");
    
    // Simulation: In a real SDK, this would open a full-screen video overlay
    const simulatedWatchTime = 2000; 
    
    Dialog.showFeedback("Loading Video...", 1000);

    setTimeout(() => {
      // In a real implementation, the SDK provides a 'rewarded' callback
      const success = true; // Simulating successful watch
      
      if (success) {
        onComplete();
      } else {
        onFail();
      }
    }, simulatedWatchTime);
  },

  /**
   * Triggers an Interstitial Ad (full-screen, usually between levels).
   * @param {Function} onComplete - Callback when the ad is closed.
   */
  async showInterstitialAd(onComplete) {
    console.log("AdManager: Requesting interstitial...");
    
    // Simulation: Interstitials are usually un-skippable for a few seconds
    Dialog.showFeedback(I18n.currentLang === 'zh' ? '正在加载...' : 'Loading...', 1000);

    setTimeout(() => {
      onComplete();
    }, 1500);
  },

  /**
   * Refreshes the bottom banner ad.
   */
  refreshBanner() {
    console.log("AdManager: Refreshing banner ad...");
    // Real SDKs usually have a method like: SDK.refreshAd('ad-space-id');
  }
};

window.AdManager = AdManager;
