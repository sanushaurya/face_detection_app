let VIDEO = document.getElementById("video");
let STATUS = document.getElementById("status");
let SIMDIV = document.getElementById("similarity");

let embeddings = {};
const THRESHOLD = 0.1;
let lastResults = null;

// Load embeddings for person1 and person2
async function loadEmbeddings() {
  const persons = ["person1", "person2"];

  for (let p of persons) {
    try {
      const res = await fetch(`embeddings/${p}_embedding.json`);
      const data = await res.json();
      embeddings[p] = new Float32Array(data.embedding);
      console.log(`Loaded embedding for ${p}`);
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

// Enhanced embedding extractor (same improved method)
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
    leftEye: 33,
    rightEye: 263,
    nose: 1,
    chin: 152,
    leftMouth: 61,
    rightMouth: 291
  };

  let derived = [
    dist(KP.leftEye, KP.rightEye),
    dist(KP.leftEye, KP.nose),
    dist(KP.rightEye, KP.nose),
    dist(KP.nose, KP.chin),
    dist(KP.leftMouth, KP.rightMouth),
    dist(KP.leftEye, KP.chin),
    dist(KP.rightEye, KP.chin)
  ];

  let raw = new Float32Array(arr);
  let der = new Float32Array(derived);

  raw = raw.map(v => v / (Math.sqrt(raw.reduce((a,b)=>a+b*b,0)) || 1));
  der = der.map(v => v / (Math.sqrt(der.reduce((a,b)=>a+b*b,0)) || 1));

  let final = new Float32Array(raw.length + der.length);
  final.set(raw);
  final.set(der, raw.length);
  return final;
}

// Start camera + face mesh
async function startCamera() {
  let faceMesh = new FaceMesh({
    locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
  });

  faceMesh.setOptions({
    refineLandmarks: true,
    maxNumFaces: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
  });

  faceMesh.onResults(res => lastResults = res);

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

// VERIFY BUTTON
document.getElementById("verifyBtn").onclick = async () => {
  if (!Object.keys(embeddings).length) {
    STATUS.innerText = "No trained embeddings loaded!";
    return;
  }

  STATUS.innerText = "Verifying...";
  SIMDIV.innerText = "";
  let sims = [];

  for (let i = 0; i < 7; i++)
 {
    await new Promise(r => setTimeout(r, 150));
    if (!lastResults || !lastResults.multiFaceLandmarks) continue;
    let emb = extractEmbedding(lastResults.multiFaceLandmarks[0]);
    sims.push(emb);
  }

  if (!sims.length) {
    STATUS.innerText = "No face detected!";
    return;
  }

  // Average the 10 frame embeddings
  let avgEmb = sims.reduce((acc, cur) => {
    for (let i = 0; i < acc.length; i++) acc[i] += cur[i];
    return acc;
  }, new Float32Array(sims[0].length));
  for (let i = 0; i < avgEmb.length; i++) avgEmb[i] /= sims.length;

  let bestPerson = "unknown";
  let bestSim = -1;

  for (let p in embeddings) {
    let sim = cosine(avgEmb, embeddings[p]);
    if (sim > bestSim) {
      bestSim = sim;
      bestPerson = p;
    }
  }

  SIMDIV.innerText = `Best Similarity: ${bestSim.toFixed(4)}`;

  if (bestSim >= THRESHOLD) {
    STATUS.innerText = `${bestPerson.toUpperCase()} ✔`;
    STATUS.style.color = "green";
  } else {
    STATUS.innerText = "UNKNOWN ✖";
    STATUS.style.color = "red";
  }
};
