import React, { useEffect, useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import { useSpeechSynthesis } from "react-speech-kit";
import { AiFillCloseCircle } from "react-icons/ai"
import socketIOClient from "socket.io-client";
import Button from '../components/elements/Button';
const ENDPOINT = "http://127.0.0.1:5000";
function Functionality() {
    const { speak } = useSpeechSynthesis();
    var { transcript, resetTranscript } = useSpeechRecognition();
    const [Socket, setSocket] = useState(null);
    const [message, setmessage] = useState("");
    const [bool, setbool] = useState(false);
    const [startstop, setstartstop] = useState(true);
    const [finalmessage, setfinalmessage] = useState("");
    const [work, setwork] = useState("");
    useEffect(() => {
        const socket = socketIOClient(ENDPOINT);
        setSocket(socket);
        socket.on("connect", () => {
            socket.emit('consumer')
            console.log("Connected to socket ", socket.id)
        });
        socket.on('connect', function () {
            socket.send('User has connected');
        })
        socket.on('message', function (msg) {
            if (msg[0] == '$') {
                setfinalmessage(msg.substring(1));
            }
            else {
                setmessage(msg);
            }
        });
        return () => socket.close();
    }, []);
    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
        return null;
    }
    const closedetection = () => {
        const data = new FormData();
        data.append("stop", "Stop/Start");
        fetch('http://localhost:5000/requests', {
            method: 'POST',
            body: data
        });
    }
    const sentencesformation = async (e, value) => {
        const data = new FormData();
        data.append("openAi", value);
        const res = await fetch('http://localhost:5000/openAi', {
            method: 'POST',
            body: data
        });
        const datares = await res.json();
        if (res.status !== 200 || !datares) {
            const error = new Error(res.error)
            throw error;
        }
        else {
            setfinalmessage(datares.text);
            speak({ text: datares.text });
        }
    }
    const startdetection = () => {
        const data = new FormData();
        data.append("detect", "Detect");
        fetch('http://localhost:5000/requests', {
            method: 'POST',
            body: data
        });
    }
    const sendspeech = async (speech) => {
        const datax = new FormData();
        datax.append("message", speech);
        if (startstop === true) {
            SpeechRecognition.stopListening();
            await fetch('http://localhost:5000/message', {
                method: 'POST',
                body: datax
            });
            setbool(true);
            setstartstop(false);
        }
        else {
            setbool(false);
            setstartstop(true);
            SpeechRecognition.startListening();
        }
    }
    const handlemessage = (e) => {
        setmessage(e.target.value);
    }
    function updatestring(message) {
        const lastIndexOfSpace = message.lastIndexOf(' ');

        if (lastIndexOfSpace === -1) {
            return message;
        }

        return message.substring(0, lastIndexOfSpace + 1);
    }
    return (
        <div className="container-sm">
            <div >
                <div>
                    <div >
                        <div
                            style={{ display: "flex", justifyContent: "space-evenly" }}
                            className="reveal-from-bottom" data-reveal-delay="600">
                            <Button color="primary" wideMobile
                                onClick={() => { setwork("Sign_Text"); startdetection(); }}>
                                Sign → Text
                            </Button>
                            <Button color="dark" wideMobile
                                onClick={() => { setwork("Speech_Sign"); SpeechRecognition.startListening({ continuous: true }); }}>
                                Speech → Sign
                            </Button>
                        </div>
                        {work === "Sign_Text" ?
                            <AiFillCloseCircle onClick={() => { setmessage(""); setfinalmessage(""); setwork(""); closedetection(); SpeechRecognition.stopListening() }} />
                            : null}
                        {work === "Speech_Sign" ?
                            <>
                                <button color="dark" wideMobile onClick={() => { sendspeech(transcript); }}>
                                    ReStart/Stop
                                </button>
                                <button color="dark" wideMobile
                                    onClick={() => { resetTranscript(); setwork(""); setbool(false); setstartstop(true); }}>
                                    Reset
                                </button>{bool === true ? <img src="http://localhost:5000/display_video" /> : null}
                            </> : null}

                        {work === "Sign_Text" ?
                            <img src="http://localhost:5000/video_feed" /> : null}
                        <h2 id="output">{message}</h2>
                        <h1 id="final_output">{finalmessage}</h1>
                        <h1 id="Speech">{transcript}</h1>
                    </div>
                </div>
                {work === "Sign_Text" ?
                    <input onChange={handlemessage} value={message}
                        onKeyDown={(e) => {
                            const messagenew = updatestring(message);
                            if (e.key === "Enter")
                                sentencesformation(e, e.target.value);
                            else if (e.key === "Backspace") { setmessage(messagenew); Socket.send(e.key) }
                        }}
                    /> : null}
            </div>
        </div >
    )
}
export default Functionality