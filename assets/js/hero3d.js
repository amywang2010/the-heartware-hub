/* ============================================================
   Heartware — hero heart
   A particle heart sampled from the Taubin implicit surface,
   lit in the brand crimson, with a blue rim light and a beat.
   Scroll drives the camera and the scale; the pointer tilts it.
   ============================================================ */

import * as THREE from 'three';

const canvas = document.getElementById('hero-canvas');
const hero = document.querySelector('.hero');

if (canvas && hero) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- sample the implicit heart ---------- */
  // F(x,y,z) = (x^2 + 9/4 y^2 + z^2 - 1)^3 - x^2 z^3 - 9/80 y^2 z^3
  // negative inside, so a ray from the origin crosses the surface once.
  function F(x, y, z) {
    const a = x * x + 2.25 * y * y + z * z - 1;
    return a * a * a - x * x * z * z * z - 0.1125 * y * y * z * z * z;
  }

  function surfaceRadius(dx, dy, dz) {
    let lo = 0, hi = 0;
    let prev = F(0, 0, 0);
    let hit = false;
    for (let r = 0.04; r <= 2.2; r += 0.02) {
      const v = F(dx * r, dy * r, dz * r);
      if (prev < 0 && v >= 0) { lo = r - 0.02; hi = r; hit = true; break; }
      prev = v;
    }
    if (!hit) return 0;
    for (let i = 0; i < 18; i++) {
      const mid = (lo + hi) / 2;
      if (F(dx * mid, dy * mid, dz * mid) < 0) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  }

  const COUNT = 26000;
  const positions = new Float32Array(COUNT * 3);
  const seeds = new Float32Array(COUNT);
  const depths = new Float32Array(COUNT);

  const GOLDEN = Math.PI * (3 - Math.sqrt(5));

  for (let i = 0; i < COUNT; i++) {
    // Fibonacci sphere, then a little jitter so the shell is not a lattice
    const t = (i + 0.5) / COUNT;
    const y = 1 - 2 * t;
    const rad = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = GOLDEN * i;
    const dx = Math.cos(theta) * rad;
    const dy = y;
    const dz = Math.sin(theta) * rad;

    const r = surfaceRadius(dx, dy, dz);
    // some points sit slightly inside so the cloud reads as volume, not a skin
    const pull = 0.9 + 0.1 * Math.pow(Math.random(), 0.6);

    positions[i * 3]     = dx * r * pull;
    positions[i * 3 + 1] = dz * r * pull;   // z becomes up
    positions[i * 3 + 2] = dy * r * pull;
    seeds[i] = Math.random();
    depths[i] = 1 - pull;
  }

  /* centre and scale */
  const geo = new THREE.BufferGeometry();
  const posAttr = new THREE.BufferAttribute(positions, 3);
  geo.setAttribute('position', posAttr);
  geo.computeBoundingBox();
  const box = geo.boundingBox;
  const centre = new THREE.Vector3();
  box.getCenter(centre);

  const size = new THREE.Vector3();
  box.getSize(size);
  const longest = Math.max(size.x, size.y, size.z);
  const norm = 2.35 / longest;

  const normPos = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT; i++) {
    normPos[i * 3]     = (positions[i * 3]     - centre.x) * norm;
    normPos[i * 3 + 1] = (positions[i * 3 + 1] - centre.y) * norm;
    normPos[i * 3 + 2] = (positions[i * 3 + 2] - centre.z) * norm;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(normPos, 3));
  geo.setAttribute('aSeed', new THREE.BufferAttribute(seeds, 1));
  geo.setAttribute('aDepth', new THREE.BufferAttribute(depths, 1));

  /* ---------- renderer ---------- */
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  });
  renderer.setClearAlpha(0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(36, 1, 0.1, 100);
  camera.position.set(0, 0, 6.4);

  const heartGroup = new THREE.Group();
  heartGroup.rotation.set(-0.12, -0.5, 0.05);
  scene.add(heartGroup);

  const uniforms = {
    uTime:   { value: 0 },
    uSize:   { value: 30.0 },
    uDpr:    { value: 1 },
    uBeat:   { value: 0 }
  };

  const vertexShader = `
    attribute float aSeed;
    attribute float aDepth;
    uniform float uTime;
    uniform float uSize;
    uniform float uDpr;
    varying float vSeed;
    varying float vDepth;
    varying float vRim;
    varying vec3 vViewNormal;

    void main() {
      vSeed = aSeed;
      vDepth = aDepth;

      vec3 p = position;
      // a slow shimmer so the cloud breathes even at rest
      p += normalize(p) * sin(uTime * 0.9 + aSeed * 12.6) * 0.008;

      vec4 mv = modelViewMatrix * vec4(p, 1.0);
      vec3 n = normalize(normalMatrix * normalize(position));
      vViewNormal = n;
      vRim = pow(1.0 - abs(dot(n, normalize(-mv.xyz))), 2.2);

      gl_Position = projectionMatrix * mv;
      gl_PointSize = uSize * uDpr * (1.0 / max(0.2, -mv.z));
    }
  `;

  const fragmentShader = `
    varying float vSeed;
    varying float vDepth;
    varying float vRim;

    void main() {
      vec2 c = gl_PointCoord - 0.5;
      float d = length(c);
      if (d > 0.5) discard;

      float core = smoothstep(0.5, 0.24, d);
      float halo = smoothstep(0.5, 0.0, d) * 0.22;

      // deep crimson body, a hotter edge, and a blue rim light
      vec3 deep = vec3(0.26, 0.008, 0.042);
      vec3 mid  = vec3(0.82, 0.035, 0.135);
      vec3 hot  = vec3(1.0, 0.34, 0.40);
      vec3 blue = vec3(0.26, 0.38, 1.0);

      vec3 col = mix(deep, mid, smoothstep(0.1, 0.7, vSeed));
      col = mix(col, hot, smoothstep(0.9, 1.0, vSeed) * 0.7);
      col = mix(col, blue, vRim * 0.30);
      col += vec3(1.0, 0.9, 0.92) * pow(vRim, 5.0) * 0.3;

      // rim-weighted so the silhouette glows and the body stays deep
      float alpha = (core * 0.7 + halo) * (0.55 + 0.45 * vSeed);
      alpha *= mix(1.0, 0.55, vDepth);
      alpha *= 0.5 + 0.8 * vRim;

      gl_FragColor = vec4(col * (0.55 + 1.6 * core), alpha * 1.05);
    }
  `;

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader,
    fragmentShader,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  });

  const points = new THREE.Points(geo, material);
  heartGroup.add(points);

  /* ---------- soft bloom behind the heart ---------- */
  function radialTexture(inner) {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, `rgba(255,80,110,${inner})`);
    g.addColorStop(0.45, 'rgba(226,18,59,0.22)');
    g.addColorStop(1, 'rgba(226,18,59,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  }

  const bloom = new THREE.Sprite(new THREE.SpriteMaterial({
    map: radialTexture(0.72),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    depthTest: false,
    transparent: true,
    opacity: 0.62
  }));
  bloom.scale.set(7.2, 7.2, 1);
  bloom.position.set(0, 0, -1.6);
  scene.add(bloom);

  /* ---------- sizing ---------- */
  let viewW = 1, viewH = 1;
  function resize() {
    const rect = canvas.getBoundingClientRect();
    viewW = Math.max(1, rect.width);
    viewH = Math.max(1, rect.height);
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(viewW, viewH, false);
    uniforms.uDpr.value = dpr;
    camera.aspect = viewW / viewH;
    camera.updateProjectionMatrix();

    // keep the heart in the right half on wide screens, high on phones
    const wide = window.innerWidth > 1024;
    heartGroup.position.x = wide ? 1.45 : 0.62;
    heartGroup.position.y = wide ? 0.12 : -0.45;
    heartGroup.scale.setScalar(wide ? 1 : 0.7);
    uniforms.uSize.value = wide ? 23 : 14;
  }
  resize();
  window.addEventListener('resize', resize);

  /* ---------- pointer + scroll ---------- */
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  window.addEventListener('pointermove', (e) => {
    pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });

  let scrollProgress = 0;
  function readScroll() {
    const rect = hero.getBoundingClientRect();
    const run = Math.max(1, hero.offsetHeight - window.innerHeight);
    scrollProgress = Math.min(1, Math.max(0, -rect.top / run));
  }
  window.addEventListener('scroll', readScroll, { passive: true });
  readScroll();

  /* ---------- loop ---------- */
  const clock = new THREE.Clock();
  let running = true;

  document.addEventListener('visibilitychange', () => {
    running = !document.hidden;
    if (running) clock.start();
  });

  function beatAt(t) {
    // lub-dub: a strong beat and a smaller one a fifth of a cycle later
    const cyc = (t * 1.05) % 1;
    const a = Math.pow(Math.max(0, Math.sin(cyc * Math.PI * 2)), 14);
    const b = 0.45 * Math.pow(Math.max(0, Math.sin((cyc - 0.22) * Math.PI * 2)), 22);
    return a + b;
  }

  function frame() {
    if (!running) return;
    const t = clock.getElapsedTime();

    pointer.x += (pointer.tx - pointer.x) * 0.045;
    pointer.y += (pointer.ty - pointer.y) * 0.045;

    const beat = beatAt(t);
    uniforms.uTime.value = t;
    uniforms.uBeat.value = beat;

    const wide = window.innerWidth > 1024;
    const pull = 1 + beat * 0.022 + scrollProgress * 0.34;
    heartGroup.scale.setScalar(pull * (wide ? 1 : 0.7));

    heartGroup.rotation.y = -0.5 + Math.sin(t * 0.16) * 0.22 + pointer.x * 0.4 + scrollProgress * 0.7;
    heartGroup.rotation.x = -0.12 + pointer.y * 0.18 + Math.cos(t * 0.2) * 0.03;
    heartGroup.rotation.z = 0.05 + Math.sin(t * 0.13) * 0.05;

    bloom.scale.setScalar(7.2 + beat * 0.35 + scrollProgress * 1.6);
    bloom.material.opacity = 0.55 + beat * 0.18;

    // a tiny camera drift keeps the perspective from going flat
    camera.position.x = pointer.x * 0.16;
    camera.position.y = -pointer.y * 0.1;
    camera.lookAt(heartGroup.position.x * 0.35, heartGroup.position.y * 0.2, 0);

    renderer.render(scene, camera);
    if (!reduced) requestAnimationFrame(frame);
  }

  renderer.render(scene, camera);
  if (!reduced) requestAnimationFrame(frame);
  else {
    // one composed frame for reduced-motion users
    heartGroup.scale.setScalar(window.innerWidth > 1024 ? 1 : 0.7);
    renderer.render(scene, camera);
  }
}
