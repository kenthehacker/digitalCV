//take text box field and append to SQL table, then call on update calendar
$("#addEvent").click(() => {
  //takes the HTML values from what the user entered into variables and sends it to function
  eventTime = String(document.getElementById('eventTime').value);
  eventDate = String(document.getElementById('eventDate').value);
  eventText = document.getElementById('newEventText').value;
  if (editing) {

  } else { addEvent(eventText,currentUser,eventTime,eventDate); }
});

function addEvent(eventText, username, eventTime, eventDate){
  //creates JSON from variables passed
    var load = JSON.stringify({event:eventText, username:username, time:eventTime, date:eventDate});
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","insertEvent.php?q="+load,true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.onreadystatechange = function(){
        if (this.status = 200 && this.readyState == 4){
          $(".displayMonth").empty();
          //clears the page and reloads it without refreshing the page so we don't get two of the same calendars displayed
          updateCal();
        }
    }
    xmlhttp.send(null);
}

if (!sessionStorage.getItem("username")) {
  updateCal();
}

function editEvent(eventText, username, eventTime, eventDate, id){
  var load = JSON.stringify({event:eventText, username:username, time:eventTime, date:eventDate, id:id});
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","editEvent.php?q="+load,true);
  xmlhttp.setRequestHeader("Content-type", "application/json");
  xmlhttp.onreadystatechange = function(){
    if (this.status = 200 && this.readyState == 4){
      $(".displayMonth").empty();
      updateCal();
    }
  }
  xmlhttp.send(null);
}
