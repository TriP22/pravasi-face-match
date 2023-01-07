import "./App.css";
import { React, useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
// import * as faceapi from "face-api.js";

import { CameraOptions, useFaceDetection } from "react-use-face-detection";
import FaceDetection from "@mediapipe/face_detection";
import { Camera } from "@mediapipe/camera_utils";

import axios from "axios";

import AiAnimation from "./assets/ai_animation.gif";
import Sound from "./assets/sound.mp3";
import * as Faces from "./assets/faces/faces";

const Data = [
  {
    id: 1,
    name: "Capt. Laxmi Sehgal",
    code: "Capt-Laxmi-Sehgal",
    image: Faces.CaptLaxmiSehgal,
  },
  {
    id: 2,
    name: "Dadabhai Naoroji",
    code: "Dadabhai-Naoroji",
    image: Faces.DadabhaiNaoroji,
  },
  {
    id: 3,
    name: "Kartar Singh Sarabha",
    code: "Kartar-Singh-Sarabha",
    image: Faces.KartarSinghSarabha,
  },
  {
    id: 4,
    name: "Lala Hardayal",
    code: "Lala-Hardayal",
    image: Faces.LalaHardayal,
  },
  {
    id: 5,
    name: "Lala Lajpat Rai",
    code: "Lala-Lajpat-Rai",
    image: Faces.LalaLajpatRai,
  },
  {
    id: 6,
    name: "Madam Cama",
    code: "Madam-Cama",
    image: Faces.MadamCama,
  },
  {
    id: 7,
    name: "Madan Lal Dhingra",
    code: "Madan-Lal-Dhingra",
    image: Faces.MadanLalDhingra,
  },
  {
    id: 8,
    name: "Mahatma Gandhi",
    code: "Mahatma-Gandhi",
    image: Faces.MahatmaGandhi,
  },
  {
    id: 9,
    name: "Netaji Subhas",
    code: "Netaji-Subhas",
    image: Faces.NetajiSubhas,
  },
  {
    id: 10,
    name: "Pandurang Bapat",
    code: "Pandurang-Bapat",
    image: Faces.PandurangBapat,
  },
  {
    id: 11,
    name: "Raja Mahendra Pratap",
    code: "Raja-Mahendra-Pratap",
    image: Faces.RajaMahendraPratap,
  },
  {
    id: 12,
    name: "Rash Behari Bose",
    code: "Rash-Behari-Bose",
    image: Faces.RashBehariBose,
  },
  {
    id: 13,
    name: "Sardarsinghji Rana",
    code: "Sardarsinghji-Rana",
    image: Faces.SardarsinghjiRana,
  },
  {
    id: 14,
    name: "Shyamji Krishnavarma",
    code: "Shyamji-Krishnavarma",
    image: Faces.ShyamjiKrishnavarma,
  },
  {
    id: 15,
    name: "Sister Nivedita",
    code: "Sister-Nivedita",
    image: Faces.SisterNivedita,
  },
  {
    id: 16,
    name: "Swami Vivekanand",
    code: "Swami-Vivekanand",
    image: Faces.SwamiVivekanand,
  },
  {
    id: 17,
    name: "Udham Singh",
    code: "Udham-Singh",
    image: Faces.UdhamSingh,
  },
  {
    id: 18,
    name: "VVS Iyer",
    code: "VVS-Iyer",
    image: Faces.VVSIyer,
  },
  {
    id: 19,
    name: "Vinayak Damodar Savarkar",
    code: "Vinayak-Damodar-Savarkar",
    image: Faces.VinayakDamodarSavarkar,
  },
  {
    id: 20,
    name: "Virendranath Chattopadhyay",
    code: "Virendranath-Chattopadhyay",
    image: Faces.VirendranathChattopadhyay,
  },
];

function App() {
  const [step, setStep] = useState(1);
  const [result, setResult] = useState(Data[0]);
  const [keyPressed, setKeyPressed] = useState(null);

  const AutoStartTimer = useRef();

  const soundRef = useRef();

  const { webcamRef, boundingBox, isLoading, detected, facesDetected } =
    useFaceDetection({
      faceDetectionOptions: {
        model: "short",
      },
      faceDetection: new FaceDetection.FaceDetection({
        locateFile: (file) =>
          `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`,
      }),
      camera: ({ mediaSrc, onFrame, width, height }: CameraOptions) =>
        new Camera(mediaSrc, {
          onFrame,
          width,
          height,
        }),
    });

  // useEffect(() => {
  //   console.log("FACE", facesDetected, boundingBox, detected);
  // }, [facesDetected]);

  useEffect(() => {
    console.log("FACE", facesDetected, boundingBox, detected);
    console.log("STEP", step);

    if (detected && step === 1) {
      AutoStartTimer.current = setTimeout(function () {
        setStep(2);
        takePicture();
      }, 1000);
      console.log("start the flow");
    } else if (detected === false && step === 1) {
      console.log("stop the flow");
      clearTimeout(AutoStartTimer.current);
    }

    if (step === 2) {
      soundRef.current.play();
    } else {
      soundRef.current.pause();
    }
  }, [detected, step]);

  function takePicture() {
    // const imageSrc = webcamRef.current.getScreenshot();

    // const screenshotBlob = new Blob([imageSrc], { type: "image/jpeg" });
    // const formData = new FormData();

    // formData.append("file", screenshotBlob);

    // Get the screenshot data from the webcam
    const screenshotData = webcamRef.current.getScreenshot();

    // Create a FormData object to store the image data
    const formData = new FormData();
    formData.append("image", screenshotData);

    // Send the POST request to the Flask API with the FormData object as the request body

    axios
      .post("http://localhost:5000/api/v1/user", formData)
      .then((response) => {
        console.log(response.data);

        let obj = Data.find((o) => o.name === response.data.name);

        setResult(obj);
        setStep(3);
        setTimeout(function () {
          setStep(1);
        }, 6000);
      })
      .catch((error) => {
        console.log(error);

        setStep(1);
      });
  }

  return (
    <div className="App">
      <audio src={Sound} ref={soundRef} loop autoPlay />

      {/* SPLASH */}
      <div
        style={{
          position: "absolute",
          top: step === 1 ? 0 : 1920,
          left: 0,
          height: 1920,
          width: 1080,
          transition: "all 0.5s",
          zIndex: 1000,
        }}
      >
        <div id="arrowAnim">
          <div className="arrowSliding">
            <div className="arrow"></div>
          </div>
          <div className="arrowSliding delay1">
            <div className="arrow"></div>
          </div>
          <div className="arrowSliding delay2">
            <div className="arrow"></div>
          </div>
          <div className="arrowSliding delay3">
            <div className="arrow"></div>
          </div>
        </div>
        <header className="app-splash-text">
          <p>Please stand at the marked position</p>
        </header>
      </div>

      {/* FACE */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: 1920,
          width: 1080,
          transition: "all 2s",
          zIndex: 1100,

          opacity: 1,
          display: "none",
        }}
      >
        <div>
          <div style={{ position: "absolute" }}>
            <p style={{ color: "#fff" }}>{`Loading: ${isLoading}`}</p>
            <p style={{ color: "#fff" }}>{`Face Detected: ${detected}`}</p>
            <p
              style={{ color: "#fff" }}
            >{`Number of faces detected: ${facesDetected}`}</p>
          </div>
          <div
            style={{ width: "1080px", height: "1920px", position: "relative" }}
          >
            {boundingBox.map((box, index) => (
              <div
                key={`${index + 1}`}
                style={{
                  border: index === 0 ? "4px solid green" : "4px solid red",
                  position: "absolute",
                  top: `${box.yCenter * 100}%`,
                  left: `${box.xCenter * 100}%`,
                  width: `${box.width * 100}%`,
                  height: `${box.height * 100}%`,
                  zIndex: 1,
                }}
              />
            ))}
            <Webcam
              ref={webcamRef}
              forceScreenshotSourceSize
              screenshotFormat="image/jpeg"
              style={{
                height: "100%",
                width: "100%",
              }}
            />
          </div>
        </div>
      </div>

      {/* AI ANIMATION */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: 1920,
          width: 1080,
          transition: "all 2s",
          zIndex: 900,

          opacity: step === 2 ? 1 : 0,
        }}
      >
        <img
          className="app-face-animation"
          src={AiAnimation}
          width="100%"
          alt="animation"
        />
      </div>

      {/*RESULT */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: 1920,
          width: 1080,
          transition: "all 2s",
          zIndex: 950,

          opacity: step === 3 ? 1 : 0,
        }}
      >
        <img
          className="app-face-animation"
          src={result.image}
          width="100%"
          alt="animation"
        />
        <div
          style={{
            position: "absolute",
            color: "#f5f5f5",
            textShadow: "2px 2px #000",
            bottom: 150,
            left: "50%",
            transform: "translateX(-50%)",
          }}
        >
          <div
            style={{
              fontSize: 32,
            }}
          >
            You resemble
          </div>
          <div
            style={{
              fontSize: 56,
              fontWeight: 700,
              whiteSpace: "nowrap",
            }}
          >
            {result.name}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
