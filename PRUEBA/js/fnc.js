let scene, camera, renderer;

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);

  document.body.appendChild(renderer.domElement);

  let textureLoader = new THREE.TextureLoader();

  let texture1 = textureLoader.load('imgs/a1.png');
  let texture2 = textureLoader.load('imgs/a3.png');

  let material1 = new THREE.MeshBasicMaterial({ map: texture1, transparent: true });
  let material2 = new THREE.MeshBasicMaterial({ map: texture2, transparent: true });

  let plane1 = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), material1);
  plane1.position.x = -1.42; // Ajusta la posición horizontal de la primera imagen
  plane1.position.y = 0.01; // Ajusta la posición vertical de la primera imagen
  plane1.scale.set(2, 2, 1); // Ajusta la escala para que cubra más espacio

  let plane2 = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), material2);
  plane2.position.x = 0.5;
  plane2.scale.set(2, 2, 1);

  scene.add(plane1);
  scene.add(plane2);

  animate();
}

function animate() {
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

init();
