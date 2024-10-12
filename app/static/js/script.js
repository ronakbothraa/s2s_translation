const recordButton = document.getElementById('recordButton')
const transriptDiv = document.getElementById('transcript')
const translateDiv = document.getElementById('translate')
const inputLanguage = document.getElementById('inputLanguage')
const outputLanguage = document.getElementById('outputLanguage')

transriptDiv.textContent = "Transcript: "
translateDiv.textContent = "Translation: "
document.getElementById("inputLanguage").options[19].selected = 'selected'
document.getElementById("outputLanguage").options[1].selected = 'selected'
let isRecording = false
let full_transcript = 'Transcript: '

recordButton.addEventListener('click', () => {
    isRecording = !isRecording
    if (isRecording) {
        full_transcript = 'Transcript: '
        transriptDiv.textContent = "Transcript: "
        translateDiv.textContent = "Translation: "
        startRecording()
        transcript()
        translate()
        recordButton.textContent = 'Stop Talking'
        recordButton.className = "btn btn-danger"
    } else {
        stopRecording()
        recordButton.className = "btn btn-primary"
        recordButton.textContent = 'Start Talking'
    }
})

async function startRecording() {
    await fetch('/start', {
        method: 'POST',
        body: JSON.stringify({
            inputLanguage: inputLanguage.options[inputLanguage.selectedIndex].value,
            outputLanguage: outputLanguage.options[outputLanguage.selectedIndex].value
        }),
        headers: {
            'Content-Type': 'application/json'
        },
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
    while (true) {
        const translation_response = await fetch('/translate', {
            method: 'POST'
        })
        const translated_data = await translation_response.json()
        translateDiv.textContent = "Translation: " + translated_data.translation
    }
}

async function stopRecording() {
    await fetch('/stop', {
        method: 'POST'
    })
}