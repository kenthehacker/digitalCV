// Displays calendar alert
function checkAlert(){
    var currentTime = new Date().toLocaleString();
    var currMonth = currentTime.substring(0,1);
    if (currentTime.substring(1,2)=="/"){
        currentTime = "0"+currentTime;
    }
    currMonth=currentTime.substring(0,2);
    var currDay = currentTime.substring(3,5);
    var currYear = currentTime.substring(6,10);

    var shifter = 0;
    var tempTime = currentTime.substring(12,currentTime.length);
    if (tempTime.substring(1,2)==":"){
        tempTime = "0"+tempTime;
    }
    var currHour = tempTime.substring(0,2);
    var currMin = tempTime.substring(3,5);

    var xmlhttp = new XMLHttpRequest();
      var load = JSON.stringify({hour:currHour, minute:currMin, day:currDay, year:currYear, username:currentUser, month:currMonth});
      xmlhttp.open("POST","alarmBridge.php?q="+load,true);
      xmlhttp.setRequestHeader("Content-type", "application/json");
      xmlhttp.onreadystatechange = function(){
          if (this.status = 200 && this.readyState == 4){
            var JSarray = JSON.parse(this.responseText);
            for (var i=0; i<JSarray.length; i++){
                alert("Happening within an hour: "+JSarray[i]);
            }
          }
    }
    xmlhttp.send(null);
}
