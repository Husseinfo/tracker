/**
 * Created by Ahmad Tfaily on 6/1/2017.
 */

$('#add').click(function () {
    var s = $('#tasks :selected').text();
    if (s != "") {
        $('#todo').append("<tr><td>" + $("#tasks :selected").text() + "<a href='#' class='close' aria-hidden='true'>&times;</a></td></tr>");
        $('#tasks :selected').remove();
    }
});
$('#save').click(function () {
    var tasks = [];
    table = document.getElementById("todo");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        tasks[i] = td.textContent;
    }
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: "POST",
        url: "/savetasks/",
        data: {
            id: $('#id').val(),
            tasks: tasks
        },
        success: function () {
            $('#success').hide(200)
            $('#success').show(200)
        }
    });
});
$("body").on('click', '#todo a', function () {
    var s = $(this).closest("td").text();
    s = s.substring(0, s.length - 1);
    $("#tasks").append('<option >' + s + '</option>');
    $(this).closest("tr").remove();
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