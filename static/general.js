// global variables don't run with strict mode
// "use strict";

////////////For yourlanding page /////////
$(document).ready(function(){
    $('body').on('click','#explain_password_trigger',function(evt){
        evt.preventDefault();
        $('#explain_password_message').toggleClass('hidden');
    });
});


function renderArticle(index,article) {
    return "<form class='container-fluid' id='boarder_this_form' action='/saved_pages_catch' method='POST'> <div class='row'>"+
           "<div class='center_this' class='col-sm-12 col-md-3' class='image_div_news' > <image src=" + article.urlToImage + " height='155'   width='235'> </div>" +
           "<div class='col-sm-12 col-md-9' class='text_div_news'> <input type='hidden' name='url' value='" + article.url + "   ' height='35' width='35'>" +
           "<h5> <span class='header_inline'>Link to Story:</span>  <a href='" + article.url + "' target='_blank'>" + article.title  + "</a></h5>" +
           "<input type='hidden' name='title' value='" + article.title + "'>" +
           "<p> <span class='header_inline'>Author(s): </span>  " + article.author +" </p>" +
           "<input type='hidden' name='author' value='"+ article.author +"' >"+
          

           "<p> <span class='header_inline'> Description:</span>  " +article.description +"</p>" +
           "<input type='hidden' name='published_at' value='" +article.publishedAt +"'>"+
           "<p>" +article.publishedAt+ "</p>"+ 
           "<input type ='hidden' class='save_story_button_div-"+ index +"' name='index'   value='" + index + "''>" +
           "<div id='save_story_button_div-"+ index +"' name='index' value='" + index + "'' </div>"+
           "<input type='submit' class=\"btn btn-default btn-sm save_btn_class\" action='submit' value='Save Story'>" +
           "</input> <br>" +
           "</div>"+
           "</form>" ;
}

