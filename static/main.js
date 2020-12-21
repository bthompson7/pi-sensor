function getTempData(){

 //1st temp sensor
 var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var tempData1 = JSON.parse(http.response);
      document.getElementById("temp-sensor-1").innerHTML = tempData1;
	console.log("RESPONSE = " + tempData1[0][0] + " " + tempData1[0][1]);
    }
  };

  http.open("GET", "/getTemp1");
  http.send();

  //2nd temp sensor
 var http2 = new XMLHttpRequest();
  http2.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var tempData2 = JSON.parse(http2.response)
      document.getElementById("temp-sensor-2").innerHTML = tempData2;
    }
  };

  http2.open("GET", "/getTemp2");
  http2.send();



}

getTempData();

//run the function every 5 minutes
setInterval(function(){
    getTempData();
}, 300000);
