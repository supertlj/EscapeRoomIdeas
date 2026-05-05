/* ============================================
   sprite-manager.js — Multi-Scene Sprite Rendering
   ============================================ */
const SpriteManager = {
  scenes: {},
  currentSceneId: 'main',
  canvas: null,
  ctx: null,
  scale: 1,
  offsetX: 0,
  offsetY: 0,

  // Design resolution (full portrait screen)
  DESIGN_W: 1080,
  DESIGN_H: 1920,
  
  // Art area (1024x1024 square) centered horizontally
  ART_SIZE: 1024,
  ART_X: 28,  // (1080 - 1024) / 2
  ART_Y: 400, // Vertical position

  init(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.scenes = {
      'main': { background: null, sprites: [] }
    };
    this.resize();
    window.addEventListener('resize', () => this.resize());
  },

  resize() {
    const dpr = window.devicePixelRatio || 1;
    const w = window.innerWidth;
    const h = window.innerHeight;

    if (w === 0 || h === 0) return;

    this.canvas.width = w * dpr;
    this.canvas.height = h * dpr;
    this.canvas.style.width = w + 'px';
    this.canvas.style.height = h + 'px';

    const screenRatio = w / h;
    const designRatio = this.DESIGN_W / this.DESIGN_H;

    if (screenRatio > designRatio) {
      this.scale = h / this.DESIGN_H;
      this.offsetX = (w - this.DESIGN_W * this.scale) / 2;
      this.offsetY = 0;
    } else {
      this.scale = w / this.DESIGN_W;
      this.offsetX = 0;
      this.offsetY = (h - this.DESIGN_H * this.scale) / 2;
    }

    // Sync UI container with canvas scaling
    const uiContainer = document.getElementById('ui-design-container');
    if (uiContainer) {
      uiContainer.style.transform = `translate(${this.offsetX}px, ${this.offsetY}px) scale(${this.scale})`;
    }
  },

  screenToDesign(sx, sy) {
    return {
      x: (sx - this.offsetX) / this.scale,
      y: (sy - this.offsetY) / this.scale
    };
  },

  /** Create or update a scene */
  async setScene(sceneId, backgroundSrc) {
    if (!this.scenes[sceneId]) {
      this.scenes[sceneId] = { background: null, sprites: [] };
    }
    
    if (backgroundSrc) {
      const img = new Image();
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = backgroundSrc;
      });
      this.scenes[sceneId].background = img;
    }
    
    this.currentSceneId = sceneId;
    return this.scenes[sceneId];
  },

  /** Add a sprite relative to the ART area (0-1024) */
  addSprite(sceneId, sprite) {
    if (!this.scenes[sceneId]) {
      this.scenes[sceneId] = { background: null, sprites: [] };
    }
    this.scenes[sceneId].sprites.push({
      visible: true,
      zLayer: 1,
      ...sprite
    });
  },

  /** Update a sprite's property */
  updateSprite(sceneId, spriteId, updates) {
    const scene = this.scenes[sceneId];
    if (scene) {
      const sprite = scene.sprites.find(s => s.id === spriteId);
      if (sprite) {
        Object.assign(sprite, updates);
      }
    }
  },

  debugMode: false,


  getSprite(sceneId, spriteId) {
    const scene = this.scenes[sceneId];
    return scene ? scene.sprites.find(s => s.id === spriteId) : null;
  },

  async loadSpriteImage(sceneId, spriteId, src) {
    const sprite = this.getSprite(sceneId, spriteId);
    if (!sprite) return;
    const img = new Image();
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = reject;
      img.src = src;
    });
    sprite.image = img;
  },

  hitTest(dx, dy) {
    const scene = this.scenes[this.currentSceneId];
    if (!scene) return null;

    // Convert design coordinates to art-local coordinates
    const lx = dx - this.ART_X;
    const ly = dy - this.ART_Y;

    // Test in reverse order (top z-layer first)
    const sorted = [...scene.sprites].sort((a, b) => (b.zLayer || 0) - (a.zLayer || 0));
    for (const s of sorted) {
      if (!s.visible) continue;
      if (lx >= s.x && lx <= s.x + s.w && ly >= s.y && ly <= s.y + s.h) {
        return s;
      }
    }
    return null;
  },

  render() {
    const ctx = this.ctx;
    const dpr = window.devicePixelRatio || 1;
    const w = this.canvas.width / dpr;
    const h = this.canvas.height / dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    const scene = this.scenes[this.currentSceneId];
    if (!scene) return;

    ctx.save();
    ctx.translate(this.offsetX, this.offsetY);
    ctx.scale(this.scale, this.scale);

    // Draw Art Frame Shadow
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 30;
    ctx.fillStyle = '#111';
    ctx.fillRect(this.ART_X - 5, this.ART_Y - 5, this.ART_SIZE + 10, this.ART_SIZE + 10);
    ctx.shadowBlur = 0;

    if (scene.background) {
      ctx.drawImage(scene.background, this.ART_X, this.ART_Y, this.ART_SIZE, this.ART_SIZE);
    }

    // Draw Sprites
    scene.sprites.forEach(s => {
      if (!s.visible) return;
      
      if (s.image) {
        ctx.save();
        if (s.blendMode) ctx.globalCompositeOperation = s.blendMode;
        
        // Apply pulsing glint if enabled
        if (s.glint) {
          const pulse = Math.sin(Date.now() / 400) * 0.4 + 1.2;
          ctx.filter = `brightness(${pulse})`;
        }

        ctx.drawImage(s.image, this.ART_X + s.x, this.ART_Y + s.y, s.w, s.h);
        ctx.restore();
      }

      // Draw debug outlines if enabled
      if (this.debugMode) {
        ctx.save();
        ctx.strokeStyle = '#ff00ff';
        ctx.lineWidth = 4;
        ctx.setLineDash([10, 5]);
        ctx.strokeRect(this.ART_X + s.x, this.ART_Y + s.y, s.w, s.h);
        
        // Draw Sprite ID
        ctx.fillStyle = '#ff00ff';
        ctx.font = 'bold 20px Arial';
        ctx.fillText(s.id, this.ART_X + s.x + 5, this.ART_Y + s.y + 22);
        ctx.restore();
      }
    });

    // Optional: Draw a thin gold border around the art
    ctx.strokeStyle = '#c9a84c';
    ctx.lineWidth = 2;
    ctx.strokeRect(this.ART_X, this.ART_Y, this.ART_SIZE, this.ART_SIZE);

    ctx.restore();

    // Global Vignette over the whole screen (DPR-scaled)
    const grd = ctx.createRadialGradient(w/2, h/2, h/4, w/2, h/2, h/1.2);
    grd.addColorStop(0, 'rgba(0,0,0,0)');
    grd.addColorStop(1, 'rgba(0,0,0,0.4)');
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, w, h);
  },

  startRenderLoop() {
    const loop = () => {
      this.render();
      requestAnimationFrame(loop);
    };
    loop();
  }
};

