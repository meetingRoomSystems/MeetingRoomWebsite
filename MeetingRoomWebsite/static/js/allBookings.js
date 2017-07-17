// this function is called from allBooking.html when the user selects a date
function start(){
  // checks if user has selected a date or  not
  if($('#date').val() == ''){
    create_post('yes',$('#name').val());
  }
  else{
    $("#results").fadeOut(50);
    document.getElementById("progress").style.visibility = "visible";
    create_post('no',$('#name').val());
  }
}

// function to make a ajax call to get bookings in json format
function create_post(outside,username) {
    var urlLink = "/"+username + "/all";
    // check if call made from rooms.html or allBooking.html
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
    // make ajax call
    $.ajax({
          url : urlLink, // the endpoint
          type : "POST", // http method
          data : { "date" : date }, // data sent with the post request

          // handle a successful response
          success : function(json) {
            console.log(date);
            console.log(json); // log the returned json to the console
            console.log("success");
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

// parse the json response and append to allBookings.html
function makeTable(json){
  var response;
  var content1 = '';
  var content2 = '';
  var content3 = '';
  var content4 = '';
  $("#rm1").text('');
  $("#rm2").text('');
  $("#rm3").text('');
  $("#rm4").text('');
  if(json.rm1.length == 0){
    // add the html code inside the div with id rm1.
    content1 +="<div class=\"col s12 m3\"><div class=\"card-panel red lighten-1 hoverable\"><span class=\"white-text\"><b>No bookings in room 1</b></span></div></div>"
    $('#rm1').append(content1);
  }
  else{
    for (i = 0; i < json.rm1.length; i++) {
      response = json.rm1[i];
      content1 += "<div class=\"col s12 m3\"><div style=\"display: inline-block;\"><div class=\"card-panel teal hoverable\"><span class=\"white-text\"><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start + " - "+ response.booking_end + "<br><b>Duration</b> : "+ response.duration + " minutes<br>Meeting is with "+response.capacity + " people</span></div></div></div>"
    }
    $('#rm1').append(content1);
  }
  if(json.rm2.length == 0){
    content2 +="<div class=\"col s12 m3\"><div class=\"card-panel red lighten-1 hoverable\"><span class=\"white-text\"><b>No bookings in room 2</b></span></div></div>"
    $('#rm2').append(content2);
  }
  else{
    for (i = 0; i < json.rm2.length; i++) {
      response = json.rm2[i];
      content2 += "<div class=\"col s12 m3\"><div style=\"display: inline-block;\"><div class=\"card-panel teal hoverable\"><span class=\"white-text\"><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start + " - "+ response.booking_end + "<br><b>Duration</b> : "+ response.duration + " minutes<br>Meeting is with "+response.capacity + " people</span></div></div></div>"
    }
    $('#rm2').append(content2);
  }

  if(json.rm3.length == 0){
    content3 +="<div class=\"col s12 m3\"><div class=\"card-panel red lighten-1 hoverable\"><span class=\"white-text\"><b>No bookings in room 3</b></span></div></div>"
    $('#rm3').append(content3);
  }
  else{
    for (i = 0; i < json.rm3.length; i++) {
      response = json.rm3[i];
      content3 += "<div class=\"col s12 m3\"><div style=\"display: inline-block;\"><div class=\"card-panel teal hoverable\"><span class=\"white-text\"><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start + " - "+ response.booking_end + "<br><b>Duration</b> : "+ response.duration + " minutes<br>Meeting is with "+response.capacity + " people</span></div></div></div>"
    }
    $('#rm3').append(content3);
  }

  if(json.rm4.length == 0){
    content4 +="<div class=\"col s12 m3\"><div class=\"card-panel red lighten-1 hoverable\"><span class=\"white-text\"><b>No bookings in room 4</b></span></div></div>"
    $('#rm4').append(content4);
  }
  else{
    for (i = 0; i < json.rm4.length; i++) {
      response = json.rm4[i];
      content4 += "<div class=\"col s12 m3\"><div style=\"display: inline-block;\"><div class=\"card-panel teal hoverable\"><span class=\"white-text\"><b>By</b> : " + response.fullname + "<br><b>Time</b> : " + response.booking_start + " - "+ response.booking_end + "<br><b>Duration</b> : "+ response.duration + " minutes<br>Meeting is with "+response.capacity + " people</span></div></div></div>"
    }
    $('#rm4').append(content4);
  }


  document.getElementById("progress").style.visibility = "hidden";
  $("#results").fadeIn(2000);

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
