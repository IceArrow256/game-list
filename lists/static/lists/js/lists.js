$(document).ready(function() {
    $('.page').each(function() {
        let url = window.location.href
        url = url.replace(/[?|&]page=\d*/gm, "");
        if (url.includes('?'))
            url = url + $(this).attr('href').replace("?", "&")
        else
            url = url + $(this).attr('href')
        $(this).attr('href', url)
    });
});

function deleteFromList(id) {
    $.ajax({
        type: 'GET',
        url: '/delete/GameInList/' + id,
        success: function(response) {
            window.location.reload()
        },
        error: function(response) {
            alert("Can't delete")
        },
        dataType: 'json',
    });
}