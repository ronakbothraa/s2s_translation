const recordButton = document.getElementById('recordButton')
const transriptDiv = document.getElementById('transcript')

let isRecording = false
let full_transcript = ''

recordButton.addEventListener('click', () => {
    if (!isRecording) {
        startRecording()
        recordButton.textContent = 'Stop Recording'
    } else {
        // stopRecording()
        recordButton.textContent = 'Start Recording'
    }
    isRecording = !isRecording
})


async function startRecording() {
    const transcript_response = await fetch('/process', {
        method: 'POST'
    })

    const transcript_data = await transcript_response.json()
    if (transcript_data.transcript != null) {
        full_transcript += transcript_data.transcript
        transriptDiv.textContent = full_transcript
    }
}