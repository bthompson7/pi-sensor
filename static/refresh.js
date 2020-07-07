var btn = document.getElementById('chkRefresh');
var countdownTimer;
var timer = document.getElementById('timer');

function startTimer(chkRefresh) {
    var numOfSeconds = 300; 
    timer.style.display = "block";
    countdownTimer = setInterval(function() {
        numOfSeconds = numOfSeconds - 1;
        timer.textContent = "Refreshing in " + numOfSeconds + " seconds";
		 if (numOfSeconds <= 0) {
                   timer.textContent = "Updating...";
		   location.reload(); 
                   timer.style.display =  "block";
		   clearInterval(countdownTimer);
		   startTimer(chkRefresh);
        }   
    }, 1000);
}


$('#chkRefresh').click(function(e){
        var timer = document.getElementById('timer');
	if(e.target.checked) {
  	localStorage.checked = true;
         var timer = setTimeout('startTimer();', 120);
  } else {
  	localStorage.checked = false;
        clearTimeout(countdownTimer);
        timer.style.display = "none";
  }
})

$( document ).ready(function() {
        var timer = document.getElementById('timer');
	document.querySelector('#chkRefresh').checked = localStorage.checked
        console.log(btn.checked)
        if(btn.checked){
            var timer = setTimeout('startTimer();', 120);
        }else{
             localStorage.checked = false;
             clearTimeout(countdownTimer);
	     timer.style.display = "none";
         }
});
