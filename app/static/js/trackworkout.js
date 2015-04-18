$(function(){
    $("#addExerciseToDatabase").hide();
    $("#addNewExerciseButton").on("click", function(){
        $("#addExerciseToDatabase").toggle();
    });
});

/**
 * An Ajax post call used to alter html elements on the page to a username fetched from the server
 * @param url The action url
 * @param dataToServer Contains any information you want to send to the server side
 * @param dataToChange 
 */
function ajaxCall(url, data1) {
    var dataToServer = JSON.stringify(data1);
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: dataToServer,
        success: function(dataToServer){
            var convertToJS = JSON.parse(dataToServer);
            if(convertToJS.isValid) {
                var exerciseName = convertToJS.exerciseName;
                var exerciseId = convertToJS.exerciseId;
                createExerciseTableRow(exerciseName);
            } else {
                alert('The data delivered to ajax was not found');
            }
        }
    });
};

/**
 * Generates a new row in the exercise list table representing the exercise added to the workout.
 * Will also generate inputs for the weight used, sets performed, and reps performed.
 */
function createExerciseTableRow(exerciseName) {
    var workoutListdiv = $('#workoutList');
    workoutListdiv.append(
        '<tr class="exerciseRow">' +
        // Show the workout name in the table
        '<td value="' + exerciseName + '">' + exerciseName + '</td>' +
        // And create the input for weight, reps and sets
        // This is delimited by an *
        '<td><textarea></textarea></td>' +
        '<td><textarea></textarea></td>' +
        '<td><textarea></textarea></td>' +
        '</tr>'
    );
}

/**
 * Generates a new hidden input in the form representing the exercise being added
 */
function createFormHiddenInput(exerciseRowsArray) {
    var form = $('#hiddenInputsForForm');
    for (index = 0; index < exerciseRowsArray.length; ++index) {
        var splitIndex = exerciseRowsArray[index].split('~');
        var exerciseName = splitIndex[0];
        var currentInput = $('input[name^="' + exerciseName + '"]');
        var amountOfCurrentLift = currentInput.length + 1;
        form.append("<input type='hidden' name='" + exerciseName + amountOfCurrentLift +"' value='" + 
            exerciseRowsArray[index] + "'></input>");
    }
}

function submitExerciseForm() {
    // TODO add verification a text field is not blank, surround in red and present message
    // TODO verify no ~ or # in text field
    var workoutList = $('#workoutList');
    var finalRowValues = [];
    var currentRowValue = [];
    // Iterate over each exercise listed
    $(workoutList).find('tr').each(function(){
        $(this).find('td').each(function(){
            // Grab the exercise name
            if($(this).text() != '') {
                currentRowValue.push($(this).text());
            }
            $(this).find('textarea').each(function(){
                //do your stuff, you can use $(this) to get current cell
                currentRowValue.push('~');
                currentRowValue.push($(this).val());
            })
        })
        finalRowValues.push(currentRowValue.join(""));
        currentRowValue.length = 0;
    })
    createFormHiddenInput(finalRowValues);
    $('#saveWorkoutForm').submit();
}

function displayAddNewExerciseForm() {

}