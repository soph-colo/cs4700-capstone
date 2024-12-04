// Basic Three.js setup
let scene, camera, renderer, cube;
let action = null;
let actionStart = null;
const CUBE_SIZE = 2.1;  // Cube size
const IMAGE_DURATION = 5000; // 5 seconds in milliseconds


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

  // Create each face of the cube 
  const faces = [
    createCubeFace('#EEEEEE', '#ff8080'), // Face 1: Light gray background, red circle (back right face, will be hidden)
    createCubeFace('#969696', '#4B7F80'), // Face 2: Darker gray background, teal circle (left face)
    createCubeFace('#FFFFFF', '#ADEAFC'), // Face 3: White background, light blue circle (top face)
    createCubeFace('#FFFFFF', '#ffb380'), // Face 4: White background, orange circle (botten face, will be hidden)
    createCubeFace('#EEEEEE', '#BBA5E8'), // Face 5: Light gray background, purple circle (right face)
    createCubeFace('#969696', '#958D48')  // Face 6: Darker gray, yellow circle (back left face, will be hidden)
  ];

  // Apply the configurations to each face of the cube
  cube = new THREE.Mesh(geometry, faces);
  scene.add(cube);

  // Rotate cube to show three faces, centered on an edge
  cube.rotation.x = 0.5;
  cube.rotation.y = Math.PI / 4;  // Rotated 45 degrees to show an edge

  animate();
}

// Function to create a face with a colored circle on a colored background
function createCubeFace(bgColor, circleColor) {
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

// Show the image based on the action and alignment
function showImage(imageSrc, alignment = "center") {
  const imageContainer = document.getElementById("image-container");
  const actionImage = document.getElementById("action-image");
  
  // Set the source of the image based on the passed parameter
  actionImage.src = imageSrc;

  // Remove all alignment classes first
  imageContainer.classList.remove("left", "right", "center");
  imageContainer.classList.add(alignment); // Add the appropriate alignment class
  imageContainer.style.display = "block"; // Show the image immediately
}

  // Hide the image when the action is neutral
function hideImage() {
  const imageContainer = document.getElementById("image-container");
  imageContainer.style.display = "none"; // Hide the image
}

// Animate function, called every frame
function animate() {
  requestAnimationFrame(animate);
  updateCube();
  renderer.render(scene, camera);
}

function updateCube() {
  if (action === "push" || action === "pull" || action === "left" || action === "right") {
    let elapsedTime = (Date.now() - actionStart) / 1000;
    if (elapsedTime >= 5) {
      action = "neutral";  // Transition to neutral after 5 seconds
      elapsedTime = 5;     // Cap the elapsed time to 5 seconds
      hideImage();         // Hide the image after 5 seconds
    }

    if (action === "push") {
      cube.position.z = -elapsedTime / 2;  // Move the cube back
      cube.scale.setScalar(1 - elapsedTime / 10); // Scale down
    } else if (action === "pull") {
      cube.position.z = elapsedTime / 2;  // Move the cube forward
      cube.scale.setScalar(1 + elapsedTime / 10); // Scale up
    } else if (action === "left") {
      cube.position.x = -elapsedTime / 2;  // Move the cube left
    } else if (action === "right") {
      cube.position.x = elapsedTime / 2;  // Move the cube right
    }
  } else if (action === "neutral") {
    cube.position.set(0, 0, 0); // Reset cube position
    cube.scale.set(1, 1, 1); // Reset cube scale
    hideImage(); // Hide the image when action is neutral
  }
}

// Button Event Handlers
function pushCube() {
  startAction("push");
  //showImage("./images/push.jpg", "center"); // Show the push image centered
}

function pullCube() {
  startAction("pull");
  //showImage("./images/pull.jpg", "center"); // Show the pull image centered
}

function leftCube() {
  startAction("left");
  //showImage("./images/left.jpg", "left"); // Show the left image on the left side
}

function rightCube() {
  startAction("right");
  //showImage("./images/right.jpg", "right"); // Show the right image on the right side
}

function neutralCube() {
  startAction("neutral");
  hideImage(); // Hide image immediately when neutral is pressed
}

function startAction(newAction) {
  // Reset cube to the neutral position and scale and hides any existing image whenever a new action starts
  hideImage(); // This allows images to be used for some commands but not all
    
  cube.position.set(0, 0, 0);
  cube.scale.set(1, 1, 1);
  
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
