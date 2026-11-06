/* ============================================================
   Heartware — hero assembly
   A chestpiece modelled in three.js. The insert shows itself
   as the page scrolls: the back plate comes away, the board
   lifts out, and the two ports separate.
   ============================================================ */

import * as THREE from 'three';
import { RoomEnvironment } from '../vendor/RoomEnvironment.js';

const canvas = document.getElementById('hero-canvas');
const hero = document.getElementById('top');
if (canvas && hero) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = window.matchMedia('(max-width: 700px)').matches;

  // the scene is cheap enough for phones, but it is scaled back there:
  // fewer pixels, smaller assembly, no pointer parallax
  start(canvas, hero, reduced, small);
}

function start(canvas, hero, reduced, small) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !small, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(small ? 1.4 : 1.75, window.devicePixelRatio || 1));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  camera.position.set(0.2, 0.25, 7.0);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.05).texture;

  const key = new THREE.DirectionalLight(0xfff4e6, 3.1);
  key.position.set(3.5, 4.5, 6);
  scene.add(key);

  const rim = new THREE.PointLight(0x35c9ff, 26, 14, 2);
  rim.position.set(-4.2, -1.4, -3.2);
  scene.add(rim);

  const fill = new THREE.PointLight(0x8fd4ff, 9, 12, 2);
  fill.position.set(0.5, -3.4, 3.2);
  scene.add(fill);

  scene.add(new THREE.AmbientLight(0x0a1520, 1.2));

  /* ---------- glow behind the instrument ---------- */
  const glowTex = (() => {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    g.addColorStop(0, 'rgba(53,201,255,.55)');
    g.addColorStop(0.45, 'rgba(53,201,255,.14)');
    g.addColorStop(1, 'rgba(53,201,255,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
  })();
  const glow = new THREE.Mesh(
    new THREE.PlaneGeometry(7.5, 7.5),
    new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })
  );
  glow.position.z = -3.2;
  scene.add(glow);

  /* ---------- materials ---------- */
  const metal = new THREE.MeshStandardMaterial({ color: 0xc8d3da, metalness: 0.95, roughness: 0.24, envMapIntensity: 1.25 });
  const darkMetal = new THREE.MeshStandardMaterial({ color: 0x2a333b, metalness: 0.85, roughness: 0.4 });
  const polymer = new THREE.MeshStandardMaterial({ color: 0x10171d, metalness: 0.15, roughness: 0.62 });
  const pearl = new THREE.MeshPhysicalMaterial({
    color: 0xeef4f8, metalness: 0.05, roughness: 0.18,
    clearcoat: 1, clearcoatRoughness: 0.12, envMapIntensity: 1.1
  });
  const accent = new THREE.MeshStandardMaterial({
    color: 0x35c9ff, metalness: 0.4, roughness: 0.3, emissive: 0x0b5f7a, emissiveIntensity: 0.9
  });
  const redTube = new THREE.MeshStandardMaterial({ color: 0x9e2b33, metalness: 0.1, roughness: 0.55 });
  const boardMat = new THREE.MeshStandardMaterial({ color: 0x0f3a2c, metalness: 0.2, roughness: 0.72 });

  /* ---------- assembly ---------- */
  const group = new THREE.Group();
  scene.add(group);

  const R = 1.18;

  // shell
  const shell = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.98, R * 0.95, 0.46, 96), polymer);
  shell.rotation.x = Math.PI / 2;
  group.add(shell);

  // rim
  const ring = new THREE.Mesh(new THREE.TorusGeometry(R, 0.055, 24, 120), metal);
  ring.position.z = 0.24;
  group.add(ring);

  // diaphragm
  const diaphragm = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.94, R * 0.94, 0.03, 96), pearl);
  diaphragm.rotation.x = Math.PI / 2;
  diaphragm.position.z = 0.23;
  group.add(diaphragm);

  // concentric machined grooves on the face
  for (let i = 1; i <= 3; i++) {
    const groove = new THREE.Mesh(
      new THREE.TorusGeometry(R * 0.32 * i, 0.008, 8, 96),
      new THREE.MeshStandardMaterial({ color: 0x6f8090, metalness: 0.9, roughness: 0.4 })
    );
    groove.position.z = 0.252;
    group.add(groove);
  }

  // back plate (lifts away on scroll)
  const back = new THREE.Group();
  const backPlate = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.83, R * 0.83, 0.07, 72), metal);
  backPlate.rotation.x = Math.PI / 2;
  back.add(backPlate);
  const backLip = new THREE.Mesh(new THREE.TorusGeometry(R * 0.83, 0.028, 16, 96), darkMetal);
  backLip.position.z = 0.035;
  back.add(backLip);
  back.position.z = -0.26;
  group.add(back);

  // insert board
  const insert = new THREE.Group();
  const pcb = new THREE.Mesh(new THREE.BoxGeometry(1.34, 1.34, 0.06), boardMat);
  insert.add(pcb);
  // copper tracks suggestion
  const track = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.035), new THREE.MeshStandardMaterial({ color: 0xb98a3c, metalness: 1, roughness: 0.35 }));
  track.position.set(0, 0.3, 0.033);
  insert.add(track);
  const track2 = track.clone();
  track2.position.set(0, 0.18, 0.033);
  track2.scale.set(0.72, 1, 1);
  insert.add(track2);

  // mic ports
  const portGeo = new THREE.CylinderGeometry(0.085, 0.085, 0.09, 24);
  const portA = new THREE.Mesh(portGeo, accent);
  portA.rotation.x = Math.PI / 2;
  portA.position.set(-0.33, -0.3, 0.06);
  const portB = new THREE.Mesh(portGeo, darkMetal);
  portB.rotation.x = Math.PI / 2;
  portB.position.set(0.36, -0.3, 0.06);
  insert.add(portA, portB);

  // cell
  const cell = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.9, 0.05), new THREE.MeshStandardMaterial({ color: 0x2b3238, metalness: 0.6, roughness: 0.5 }));
  cell.position.set(0.62, 0.1, 0.02);
  insert.add(cell);

  insert.position.z = -0.12;
  group.add(insert);

  // stem + tubing
  const stem = new THREE.Group();
  const stemBody = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.2, 0.44, 40), metal);
  stemBody.position.set(0, -0.5, 0);
  stem.add(stemBody);
  const stemCollar = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.035, 16, 64), darkMetal);
  stemCollar.rotation.x = Math.PI / 2;
  stemCollar.position.y = -0.28;
  stem.add(stemCollar);
  stem.position.set(0.62, -1.12, 0.02);
  stem.rotation.z = -0.55;
  group.add(stem);

  // two tubes leaving the frame
  const tubeCurves = [
    new THREE.CatmullRomCurve3([
      new THREE.Vector3(0.9, -1.4, 0.02),
      new THREE.Vector3(1.18, -1.95, 0.18),
      new THREE.Vector3(1.42, -2.35, 0.4)
    ]),
    new THREE.CatmullRomCurve3([
      new THREE.Vector3(0.82, -1.42, -0.06),
      new THREE.Vector3(1.02, -2.0, -0.24),
      new THREE.Vector3(1.18, -2.42, -0.5)
    ])
  ];
  tubeCurves.forEach(curve => {
    const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, 0.08, 14, false), redTube);
    tube.visible = !small;
    group.add(tube);
  });

  // a lit ring inside the rim, the only cyan on the object itself
  const litRing = new THREE.Mesh(
    new THREE.TorusGeometry(R * 0.985, 0.011, 8, 120),
    new THREE.MeshStandardMaterial({ color: 0x35c9ff, emissive: 0x1d8fb8, emissiveIntensity: 1.6, metalness: 0.4, roughness: 0.3 })
  );
  litRing.position.z = 0.243;
  group.add(litRing);

  // base orientation: a three-quarter view, tilted so the face catches light
  const baseRotY = small ? -0.62 : -0.86;
  const baseRotX = small ? 0.42 : 0.52;
  const baseX = small ? 0.75 : 2.5;
  const baseY = small ? 1.5 : 0.1;
  const baseScale = small ? 0.52 : 0.8;
  group.scale.setScalar(baseScale);
  group.rotation.set(baseRotX, baseRotY, 0.06);
  group.position.set(baseX, baseY, 0);

  /* ---------- dust ---------- */
  const dustCount = 220;
  const dustGeo = new THREE.BufferGeometry();
  const positions = new Float32Array(dustCount * 3);
  for (let i = 0; i < dustCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 12;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 8;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 6 - 1.5;
  }
  dustGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({
    color: 0x7fd8ff, size: 0.018, transparent: true, opacity: 0.5, sizeAttenuation: true, depthWrite: false
  }));
  scene.add(dust);

  /* ---------- sizing ---------- */
  function resize() {
    const w = canvas.clientWidth || hero.clientWidth;
    const h = canvas.clientHeight || hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);

  /* ---------- pointer parallax ---------- */
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  window.addEventListener('pointermove', e => {
    pointer.tx = (e.clientX / window.innerWidth - 0.5) * 2;
    pointer.ty = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  /* ---------- scroll progress ---------- */
  let scrollP = 0;
  function readScroll() {
    const rect = hero.getBoundingClientRect();
    const span = window.innerHeight * 0.85;
    scrollP = Math.max(0, Math.min(1, -rect.top / span));
  }
  window.addEventListener('scroll', readScroll, { passive: true });
  readScroll();

  /* ---------- loop ---------- */
  let visible = true;
  const io = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
  }, { threshold: 0.01 });
  io.observe(hero);

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) clock.start();
  });

  const clock = new THREE.Clock();
  let frame = 0;

  function render() {
    frame = requestAnimationFrame(render);
    if (!visible || document.hidden) return;

    const t = clock.getElapsedTime();
    const p = scrollP;

    pointer.x += (pointer.tx - pointer.x) * 0.045;
    pointer.y += (pointer.ty - pointer.y) * 0.045;

    if (!reduced) {
      group.rotation.y = baseRotY + pointer.x * 0.1 + Math.sin(t * 0.22) * 0.05 + p * 0.5;
      group.rotation.x = baseRotX + pointer.y * 0.07 + Math.sin(t * 0.17) * 0.02 - p * 0.14;
      group.position.y = baseY + Math.sin(t * 0.5) * 0.02 - p * 0.16;
      group.position.x = baseX + pointer.x * 0.06;
    }

    // the assembly opens as the hero leaves
    const e = p * p * (3 - 2 * p);
    back.position.z = -0.26 - e * 1.35;
    back.position.y = e * 0.06;
    back.rotation.x = e * 0.18;
    insert.position.z = -0.12 + e * 0.72;
    insert.rotation.z = e * 0.1;
    portA.position.z = 0.06 + e * 0.34;
    portB.position.z = 0.06 + e * 0.34;
    cell.position.z = 0.02 + e * 0.22;

    glow.material.opacity = 0.72 + Math.sin(t * 1.1) * 0.06;

    dust.rotation.y = t * 0.02;
    dust.position.y = Math.sin(t * 0.24) * 0.12;

    camera.position.x = 0.2 + pointer.x * 0.22;
    camera.position.y = 0.25 - pointer.y * 0.16;
    camera.lookAt(small ? 0.45 : 1.35, small ? 0.15 : -0.05, 0);

    renderer.render(scene, camera);
  }
  render();
}
