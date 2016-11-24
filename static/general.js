// global variables don't run with strict mode
// "use strict";

var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."
////////////For yourlanding page /////////
function showStories(topic_id, source_logo_url, response){
    if('never' in response){
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html("<p>" + response['never'] + "</p>")
    } else if('not ok' in response){
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html("<p>" + response['not ok'] + "</p><image src='" + source_logo_url + "' height='65'  width='65'>");

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);

        //figure out how to make this image just appear
        for(var i =0; i < response['ok']['headlines_response']["articles"].length; i++){
            console.log(i);
            console.log(response["articles"][i]["url"]);
            // I believe this is put here by accident b/c no evt
            //  var  btn= $(evt.currentTarget);
            //  var form = btn.closest('form');
            // var url=form.find('input[name="url"]').val();

            results_div.append(
                    //works but not what I want iframe killer for some impacts useage
                    // "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] +    "'"+ "style='width:100%;'frameborder='0'></iframe>" +

                    "<form action='/saved_pages_catch' method='POST'>"+
                    "<image src=" + response["articles"][i]["urlToImage"]+ " height='125'    width='175'>" +
                    "<input type='hidden' name='url' value='" + response["articles"][i]["url"] + "   ' height='35' width='35'>" +
                    "<a href='" + response["articles"][i]["url"] + "'onclick=\"window.open(' "+     response["articles"][i]["url"]+ "', 'newwindow', 'width=675, height=400')   ; return false;\"><p>" + response['articles'][i]['title']  + "</p></a>" +
                    "<input type='hidden' name='title' value='" + response["articles"][i]["title"   ] + "'>" +
                    "<p> Author(s): </p>" +
                    "<input type='hidden' name='author' value='"+ response["articles"][i]['author'] +"' >"+
                    "<p>" + response["articles"][i]['author'] + "</p>" + 
                    "<p> Description: </p>" +
                    "<p>" +response["articles"][i]["description"] +"</p>" +
                    "<input type='hidden' name='published_at' value='" +response["articles"][i]["publishedAt"] +"'>"+
                    "<p>" +response["articles"][i]["publishedAt"]+ "</p>"+ 
                    "<input type ='hidden' class='save_story_button_div-"+ i +"' name='index'   value='" + i + "''>" +
                    "<div id='save_story_button_div-"+ i +"' name='index' value='" + i + "''>"+
                    "<input type='submit' class='save_btn_class' action='submit' value='Save    Story'> </input>" +
                    "</div>"+
                    "</form>" 
            );
        }

    } else{
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html( "<image src='" + source_logo_url + "' height='65'  width='65'>");

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);

        //figure out how to make this image just appear
        for(var i =0; i < response["articles"].length; i++){
            console.log(i);
            console.log(response["articles"][i]["url"]);
            // I believe this is put here by accident b/c no evt
            //  var  btn= $(evt.currentTarget);
            //  var form = btn.closest('form');
            // var url=form.find('input[name="url"]').val();

            results_div.append(
                    //works but not what I want iframe killer for some impacts useage
                    // "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] +    "'"+ "style='width:100%;'frameborder='0'></iframe>" +

                    "<form action='/saved_pages_catch' method='POST'>"+
                    "<image src=" + response["articles"][i]["urlToImage"]+ " height='125'    width='175'>" +
                    "<input type='hidden' name='url' value='" + response["articles"][i]["url"] + "   ' height='35' width='35'>" +
                    "<a href='" + response["articles"][i]["url"] + "'onclick=\"window.open(' "+     response["articles"][i]["url"]+ "', 'newwindow', 'width=675, height=400')   ; return false;\"><p>" + response['articles'][i]['title']  + "</p></a>" +
                    "<input type='hidden' name='title' value='" + response["articles"][i]["title"] + "'>" +
                    "<p> Author(s): </p>" +
                    "<input type='hidden' name='author' value='"+ response["articles"][i]['author'] +"' >"+
                    "<p>" + response["articles"][i]['author'] + "</p>" + 
                    "<p> Description: </p>" +
                    "<p>" +response["articles"][i]["description"] +"</p>" +
                    "<input type='hidden' name='published_at' value='" +response["articles"][i]["publishedAt"] +"'>"+
                    "<p>" +response["articles"][i]["publishedAt"]+ "</p>"+ 
                    "<input type ='hidden' class='save_story_button_div-"+ i +"' name='index'   value='" + i + "''>" +
                    "<div id='save_story_button_div-"+ i +"' name='index' value='" + i + "''>"+
                    "<input type='submit' class='save_btn_class' action='submit' value='Save Story'> </input>" +
                    "</div>"+
                    "</form>" 
            );
        }
    }



}


