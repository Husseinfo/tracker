/**
 * Created by Ahmad Tfaily on 5/15/2017.
 */

let image = [];

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#uploaded').attr('src', e.target.result);
            image[0] = e.target.result;
            showImage();
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function showImage() {
    var img = document.getElementById('uploaded');
    img.style.visibility = 'visible';
}

$('#file').on('change', function () {
    $('#uploaded').show(200);
    $('#uploaded').attr('width', '100%');
    $('#btnRecognize').prop('disabled', false);
});

$('#btnRecognize').click(function () {
    $('#loader').addClass('loader');
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')}, type: "POST", url: "/recognizephoto/", data: {
            photos: image
        }, success: function (data) {
            $('#loader').removeClass('loader');
            if (data.id === null) {
                $('.alert.alert-dismissable.alert-danger').show(200);
                return;
            }
            $('#go').parent().attr('href', '/profile/' + data.id);
            $('#go').html(data.name + ' (' + data.percentage + '%)');
            $('#go').removeAttr('style');
        }
    });
});

$('#reset').click(function () {
    image = null;
    $('#file').val('');
    $('#btnRecognize').prop('disabled', true);
    $('#go').attr('style', 'visibility: hidden');
    $('#uploaded').hide(200);
    $('.alert.alert-dismissable.alert-danger').hide(200);
});
