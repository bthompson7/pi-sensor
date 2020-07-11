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
         localStorage.setItem('refresh', true);
         var timer = setTimeout('startTimer();', 120);
  }else {
        localStorage.setItem('refresh',false);
        clearTimeout(countdownTimer);
        timer.style.display = "none";
  }
})

$(document).ready(function() {
        var timer = document.getElementById('timer');
        if(localStorage.getItem('refresh') === "true"){
            var timer = setTimeout('startTimer();', 120);
            document.querySelector('#chkRefresh').checked = true
        }else{
             localStorage.setItem('refresh', false);
             document.querySelector('#chkRefresh').checked = false;
             clearTimeout(countdownTimer);
	     timer.style.display = "none";
         }
});
