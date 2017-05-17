/**
 * Created by hussein on 5/17/17.
 */
$(function () {
    var id = $('title').html().split('|')[1].trim().replace(/ /g,'');
    $('#'+id).addClass('active');
});
