// Basic Three.js setup
let scene, camera, renderer, cube;
let action = null;
let actionStart = null;
const CUBE_SIZE = 2.1;  // Cube size

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 6;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.getElementById("container").appendChild(renderer.domElement);

  // Set the renderer's background color to light gray
  renderer.setClearColor(0x494949, 1);

  document.getElementById("container").appendChild(renderer.domElement);
  
  // Create a box geometry for the cube
  const geometry = new THREE.BoxGeometry(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE);

  // Create materials for each face with slight variations in base color
  const materials = [
    createCircleMaterial('#EEEEEE', '#ff8080'), // Face 1: Light gray background, red circle (back right face, will be hidden)
    createCircleMaterial('#969696', '#4B7F80'), // Face 2: Darker gray background, teal circle (left face)
    createCircleMaterial('#FFFFFF', '#ADEAFC'), // Face 3: White background, light blue circle (top face)
    createCircleMaterial('#FFFFFF', '#ffb380'), // Face 4: White background, orange circle (botten face, will be hidden)
    createCircleMaterial('#EEEEEE', '#BBA5E8'), // Face 5: Light gray background, purple circle (right face)
    createCircleMaterial('#969696', '#958D48')  // Face 6: Darker gray, yellow circle (back left face, will be hidden)
  ];

  // Apply the materials to each face of the cube
  cube = new THREE.Mesh(geometry, materials);
  scene.add(cube);

  // Rotate cube to show three faces, centered on an edge
  cube.rotation.x = 0.5;
  cube.rotation.y = Math.PI / 4;  // Rotated 45 degrees to show an edge

  animate();
}

// Function to create a material with a colored circle on a colored background
function createCircleMaterial(bgColor, circleColor) {
  const canvas = document.createElement('canvas');
  canvas.width = 256;
  canvas.height = 256;
  const context = canvas.getContext('2d');

  // Draw background color
  context.fillStyle = bgColor;
  context.fillRect(0, 0, 256, 256);

  // Draw circle in the center
  context.fillStyle = circleColor;
  context.beginPath();
  context.arc(128, 128, 80, 0, Math.PI * 2);
  context.fill();

  const texture = new THREE.CanvasTexture(canvas);
  return new THREE.MeshBasicMaterial({ map: texture });
}

// Animate function, called every frame
function animate() {
  requestAnimationFrame(animate);
  updateCube();
  renderer.render(scene, camera);
}

// Handles the cube's movement based on action
function updateCube() {
  if (action === "push" || action === "pull") {
    let elapsedTime = (Date.now() - actionStart) / 1000;
    if (elapsedTime >= 5) {
      action = "neutral";
      elapsedTime = 5;
    }

    if (action === "push") {
      cube.position.z = -elapsedTime / 2;
      cube.scale.setScalar(1 - elapsedTime / 10);
    } else if (action === "pull") {
      cube.position.z = elapsedTime / 2;
      cube.scale.setScalar(1 + elapsedTime / 10);
    }
  } else if (action === "neutral") {
    cube.position.set(0, 0, 0);
    cube.scale.set(1, 1, 1);
  }
}

// Button Event Handlers
function pushCube() {
  startAction("push");
}

function pullCube() {
  startAction("pull");
}

function neutralCube() {
  startAction("neutral");
}

function startAction(newAction) {
  action = newAction;
  actionStart = Date.now();
}

// Adjust on window resize
window.addEventListener("resize", () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

init();
