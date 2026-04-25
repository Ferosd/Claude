(function heroAnimation() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  if (window.innerWidth < 768) {
    const fb = document.createElement('div');
    fb.className = 'hero-canvas-fallback';
    canvas.parentNode.insertBefore(fb, canvas);
    return;
  }

  function waitForThree(fn) {
    typeof THREE !== 'undefined' ? fn() : setTimeout(() => waitForThree(fn), 50);
  }

  function applyFallback() {
    const fb = document.createElement('div');
    fb.className = 'hero-canvas-fallback';
    if (canvas.parentNode) canvas.parentNode.insertBefore(fb, canvas);
  }

  function setupScene() {
    const COLS = 20, ROWS = 16, SPACING = 1.5;
    const halfW = (COLS - 1) * SPACING / 2;
    const halfH = (ROWS - 1) * SPACING / 2;
    const COUNT = COLS * ROWS;

    const scene  = new THREE.Scene();
    const W      = canvas.clientWidth  || window.innerWidth;
    const H      = canvas.clientHeight || window.innerHeight;
    const camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 100);
    camera.position.set(0, 20, 28);
    camera.lookAt(0, -2, 0);

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const geo  = new THREE.BoxGeometry(0.6, 0.6, 0.6);
    const mat  = new THREE.MeshLambertMaterial({ color: 0xffffff });
    const mesh = new THREE.InstancedMesh(geo, mat, COUNT);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const dir = new THREE.DirectionalLight(0x00D4AA, 1.4);
    dir.position.set(4, 10, 6);
    scene.add(dir);

    const cLow  = new THREE.Color('#052a22');
    const cMid  = new THREE.Color('#00D4AA');
    const cHigh = new THREE.Color('#80fff0');
    const dummy = new THREE.Object3D();
    const col   = new THREE.Color();

    for (let i = 0; i < COUNT; i++) mesh.setColorAt(i, cLow);
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;

    let t = 0, firstFrame = true;

    function tick() {
      requestAnimationFrame(tick);
      t += 0.016;

      camera.position.x = Math.sin(t * 0.15) * 28;
      camera.position.z = Math.cos(t * 0.15) * 28;
      camera.lookAt(0, -2, 0);

      for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
          const i  = r * COLS + c;
          const ht = Math.sin(c * 0.5 + r * 0.4 + t * 1.2) * 1.2;

          dummy.position.set(c * SPACING - halfW, ht, r * SPACING - halfH);
          dummy.updateMatrix();
          mesh.setMatrixAt(i, dummy.matrix);

          const norm = (ht + 1.2) / 2.4;
          norm < 0.5
            ? col.copy(cLow).lerp(cMid, norm * 2)
            : col.copy(cMid).lerp(cHigh, (norm - 0.5) * 2);
          mesh.setColorAt(i, col);
        }
      }

      mesh.instanceMatrix.needsUpdate = true;
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      renderer.render(scene, camera);

      if (firstFrame) {
        firstFrame = false;
        canvas.style.transition = 'opacity 1.5s ease';
        canvas.style.opacity = '1';
      }
    }

    tick();

    window.addEventListener('resize', () => {
      const nw = canvas.clientWidth, nh = canvas.clientHeight;
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh);
    }, { passive: true });
  }

  waitForThree(() => { try { setupScene(); } catch(e) { applyFallback(); } });

  // Staggered entrance for hero content
  const delays = [0.2, 0.4, 0.7, 0.9];
  document.querySelectorAll('.reveal-hero').forEach((el, i) => {
    const d = delays[i] !== undefined ? delays[i] : 0.9 + i * 0.1;
    el.style.transform  = `translateY(${16 + i * 4}px)`;
    el.style.transition = `opacity .7s cubic-bezier(.4,0,.2,1) ${d}s,transform .7s cubic-bezier(.4,0,.2,1) ${d}s`;
    requestAnimationFrame(() => requestAnimationFrame(() => {
      el.style.opacity   = '1';
      el.style.transform = 'translateY(0)';
    }));
  });

  const hint = document.getElementById('heroScrollHint');
  if (hint) window.addEventListener('scroll', () => {
    hint.style.opacity = window.scrollY > 100 ? '0' : '1';
  }, { passive: true });
})();
