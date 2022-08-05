// Grab elements, create settings, etc.
function deleteUser(id, fName, lName) {
    if (!confirm('Are you sure you want to delete ' + fName + ' ' + lName + '?'))
        return;
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/deleteuser/",
        data: {
            id: id
        },
        success: function () {
            $('#' + id).hide(300);
            $('#' + id).remove();
            alert('deleted!');
        }
    });
}
