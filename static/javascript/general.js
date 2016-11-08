var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."

function showStories(response){

        $("#results").html("");

        for (var i =0; i < response['articles'].length; i++){

           <!--figure out how to make this image just appear-->
           $("#results").html(
           "<a href=" +response['articles'][i]['urlToImage']+ ">"+ Image "</a>"
            "<a href=" +response['articles'][i]['url']+ ">" + 
             response['articles'][i]['title']  + "</a>" +
            "<p>" +  response['articles'][i]['author'] + "</p>" + 
            "<p>" +response['articles'][i]['description'] +"</p>" +
            "<p>" +response['articles'][i]['publishedAt']+ "</p>" )
            
        }

    }
    function getRequestInfo(evt){
        evt.preventDefault();
        var formInputs={
            "source_id": $('.source_name').attr("id")
            "sortby":$('#sortby').val()
        };
        #QUESTION HOW DO I PUT VARIABLE IN BELOW
        $.get('/news-landing.json',
                formInputs,
                showStories;
    }
    $('#chose_source_btn').on('click', getRequestInfo);