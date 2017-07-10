function display_c(){
  var refresh=1000; // Refresh rate in milli seconds
  mytime=setTimeout('display_ct()',refresh)
}
function display_ct() {
  var strcount;
  var x = new Date();
  var x1= x.getDate() + "/" + x.getMonth() + "/" +  x.getFullYear();
  x1 = x1 + " - " + x.getHours( )+ ":" + x.getMinutes() + ":" + x.getSeconds();
  document.getElementById('ct').innerHTML = x1;
  document.getElementById('ct').style.fontSize='24px';
  tt=display_c();
}
