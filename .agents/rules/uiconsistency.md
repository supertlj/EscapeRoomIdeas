---
trigger: always_on
---

All game-state feedback (Unlocked, Invalid Code, Item Found) MUST use the global Dialog.showFeedback system. Avoid custom alert() calls or ad-hoc text overlays. This ensures a consistent "premium" look and feel (gold pill style) across all puzzles and rooms.