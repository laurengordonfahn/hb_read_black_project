"use strict";
var passwordtext = $('#explain_password').data('password');
//"Passwords must contain at least 6 characters."
//////////////////// 
function showStories(response){

        $("#results").html("");
        console.log(response);
        
           //figure out how to make this image just appear
        for (var i =0; i < response["articles"].length; i++){
             console.log(i);
           $("#results").append(
            //works but not what I want
           "<iframe id=\"theFrame\" src= "+ "'"+ response["articles"][i]["url"] + "'"+ "style='width:100%;'frameborder='0'></iframe>" +
//              "<a href='http://twitter.github.io/bootstrap/' class='btn bootpopup' title='This is title' target='popupModal2'>Open modal</a>

// <div id='popupModal2' class='modal hide fade' tabindex='-1' role='dialog'>
//     <div class='modal-header'>
//         <button type='button' class='close' data-dismiss='modal'>"+ response["articles"][i]["url"] +"</button>
//             <h3>Title</h3>
//     </div>
//     <div class='modal-body'>
//       <iframe src='' style='zoom:0.60' frameborder='5' height='350' width='99.6%''></iframe>
//     </div>
//     <div class='modal-footer'>
//         <button class='btn' data-dismiss='modal'>OK</button>
//     </div>
// </div>
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

////////////////////

var story_count = 1;

function addStoryHtml(evt){
    evt.preventDefault();

    // (var index=1, ,'click', i++){
    //     $(".category").addClass(story_count)
    // }
    //CHANGE THIS SO THE NAME VALUE IS DIFFERENT
    $(".add_story_div").html(
        "<p>Type</p>
        <select  name='type-'"+ story_count +">
            <option value='text'> Text </option>
            <!-- <option value='audio'> Audio </option>
            <option value='video'> Video </option> -->
        </select>
        <p> ALL OF OUR TEXT IS SOURCED BY NEWS API *** FINISH THE INFO THEY ASK FOR HERE***</p>
        <br>
    
        <p> Topic Category </p>
        <select id = 'category-' "+ story_count + " name='category'>
            <option value='business'> Business </option>
            <option value='entertainment'> Entertainment </option>
            <option value='gaming'>Gaming </option>
            <option value='general'>General </option>
            <option value='music'> Music</option>
            <option value='science-and-nature'> Science-and-Nature </option>
            <option value='technology'> Technology</option>
        </select>
        <br>

        <!-- TEST OUT SOME DAY HAVING MORE THAN ONE can also add country -->
        <p>Language</p>
        <select id = 'language-'" + story_count+ " name='language'>
            <option value = 'en'>English</option>
            <option value = 'de'>German</option>
            <option value = 'fr'>French</option>
            <option value = 'all'> All</option>
        </select>
        <br>
        <!-- AT SOME POINT CHOSE MULTIPLE PLACES -->
        <p>Country</p>
        <select id = 'country-' " +  story_count + " name='country' +{{ index }} >
            <option value = 'au'> Austraila</option>
            <option value = 'de'>Germany</option>
            <option value = 'gb'>Great Britian</option>
            <option value = 'in'>India</option>
            <option value = 'it'>Italy</option>
            <option value = 'us'>United States</option>
        </select>
        <br>

        <div class='add_story_div'></div>
        
        <input type='submit' name='keyword_txt_btn' value='Submit'>
    </form>
    <br>");

    story_count ++
}

$("#add_story").on('click', addStoryHtml);

////////////////////
// function submit_landing(){
//     $("keyword_txt_btn").on("submit", )
// }
// function processAllForm(evt){
//     evt.preventDefault();

//     var formInputs = { 
//         "index": story_count,
//         "story"=[]
//     };

//     for(i = 0; i < range(story_count + 1); i++){
            
//         var topic_dictionary = { "type": $("#type-" +i).val(),
//             "category": $("category-" + i).val() ,
//             "language": $("language-"+ i).val() ,
//             "country": $("country-" +i).val()
//         };
//         story.push(topic_dictionary);
//     }

//     $.post('/new_landing_catch', formInputs, submit_landing);
// }

// $('#keyword_txt_btn').on('click', processAllForm)

function addHiddenCount(){
    $('#add_story').html(story_count);
}
$('#add_story').on('click', addHiddenCount)

//     $('.bootpopup').click(function(){
//   var frametarget = $(this).attr('href');
//   var targetmodal = $(this).attr('target');
//   if (targetmodal == undefined) {
//     targetmodal = '#popupModal';
//   } else { 
//     targetmodal = '#'+targetmodal;
//   }
//   if ($(this).attr('title') != undefined) {
//     $(targetmodal+ ' .modal-header h3').html($(this).attr('title'));
//     $(targetmodal+' .modal-header').show();
//   } else {
//      $(targetmodal+' .modal-header h3').html('');
//     $(targetmodal+' .modal-header').hide();
//   }  
//     $(targetmodal).on('show', function () {
//         $('iframe').attr("src", frametarget );   
//     });
//     $(targetmodal).modal({show:true});
//   return false;

// });