// Grab elements, create settings, etc.
function deleteUser(id,fName,lName)
{
    if (!confirm('Are you sure you want to delete '+fName+' '+lName+'?'))
        return;
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/deleteuser/",
        data: {
            id: id
        },
        success: function () {
            $('#'+id).hide(300);
            $('#'+id).remove();
            alert('deleted!');
        }
    });
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