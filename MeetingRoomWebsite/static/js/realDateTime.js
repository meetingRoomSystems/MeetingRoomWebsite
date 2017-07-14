function display_c(){
  var refresh=1000; // Refresh rate in milli seconds
  mytime=setTimeout('display_ct()',refresh)
}
function display_ct() {
  var strcount;
  var x = new Date();
  var mm = (x.getMonth()+1 > 9 ? '' : '0') + (x.getMonth()+1);
  var dd= (x.getDate() > 9 ? '' : '0') + x.getDate();
  var x1= dd + "/" + mm + "/" +  x.getFullYear();

  var hh = (x.getHours() > 9 ? '' : '0') + (x.getHours());
  var m = (x.getMinutes() > 9 ? '' : '0') + (x.getMinutes());
  var ss = (x.getSeconds() > 9 ? '' : '0') + (x.getSeconds());
  var x2 = hh + ":" + m + ":" + ss;
  var dateTime = x1 + " - " + x2;
  document.getElementById('ct').innerHTML = dateTime;
  document.getElementById('ct').style.fontSize='16px';
  tt=display_c();
}
