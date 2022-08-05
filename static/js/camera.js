/**
 * Created by hussein on 5/15/17.
 */
// Grab elements, create settings, etc.
counter = 3;
var photos = [];
var nbPhoto = 3;
var video = document.getElementById('video');

// Get access to the camera!
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
}

// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

function takePhotos() {
    context.drawImage(video, 0, 0, 320, 240);
    photos[nbPhoto - counter] = document.getElementById("canvas").toDataURL("image/png");
}

// Trigger photo take
$('#capture').click(function () {
    if (counter == 0)
        return;
    context.drawImage(video, 0, 0, 320, 240);
    takePhotos();
    counter--;
    document.getElementById("counter").innerHTML = counter;
    if (counter == 0) {
        $.ajax({
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            type: "POST",
            url: "/recognizephoto/",
            data: {
                photos: photos
            },
            success: function (data) {
                $('#go').prop('disabled', true);
                counter = 3;
                document.getElementById("counter").innerHTML = counter;
                if (data.id === null) {
                    $('#go').hide();
                    $('#percentage').css('width', '0%').attr('aria-valuenow', 0).html('');
                    return;
                }
                document.getElementById("counter").innerHTML = counter;
                $('#go').html(data.name);
                $('#go').removeAttr('style');
                if (data.name == 'Unknown') {
                    $('#percentage').css('width', '0%').attr('aria-valuenow', 0).html('');
                    return;
                }
                $('#go').prop('disabled', false);
                $('#go').parent().attr('href', '/profile/' + data.id);
                var percent = String(data.percentage);
                $('#percentage').css('width', percent + '%').attr('aria-valuenow', percent).html(percent + ' %');
            }
        });
    }
});
