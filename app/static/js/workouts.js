function deleteWorkout(id) {
    var dataToServer = JSON.stringify(id);
    $.ajax({
        url: '/deleteWorkout',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: dataToServer,
        success: function(dataToServer){
            var convertToJS = JSON.parse(dataToServer);
            if(convertToJS.isValid) {
                window.location.reload();
            } else {
                alert('The workout with the given id: ' + id + ' was not found.');
            }
        }
    });
}