//////////For  saving a story in yourlanding page //////////////
function stopSaveForm(evt){
    evt.preventDefault();
    // debugger
    var btn= $(evt.currentTarget);
    var form = btn.closest('form');
    var url=form.find('input[name="url"]').val();
    var title=form.find('input[name="title"]').val();
    var author=form.find('input[name="author"]').val();
    var published_at=form.find('input[name="published_at"]').val();
    /// gives me an i that is unique
    var which_div=form.find('input[name="index"]').val();
    console.log(which_div);

    var formInputs={ 
        'url': url,
        'title':title,
        'author': author,
        'published_at': published_at

    };
    var find_this = '#save_story_button_div-' + which_div;
    var alertSaved = function(response){
        // var targetDiv= form.find
        // var values = form.find('div.save_story_button_div').val();
        // $('.save_story_button_div').html

        console.log(find_this);

        if(response['ok']){
            console.log("AlertSaved line 78 running");
            $(find_this).html("");
            $(find_this).html(
                    "<p> Story Saved</p>" +
                    "<input type='submit' class='unsave_btn_class' value='Remove From Saved'> </input>");
        } else if(response['no']){
            $(find_this).html("");
            $(find_this).html("<p>This story is already in your saved folder. </p>" +
                    "<input type='submit' class='unsave_btn_class' value='Remove From Saved'> </input>");
        }

        // This works here and makes the pop up come that says it deletes the story and it works
        $('.unsave_btn_class').on('click', unsaveStory);
    };

    function testClick(evt){
        console.log(evt);
    }

    function alertUnsaved(response){
        $(find_this).html("");
        $(find_this).html("<p> This Story has been removed from your saved stories page </p> <br> <input type='submit' class='save_btn_class'action='submit' value='Save Story'> </input>");
    }

    function unsaveStory(evt){
        evt.preventDefault();
        console.log('This means unsaveStory is running');

        var  btn= $(evt.currentTarget);
        var form = btn.closest('form');
        var url=form.find('input[name="url"]').val();
        var title=form.find('input[name="title"]').val();
        var author=form.find('input[name="author"]').val();
        var published_at=form.find('input[name="published_at"]').val();

        var formInputs={ 
            'url': url,
            'title':title,
            'author': author,
            'published_at': published_at
        };

        console.log(formInputs);

        $.post("/unsaved_pages_catch",
            formInputs,
            alertUnsaved
        );
    }

    $.post("/saved_pages.json",
        formInputs,
        alertSaved
    );
}

//$('.save_btn_class').on('click',stopSaveForm);
$('body').on('click','.save_btn_class',stopSaveForm);
/////////remove a saved story line from the saved page after clicking a button that should trigger stopsaveform above to remove it from the database /////

function removeSavedStoryFromSavedPage(evt){
    var btn= $(evt.currentTarget);
    var form = btn.closest('form');
    console.log(form);
    form.html("");
}

$('#refresh_saved_without_removed').on('click', removeSavedStoryFromSavedPage);

///////////for yourlanding page chose a source drop down //////////////

function getRequestInfo(evt){
    evt.preventDefault();

    var btn = $(evt.currentTarget);

    var form = btn.closest('form');
    var option= btn.closest('option');
    console.log(form);
    console.log(option);

    var values = form.find('select.source_name').val();
    console.log(values);
    values_split= values.split(",");
    console.log(values_split);

    var id = values_split[0];
    var source_logo_url = values_split[1];
    var sortby = form.find('select.sortby').val();

    var topic_id = form.attr('topic-id');

    console.log(source_logo_url);
    // console.log($(".source_name").val())
    // console.log($("#sortby").val())
    var formInputs={
        "topic_id": topic_id,
        "source_id": id,
        "sortby":sortby,
    };

    var handler = function(response){
        return showStories(topic_id, source_logo_url, response);
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
        var landing_name =response['landing_name']
            $('#landing_name_musts').html("<p>'You already have a news page named '" + landing_name + "' please chose a unique news paper name. </p>");
    } else if(response['landing_name_used'] === 'no'){
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
                "<option value = 'au'> Australia</option>"+
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
    } else if(response['landing_name_needed'] === 'yes'){
        $('#landing_name_musts').html("<p>Please, name your news paper before building its content.</p>");
    }

}
function mustNameLanding(evt){
    evt.preventDefault();
    var landing_name=$('#new_landing_name').val();

    var formInputs ={
        'new_landing_name': landing_name
    };

    console.log(formInputs);
    $.post(
        '/check_landing_name.json',
        formInputs,
        warnUniqueLandingName);
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
    console.log("This is testing that addHiddenCount is running");
    $('#hidden_story_count').val(window.STORY_COUNT.toString());
}

