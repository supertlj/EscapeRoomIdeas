---
trigger: always_on
---

All user-facing text strings MUST be wrapped in I18n.t() or include a dual-language check (I18n.currentLang === 'zh' ? ... : ...). Never hardcode English-only or Chinese-only strings directly into the logic.