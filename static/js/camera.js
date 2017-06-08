/**
 * Created by hussein on 5/15/17.
 */
// Grab elements, create settings, etc.
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
function takePhotos(num) {
    var photos = [];
    for (var i = 0; i < num; i++) {
        alert('Ready?');
        context.drawImage(video, 0, 0, 320, 240);
        photos[i] = document.getElementById("canvas").toDataURL("image/png");
    }
    return photos;
}
// Trigger photo take
$('#capture').click(function () {
    context.drawImage(video, 0, 0, 320, 240);
    var photos = takePhotos(3);
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/recognizephoto/",
        data: {
            photos: photos
        },
        success: function (data) {
            if (data.id === null) {
                $('#go').attr('style', 'visibility: hidden');
                return;
            }
            $('#go').html(data.name);
            $('#go').removeAttr('style');
            if (data.name == 'Unknown') {
                $('#go').prop('disabled', true);
                return;
            }
            $('#go').prop('disabled', false);
            $('#go').parent().attr('href', '/profile/' + data.id);
            var percent = String(data.percentage);
            console.log(percent+'%');
            console.log(String(3));
            $('#percentage').css('width', percent+'%').attr('aria-valuenow', percent);
            $('#percentage').html(percent + ' %');
        }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}