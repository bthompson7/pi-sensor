function getTempData(){
document.getElementById("temp-sensor-1").innerHTML = "Loading...";
document.getElementById("temp-sensor-2").innerHTML = "Loading...";

 //1st temp sensor
 var http = new XMLHttpRequest();
  http.onreadystatechange = function() {

    if (this.readyState == 4 && this.status == 200) {
      var tempData1 = JSON.parse(http.response);
      var tempValue = tempData1['temp'];
      var humidValue = tempData1['humid'];
      var date = tempData1['last_updated'];

      var sensorInfoElement = document.getElementsByClassName("sensor-info-1")[0];

	   console.log(currentTimeUnix() - date);
 	   if(currentTimeUnix() - date >= 3600){ //3600 is one hour in unix time https://www.epochconverter.com/
	     console.log("Data is an hour old.");
	    sensorInfoElement.hidden = true;
    	   }else{
              console.log("data is up to date");

              if(sensorInfoElement.hidden){
		sensorInfoElement.hidden = false;
               }
     	      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      	      document.getElementById("temp-sensor-1").innerHTML = stringToDisplay;
       	   }


    }else if(this.readyState == 4  && this.status != 200){

	console.log("error = " + http.response);
	var error = JSON.parse(http.response);
        document.getElementById("temp-sensor-1").innerHTML = error[0];
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
      var date = tempData2['last_updated'];

        var sensorInfoElement = document.getElementsByClassName("sensor-info-2")[0];

	   console.log(currentTimeUnix() - date);
           if(currentTimeUnix() - date >= 3600){ //3600 is one hour in unix time https://www.epochconverter.com/
            console.log("Data is an hour old.");
            sensorInfoElement.hidden = true;
           }else{
              console.log("data is up to date");

              if(sensorInfoElement.hidden){
                sensorInfoElement.hidden = false;
               }
              var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
              document.getElementById("temp-sensor-2").innerHTML = stringToDisplay;
           }


    }else if(this.readyState == 4 && this.status != 200){
	console.log("error = " + http2.response);
	var error = JSON.parse(http2.response);
        document.getElementById("temp-sensor-2").innerHTML = error[0];
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


getTempData();

setInterval(function(){
    getTempData();
}, 300000);



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
