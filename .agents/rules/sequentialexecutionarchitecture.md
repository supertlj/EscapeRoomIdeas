---
trigger: always_on
---

All user interactions are managed via a global re-entrant task counter (Engine.busyCount). The Engine automatically locks interaction (and dims navigation UI) whenever a core action—like switchScene, goBack, or pickupItem—is in progress. This allows room-level logic to remain simple and synchronous, while the Engine ensures that animations and transitions never overlap or cause race conditions.