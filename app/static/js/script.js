const recordButton = document.getElementById('recordButton')
const transriptDiv = document.getElementById('transcript')
const translateDiv = document.getElementById('translate')

let isRecording = false
let full_transcript = ''

recordButton.addEventListener('click', () => {
    isRecording = !isRecording
    if (isRecording) {
        startRecording()
        transcript()
        translate()
        recordButton.textContent = 'Stop Recording'
    } else {
        stopRecording()
        recordButton.textContent = 'Start Recording'
    }
})

async function startRecording() {
    await fetch('/start', {
        method: 'POST'
    })
}

async function transcript() {
    while (isRecording) {
        const transcript_response = await fetch('/transcript', {
            method: 'POST'
        })
        const transcripted_data = await transcript_response.json()
        console.log("transcripted: ", transcripted_data.transcript)
        if (transcripted_data.transcript != null) {
            full_transcript += transcripted_data.transcript
            transriptDiv.textContent = full_transcript
        }
    }
    
}

async function translate() {
    while (isRecording) {
        const translation_response = await fetch('/translate', {
            method: 'POST'
        })
        const translated_data = await translation_response.json()
        console.log("translated: ", translated_data.translation)
        translateDiv.textContent = translated_data.translation
    }
    const translation_response = await fetch('/translate', {
        method: 'POST'
    })
    const translated_data = await translation_response.json()
    console.log("translated: ", translated_data.translation)
    translateDiv.textContent = translated_data.translation
}

async function stopRecording() {
    await fetch('/stop', {
        method: 'POST'
    })
}