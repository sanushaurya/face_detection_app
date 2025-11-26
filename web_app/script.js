let VIDEO = document.getElementById("video");
let CANVAS = document.getElementById("output_canvas");
let CTX = CANVAS.getContext("2d");

let embeddings = {};
const THRESHOLD = 0.1; // Threshold for similarity

// State for tracking multiple faces
// We will store the last identified name for each face index to avoid flickering
// However, face index order isn't guaranteed in MediaPipe, so we'll just re-verify every few frames.
let lastVerificationTime = 0;
const VERIFY_INTERVAL = 200; // Verify every 200ms
let faceLabels = []; // Stores { box: [x,y,w,h], label: "Name", color: "green" }

// Resize canvas to full screen
function resizeCanvas() {
  CANVAS.width = window.innerWidth;
  CANVAS.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Load embeddings
async function loadEmbeddings() {
  const persons = ["Aditya", "person2"]; // Add more names here as needed

  for (let p of persons) {
    try {
      const res = await fetch(`embeddings/${p}_embedding.json`);
      if (res.ok) {
        const data = await res.json();
        embeddings[p] = new Float32Array(data.embedding);
        console.log(`Loaded embedding for ${p}`);
      }
    } catch (e) {
      console.warn(`Could not load ${p} embedding`);
    }
  }
}
loadEmbeddings();

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

function extractEmbedding(landmarks) {
  let arr = [];
  for (let lm of landmarks) arr.push(lm.x, lm.y, lm.z);

  function dist(a, b) {
    return Math.hypot(
      landmarks[a].x - landmarks[b].x,
      landmarks[a].y - landmarks[b].y,
      landmarks[a].z - landmarks[b].z
    );
  }

  const KP = {
    leftEye: 33, rightEye: 263, nose: 1, chin: 152,
    leftMouth: 61, rightMouth: 291
  };

  let derived = [
    dist(KP.leftEye, KP.rightEye), dist(KP.leftEye, KP.nose),
    dist(KP.rightEye, KP.nose), dist(KP.nose, KP.chin),
    dist(KP.leftMouth, KP.rightMouth), dist(KP.leftEye, KP.chin),
    dist(KP.rightEye, KP.chin)
  ];

  let raw = new Float32Array(arr);
  let der = new Float32Array(derived);

  raw = raw.map(v => v / (Math.sqrt(raw.reduce((a, b) => a + b * b, 0)) || 1));
  der = der.map(v => v / (Math.sqrt(der.reduce((a, b) => a + b * b, 0)) || 1));

  let final = new Float32Array(raw.length + der.length);
  final.set(raw);
  final.set(der, raw.length);
  return final;
}

function identifyFace(landmarks) {
  if (!Object.keys(embeddings).length) return { name: "Loading...", color: "yellow" };

  const emb = extractEmbedding(landmarks);
  let bestPerson = "unknown";
  let bestSim = -1;

  for (let p in embeddings) {
    let sim = cosine(emb, embeddings[p]);
    if (sim > bestSim) {
      bestSim = sim;
      bestPerson = p;
    }
  }

  if (bestSim >= THRESHOLD) {
    return { name: bestPerson.toUpperCase(), color: "#00FF00" }; // Green
  } else {
    return { name: "Unknown", color: "#FF0000" }; // Red
  }
}

function drawResults(results) {
  CTX.clearRect(0, 0, CANVAS.width, CANVAS.height);

  if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
    return;
  }

  const now = Date.now();
  const shouldVerify = (now - lastVerificationTime > VERIFY_INTERVAL);
  if (shouldVerify) {
    lastVerificationTime = now;
    faceLabels = []; // Reset labels for this frame
  }

  // Loop through all detected faces
  results.multiFaceLandmarks.forEach((landmarks, index) => {
    // Calculate bounding box
    let minX = 1, minY = 1, maxX = 0, maxY = 0;
    for (let lm of landmarks) {
      if (lm.x < minX) minX = lm.x;
      if (lm.x > maxX) maxX = lm.x;
      if (lm.y < minY) minY = lm.y;
      if (lm.y > maxY) maxY = lm.y;
    }

    const x = minX * CANVAS.width;
    const y = minY * CANVAS.height;
    const w = (maxX - minX) * CANVAS.width;
    const h = (maxY - minY) * CANVAS.height;

    // Identify Face (only if we are verifying this frame, OR use cached label if available)
    // Since face index order can change, we'll just re-verify every interval.
    // For smoother UI, if we are NOT verifying, we might want to skip drawing or just draw box.
    // But to keep it simple and responsive:

    let labelData;
    if (shouldVerify) {
      labelData = identifyFace(landmarks);
      faceLabels.push(labelData); // Cache it (simple cache, assumes order stays same for 200ms)
    } else {
      // Use cached label if exists, else default
      labelData = faceLabels[index] || { name: "...", color: "gray" };
    }

    // Draw Box
    CTX.strokeStyle = labelData.color;
    CTX.lineWidth = 4;
    CTX.strokeRect(x, y, w, h);

    // Draw Text Background
    const text = labelData.name;
    CTX.font = "bold 24px Arial";
    const textWidth = CTX.measureText(text).width;

    CTX.fillStyle = labelData.color;
    CTX.fillRect(x, y - 30, textWidth + 20, 30);

    // Draw Text
    CTX.fillStyle = "black";
    CTX.fillText(text, x + 10, y - 7);
  });
}

