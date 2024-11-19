const recordButton = document.getElementById('recordButton')
const resetButton = document.getElementById('resetButton')
const speakButton = document.getElementById('speakButton')
const transriptDiv = document.getElementById('transcript')
const translateDiv = document.getElementById('translate')
const inputLanguage = document.getElementById('inputLanguage')
const outputLanguage = document.getElementById('outputLanguage')

transriptDiv.textContent = "Transcript: "
translateDiv.textContent = "Translation: "
document.getElementById("inputLanguage").options[19].selected = 'selected'
document.getElementById("outputLanguage").options[1].selected = 'selected'
let isRecording = false

speakButton.addEventListener('click', () => {
    speak()
})

async function speak() {
    const a = await fetch('/tts', {
        method: 'POST',
        body: JSON.stringify({
            translatedData: translateDiv.textContent
        }),
        headers: {
            'Content-Type': 'application/json'
        },
    })
    const b = await a.json()
    console.log(b)
}


recordButton.addEventListener('click', () => {
    isRecording = !isRecording
    if (isRecording) {
        speakButton.disabled = true
        resetButton.disabled = true
        transriptDiv.textContent = "Transcript: "
        translateDiv.textContent = "Translation: "
        start()
        transcript()
        translate()
        recordButton.textContent = 'Stop Talking'
        recordButton.className = "btn btn-danger"
    } else {
        stop()
        recordButton.className = "btn btn-primary"
        recordButton.textContent = 'Start Talking'
        speakButton.disabled = false
        resetButton.disabled = false
    }
})

resetButton.addEventListener('click', () => {
    transriptDiv.textContent = "Transcript: "
    translateDiv.textContent = "Translation: "
})

// async function loading_button(button, condition=false, till=0){
//     time = 1;
//     buttonContent = button.innerHTML;
    
//     button.disabled = true; 
//     button.innerHTML = `Starting: ${time}s`;
//     var timerInterval = setInterval(function () {
//         time++; 
//         button.innerHTML = `Starting: ${time}s`;

//         if (!condition && time > till) {
//             clearInterval(timerInterval);
//             button.innerHTML = buttonContent;
//             button.disabled = false;
//         }
//     }, 1000);
// }

// speakButton.addEventListener('click', () => {
//     loading_button(speakButton, false, till=5)
//     // output = fetch('/generate_tts', {
//     //     method: 'POST',
//     //     body: JSON.stringify({
//     //         input: translateDiv.textContent
//     //     }),
//     //     headers: {
//     //         'Content-Type': 'application/json'
//     //     },
//     // })
//     // const msg = new SpeechSynthesisUtterance(full_transcript)
//     // window.speechSynthesis.speak(msg)
// })  

function start() {
    a = fetch('/start', {
        method: 'POST',
        body: JSON.stringify({
            inputLanguage: inputLanguage.options[inputLanguage.selectedIndex].value,
            outputLanguage: outputLanguage.options[outputLanguage.selectedIndex].value
        }),
        headers: {
            'Content-Type': 'application/json'
        },
    })
    console.log("started")
}

async function transcript() {
    while (true) {
        const transcript_response = await fetch('/transcript', {
            method: 'POST',
            body: JSON.stringify({
                isRecording: isRecording
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const transcripted_data = await transcript_response.json()
        if (transcripted_data.transcript != false) {
            console.log(transcripted_data)
            transriptDiv.textContent += transcripted_data.transcript
        } else {
            console.log(transcripted_data)
            break
        }
    }
}

async function translate() {
    while (true) {
        const translation_response = await fetch('/translate', {
            method: 'POST',
            body: JSON.stringify({
                isRecording: isRecording
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const translated_data = await translation_response.json()
        if (translated_data.translation != false) {
            console.log(translated_data)
            translateDiv.textContent = translated_data.translation
        } else {
            console.log(translated_data)
            break
        }
    }
}

async function stop() {
    await fetch('/stop', {
        method: 'POST'
    })
}