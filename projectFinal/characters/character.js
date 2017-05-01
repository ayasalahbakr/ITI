var textInput = document.getElementById('name');
var nxt = document.getElementById('nxt');
var gender_f = document.getElementById('f-radio');
var gender_m = document.getElementById('m-radio');
var gender_img_f = document.getElementById('female');
var gender_img_m = document.getElementById('male');

var playerInfo = [];
var playerNames;
var playerFound;

gender_img_f.addEventListener('click', function check_f() {
gender_f.setAttribute("checked", "checked");
gender_m.removeAttribute("checked");
});

gender_img_m.addEventListener('click', function check_m() {
gender_m.setAttribute("checked", "checked");
gender_f.removeAttribute("checked");
});

// Clicing on next button
nxt.onclick = function (e) {

  playerFound = false;

  playerInfo[0] = textInput.value;
  playerInfo[1] = document.querySelector('input[name="gender"]:checked').value;

  if(localStorage.Players)
  {
    playerNames = localStorage.Players.split(",");

    for (var i in playerNames) {
      if (playerInfo[0] == playerNames[i]) {
        playerFound = true;
        break;
      }
    }
  }

  if (playerFound != true) {
    localStorage.setItem(playerInfo[0],playerInfo);
    playerNames.push(playerInfo[0]);
    localStorage.setItem("Players",playerNames);
    playerFound = false;
  }

};

// Function to load players
function loadPlayers(){
  if(localStorage.Players) {
    playerNames = localStorage.Players.split(",");
  }
  else {
    playerNames = [];
  }
}

loadPlayers();
