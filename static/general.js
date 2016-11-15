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

var story_count = 0;
console.log("This is makeing sure javascript is running" + story_count);
function addStoryHtml(response){

    if(response['status'] != "ok"){
        var type=$('#type-' +story_count).val();
        var category = $('#category-' + story_count).val();
        var country=$('#country-' + story_count).val();
        var language=$('#language-'+ story_count).val();
        alert("The Story Query for"+ category + type + "news from" + country + "in the language" + language +"is not supported right now.");
    }

    else{

        $("#add_story_div").html("")

        console.log("This is running addStoryHtml")

        $("#stories_you_have_so_far").append("<p> Your Stories So Far on the News Landing</p> <br> <p> Your Story request for " + category + type + "news from" + country + "in the language" + language + "has been saved to your landing page.</p>")
        $("#add_story_div").html(
            "<p>Type</p><select id = 'type-" + story_count+"' name='type-"+ story_count + "'> " +
                "<option value='text'> Text </option> " +
                "<!-- <option value='audio'> Audio </option>" +
                "<option value='video'> Video </option> -->" +
            "</select>" +
            "<p> ALL OF OUR TEXT IS SOURCED BY NEWS API *** FINISH THE INFO THEY ASK FOR HERE***</p>" +
            "<br>" +
        
            "<p> Topic Category </p>" +
            "<select id='category-" + story_count +"'name='category-"+ story_count + "'>" +
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
            "<select id='language-" + story_count + "'name='language-" + story_count + "'>"+
                "<option value = 'en'>English</option>" +
                "<option value = 'de'>German</option>"+
                "<option value = 'fr'>French</option>"+
                "<option value = 'all'> All</option>"+
           " </select>" +
           " <br> "+
            "<!-- AT SOME POINT CHOSE MULTIPLE PLACES -->"+
            "<p>Country</p>" +
            "<select id='country-" + story_count + "' name='country-" + story_count + "'>"+
                "<option value = 'au'> Austraila</option>"+
                "<option value = 'de'>Germany</option>" +
                "<option value = 'gb'>Great Britian</option>" +
                "<option value = 'in'>India</option>" +
                "<option value = 'it'>Italy</option>" +
                "<option value = 'us'>United States</option>" +
            "</select>" +
            "<br>" +
            "<p>Add A Story</p>" +
            "<input id='hidden_story_count' type='hidden' name='story_count' value='"+(story_count + 1)+"'>" +       
            "<input id='#add_story' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add Story'>"    +
            "</form>" +
            "<br>"
            );
    
            story_count++;
    }
}

function checkStoryQuery(evt){
    evt.preventDefault();
    console.log("checkStoryQuery is running")

    var type=$('#type-' +story_count).val();
    var category = $('#category-' + story_count).val();
    var country=$('#country-' + story_count).val();
    var language=$('#language-'+ story_count).val();
    var landing_name=$('#new_landing_name').val();
    var story_count =$('#hidden_story_count').val();
    var formInputs={
            'type': type,
            'category': category,
            'country': country,
            'language': language,
            'new_landing_name': landing_name,
            'story_count': story_count
    };
    console.log(formInputs)
    $.post(
        '/cautious_query_api.json', 
        formInputs,
        addStoryHtml);
}

$("#add_story").on('click', checkStoryQuery);


function addHiddenCount(){


    console.log("This is testing that addHiddenCount is running")
    $('#hidden_story_count').val(story_count.toString());
}
$('#add_story').on('click', addHiddenCount);



////////////////////////////////
function warnUniqueLandingName(response){
    if (response['landing_name_used'] === 'yes'){
        var landing_name =$('new_landing_name').val();
        alert('You already have a news landing page named ' + landing_name + 'please make a unique landing name.');
    }
    else if(response['landing_name_used'] === 'no'){
        $('#new_landing_name').attr('readonly');
    }
    else if(response['landing_name_needed'] === 'yes'){
        alert('You must name this landing page');

    }

}
function mustNameLanding(evt){
    evt.preventDefault();
    var landing_name =$('new_landing_name').val();
    var formInputs ={
        'new_landing_name': landing_name
    };
    $.post(
        '/check_landing_name.json',
        formInputs,
        warnUniqueLandingName)
}
$('#add_story').one('click', mustNameLanding);



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
    evt.preventDefault();

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

//////////////////////////////

   

















