/**
 * Created by Ahmad Tfaily on 6/1/2017.
 */
$('#add').click(function () {
    $('#todo').append("<tr><td>" + $("#tasks :selected").text() +"<a href='#' class='close' aria-hidden='true'>&times;</a></td></tr>");
});
$('#save').click(function () {
    alert('save');
    var tasks = [];
    table = document.getElementById("todo");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        tasks[i]=td.textContent.split('&times;')[0];
    }
    alert(tasks);
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/savetasks/",
        data: {
            id: $('#id').val(),
            tasks: tasks
        },
        success: function () {
            alert('saved!');
        }
    });
});
$("body").on('click', '#todo a', function () {
        $(this).closest("td").remove();
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