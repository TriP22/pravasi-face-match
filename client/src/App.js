import "./App.css";
import { React, useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import FeatherIcon from "feather-icons-react";

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
    gender: "Female",
  },
  {
    id: 2,
    name: "Dadabhai Naoroji",
    code: "Dadabhai-Naoroji",
    image: Faces.DadabhaiNaoroji,
    gender: "Male",
  },
  {
    id: 3,
    name: "Kartar Singh Sarabha",
    code: "Kartar-Singh-Sarabha",
    image: Faces.KartarSinghSarabha,
    gender: "Male",
  },
  {
    id: 4,
    name: "Lala Hardayal",
    code: "Lala-Hardayal",
    image: Faces.LalaHardayal,
    gender: "Male",
  },
  {
    id: 5,
    name: "Lala Lajpat Rai",
    code: "Lala-Lajpat-Rai",
    image: Faces.LalaLajpatRai,
    gender: "Male",
  },
  {
    id: 6,
    name: "Madam Cama",
    code: "Madam-Cama",
    image: Faces.MadamCama,
    gender: "Female",
  },
  {
    id: 7,
    name: "Madan Lal Dhingra",
    code: "Madan-Lal-Dhingra",
    image: Faces.MadanLalDhingra,
    gender: "Male",
  },
  {
    id: 8,
    name: "Mahatma Gandhi",
    code: "Mahatma-Gandhi",
    image: Faces.MahatmaGandhi,
    gender: "Male",
  },
  {
    id: 9,
    name: "Netaji Subhas",
    code: "Netaji-Subhas",
    image: Faces.NetajiSubhas,
    gender: "Male",
  },
  {
    id: 10,
    name: "Pandurang Bapat",
    code: "Pandurang-Bapat",
    image: Faces.PandurangBapat,
    gender: "Male",
  },
  {
    id: 11,
    name: "Raja Mahendra Pratap",
    code: "Raja-Mahendra-Pratap",
    image: Faces.RajaMahendraPratap,
    gender: "Male",
  },
  {
    id: 12,
    name: "Rash Behari Bose",
    code: "Rash-Behari-Bose",
    image: Faces.RashBehariBose,
    gender: "Male",
  },
  {
    id: 13,
    name: "Sardarsinghji Rana",
    code: "Sardarsinghji-Rana",
    image: Faces.SardarsinghjiRana,
    gender: "Male",
  },
  {
    id: 14,
    name: "Shyamji Krishnavarma",
    code: "Shyamji-Krishnavarma",
    image: Faces.ShyamjiKrishnavarma,
    gender: "Male",
  },
  {
    id: 15,
    name: "Sister Nivedita",
    code: "Sister-Nivedita",
    image: Faces.SisterNivedita,
    gender: "Female",
  },
  {
    id: 16,
    name: "Swami Vivekanand",
    code: "Swami-Vivekanand",
    image: Faces.SwamiVivekanand,
    gender: "Male",
  },
  {
    id: 17,
    name: "Udham Singh",
    code: "Udham-Singh",
    image: Faces.UdhamSingh,
    gender: "Male",
  },
  {
    id: 18,
    name: "VVS Iyer",
    code: "VVS-Iyer",
    image: Faces.VVSIyer,
    gender: "Male",
  },
  {
    id: 19,
    name: "Vinayak Damodar Savarkar",
    code: "Vinayak-Damodar-Savarkar",
    image: Faces.VinayakDamodarSavarkar,
    gender: "Male",
  },
  {
    id: 20,
    name: "Virendranath Chattopadhyay",
    code: "Virendranath-Chattopadhyay",
    image: Faces.VirendranathChattopadhyay,
    gender: "Male",
  },
];

const MaleArr = Data.filter((x) => x.gender === "Male");
const FemaleArr = Data.filter((x) => x.gender === "Female");

