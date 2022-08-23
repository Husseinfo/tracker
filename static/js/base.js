$(() => {
    const id = $('title').html().split('|')[1].trim().replace(/ /g, '');
    $('#' + id).addClass('active');
});
