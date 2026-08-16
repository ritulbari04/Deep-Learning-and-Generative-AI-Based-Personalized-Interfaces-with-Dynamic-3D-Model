console.log("JS Loaded");
import * as THREE from 'three';
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

// Scene setup
const scene = new THREE.Scene();

// Renderer setup
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0xffffff);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

// Camera setup
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
camera.position.set(0, 1.5, -3);
camera.lookAt(0, 1.5, 0);

// Ground
const groundGeometry = new THREE.PlaneGeometry(20, 20, 32, 32);
groundGeometry.rotateX(-Math.PI / 2);
const groundMaterial = new THREE.MeshStandardMaterial({ color: 0x555555, side: THREE.DoubleSide });
const groundMesh = new THREE.Mesh(groundGeometry, groundMaterial);
groundMesh.receiveShadow = true;
scene.add(groundMesh);

// Lights
const spotlight = new THREE.SpotLight(0xffffff, 3, 100, Math.PI / 6, 0.5);
spotlight.position.set(0, 2.5, 5);
spotlight.target.position.set(0, 1.5, 0);
spotlight.castShadow = true;
scene.add(spotlight);
scene.add(spotlight.target);

const ambientLight = new THREE.AmbientLight(0xffffff, 5);
scene.add(ambientLight);

// Animation mixer and jaw reference
let mixer, jawBone = null, jawMorph = null;
let allowAnimation = false;

// Audio setup
const listener = new THREE.AudioListener();
camera.add(listener);
const sound = new THREE.Audio(listener);
const audioLoader = new THREE.AudioLoader();
let analyser;

// Load GLB model
const loader = new GLTFLoader();
loader.load("untitled2.glb", (gltf) => {
  const model = gltf.scene;
  model.position.set(0, -1, 0);
  model.scale.set(2, 2, 2);
  model.rotation.y = Math.PI;

  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;

      if (child.morphTargetDictionary && child.morphTargetInfluences) {
        if ("MouthOpen" in child.morphTargetDictionary) {
          console.log("Found morph target: MouthOpen");
          jawMorph = {
            influences: child.morphTargetInfluences,
            index: child.morphTargetDictionary["MouthOpen"]
          };
        }
      }
    }

    if (child.isBone && child.name.toLowerCase().includes("jaw")) {
      console.log("Found jaw bone:", child.name);
      jawBone = child;
    }

    if (child.name.toLowerCase().includes("head")) {
      console.log("Fixing head rotation for:", child.name);
      child.rotation.y = Math.PI;
    }
  });

  scene.add(model);

  if (gltf.animations && gltf.animations.length) {
    mixer = new THREE.AnimationMixer(model);
    gltf.animations.forEach((clip) => {
      mixer.clipAction(clip).play();
    });
  }
});

// Animation loop
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();

  if (sound.isPlaying && allowAnimation) {
    if (mixer) mixer.update(delta);

    if (analyser) {
      const volume = analyser.getAverageFrequency() / 256;

      if (jawMorph) {
        jawMorph.influences[jawMorph.index] = volume;
      }

      if (jawBone) {
        jawBone.rotation.x = -volume * 0.5;
      }
    }
  } else {
    if (jawMorph) jawMorph.influences[jawMorph.index] = 0;
    if (jawBone) jawBone.rotation.x = 0;
  }

  renderer.render(scene, camera);
}
animate();

// Button interaction
// Button interaction
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById("submitQuery").addEventListener("click", async function(event) {
    event.preventDefault();

    const query = document.getElementById("userQuery").value.trim();

    try {
      const response = await fetch(`http://127.0.0.1:5000/ask/${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      console.log("Response:", data);

      // Display the response in the response box
      const responseTextElement = document.getElementById("responseText");
      responseTextElement.textContent = data["response"] || "No answer received";

      // Load and play the audio response
      audioLoader.load(`http://127.0.0.1:5000/audio`, function(buffer) {
        sound.setBuffer(buffer);
        sound.setLoop(false);
        sound.setVolume(1.0);
        sound.play();

        allowAnimation = true;
        analyser = new THREE.AudioAnalyser(sound, 32);
      });

    } catch (error) {
      console.error('Fetch error:', error);
    }
  });
});



// document.getElementById("submitQuery").addEventListener("click", () => {
//   const query = document.getElementById("userQuery").value;
//   if (query.trim() && audioReady) {
//     console.log("User query:", query);
//     allowAnimation = true;
//     sound.play();
//   }
// });
