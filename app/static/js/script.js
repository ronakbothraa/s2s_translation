const recordButton = document.getElementById('recordButton')
const transriptDiv = document.getElementById('transcript')

let isRecording = false
let mediaRecorder
let intervalId
let full_transcript = ''

recordButton.addEventListener('click', () => {
    if (!isRecording) {
        // startRecording()
        recordButton.textContent = 'Stop Recording'
    } else {
        // stopRecording()
        recordButton.textContent = 'Start Recording'
    }
    isRecording = !isRecording
})