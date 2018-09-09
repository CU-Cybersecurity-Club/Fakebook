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
  // Achievement
  try {
    // Weird logic here:
    // If it's not in a post, accessing 'player' will throw an error
    // This means players can't alert themselves
    attacker = player
    victim = getCookie('player')
    achieve(attacker, 'alert');
    if (attacker != victim) {
      achieve(victim, 'hit-by-alert');
    }
  } catch (e) {}

  old_alert.apply(window, arguments);
}

function achieve(player, id) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/achieve", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    player: player,
    id: id
  }));
}
