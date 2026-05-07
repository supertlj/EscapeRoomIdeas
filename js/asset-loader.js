/* ============================================
   AssetLoader.js — Central Asset Management
   ============================================ */
const AssetLoader = {
  images: {},
  
  async loadImage(id, src) {
    if (this.images[id]) return this.images[id];
    
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        this.images[id] = img;
        resolve(img);
      };
      img.onerror = () => {
        console.error(`Failed to load asset: ${src}`);
        reject(new Error(`Failed to load asset: ${src}`));
      };
      img.src = src;
    });
  },

  /**
   * Loads an image and removes a black background (useful for AI generated sprites)
   */
  async loadTransparentImage(id, src, threshold = 25) {
    const img = await this.loadImage(id + '_raw', src);
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
      // If the pixel is very dark, make it transparent
      if (data[i] < threshold && data[i+1] < threshold && data[i+2] < threshold) {
        data[i+3] = 0;
      }
    }
    
    ctx.putImageData(imageData, 0, 0);
    this.images[id] = canvas;
    return canvas;
  },

  getImage(id) {
    return this.images[id];
  },

  clear() {
    this.images = {};
  }
};

window.AssetLoader = AssetLoader;
