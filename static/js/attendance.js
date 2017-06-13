/**
 * Created by hussein on 5/31/17.
 */

function sort() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function onCalendarChange(date, state) {
    var table, tr, td, i;
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
    date = String(date);
    var _day = date.split(' ')[2];
    var _month = date.split(' ')[1];
    var _year = date.split(' ')[3];
    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2].textContent;
        var day = td.split(' ')[1].split(',')[0];
        var month = td.split(' ')[0];
        var year = td.split(', ')[1].split(',')[0];
        if (td) {

            if (month == _month && day == _day && year == _year) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

$(function () {
    var myCalendar = new dhtmlxCalendarObject("calendar");
    myCalendar.attachEvent("onChange", onCalendarChange);
    var myCalendar = new dhtmlXCalendarObject("calendar2");
    myCalendar.attachEvent("onChange", onCalendarChange);
});