function showStories(topic_id, source_logo_url, response){
    if('never' in response){
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html("<p>" + response['never'] + "</p>")
    } else if('not ok' in response){
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html("<p>" + response['not ok'] + "</p><image src='" + source_logo_url + "' height='120'  width='120'>");

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);

        //figure out how to make this image just appear
        $.each(response.ok.articles,function(index,article){
            console.log(index);
            console.log(article.url)
            results_div.append(renderArticle(index,article));
        })

    } else{
        $("#logo-" + topic_id).html("");
        $("#logo-" + topic_id).html( "<image src='" + source_logo_url + "' height='120'  width='120'>");

        var results_div = $("#topic-results-" + topic_id);

        results_div.html("");

        console.log(response);

        $.each(response.articles,function(index,article){
            console.log(index);
            console.log(article.url)
            results_div.append(renderArticle(index,article));
        })
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

        console.log("RIGHT HERE")
        console.log($(find_this).html());

        if(response['ok']){
            console.log("AlertSaved line 78 running");
            $(find_this).html("");
            $(find_this).html(
                    "<p> Story Saved</p>" +
                    "<input type='submit' class='unsave_btn_class btn-default btn-sm' value='Remove From Saved'> </input>");
        } else if(response['no']){
            $(find_this).html("");
            $(find_this).html("<p>This story is already in your saved folder. </p>" +
                    "<input type='submit' class='unsave_btn_class btn-default btn-sm ' value='Remove From Saved'> </input>");
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
    $.get("/news-landing.json",
            formInputs,
            handler);
}
$("input.chose_source_btn").on("click", getRequestInfo);

//////////////Runs on new_landing page when need to make the landig name unique for user and need to be named/////
var STORY_COUNT = 0;

function createNewNewspaper(evt) {
    evt.preventDefault();
    var form  = $(evt.currentTarget).closest('form');
    var input = form.find('input[type="text"]');
    var name  = input.val();
    var data  = {'new_landing_name': name};
    var warn  = form.find('span.help-block');

    var handler = function(response) {
        if (response['landing_name_used'] === 'yes') {
            warn.html("You already have a news page named '" + name + "'");
        } else if (response['landing_name_needed'] === 'yes') {
            warn.html("Please name your newspaper before building its content");
        } else if (response['landing_name_used'] === 'no') {
            warn.html('');
            input.attr('disabled',true);
            $('.create_new_newspaper_new_topic form input[name="landing_name"]').val(name);
            $('.create_new_newspaper_new_topic').removeClass('hidden');
        }
    };

    $.post('/check_landing_name.json',data,handler);
}

function createNewNewspaperAddTopic(evt) {
    evt.preventDefault();
    var form = $(evt.currentTarget).closest('form');

    var help = form.find('span.help-block');

    var data = {
        'media_type': 'text',
        'category': form.find('select[name="topic-category"]').val(),
        'country': form.find('select[name="topic-country"]').val(),
        'language': form.find('select[name="topic-language"]').val(),
        'new_landing_name': form.find('input[name="landing_name"]').val()
    };

    console.log(data);

    handler = function(response) {

        if (response['status'] != "ok") {
            help.html('Sorry, that topic is unsupported right now');
            return;
        }

        help.html('');

        $('.create_new_newspaper_topics').removeClass('hidden');

        $('.create_new_newspaper_topics table tbody').append(
            "<tr><td>" + response['category'] + "</td>" +
                "<td>" + response['language'] + "</td>" +
                "<td>" + response['country']  + "</td></tr>"
        );
    };

    $.post('/cautious_query_api.json', data, handler);
}

$(document).ready(function(){
    $('body').on('click','.create_new_newspaper',createNewNewspaper);
    $('body').on('click','.create_new_newspaper_new_topic button',createNewNewspaperAddTopic);
});

///////////////new_landing page creation button click counter/ id and name attribute counter/////////////

function addToStoryCount(evt){
    evt.preventDefault();
    STORY_COUNT = window.STORY_COUNT + 1;
    console.log(window.STORY_COUNT +  " This is the count in addToStoryCount");
}
$('#add_story').on('click', addToStoryCount);

console.log("This is makeing sure javascript is running" + window.STORY_COUNT);

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

function showAlertWarn($el,msg) {
    $el.html(
        '<div class="alert alert-warning alert-dismissible" role="alert">' +
          '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
          msg +
        '</div>'
    );
}

function showAlertSuccess($el,msg) {
    $el.html(
        '<div class="alert alert-success alert-dismissible" role="alert">' +
          '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
          msg +
        '</div>'
    );
}

// landing.html
function addStoryHtmlOnLanding(response){

    if(response['status'] != "ok"){
        var msg = "The Story Query for "+ response['category'] +" " + response['media_type'] + " news from " + response['country'] + " in the language " + response['language'] +" is not supported right now.";
        showAlertWarn($('#add_new_story_refill_alert'), msg);
    } else{

        ///// IS there a better more dynamic way to run this ?////// 
        console.log(response['landingname']);
        $('#add_new_story_refill_alert').html("");
        $('#add_new_story_refill_options').html( "<p> Press refresh to add new topic </p><br><a href=\"/yourlanding/"+response['landingname']+"\" ><button>Refresh With new topic</button></a> <br>"
        );

    }      
}

// landing.html
function createNewStoryForm(evt){
    evt.preventDefault();
    var btn= $(evt.currentTarget);
    var form = btn.closest('form');
    var landingname= form.find('input[name="hidden_landingname_add_story"]').val(); 
    var topic_count = form.find('input[name="hidden_count_add_story"]').val();

    $('#add_new_story_refill_alert').html("");
    $('#add_new_story_refill_options').html("");
    $('#add_new_story_refill_options').html(
        "<form>" + 
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
        "<p>Add this Topic</p>" +
        "<input id='hidden_story_count' type='hidden' name='story_count' value='"+ topic_count +"'>" + 
        "<input id='new_landing_name' type='hidden' name='new_landing_name' value= \""+ landingname +"\">" +      
        "<input id='add_story_to_a_landing' type='submit' id='keyword_txt_btn' name='keyword_txt_btn' value='Add this Topic'>"    +
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
            'media_type': 'text',
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
    $('#story_removed_flash').prepend("<p> The story " + response['title'] + " has been removed </p>");

}
function removeStoryFromSavedPages2(evt){
    //// I need help because this doesn't have the attributes?
    var id = $(this).attr("id");
    var url = $(this).attr("data-href");
    var title = $(this).attr('data-title');

    $(this).closest('li').remove();

    console.log(url);
    $.post('/unsaved_pages_two_catch',{'id_btn': id, 'url': url , 'title': title }, changeButton);
}

$('.unsave_btn_class_two').on('click', removeStoryFromSavedPages2);