////////// Add a new story to the new_landing//////
function addStoryHtml(response){

    console.log(response);

    if(response['status'] != "ok"){
        console.log("WE have error in addstoryhtml");
        // $('#stories_not_possible').html('hello');
        $('#stories_you_have_so_far').prepend("The Story search for "+ response['category'] +" news from " + response['country'] + " in the language " + response['language'] +" is not supported right now.");
    } else {

        $("#add_story_div").html("");

        console.log("This is running addStoryHtml");
        console.log(window.STORY_COUNT +  " This is the count in addHTML");
        $("#stories_you_have_so_far").append("<p> Your request for the following news has been saved to this new news page are: </p> <br>");

        $("#stories_you_have_so_far").append(" <p> " + response['category'] + " news from " + response['country'] + " in the language " + response['language'] + " has been saved to your landing page.</p>");
        $("#add_story_div").html(
                "<p>Type</p><select id = 'type-" + window.STORY_COUNT+"' name='type-"+ window.STORY_COUNT + "'> " +
                "<option value='text'> Text </option> " +
                "<!-- <option value='audio'> Audio </option>" +
                "<option value='video'> Video </option> -->" +
                "</select>" +
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
                "<option value = 'au'> Australia</option>"+
                "<option value = 'de'>Germany</option>" +
                "<option value = 'gb'>Great Britian</option>" +
                "<option value = 'in'>India</option>" +
                "<option value = 'it'>Italy</option>" +
                "<option value = 'us'>United States</option>" +
                "</select>" +
                "<br>" +
                "<p>Add A Story</p>" +
                "<input id='hidden_story_count' type='hidden' name='story_count' value='"+(window.STORY_COUNT)+"'>" +       
                "<input id='add_story' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add Story'>"  +
                "</form>" +
                "<br>"
                );

        $("#add_story").on('click', checkStoryQuery);
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
        'media_type': type,
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

/////////Function Logic for Deleting a Landing from the profile page/////////////
function deleteLandingOnScreen(result){
    var html_string =  "<p>Your Landing Pages: </p>" ;
    var landingnames = result.landings;
    console.log(landingnames);

    if(results.length === 0){
        html_string += "You have no News Pages at this time, create a new one: <a  href='/new_landing/{{ current_user.username }}'><button>Add A New News Page</button></a>";
        $('#update_your_landings').html(html_string);
    } else {
        for(var i=0; i < landingnames.length; i++){
            console.log(landingnames[i]); console.log("xxxxx");
            html_string += "<a href=\"/yourlanding/" + landingnames[i] + "\"><button>" + landingnames[i] + " </button> </a>" + 
                // "<form action=\"/delete_catch\">" +
                "<button> class=\"delete_landing_btn\" name=\"" + landingnames[i] +"\" type=\"submit\" value=\"Delete this Landing\" ></button> " 
                //+ "</form>" 
            $('#update_your_landings').html(html_string);
        }
    }
    $('#update_your_landings').html(html_string);

    $('.delete_landing_btn').on('click', deleteRequest);
}

function deleteRequest(evt){
    console.log(evt);
    evt.preventDefault();

    var btn = $(evt.currentTarget);

    var name = btn.attr('name');
    console.log(name);

    var formInputs={ 
        "landingname": name
    };

    $.post("/delete_landing.json",
            formInputs,
            deleteLandingOnScreen);
}

$('.delete_landing_btn').on('click', deleteRequest);

///////////////Add a new story to an exhisting landing ////////////


function addStoryHtmlOnLanding(response){


    if(response['status'] != "ok"){

        console.log('in not ok conditional block');
        $('#add_new_story_refill_div').prepend("<br> The Story Query for "+ response['category'] +" " + response['media_type'] + " news from " + response['country'] + " in the language " + response['language'] +" is not supported right now.<br> ");
    } else{

        ///// IS there a better more dynamic way to run this ?////// 
        console.log(response['landingname']);
        $('#add_new_story_refill_div').html("");
        $('#add_new_story_refill_div').html( "<p> Press Refresh to Add New Story </p><br><a href=\"/yourlanding/"+response['landingname']+"\" ><button>Refresh With new Story</button></a> <br>"
        );

    }      
}

function createNewStoryForm(evt){
    evt.preventDefault();
    var btn= $(evt.currentTarget);
    var form = btn.closest('form');
    var landingname= form.find('input[name="hidden_landingname_add_story"]').val(); 
    var topic_count = form.find('input[name="hidden_count_add_story"]').val();

    $('#add_new_story_refill_div').html("");
    $('#add_new_story_refill_div').html(
        "<form>" + 
        "<p>Type</p><select id = 'type-" + topic_count +"' name='type-"+ topic_count + "'> " +
        "<option value='text'> Text </option> " +
        "<!-- <option value='audio'> Audio </option>" +
        "<option value='video'> Video </option> -->" +
        "</select>" +

        "<p> Topic Category </p>" +
        "<select id='category-" + topic_count +"'name='category-"+ topic_count + "'>" +
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
        "<select id='language-" + topic_count + "'name='language-" + topic_count + "'>"+
        "<option value = 'en'>English</option>" +
        "<option value = 'de'>German</option>"+
        "<option value = 'fr'>French</option>"+
        "<option value = 'all'> All</option>"+
        " </select>" +
        " <br> "+
        "<!-- AT SOME POINT CHOSE MULTIPLE PLACES -->"+
        "<p>Country</p>" +
        "<select id='country-" + topic_count + "' name='country-" + topic_count + "'>"+
        "<option value = 'au'> Australia</option>"+
        "<option value = 'de'>Germany</option>" +
        "<option value = 'gb'>Great Britian</option>" +
        "<option value = 'in'>India</option>" +
        "<option value = 'it'>Italy</option>" +
        "<option value = 'us'>United States</option>" +
        "</select>" +
        "<br>" +
        "<p>Add this Story</p>" +
        "<input id='hidden_story_count' type='hidden' name='story_count' value='"+ topic_count +"'>" + 
        "<input id='new_landing_name' type='hidden' name='new_landing_name' value= \""+ landingname +"\">" +      
        "<input id='add_story_to_a_landing' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add this Story'>"    +
        "</form>" +
        "<br>"
    );

    $("#add_story_to_a_landing").on('click', function(evt){
        evt.preventDefault();
        console.log("Inline function getting thrown too soon!");
        var type=$('#type-' + topic_count).val();
        var category = $('#category-' + topic_count).val();
        var country = $('#country-' + topic_count).val();
        var language = $('#language-'+ topic_count).val();
        var landing_name = $('#new_landing_name').val();
        console.log(landing_name);
        var count_of_story = $('#hidden_story_count').val();

        var formInputs = {
            'media_type': type,
            'category': category,
            'country': country,
            'language': language,
            'new_landing_name': landing_name,
            'story_count': count_of_story
        };

        $.post(
            '/cautious_query_api.json', 
            formInputs,
            addStoryHtmlOnLanding);
    });

}

$('#add_story_to_exhisting_landing').on('click', createNewStoryForm);

function changeButton(response){

    $('#remove-'+ response['id_btn']).html("");
    $('story_removed_flash').prepend("<p> The story " + response['title'] + " has been removed </p>");

}
function removeStoryFromSavedPages2(evt){
    //// I need help because this doesn't have the attributes?
    var id = $(this).attr("id");
    var url = $(this).next().attr("href");
    var title = $(this).next().attr('title');

    $(this).closest('li').remove();

    console.log(url);
    $.post('/unsaved_pages_two_catch',{'id_btn': id, 'url': url , 'title': title }, changeButton);
}

$('.unsave_btn_class_two').on('click', removeStoryFromSavedPages2);
