let photo;
let video = document.getElementById('video');


// Elements for taking the snapshot
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

function takePhotos() {
    context.drawImage(video, 0, 0, 320, 240);
    photo = document.getElementById("canvas").toDataURL("image/png");
}

// Trigger photo take
$('#capture').click(function () {
    context.drawImage(video, 0, 0, 320, 240);
    takePhotos();
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/recognize/",
        data: {
            photos: [photo]
        },
        success: function (data) {
            const go = $('#go');
            const percentage = $('#percentage');
            go.prop('disabled', true);
            if (data.id === null) {
                go.hide();
                percentage.css('width', '0%').attr('aria-valuenow', 0).html('');
                return;
            }
            go.html(data.name);
            go.removeAttr('style');
            if (data.name === 'Unknown') {
                percentage.css('width', '0%').attr('aria-valuenow', 0).html('');
                return;
            }
            go.prop('disabled', false);
            go.parent().attr('href', '/profile/' + data.id);
            const percent = String(data.percentage);
            percentage.css('width', percent + '%').attr('aria-valuenow', percent).html(percent + ' %');
        }
    });
});

$(() => {
    video = document.getElementsByTagName('video')[0];

    const facingMode = "user";
    const constraints = {
        audio: false,
        video: {
            facingMode: facingMode
        }
    };
    navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
        video.srcObject = stream;
    });
});