function App() {
  const [step, setStep] = useState(1);
  const [personImage, setImage] = useState(null);
  const [result, setResult] = useState(Data[0]);
  const [keyPressed, setKeyPressed] = useState(null);
  const [loading, setLoading] = useState(false);

  const webcamRef = useRef();
  const soundRef = useRef();

  useEffect(() => {
    if (step === 2) {
      soundRef.current.play();
    } else {
      soundRef.current.pause();
    }
  }, [step]);

  function takePicture(personImg) {
    // Create a FormData object to store the image data
    const formData = new FormData();
    formData.append("image", personImg);

    // Send the POST request to the Flask API with the FormData object as the request body
    setLoading(true);
    axios
      .post("http://localhost:5000/api/v1/user", formData)
      .then((response) => {
        console.log(response.data);

        if (response.data?.gender === "Male") {
          const resultObj = MaleArr[Math.floor(Math.random() * 17)];
          setResult(resultObj);
          setStep(3);
          setTimeout(function () {
            setStep(1);
            setImage(null);
          }, 6000);
        } else if (response.data?.gender === "Female") {
          const resultObj = FemaleArr[Math.floor(Math.random() * 3)];
          console.log(resultObj);

          setResult(resultObj);

          setStep(3);
          setTimeout(function () {
            setStep(1);
            setImage(null);
          }, 6000);
        }
      })
      .catch((error) => {
        console.log(error);

        setStep(1);
        setImage(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  useEffect(() => {
    // Add an event listener to the document to listen for key press events
    document.addEventListener("keydown", handleKeyPress);

    // Remove the event listener when the component is unmounted
    return () => {
      document.removeEventListener("keydown", handleKeyPress);
    };
  }, []); // Don't re-run the effect

  function handleKeyPress(event) {
    // Check which key was pressed
    if (event.key === "n" || event.key === "N") {
      setKeyPressed("Modi");
    } else if (event.key === "m" || event.key === "M") {
      setKeyPressed("Male");
    } else if (event.key === "f" || event.key === "F") {
      setKeyPressed("Female");
    } else if (event.key === "c" || event.key === "C") {
      setKeyPressed(null);
    }
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
        <header className="app-splash-text">
          <p>Please stand at the marked position</p>
        </header>
        {personImage ? (
          <img
            src={personImage}
            alt="person"
            style={{
              width: "100%",
              height: "100%",
              zIndex: -10,
              position: "absolute",
              objectFit: "contain",
              inset: 0,
            }}
          />
        ) : (
          <Webcam
            ref={webcamRef}
            forceScreenshotSourceSize
            screenshotFormat="image/jpeg"
            style={{
              height: "100%",
              width: "100%",
              zIndex: -10,
              position: "absolute",
              inset: 0,
            }}
          />
        )}
        <div className="app-splash-buttons">
          {personImage ? (
            <>
              <button
                className="app-splash-button"
                onClick={() => {
                  setImage(null);
                }}
              >
                <FeatherIcon
                  className="app-splash-button-icon"
                  icon="refresh-ccw"
                  size="32"
                />
                <div className="app-splash-button-text">Retake</div>
              </button>
              <button
                className="app-splash-button"
                onClick={() => {
                  setStep(2);

                  if (keyPressed != null) {
                    if (keyPressed === "Modi") {
                      setTimeout(function () {
                        let obj = Data.find(
                          (o) => o.name === "Shyamji Krishnavarma"
                        );

                        setResult(obj);
                        setStep(3);
                        setTimeout(function () {
                          setStep(1);
                          setImage(null);
                        }, 6000);
                      }, 5000);
                    } else if (keyPressed === "Male") {
                      setTimeout(function () {
                        const resultObj =
                          MaleArr[Math.floor(Math.random() * 17)];
                        console.log(resultObj);

                        setResult(resultObj);
                        setStep(3);
                        setTimeout(function () {
                          setStep(1);
                          setImage(null);
                        }, 6000);
                      }, 5000);
                    } else if (keyPressed === "Female") {
                      setTimeout(function () {
                        const resultObj =
                          FemaleArr[Math.floor(Math.random() * 3)];
                        console.log(resultObj);

                        setResult(resultObj);

                        setStep(3);
                        setTimeout(function () {
                          setStep(1);
                          setImage(null);
                        }, 6000);
                      }, 5000);
                    }
                  } else {
                    takePicture(personImage);
                  }
                }}
              >
                <div className="app-splash-button-text">Proceed</div>
                <FeatherIcon
                  className="app-splash-button-icon"
                  icon="chevron-right"
                  size="32"
                />
              </button>
            </>
          ) : (
            <>
              <button
                className="app-splash-button"
                onClick={() => {
                  setImage(webcamRef.current.getScreenshot());
                }}
              >
                <FeatherIcon
                  className="app-splash-button-icon"
                  icon="camera"
                  size="32"
                />
                <div className="app-splash-button-text">Take Picture</div>
              </button>
            </>
          )}
        </div>
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
          zIndex: -800,

          opacity: step === 3 && !loading ? 1 : 0,
          bottom: step === 3 && !loading ? -1920 : 0,
        }}
      >
        {step === 3 && (
          <>
            <img
              className="app-face-animation"
              src={result?.image}
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
                {result?.name}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
