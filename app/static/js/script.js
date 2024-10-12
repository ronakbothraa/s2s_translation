const recordButton = document.getElementById('recordButton')
const transriptDiv = document.getElementById('transcript')

let isRecording = false
let full_transcript = ''

recordButton.addEventListener('click', () => {
    isRecording = !isRecording
    if (isRecording) {
        startRecording()
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
    console.log("threads started")
    while (isRecording) {
        console.log("fetching data")
        const transcript_response = await fetch('/process', {
            method: 'POST'
        })
        console.log("data received!", transcript_response)
    
        const transcript_data = await transcript_response.json()
        if (transcript_data.transcript != null) {
            full_transcript += transcript_data.transcript
            transriptDiv.textContent = full_transcript
        }
        console.log("data displayed!", full_transcript)
    }
}

async function stopRecording() {
    await fetch('/stop', {
        method: 'POST'
    })
    console.log("threads stopped")
}