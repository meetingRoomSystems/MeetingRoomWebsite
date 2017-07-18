function start(){
  $("#results").fadeOut(50);
  document.getElementById("progress").style.visibility = "visible";
  create_post('no',$('#name').val());
}

function create_post(outside,username) {
    var urlLink = "/"+username + "/all";
    if(outside == 'yes'){
      var today = new Date();
      var mm = (today.getMonth()+1 > 9 ? '' : '0') + (today.getMonth()+1);
      var dd= (today.getDate() > 9 ? '' : '0') + today.getDate();
      var date = today.getFullYear() + "-" + mm + "-" + dd;
      document.getElementById("error").style.visibility = "hidden";
      $('#title_booking').text("All bookings for today");

    }
    else{
      var today = new Date();
      today.setHours(0,0,0,0)
      var d = new Date($('#date').val());
      var mm = (d.getMonth()+1 > 9 ? '' : '0') + (d.getMonth()+1);
      var dd= (d.getDate() > 9 ? '' : '0') + d.getDate();
      var date = d.getFullYear() + "-" + mm + "-" + dd;
      if(today>d){
        $("#results").fadeOut();
        document.getElementById("progress").style.visibility = "hidden";
        document.getElementById("error").style.visibility = "visible";
        $('#error').html("<h4 style=\"color:red\">Pick a date from today onwards</div>");
        return
      }
      document.getElementById("error").style.visibility = "hidden";
      if(today.getTime() === d.getTime()){
        $('#title_booking').text("All Bookings for Today")
      }
      else{
        $('#title_booking').text("All Bookings on " + $('#date').val())
      }
    }

    $.ajax({
          url : urlLink, // the endpoint
          type : "POST", // http method
          data : { "date" : date }, // data sent with the post request

          // handle a successful response
          success : function(json) {
            console.log(date);
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            makeTable(json)
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#error').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
};

function makeTable(json){
  console.log(json.bookings)
  var response;
  var content = '';
  $("#booking_results").text('');

  if(json.bookings == "[]"){
    content +="<h4 style=\"font-size:30px\">No Bookings for any rooms</h4>"
    $('#booking_results').append(content);
    document.getElementById("progress").style.visibility = "hidden";
    $("#results").fadeIn(2000);
  }
  else{
    for (i = 0; i < json.bookings.length; i++) {
      response = json.bookings[i];
      if(response.room == "1"){
        content += "<div class=\"col s12 m6\"><div class=\"card horizontal hoverable z-depth-5\"><div class=\"card-image\"><img src=\"../static/room1.jpg\"></div><div class=\"card-stacked\"><div class=\"card-content\"><p><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start  + " - " + response.booking_end + " ( " + response.duration + " mins )<br><b>Room</b> : "+ response.room + "<br>Meeting is with " + response.capacity +" people</p></div></div></div></div>"
      }
      else if(response.room == "2"){
        content += "<div class=\"col s12 m6\"><div class=\"card horizontal hoverable z-depth-5\"><div class=\"card-image\"><img src=\"../static/room2.jpg\"></div><div class=\"card-stacked\"><div class=\"card-content\"><p><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start  + " - " + response.booking_end + " ( " + response.duration + " mins )<br><b>Room</b> : "+ response.room + "<br>Meeting is with " + response.capacity +" people</p></div></div></div></div>"
      }
      else if(response.room == "3"){
        content += "<div class=\"col s12 m6\"><div class=\"card horizontal hoverable z-depth-5\"><div class=\"card-image\"><img src=\"../static/room3.jpg\"></div><div class=\"card-stacked\"><div class=\"card-content\"><p><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start  + " - " + response.booking_end + " ( " + response.duration + " mins )<br><b>Room</b> : "+ response.room + "<br>Meeting is with " + response.capacity +" people</p></div></div></div></div>"
      }
      else if(response.room == "4"){
        content += "<div class=\"col s12 m6\"><div class=\"card horizontal hoverable z-depth-5\"><div class=\"card-image\"><img src=\"../static/room4.jpg\"></div><div class=\"card-stacked\"><div class=\"card-content\"><p><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start  + " - " + response.booking_end + " ( " + response.duration + " mins )<br><b>Room</b> : "+ response.room + "<br>Meeting is with " + response.capacity +" people</p></div></div></div></div>"
      }

    }
    $('#booking_results').append(content);
    document.getElementById("progress").style.visibility = "hidden";
    $("#results").fadeIn(2000);
  }


}

$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
