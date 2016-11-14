"use strict";
var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."
//////////////////// 
function showStories(topic_id,response){

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);
       
           //figure out how to make this image just appear
        for (var i =0; i < response["articles"].length; i++){
             console.log(i);
           results_div.append(
            //works but not what I want iframe killer for some impacts useage
           // "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] + "'"+ "style='width:100%;'frameborder='0'></iframe>" +
            
           "<form action='/saved_pages_catch'>"+
           "<a href=" + response["articles"][i]["urlToImage"]+ "> Image </a>" +
           "<input type='hidden' name='url' value='" + response["articles"][i]["url"] + "'>" +
            "<a href=" + response["articles"][i]["url"]+ ">" + "</a>" +
            "<p>" + response['articles'][i]['title']  + "</p>" +
            "<input type='hidden' name='author' value='"+response["articles"][i]['author'] +"' >"+
            "<p>" + response["articles"][i]['author'] + "</p>" + 
            "<p>" +response["articles"][i]["description"] +"</p>" +
            "<input type='hidden' name='published_at' value='" +response["articles"][i]["publishedAt"] +"'>"+
            "<p>" +response["articles"][i]["publishedAt"]+ "</p>"+ 
            "<input type='submit' class='save_btn_class'action='submit' value='Save Story'> </input>" +
            "</form>" 
            );
        }
    }

    function stopSaveForm(evt){
        evt.preventDefault();
        debugger
        var  btn= $(evt.currentTarget);
        var form = btn.closest('form');
        var url=form.find('input[name="url"]').val()
        var title=form.find('input[name="author"]').val()
        var author=form.find('input[name="title"]').val()
        var published_at=form.find('input[name="published_at"]').val()

    
        var formInputs={ 
            
                'url': url,
                'title':title,
                'author': author,
                'published_at': published_at
    
            };

        var alertSaved = function(response) {


        };

        $.post("/saved_pages_catch",
                formInputs,
                alertSaved
                );

    }

    //$('.save_btn_class').on('click',stopSaveForm);
    $('body').on('click','.save_btn_class',stopSaveForm);

    function getRequestInfo(evt){
        evt.preventDefault();

        var btn = $(evt.currentTarget);

        var form = btn.closest('form');

        var id = form.find('select.source_name').val();

        var sortby = form.find('select.sortby').val();


        var topic_id = form.attr('topic-id');

        // console.log($(".source_name").val())
        // console.log($("#sortby").val())
        var formInputs={
            "topic_id": topic_id,
            "source_id": id,
            "sortby":sortby
        };

        var handler = function(response) {
            return showStories(topic_id,response);
        }

        //QUESTION HOW DO I PUT VARIABLE IN BELOW
        $.get("/news-landing.json",
                formInputs,
                handler);
    }
    $("input.chose_source_btn").on("click", getRequestInfo);

////////////////////

var story_count = 1;
console.log("This is makeing sure javascript is running" + story_count);
function addStoryHtml(){


    // (var index=1, ,'click', i++){
    //     $(".category").addClass(story_count)
    // }
    //CHANGE THIS SO THE NAME VALUE IS DIFFERENT
    console.log("This is running addStoryHtml")
    $("#add_story_div").append(
        "<p>Type</p><select name='type-"+ story_count + "'> " +
            "<option value='text'> Text </option> " +
            "<!-- <option value='audio'> Audio </option>" +
            "<option value='video'> Video </option> -->" +
        "</select>" +
        "<p> ALL OF OUR TEXT IS SOURCED BY NEWS API *** FINISH THE INFO THEY ASK FOR HERE***</p>" +
        "<br>" +
    
        "<p> Topic Category </p>" +
        "<select name='category-"+ story_count + "'>" +
            "<option value='business'> Business </option>" +
            "<option value='entertainment'> Entertainment </option>" +
            "<option value='gaming'>Gaming </option>" +
            "<option value='general'>General </option>" +
            "<option value='music'> Music</option>" +
            "<option value='science-and-nature'> Science-and-Nature </option>" +
            "<option value='technology'> Technology</option>" +
        "</select>" +
        "<br>" +

        "<!-- TEST OUT SOME DAY HAVING MORE THAN ONE can also add country -->"+
        "<p>Language</p>"+
        "<select name='language-" + story_count + "'>"+
            "<option value = 'en'>English</option>" +
            "<option value = 'de'>German</option>"+
            "<option value = 'fr'>French</option>"+
            "<option value = 'all'> All</option>"+
       " </select>" +
       " <br> "+
        "<!-- AT SOME POINT CHOSE MULTIPLE PLACES -->"+
        "<p>Country</p>" +
        "<select name='country-" + story_count + "'>"+
            "<option value = 'au'> Austraila</option>"+
            "<option value = 'de'>Germany</option>" +
            "<option value = 'gb'>Great Britian</option>" +
            "<option value = 'in'>India</option>" +
            "<option value = 'it'>Italy</option>" +
            "<option value = 'us'>United States</option>" +
        "</select>" +
        "<br>" +
    "</form>" +
    "<br>"
    );

    story_count++;
}

$("#add_story").on('click', addStoryHtml);


function addHiddenCount(){


    console.log("This is testing that addHiddenCount is running")
    $('#hidden_story_count').val(story_count.toString());
}
$('#add_story').on('click', addHiddenCount)


/////////////////////////////////
function deleteLandingOnScreen(result){
    var landingnames = result.landings;

    var html_string =  "<p>Your Landing Pages: </p>" ;

    for(var i=0; i < landingnames.length; i++){
        html_string += "<a href='/yourlanding/" + landingnames[i] + "'><button>" + landingnames[i] + " </button> </a>" + 
                "<form action='/delete_catch'>" +
                    "<input class='delete_landing_btn' name='" + landingnames[i] +"' type='submit'value='Delete this Landing'>" +
                "</form>" 
            
        }


    $('update_your_landings').html(html_string);

}

function deleteRequest(evt){
    evt.preventDefault()

    var btn = $(evt.currentTarget);

    var name = btn.attr('name');
    
    var formInputs={ 
        "landingname": name
    };

    $.post("/delete_landing.json",
                formInputs,
                deleteLandingOnScreen);
}

$('.delete_landing_btn').on('click', deleteRequest)

