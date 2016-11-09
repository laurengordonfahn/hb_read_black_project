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