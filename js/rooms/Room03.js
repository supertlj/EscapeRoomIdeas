class Room03 extends BaseRoom {
  async setup() {
    const padded = String(this.roomData.room_number).padStart(2, '0');
    const assetPath = `assets/rooms/room_${padded}`;
    
    // Clear old scenes
    SpriteManager.scenes = {};

    this.state = {
      lightOn: true
    };

    // Placeholder background since we don't have the asset yet
    // In a real scenario, we would wait for the user to provide background.webp
    const loadScene = async (sceneId, src) => {
      const img = new Image();
      // NOTE: This will fail until the asset exists.
      // I am defining it here so the engine is ready once you drop the file in.
      try {
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = src;
        });
        SpriteManager.scenes[sceneId] = { background: img, sprites: [] };
      } catch (e) {
        console.warn(`Room03: Could not load ${src}. Using black background.`);
        SpriteManager.scenes[sceneId] = { background: null, sprites: [] };
      }
    };

    await loadScene('main', `${assetPath}/background.webp`);
    
    SpriteManager.currentSceneId = 'main';

    this.initInspectModal();
    this.setupMainScene();
  }

  setupMainScene() {
    // Basic interaction to show the room is active
    SpriteManager.addSprite('main', {
      id: 'placeholder_interact', x: 400, y: 400, w: 224, h: 224,
      style: { border: '2px dashed rgba(201, 168, 76, 0.5)' },
      onClick: () => {
        Dialog.showFeedback(I18n.currentLang === 'zh' ? '这里需要宏伟走廊的背景图。' : 'Waiting for the Grand Corridor assets.');
      }
    });
  }

  getInteractiveHotspots(itemId) {
    return [];
  }

  cleanup() {
    console.log("Room03: Cleaning up listeners.");
  }
}

// Register class globally
window.Room03 = Room03;
