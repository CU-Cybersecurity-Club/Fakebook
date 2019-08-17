function openNav() {
  document.getElementById("ctf-toggle").onclick = closeNav
  document.getElementById("ctf-toggle").innerHTML = "&#8249;"
  document.getElementById("ctf-dashboard").style.marginLeft = "0";
  document.getElementById("overlay").style.background = "#000B";
  document.getElementById("overlay").style.pointerEvents = undefined;
  document.getElementById("ctf-player").value = getCookie('player');
}

function closeNav() {
  document.getElementById("ctf-toggle").onclick = openNav
  document.getElementById("ctf-toggle").innerHTML = "&#8250;"
  document.getElementById("ctf-dashboard").style.marginLeft = "-370px";
  document.getElementById("overlay").style.background = "#0000";
  document.getElementById("overlay").style.pointerEvents = "none";
  var player = document.getElementById("ctf-player").value;
  achieve(player, 'created-account');
}

function disableDashboard() {
  document.getElementById("ctf-links").style.color = "#555";
  document.getElementById("ctf-toggle").style.color = "#555";
  document.getElementById("ctf-links").style.pointerEvents = "none";
  document.getElementById("ctf-toggle").style.pointerEvents = "none";
}

function enableDashboard() {
  document.getElementById("ctf-links").style.color = "#FFF";
  document.getElementById("ctf-toggle").style.color = "#FFF";
  document.getElementById("ctf-links").style.pointerEvents = "";
  document.getElementById("ctf-toggle").style.pointerEvents = "";
}

function onPlayerKey(ele) {
  if(!ele.value) {
    disableDashboard();
  }
  else {
    setCookie('player', ele.value, 7);
    enableDashboard();
  }
}

var player = getCookie('player');
if(!player) {
  disableDashboard();
  openNav();
}
else {
	achieve(player, 'created-account');
}