// Start camera + face mesh
async function startCamera() {
  let faceMesh = new FaceMesh({
    locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
  });

  faceMesh.setOptions({
    refineLandmarks: true,
    maxNumFaces: 4, // Allow multiple faces
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
  });

  faceMesh.onResults(drawResults);

  let stream = await navigator.mediaDevices.getUserMedia({ video: true });
  VIDEO.srcObject = stream;
  await VIDEO.play();

  const camera = new Camera(VIDEO, {
    onFrame: async () => {
      await faceMesh.send({ image: VIDEO });
    },
    width: 640,
    height: 480
  });

  camera.start();
}

startCamera();

// SAVE BUTTON (Only on Register Page)
const saveBtn = document.getElementById("saveBtn");
if (saveBtn) {
  saveBtn.onclick = async () => {
    const nameInput = document.getElementById("personName");
    const name = nameInput.value.trim();

    if (!name) {
      alert("Please enter a name first!");
      return;
    }

    // We need to access the last results from the camera loop
    // Since we removed 'lastResults' global, we need to capture it or just warn user
    // Ideally, we should capture the latest landmarks in drawResults if we are in registration mode.
    // For simplicity, let's just alert if no face is visible on screen (which we can't easily check without global state).
    // Let's add a global 'latestLandmarks' just for registration.

    alert("Please ensure your face is visible and wait for the green box.");
    // Note: The original save logic relied on 'lastResults'. 
    // We need to restore a way to get the current face for registration.
  };
}

// Restore global variable for registration usage
let latestLandmarksForSave = null;
const originalDrawResults = drawResults;
drawResults = (results) => {
  if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
    latestLandmarksForSave = results.multiFaceLandmarks[0];
  } else {
    latestLandmarksForSave = null;
  }
  originalDrawResults(results);
};

if (saveBtn) {
  saveBtn.onclick = async () => {
    const nameInput = document.getElementById("personName");
    const name = nameInput.value.trim();

    if (!name) {
      alert("Please enter a name first!");
      return;
    }

    if (!latestLandmarksForSave) {
      alert("No face detected! Please look at the camera.");
      return;
    }

    const emb = extractEmbedding(latestLandmarksForSave);
    const embArray = Array.from(emb);

    const data = {
      name: name,
      embedding: embArray
    };

    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${name}_embedding.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    alert(`Saved ${name}_embedding.json! \n\nPlease move this file to the 'web_app/embeddings/' folder.`);
  };
}
