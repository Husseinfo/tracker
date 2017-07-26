// Grab elements, create settings, etc.
$(function () {
    $('#device').change(function () {
        if ($('#device').val() == 0) {
            $('.modal-header').empty();
            $('.modal-header').prepend('<video id="video" width="640" height="480" class="img-thumbnail"></video>');
        }
        else {
            $('.modal-header').empty();
            $('.modal-header').prepend('<img id="image" src="http://192.168.0.2/cgi-bin/nph-zms?monitor=4" width=640 height=480 class="img-thumbnail"/>');
        }
    });
});

$.urlParam = function (name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results !== null)
        return results[1] || 0;
};

var user = $.urlParam('user');
if (user !== null) {
    $('#user_id').val(user);
}

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

// Trigger photo take
$('#capture').click(function () {
    var id = $('#user_id').val();
    var number = $('#number').val();
    if (id <= 0 || number <= 0) {
        alert('ID and Number must have positive values!');
        return;
    }
    alert('Taking ' + number + ' photos for user: ' + $('#user_id option[value="' + id + '"]').text() + '\nPress ok when ready.');
    $(this).css('disabled', 'true');
    if ($('#device').val() == 0) {
        var photos = takePhotos(number);
        $.ajax({
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            type: "POST",
            url: "/sendimage/",
            data: {
                label: id,
                photos: photos
            },
            success: function () {
                $('#loader').removeClass('loader');
                alert('Uploaded!');
            }
        });
    }
    else {
        alert('Ready?');
        $.ajax({
            type: "GET",
            url: "/remotecapture/",
            data: {
                user: id,
                number: number
            },
            success: function () {
                $('#loader').removeClass('loader');
                alert('Uploaded!');
            }
        });
    }
});

function takePhotos(num) {
    var photos = [];
    for (var i = 0; i < num; i++) {
        alert('Ready?');
        context.drawImage(video, 0, 0, 320, 240);
        photos[i] = document.getElementById("canvas").toDataURL("image/png");
    }
    return photos;
}

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
