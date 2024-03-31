const video = document.getElementsByTagName('video')[0];
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capture');
const recognizeButton = document.getElementById('recognize');

function openCamera() {
    navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
            facingMode: "user"
        }
    }).then(function (stream) {
        video.classList = [];
        canvas.classList = ['d-none'];
        video.srcObject = stream;
        captureButton.classList.remove('d-none');
    });
}

function capture() {
    const width = video.getBoundingClientRect().width;
    const height = video.getBoundingClientRect().height;
    canvas.width = width;
    canvas.height = height;
    context.drawImage(video, 0, 0, width, height);
    video.classList = ['d-none'];
    canvas.classList = [];
    video.srcObject.getTracks().forEach(track => track.stop());
    recognizeButton.classList.remove('d-none');
}

function recognize() {
    document.getElementById('frame').value = canvas.toDataURL();
    document.getElementsByTagName('form')[0].submit();
}
