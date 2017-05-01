var images = document.getElementsByClassName('dis');
for(var i=0;i<images.length;i++)
{
  images[i].style.opacity="0";
}

function disp(){
var step=1; // Change this step value
var y=document.getElementById('i1').offsetTop;
if(y < 120 ){y= y +step;
document.getElementById('i1').style.top= y + "px"; // vertical movment
my_time=setTimeout('disp()',10);
}
if(y==120)
  {
      for(var i=0;i<images.length;i++)
      {
        images[i].setAttribute( "style", "-webkit-transition: opacity 1s ease-in-out; -moz-transition: opacity 1s ease-in-out; -o-transition: opacity 1s ease-in-out; transition: opacity 1s ease-in-out;");
      }
  }
}
window.addEventListener("load", disp);
