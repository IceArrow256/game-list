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

function deleteByCategory(category, id) {
    $.ajax({
        type: 'GET',
        url: `/delete/${category}/${id}`,
        success: function(response) {
            window.location.reload()
        },
        error: function(response) {
            alert("Can't delete")
        },
        dataType: 'json',
    });
}


function deleteFromList(id) {
    $.ajax({
        type: 'GET',
        url: '/delete/GameInList/' + id,
        success: function(response) {
            $("#list" + id).html("Add to list")
            $("#list" + id).attr("onclick", `addToList(${response.id});`)
            $("#list" + id).prop('id', 'game' + response.id);
            return true;
        },
        error: function(response) {
            alert("Can't delete")
        },
        dataType: 'json',
    });
}

function addToList(id) {
    $.ajax({
        type: 'GET',
        url: '/create/GameInList/' + id,
        success: function(response) {
            $("#game" + id).html("Delete from list")
            $("#game" + id).attr("onclick", `deleteFromList(${response.id});`)
            $("#game" + id).prop('id', 'list' + response.id);
            return true;
        },
        error: function(response) {
            alert("Can't add")
        },
        dataType: 'json',
    });

}