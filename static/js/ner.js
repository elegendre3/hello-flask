//import $ from "jQuery";

// TEST data
CLFS = {'token': ['model1', 'model2']}


$(function() {

    $('#text-form').submit(function(e) {
        var clfId = $('#ner-clf').val();
        var selectedModel = $('#ner-model').val();
        console.log('model selected:  ' +  selectedModel)
        var text = $('#ner-text').val().trim();
        if (clfId != null) {
            clearResponse()
            var settings = {
                "url": '/spacy/ner/predict',
                "method": "POST",
                "timeout": 0,
                "headers": {
                    "Content-Type": "application/json"
                },
                "data": JSON.stringify({"text":text}),
            };

            $.ajax(settings,).done(function (response) {
                    console.log(response);
                    renderbasicNERResponse(text, response);
                });

        } else {
            console.log('No class was selected.')
        }

        // IMPORTANT: avoids the normal submit and reload
        return false
    });
});


function getCharInfo(text, data) {
// This will not work if entities overlap or if they arent sorted
    var whole_text = text;
    var entities = data["data"];
    console.log("entities");
    console.log(entities);
    var prec_idx = 0;
    var nul_lab = "O";
    var charInfo = [];

    // make list of all (including negative) entities containing [start_idx: int, end_idx: int, label: str]
    $.each(entities, function (el) {
        console.log("entity");
        console.log(el);
        var entity = entities[el];
        var layout = entity["layout"];
        console.log("layout");
        console.log(layout);
        charInfo.push([prec_idx, layout["start"], nul_lab]);
        charInfo.push([layout["start"], layout["end"] + 1, entity["label"]]);
        prec_idx = layout["end"] + 1;
    });
    charInfo.push([prec_idx, whole_text.length + 1, nul_lab]);
    console.log("charInfo");
    console.log(charInfo);
    return charInfo;
}

function renderNERResponse(text, data) {
    var entities = getCharInfo(text, data);

    // Clear the previous response output
    clearResponse();

    $.each(entities, function (el) {
        var entity = entities[el];
        var tokens = text.slice(entity[0], entity[1]);
        var highlight = '<mark class="' + entity[2] + '">' + tokens + "</mark> ";
        $("#resp").append(highlight);
    });
}

function renderbasicNERResponse(text, data) {
    // Clear the previous response output
    console.log('rendbasic gets called');
    clearResponse();
    $("#resp").append(data);
}

function clearResponse() {
    $('#resp').empty()
}
