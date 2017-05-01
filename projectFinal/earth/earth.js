// Global Variables
var imgSrc;
var pureName;
var userInputValue;
var imgArray = [];
var imgName = [];
var imgToHide = [];

var correctLetters=0;
var wrongLetters=0;
var totalTry=0;
var accuracy=0;

var factVar = "earthFact1";
var text;
var possible;
var left;
var x;

var step=2.5;
var p=document.getElementById("inptdiv");


//Generate Random Characters
function myFunction() {
   text = "";
   possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

   text = possible.charAt(Math.floor(Math.random() * possible.length));
   left=Math.random();
   left *= 90;

    x = document.createElement("img");
    x.setAttribute("src", factVar+text+".png");
    x.setAttribute("name", factVar+text);
    x.setAttribute("width", "100px");
    x.setAttribute("height", "100px");

    x.style.position="absolute";
    x.style.left=left+"%";
    x.style.top="0%";
    document.body.appendChild(x);
    return x;
}

// this function is used to display images with movment
function disp(f)
{
  step; // to increase generated images speed ex: 3 , 5

  var y=f.offsetTop;
  if(y < 300 )
  {
      y= y +step;
      my_time=setTimeout(function() {disp(f)},10);
      f.style.top= y + "px"; // vertical movment
  }

  if(y == 300)
    {
      var image_x = f;
      image_x.parentNode.removeChild(image_x);
    }

  }


// Function to hide images
  function hideImages()
  {
    imgArray = document.getElementsByTagName("img");

    // this loop is used to get pure name of images
    for (var i = 0; i < imgArray.length; i++) {
    imgSrc = imgArray[i].src;
    imgSrc = imgSrc.replace(/^.*[\\\/]/, '');
    pureName = imgSrc.split('.');
    imgName[i] = pureName[0];
  }

    // this loop is used to hide images according to user input
    for (var x = 0; x < imgArray.length; x++) {
    userInputValue = document.getElementById("userInput").value.toUpperCase();
    userInputValue =  factVar + userInputValue;

      if (userInputValue == imgName[x]) {
        imgToHide = document.getElementsByName(userInputValue);

        for (var n = 0; n < imgToHide.length; n++) {
          imgToHide[n].parentNode.removeChild(imgToHide[n]);
          correctLetters++;
        } // End For
      } // End If
    }

    totalTry++;
    wrongLetters = totalTry - correctLetters;
    console.log("Correct = " + correctLetters);
    console.log("Total = " + totalTry);
    console.log("Wrong = " + wrongLetters);
    console.log("Accuracy = " + (correctLetters/totalTry) * 100 + "%");
    p.textContent="Correct: "+correctLetters+ '\xa0\xa0\xa0\xa0\xa0\xa0\xa0' +" Wrong: "+wrongLetters;

    switch (correctLetters) {
      case 10:
        step+=.25;
        console.log("Current Speed = " + step);
      break;
      case 20:
        step+=.25;
        console.log("Current Speed = " + step);
        // console.log("Fact 1");
        fact1PopUp();
        factVar = "earthFact2";
      break;
      case 40:
        step+=.25;
        console.log("Current Speed = " + step);
      break;
      case 50:
        step+=.25;
        console.log("Current Speed = " + step);
        // console.log("Fact 2");
        fact2PopUp();
      break;
    }

    switch (wrongLetters) {
      case 10:
      // alert("Game Over")
      gameOverPopUp();
      break;
    }

    userInputValue="";
    userInput.value = userInputValue;
  }

// this is used to generate images
window.addEventListener("load", function() {
    var f = myFunction();
    disp(f);
    setInterval(function () {
    f=myFunction();
    disp(f);}, 1000);
});

// calling hide images functions
userInput.addEventListener("keyup",hideImages);

//pop up
function gameOverPopUp() {
  // Get the modal
  var modal = document.getElementById('gameover');
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
      modal.style.display = "none";
      window.location="../levels/levels.html";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
          window.location="../levels/levels.html";

      }
  }
}

function fact1PopUp() {
  // Get the modal
  var modal = document.getElementById('fact1');
  // Get the <span> element that closes the modal
  var span1 = document.getElementsByClassName("close")[0];
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span1.onclick = function() {
      modal.style.display = "none";
      window.location="../levels/levels.html";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }
}


function fact2PopUp() {
  // Get the modal
  var modal = document.getElementById('fact2');
  // Get the <span> element that closes the modal
  var span2 = document.getElementsByClassName("close")[0];
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span2.onclick = function() {
      modal.style.display = "none";
      window.location="../levels/levels.html";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
          window.location="../levels/levels.html";

      }
  }
}
