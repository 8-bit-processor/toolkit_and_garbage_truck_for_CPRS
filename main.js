let outBoxResult;

function clearInputBox() {
    document.getElementById('inputbox').value = '';
    return
}

function getInputBox(){
    const input = document.getElementById('inputbox').value.trim();
    if (input !== '') {
        outBoxResult = stringToArray(input);
        clearInputBox();
        return outBoxResult;
    }
}

function displayOutputText(){
    // simply output the input data for now
    const displayBox = document.getElementById('outbox');
    displayBox.style.fontWeight = 'bold';
    displayBox.innerHTML = outBoxResult;
    return
}

// all functions start with accepting input from the input box
// the input box data is then converted to an array for futher NLP processing 
// currently displayoutputText does nothing but show the array as is
// each function will then process the array separately to produce the desired refined output 

function stringToArray(input) {
    let wordsArray = input.split(" ");
    return wordsArray;
}

function makeLabLetter(){
    result= getInputBox();
    displayOutputText();
    return
}

function makeNote(){
    result= getInputBox();
    displayOutputText();
    return
}

function extractScreening(){
    result= getInputBox();
    displayOutputText();
    return
}

function translateRadiologyReport(){
    result= getInputBox();
    displayOutputText();
    return
}

function chatbotWithOllama(){
    result= getInputBox();
    displayOutputText();
    return
}


makeLabLetter()
makeNote()
extractScreening()
translateRadiologyReport()
chatbotWithOllama()
