// Grab elements, create settings, etc.
$('#delete').click(function () {
    var id = jQuery(this).parent().attr('id');
    var tr = jQuery(this).parent().parent()
    alert('ID and Number must have positive values!' + id);
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/delete_user/",
        data: {
            id: id
        },
        success: function () {
            tr.hide(100);
            tr.remove();
            alert('Uploaded!');
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