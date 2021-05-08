function processRecommendations(data) {
    console.log(data)
    console.log("processing recos")

    if (!jQuery.isEmptyObject(data)) {
        $("#suggestionsList").removeClass('d-none');
        document.getElementById('suggestionsList').innerHTML = ""


        for (i = 0; i < data.length; i++) {
            console.log(data[i])

            document.getElementById('suggestionsList').innerHTML +=
                '<div class="accordion-item">' +
                    '<h2 class="accordion-header" id="heading' + i + '">' +
                      '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse' + i + '" aria-expanded="false" aria-controls="collapse' + i + '">' +
                        data[i]["node"]["name"] + '&nbsp' +
                        '<span class="badge bg-secondary">' + data[i]["score"] + '</span>' +
                      '</button>' +
                    '</h2>' +
                    '<div id="collapse' + i + '" class="accordion-collapse collapse" aria-labelledby="heading' + i + '" data-bs-parent="#suggestionsList">' +
                      '<div class="accordion-body">' +
                        data[i]["summary"] + '&nbsp;<a href=' + data[i]["link"] + ' target="_blank" rel="noopener noreferrer">Learn more...</a>' +
                      '</div>' +
                    '</div>' +
                    '</div>'
        }
    }
    else {
        alert("No documents found with the combination of properties selected. Please try again.");
    }
}

$(function() {
    $("button#applyFilter").bind('click', function() {

        $("#applySpinner").removeClass('d-none');

        var jur = document.getElementById('jur').value;
        var pa = document.getElementById('pa').value;
        var rtype = document.getElementById('rtype').value;
        console.log('selected jur ['+ jur + ']')
        console.log('selected pa ['+ pa + ']')
        console.log('selected resourcetype ['+ rtype + ']')
        $.getJSON(URL_ROOT + '_filter_recommendations', {
                "title": document.getElementById('sampleDocTitle').innerHTML,
                "practiceArea": pa,
                "jurisdiction": jur,
                "resourceType": rtype
            }, function(data) {

                $("#applySpinner").addClass('d-none');
                processRecommendations(data)

        });
    });
    return false;
})



$(function() {
  $('button#search_button').bind('click', function() {

    $.getJSON(URL_ROOT + '_search_doc', {
            "title": document.getElementById('search_title').value
        }, function(doc) {
        console.log(doc)
        if (!jQuery.isEmptyObject(doc)) {
            document.getElementById('initialDoc').style.display = 'block';
            document.getElementById('sampleDocTitle').innerHTML = doc["title"];
            document.getElementById('sampleDocText').innerHTML = doc["summary"];
            document.getElementById('sampleDocLink').href = doc["originalURL"];
        }
        else {
            alert("No document found with the entered title. Please try again.");
            window.location.reload();
        }

    $("#suggestionsTitle").removeClass('d-none');
    $("#suggestionsSpinner").removeClass('d-none');
    document.getElementById('suggestionsList').innerHTML = ""


    $.getJSON(URL_ROOT + '_get_recommendations', {
            "docId": doc["id"]
        }, function(data) {
        $("#suggestionsSpinner").addClass('d-none');
        processRecommendations(data)
    });
  });
  return false;
});
