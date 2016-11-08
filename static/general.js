"use strict";
var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."

function showStories(response){

        $("#results").html("");
        console.log(response);
        
           //figure out how to make this image just appear
        for (var i =0; i < response["articles"].length; i++){
             console.log(i);
           $("#results").append(
           "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] + "'"+ "style='width:100%;'frameborder='0'></iframe>" +
           "<a href=" + response["articles"][i]["urlToImage"]+ "> Image </a>" +
            "<a href=" + response["articles"][i]["url"]+ ">" + 
             response['articles'][i]['title']  + "</a>" +
            "<p>" +  response["articles"][i]['author'] + "</p>" + 
            "<p>" +response["articles"][i]["description"] +"</p>" +
            "<p>" +response["articles"][i]["publishedAt"]+ "</p>" 
            );
        }
    }
    function getRequestInfo(evt){
        evt.preventDefault();
        console.log($(".source_name").val())
        console.log($("#sortby").val())
        var formInputs={
            "source_id": $(".source_name").val(),
            "sortby":$("#sortby").val()
        };
        //QUESTION HOW DO I PUT VARIABLE IN BELOW
        $.get("/news-landing.json",
                formInputs,
                showStories);
    }
    $("#chose_source_btn").on("click", getRequestInfo);