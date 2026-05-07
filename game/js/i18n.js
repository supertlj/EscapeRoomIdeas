/* ============================================
   i18n.js — Language Manager
   ============================================ */
const I18n = {
  currentLang: 'en',

  init() {
    const saved = localStorage.getItem('grandview_lang');
    if (saved) {
      this.currentLang = saved;
    } else {
      const browserLang = navigator.language || navigator.userLanguage;
      if (browserLang && browserLang.startsWith('zh')) {
        this.currentLang = 'zh';
      } else {
        this.currentLang = 'en';
      }
    }
  },

  toggle() {
    this.currentLang = this.currentLang === 'en' ? 'zh' : 'en';
    localStorage.setItem('grandview_lang', this.currentLang);
    return this.currentLang;
  },

  /** Get localized text from a bilingual object {"en": "...", "zh": "..."} */
  t(obj) {
    if (!obj) return '';
    if (typeof obj === 'string') return obj;
    return obj[this.currentLang] || obj['en'] || '';
  },

  /** Get localized text from an array of bilingual objects */
  tArray(arr) {
    if (!arr) return [];
    return arr.map(item => this.t(item));
  }
};
