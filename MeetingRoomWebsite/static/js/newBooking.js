function start(){
  document.getElementById("progress").style.visibility = "visible";
  create_post('no',$('#name').val());

}

function create_post(outside,username) {
    var urlLink = "/"+username + "/new/";
    if(outside == 'yes'){
      var today = new Date();
      today.setHours(0,0,0,0)
      var mm = (today.getMonth()+1 > 9 ? '' : '0') + (today.getMonth()+1);
      var dd= (today.getDate() > 9 ? '' : '0') + today.getDate();
      var date = today.getFullYear() + "-" + mm + "-" + dd;
      document.getElementById("error").style.visibility = "hidden";
      $('#title_booking').text("All Avaiable Bookings for Today");
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
        document.getElementById("error").style.visibility = "visible";
        $('#error').html("<h4 style=\"color:red\">Pick a date from today onwards</div>");
        return
      }
      document.getElementById("error").style.visibility = "hidden";
      $('#title_booking').text("All Available Bookings on " + $('#date').val())

    }

    $.ajax({
          url : urlLink, // the endpoint
          type : "POST", // http method
          data : { "date" : date, "room" : '0' }, // data sent with the post request

          // handle a successful response
          success : function(json) {
            console.log(json); // log the returned json to the console
            makeTable(json,outside)
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#error').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
};

function makeTable(json,outside){
  if(outside == 'yes'){
    var d = new Date();
  }
  else{
    var d = new Date($('#date').val());
  }
  var textRoom1 = '';
  var textRoom2 = '';
  var textRoom3 = '';
  var textRoom4 = '';
  var popups = '';
  var script1 = '';
  var script2 = 'window.onclick = function(event) {';
  var mm = (d.getMonth()+1 > 9 ? '' : '0') + (d.getMonth()+1);
  var dd= (d.getDate() > 9 ? '' : '0') + d.getDate();
  var date = d.getFullYear()+ mm + dd;
  $('#l1').text('');
  $('#l2').text('');
  $('#l3').text('');
  $('#l4').text('');
  $('#popups').text('');
  $('#script').text('');
  var availableRoom1 = json.room1;
  var availableRoom2 = json.room2;
  var availableRoom3 = json.room3;
  var availableRoom4 = json.room4;
  var allTimings = ["08:00:00","08:30:00","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00", "16:30:00", "17:00:00","17:30:00"];
  var arrayLength = allTimings.length;
  for (var i = 0; i < arrayLength; i++) {
      if(availableRoom1.includes(allTimings[i])){
        textRoom1 += "<li class=\"list\"><a class=\"available\" onclick=\"document.getElementById('" +allTimings[i]+ "_1').style.display='block'\">" + allTimings[i] + "</a></li>";
        popups += "<div id=\""+ allTimings[i] + "_1\" class=\"modal_form\"><form class=\"modal-content animate\" action=\"/"+$('#name').val()+"/new/1/" +date+"/"+allTimings[i].replace(/:/g , "") + "\" method=\"get\"><div class=\"container\"><p>You are about to make a booking on " + $('#date').val() +" at "+ allTimings[i] +" in Room 1. Enter the number of people below and press confirm to make the booking</p><label><b>Number of people</b></label><input type=\"number\" placeholder=\"Enter Number of people\" min=\"1\" max=\"10\" name=\"capacity\" required><button type=\"submit\">Confirm</button></div><div class=\"container\"><button type=\"button\" onclick=\"document.getElementById('"+ allTimings[i] +"_1').style.display='none'\" class=\"cancelbtn\">Cancel</button></div></form></div>"
        script1 += "var one_" + i +" = document.getElementById(\""+allTimings[i]+"_1\");"
        script2 += "if (event.target == one_" + i + ") { one_" + i + ".style.display = \"none\"};"
      }
      else{
        textRoom1 += "<li class=\"list\"><a class=\"busy\">" + allTimings[i] + "</a></li>";
      }
      if(availableRoom2.includes(allTimings[i])){
        textRoom2 += "<li class=\"list\"><a class=\"available\" onclick=\"document.getElementById('" +allTimings[i]+ "_2').style.display='block'\">"  + allTimings[i] + "</a></li>";
        popups += "<div id=\""+ allTimings[i] + "_2\" class=\"modal_form\"><form class=\"modal-content animate\" action=\"/"+$('#name').val()+"/new/2/" +date+"/"+allTimings[i].replace(/:/g , "") + "\" method=\"get\"><div class=\"container\"><p>You are about to make a booking on " + $('#date').val() +" at "+ allTimings[i] +" in Room 2. Enter the number of people below and press confirm to make the booking</p><label><b>Number of people</b></label><input type=\"number\" placeholder=\"Enter Number of people\" min=\"1\" max=\"15\" name=\"capacity\" required><button type=\"submit\">Confirm</button></div><div class=\"container\"><button type=\"button\" onclick=\"document.getElementById('"+ allTimings[i] +"_2').style.display='none'\" class=\"cancelbtn\">Cancel</button></div></form></div>"
        script1 += "var two_" + i +" = document.getElementById(\""+allTimings[i]+"_2\");"
        script2 += "if (event.target == two_" + i + ") { two_" + i + ".style.display = \"none\"};"
      }
      else{
        textRoom2 += "<li class=\"list\"><a class=\"busy\">" + allTimings[i] + "</a></li>";
      }
      if(availableRoom3.includes(allTimings[i])){
        textRoom3 += "<li class=\"list\"><a class=\"available\" onclick=\"document.getElementById('" +allTimings[i]+ "_3').style.display='block'\">"  + allTimings[i] + "</a></li>";
        popups += "<div id=\""+ allTimings[i] + "_3\" class=\"modal_form\"><form class=\"modal-content animate\" action=\"/"+$('#name').val()+"/new/3/" +date+"/"+allTimings[i].replace(/:/g , "") + "\" method=\"get\"><div class=\"container\"><p>You are about to make a booking on " + $('#date').val() +" at "+ allTimings[i] +" in Room 3. Enter the number of people below and press confirm to make the booking</p><label><b>Number of people</b></label><input type=\"number\" placeholder=\"Enter Number of people\" min=\"1\" max=\"5\" name=\"capacity\" required><button type=\"submit\">Confirm</button></div><div class=\"container\"><button type=\"button\" onclick=\"document.getElementById('"+ allTimings[i] +"_3').style.display='none'\" class=\"cancelbtn\">Cancel</button></div></form></div>"
        script1 += "var three_" + i +" = document.getElementById(\""+allTimings[i]+"_3\");"
        script2 += "if (event.target == three_" + i + ") { three_" + i + ".style.display = \"none\"};"
      }
      else{
        textRoom3 += "<li class=\"list\"><a class=\"busy\">" + allTimings[i] + "</a></li>";
      }
      if(availableRoom4.includes(allTimings[i])){
        textRoom4 += "<li class=\"list\"><a class=\"available\" onclick=\"document.getElementById('" +allTimings[i]+ "_4').style.display='block'\">"  + allTimings[i] + "</a></li>";
        popups += "<div id=\""+ allTimings[i] + "_4\" class=\"modal_form\"><form class=\"modal-content animate\" action=\"/"+$('#name').val()+"/new/4/" +date+"/"+allTimings[i].replace(/:/g , "") + "\" method=\"get\"><div class=\"container\"><p>You are about to make a booking on " + $('#date').val() +" at "+ allTimings[i] +" in Room 4. Enter the number of people below and press confirm to make the booking</p><label><b>Number of people</b></label><input type=\"number\" placeholder=\"Enter Number of people\" min=\"1\" max=\"20\" name=\"capacity\" required><button type=\"submit\">Confirm</button></div><div class=\"container\"><button type=\"button\" onclick=\"document.getElementById('"+ allTimings[i] +"_4').style.display='none'\" class=\"cancelbtn\">Cancel</button></div></form></div>"
        script1 += "var four_" + i +" = document.getElementById(\""+allTimings[i]+"_4\");"
        script2 += "if (event.target == four_" + i + ") { four_" + i + ".style.display = \"none\"};"
      }
      else{
        textRoom4 += "<li class=\"list\"><a class=\"busy\">" + allTimings[i] + "</a></li>";
      }
  }
  $('#l1').append(textRoom1);
  $('#l2').append(textRoom2);
  $('#l3').append(textRoom3);
  $('#l4').append(textRoom4);
  $('#popups').append(popups);
  script2 += "}"
  script = "<script>" + script1 +" " + script2 + "</script>"
  $('#script').append(script);
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
