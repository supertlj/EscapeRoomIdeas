---
trigger: always_on
---

All inventory items MUST be defined in the room's .json file with an explicit type property. The Inventory.js logic is strictly driven by these categories:

tool: Standard selection for environmental interaction.
document: Triggers a static inspection modal (uses examineBg).
interactive: Switches to a dedicated interactive engine scene (uses examineScene).