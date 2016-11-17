// global variables don't run with strict mode
// "use strict";

var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."
////////////For yourlanding page /////////
function showStories(topic_id,response){

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);
       
           //figure out how to make this image just appear
        for (var i =0; i < response["articles"].length; i++){
             console.log(i);
             console.log(response["articles"][i]["url"])
           results_div.append(
            //works but not what I want iframe killer for some impacts useage
           // "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] + "'"+ "style='width:100%;'frameborder='0'></iframe>" +
            
           "<form action='/saved_pages_catch'>"+
           // "<a href=" + response["articles"][i]["urlToImage"]+ "> Image </a>" +
           "<input type='hidden' name='url' value='" + response["articles"][i]["url"] + "'>" +
            "<a href='" + response["articles"][i]["url"] + "'onclick=\"window.open(' "+ response["articles"][i]["url"]+ "', 'newwindow', 'width=675, height=400'); return false;\"><p>" + response['articles'][i]['title']  + "</p></a>" +
            "<input type='hidden' name='title' value='" + response["articles"][i]["title"] + "'>" +
            "<p> Author(s): </p>" +
            "<input type='hidden' name='author' value='"+ response["articles"][i]['author'] +"' >"+
            "<p>" + response["articles"][i]['author'] + "</p>" + 
            "<p> Description: </p>" +
            "<p>" +response["articles"][i]["description"] +"</p>" +
            "<input type='hidden' name='published_at' value='" +response["articles"][i]["publishedAt"] +"'>"+
            "<p>" +response["articles"][i]["publishedAt"]+ "</p>"+ 
            "<input type='submit' class='save_btn_class'action='submit' value='Save Story'> </input>" +
            "</form>" 
            );
        }
    }

    //////////////// didn't work when click on link to story url open new window in small demension/////////
    /// this goes in the  a tag rel='external-new-window'
// $(document).ready(function() {
//     $('a[rel|=external]').click(function(){
//         window.open(this.href);
//         return false;
//     });
//     $('a[rel=external-new-window]').click(function(){
//         window.open(this.href, "myWindowName", "width=800, height=600");
//         return false;
//     });
// })



//////////For  saving a story in yourlanding page //////////////
    function stopSaveForm(evt){
        evt.preventDefault();
        debugger
        var  btn= $(evt.currentTarget);
        var form = btn.closest('form');
        var url=form.find('input[name="url"]').val()
        var title=form.find('input[name="title"]').val()
        var author=form.find('input[name="author"]').val()
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



///////////for yourlanding page chose a source drop down //////////////

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
            "sortby":sortby,
        };

        var handler = function(response) {
            return showStories(topic_id,response);
        }
        console.log(formInputs);
        //QUESTION HOW DO I PUT VARIABLE IN BELOW
        $.get("/news-landing.json",
                formInputs,
                handler);
    }
    $("input.chose_source_btn").on("click", getRequestInfo);

//////////////Runs on new_landing page when need to make the landig name unique for user and need to be named/////
var STORY_COUNT = 0;
function warnUniqueLandingName(response){
    if (response['landing_name_used'] === 'yes'){
        var landing_name =$('new_landing_name').val();
        alert('You already have a news landing page named ' + landing_name + 'please make a unique landing name.');
    }
    else if(response['landing_name_used'] === 'no'){
        $('#new_landing_name').attr('readonly', true);
        $('#add_first_story_div').html("");

        $("#add_story_div").html(
            "<p>Type</p><select id = 'type-" + window.STORY_COUNT+"' name='type-"+ window.STORY_COUNT + "'> " +
                "<option value='text'> Text </option> " +
                "<!-- <option value='audio'> Audio </option>" +
                "<option value='video'> Video </option> -->" +
            "</select>" +
            "<p> ALL OF OUR TEXT IS SOURCED BY NEWS API *** FINISH THE INFO THEY ASK FOR HERE***</p>" +
            "<br>" +
        
            "<p> Topic Category </p>" +
            "<select id='category-" + window.STORY_COUNT +"'name='category-"+ window.STORY_COUNT + "'>" +
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
            "<select id='language-" + window.STORY_COUNT + "'name='language-" + window.STORY_COUNT + "'>"+
                "<option value = 'en'>English</option>" +
                "<option value = 'de'>German</option>"+
                "<option value = 'fr'>French</option>"+
                "<option value = 'all'> All</option>"+
           " </select>" +
           " <br> "+
            "<!-- AT SOME POINT CHOSE MULTIPLE PLACES -->"+
            "<p>Country</p>" +
            "<select id='country-" + window.STORY_COUNT + "' name='country-" + window.STORY_COUNT + "'>"+
                "<option value = 'au'> Austraila</option>"+
                "<option value = 'de'>Germany</option>" +
                "<option value = 'gb'>Great Britian</option>" +
                "<option value = 'in'>India</option>" +
                "<option value = 'it'>Italy</option>" +
                "<option value = 'us'>United States</option>" +
            "</select>" +
            "<br>" +
            "<p>Add A Story</p>" +
            "<input id='hidden_story_count' type='hidden' name='window.STORY_COUNT' value='"+(window.STORY_COUNT)+"'>" +       
            "<input id='add_story' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add Story'>"    +
            "</form>" +
            "<br>");
        $('#add_story').on('click', addHiddenCount);
        $("#add_story").on('click', checkStoryQuery);
    }
    else if(response['landing_name_needed'] === 'yes'){
        alert('You must name this landing page');

    }

}
function mustNameLanding(evt){
    evt.preventDefault();
    var landing_name =$('#new_landing_name').val();
    var formInputs ={
        'new_landing_name': landing_name
    };
    $.post(
        '/check_landing_name.json',
        formInputs,
        warnUniqueLandingName)
}


