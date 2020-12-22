function getTempData(){
document.getElementById("temp-sensor-1").innerHTML = "Loading...";
document.getElementById("temp-sensor-2").innerHTML = "Loading...";

 //1st temp sensor
 var http = new XMLHttpRequest();
  http.onreadystatechange = function() {

    if (this.readyState == 4 && this.status == 200) {
      var tempData1 = JSON.parse(http.response);
      var tempValue = tempData1[0][0];
      var humidValue = tempData1[0][1];
      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-1").innerHTML = stringToDisplay;
    }else if(this.readyState == 4  && this.status != 200){
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
      var tempValue = tempData2[0][0];
      var humidValue = tempData2[0][1];
      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-2").innerHTML = stringToDisplay;
    }else if(this.readyState == 4 && this.status != 200){
	var error = JSON.parse(http2.response);
        document.getElementById("temp-sensor-2").innerHTML = error[0];
    }


  };

  http2.open("GET", "/getTemp2");
  http2.send();



}

getTempData();

setInterval(function(){
    getTempData();
}, 300000);
