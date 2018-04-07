/*
 *  This is code for the CTF. It's not part of the game.
 *  You can probably hack it, but it's not really in the spirit of things.
 */

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

old_alert = alert;
alert = function() {
  console.log("Called alert with:");
  console.log(arguments);
  console.log(old_alert)
  console.log(alert)
  old_alert.apply(window, arguments);
}
