/**
 * Created by Ahmad Tfaily on 5/15/2017.
 */

var image = null;
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#uploaded').attr('src', e.target.result);
            image = e.target.result;
            showImage();
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function showImage() {
    var img = document.getElementById('uploaded');
    img.style.visibility = 'visible';
}

$('#file').on('change', function(){
    $('#uploaded').show(200);
    $('#uploaded').attr('width', '100%');
    $('#btnRecognize').prop('disabled', false);
});

$('#btnRecognize').click(function () {
    $('#loader').addClass('loader');
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/recognizephoto/",
        data: {
            photo: image
        },
        success: function (data) {
            $('#loader').removeClass('loader');
            $('#go').parent().attr('href', '/profile/'+data.id);
            $('#go').html(data.name);
            $('#go').removeAttr('style');
        }
    });
});

$('#reset').click(function(){
   image = null;
   $('#file').val('');
   $('#btnRecognize').prop('disabled', true);
   $('#go').attr('style', 'visibility: hidden');
   $('#uploaded').hide(200);
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
