
// Our random guess model
// this function return a random int [min, max]
// From: https://stackoverflow.com/questions/1527803/generating-random-whole-numbers-in-javascript-in-a-specific-range
function getRandomInt(min, max) {
	// round up
    min = Math.ceil(min);
    // round down
    max = Math.floor(max);
    // Math.random() random number in the range 0–1 
    // inclusive of 0, but not 1
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function show_vampire() {
	var student_id = getRandomInt(1, 3);
	// Create student id string based on 'Model' component
	var student_id_str = 'student_' + student_id.toString() + '_image';
	// change icon
    document.getElementById(student_id_str).src='src/vampire.jpg';
}

  