$('#add_first_story_btn').on('click', mustNameLanding);


///////////////new_landing page creation button click counter/ id and name attribute counter/////////////

function addToStoryCount(evt){
    evt.preventDefault();
    STORY_COUNT = window.STORY_COUNT + 1;
    console.log(window.STORY_COUNT +  " This is the count in addToStoryCount");
}
$('#add_story').on('click', addToStoryCount);

console.log("This is makeing sure javascript is running" + window.STORY_COUNT);

////// newlanding page add a counter for the number new stories added to a landing page////////
function addHiddenCount(){


    console.log("This is testing that addHiddenCount is running")
    $('#hidden_story_count').val(window.STORY_COUNT.toString());
}




////////// Add a new story to the new_landing//////
function addStoryHtml(response){

    console.log(response);

    if(response['status'] != "ok"){
        
        alert("The Story Query for "+ response['category'] +" " + response['media_type'] + " news from" + response['country'] + " in the language " + response['language'] +" is not supported right now.");
    }

    else{

        $("#add_story_div").html("")

        console.log("This is running addStoryHtml");
        console.log(window.STORY_COUNT +  " This is the count in addHTML");

        $("#stories_you_have_so_far").append("<p> Your Stories So Far on the News Landing</p> <br> <p> Your Story request for " + response['category'] + " " + response['media_type'] + " news from " + response['country'] + " in the language " + response['language'] + " has been saved to your landing page.</p>")
        $("#add_story_div").html(
            "<p>Type</p><select id = 'type-" + window.STORY_COUNT+"' name='type-"+ window.STORY_COUNT + "'> " +
                "<option value='text'> Text </option> " +
                "<!-- <option value='audio'> Audio </option>" +
                "<option value='video'> Video </option> -->" +
            "</select>" +
            "<p> ALL OF OUR TEXT IS SOURCED BY NEWS API *** FINISH THE INFO THEY ASK FOR HERE***</p>" +
            "<br>" +
        
            "<p> Topic Category </p>" +
            "<select id='category-" + window.STORY_COUNT +"'name='category-"+ window.STORY_COUNT + "'>" +
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
            "<select id='language-" + window.STORY_COUNT + "'name='language-" + window.STORY_COUNT + "'>"+
                "<option value = 'en'>English</option>" +
                "<option value = 'de'>German</option>"+
                "<option value = 'fr'>French</option>"+
                "<option value = 'all'> All</option>"+
           " </select>" +
           " <br> "+
            "<!-- AT SOME POINT CHOSE MULTIPLE PLACES -->"+
            "<p>Country</p>" +
            "<select id='country-" + window.STORY_COUNT + "' name='country-" + window.STORY_COUNT + "'>"+
                "<option value = 'au'> Austraila</option>"+
                "<option value = 'de'>Germany</option>" +
                "<option value = 'gb'>Great Britian</option>" +
                "<option value = 'in'>India</option>" +
                "<option value = 'it'>Italy</option>" +
                "<option value = 'us'>United States</option>" +
            "</select>" +
            "<br>" +
            "<p>Add A Story</p>" +
            "<input id='hidden_story_count' type='hidden' name='window.STORY_COUNT' value='"+(window.STORY_COUNT)+"'>" +       
            "<input id='add_story' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add Story'>"    +
            "</form>" +
            "<br>"
            );

        $('#add_story').on('click', addHiddenCount);
        $("#add_story").on('click', checkStoryQuery);
            
            //possibly not needed because of event handerl addToStoryCount
            // window.STORY_COUNT++;
    }
}

function checkStoryQuery(evt){
    evt.preventDefault();
    console.log("checkStoryQuery is running");
    console.log(window.STORY_COUNT +  " This is the count in checkStoryQuery");
    var type=$('#type-' + window.STORY_COUNT).val();
    console.log(type);
    var category = $('#category-' + window.STORY_COUNT).val();
    var country = $('#country-' + window.STORY_COUNT).val();
    var language = $('#language-'+ window.STORY_COUNT).val();
    var landing_name = $('#new_landing_name').val();
    var count_of_story = $('#hidden_story_count').val();
    
    var formInputs = {
            'type': type,
            'category': category,
            'country': country,
            'language': language,
            'new_landing_name': landing_name,
            'story_count': count_of_story
    };

    console.log(formInputs)
    $.post(
        '/cautious_query_api.json', 
        formInputs,
        addStoryHtml);
}

console.log($("#add_story"));






/////////Function Logic for Deleting a Landing from the profile page/////////////
function deleteLandingOnScreen(result){
    var landingnames = result.landings;

    var html_string =  "<p>Your Landing Pages: </p>" ;

    for(var i=0; i < landingnames.length; i++){
        html_string += "<a href='/yourlanding/" + landingnames[i] + "'><button>" + landingnames[i] + " </button> </a>" + 
                "<form action='/delete_catch'>" +
                    "<input class='delete_landing_btn' name='" + landingnames[i] +"' type='submit'value='Delete this Landing'>" +
                "</form>" 
            
        }


    $('#update_your_landings').html(html_string);

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

   

















