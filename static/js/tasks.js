/**
 * Created by Ahmad Tfaily on 6/1/2017.
 */
$(document).ready(function () {
    $('button').click(function () {
        $('#todo').append("<tr><td class=''>" + $("input[name=task]").val() + " <a href='#' class='close' aria-hidden='true'>&times;</a></td></tr>");
    });
    $("body").on('click', '#todo a', function () {
        $(this).closest("td").remove();
    });
});