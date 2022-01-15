function getTempData(){
document.getElementById("temp-sensor-1").innerHTML = "Loading Data...";
document.getElementById("temp-sensor-2").innerHTML = "Loading Data...";

 //1st temp sensor
 var http = new XMLHttpRequest();
  http.onreadystatechange = function() {

    if (this.readyState == 4 && this.status == 200) {
      var tempData1 = JSON.parse(http.response);
      var tempValue = tempData1['temp'];
      var humidValue = tempData1['humid'];
      var unixTime = tempData1['last_updated'];
      var sensorInfoElement = document.getElementsByClassName("sensor-info-1")[0];

      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-1").innerHTML = stringToDisplay;

      document.getElementById("last-updated-1").innerHTML = "Last Updated: " + timeSince(unixTime);
      document.getElementById("hidden-time-1").innerHTML = unixTime;

    }else if(this.readyState == 4  && this.status != 200){

	console.error(http.response);
        document.getElementById("temp-sensor-1").innerHTML = http.response;
   }

  };

  http.open("GET", "/getTemp1");
  http.send();

  //2nd temp sensor
 var http2 = new XMLHttpRequest();
  http2.onreadystatechange = function() {

    if (this.readyState == 4 && this.status == 200) {
      var tempData2 = JSON.parse(http2.response)
      var tempValue = tempData2['temp'];
      var humidValue = tempData2['humid'];
      var dewPointValue = tempData2['dew_point']
      var unixTime  = tempData2['last_updated'];
      var sensorInfoElement = document.getElementsByClassName("sensor-info-2")[0];

      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-2").innerHTML = stringToDisplay;
      document.getElementById("last-updated-2").innerHTML = "Last Updated: " + timeSince(unixTime);
      document.getElementById("hidden-time-2").innerHTML = unixTime;


    }else if(this.readyState == 4 && this.status != 200){
	console.error(http2.response);
        document.getElementById("temp-sensor-2").innerHTML = http2.response;
    }


  };

  http2.open("GET", "/getTemp2");
  http2.send();



}


function getCurrentDate(){

var d = new Date();

var year = d.getFullYear();
var month = d.getMonth() + 1;
var dayOfMonth = d.getDate();

return year + "-" + month + "-" + dayOfMonth;


}

function currentTimeUnix(){
return Math.floor(new Date().getTime()/1000.0);

}

// Inital page load
getTempData();

setInterval(getTempData, 300000);
setInterval(renderTimeSince, 1000);

function renderTimeSince(unixTime) {
  var sensorTime1 = document.getElementById("hidden-time-1").innerHTML;
  var sensorTime2 = document.getElementById("hidden-time-2").innerHTML;
  document.getElementById("last-updated-1").innerHTML = "Last Updated: " + timeSince(sensorTime1);
  document.getElementById("last-updated-2").innerHTML = "Last Updated: " + timeSince(sensorTime2);
}

// Please ignore this disaster
function timeSince(date) {

  var seconds = Math.floor((new Date() - date) / 1000);
  var intervalType;

  var interval = Math.floor(seconds / 31536000);
  if (interval >= 1) {
    intervalType = 'year';
  } else {
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
      intervalType = 'month';
    } else {
      interval = Math.floor(seconds / 86400);
      if (interval >= 1) {
        intervalType = 'day';
      } else {
        interval = Math.floor(seconds / 3600);
        if (interval >= 1) {
          intervalType = "hour";
        } else {
          interval = Math.floor(seconds / 60);
          if (interval >= 1) {
            intervalType = "minute";
          } else {
            interval = seconds;
            intervalType = "second";
          }
        }
      }
    }
  }

   if (interval > 1 || interval === 0) {
    intervalType += 's ago';
  } else if (interval == 1) {
    intervalType += ' ago';
  }


  return interval + ' ' + intervalType;
}


function setCookie(cname,cvalue,exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
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
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
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


function darkMode(){
var isDarkMode = getCookie("mode");

if(isDarkMode === ""){
  console.log("creating cookie");
  setCookie("mode", "dark", 365);
  var element = document.body;
  element.classList.toggle("dark-mode");
}



if(isDarkMode == "light"){
  setCookie("mode", "dark", 365);
  var element = document.body;
  element.classList.toggle("dark-mode");

}else if(isDarkMode == "dark"){
  setCookie("mode", "light", 365);
   var element = document.body;
   element.classList.toggle("dark-mode");

}

console.log(isDarkMode);

}


function bodyLoadDarkMode(){

var isDarkMode = getCookie("mode");

if(isDarkMode == "dark"){
var element = document.body;
element.classList.toggle("dark-mode");

}


}

bodyLoadDarkMode();
