const currDate = new Date();
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let tempM = currDate.getMonth();
let tempY = currDate.getFullYear();
let currentMonth = new Month(tempY, tempM);
var currentUser = "";
var deleting = false;
var editing = false;
var sharing  = false;
var eventTime = "";
var eventDate = "";
var eventText = "";
initalize();

// Move calendar view to current month
$("#today").click(() => {
  $(".displayMonth").empty();
  initalize();
  updateCal();
});

// Calendar to last month
$("#prev").click(() => {
  $(".displayMonth").empty();
  currentMonth = currentMonth.prevMonth();
  if (tempM == 0) { tempM = 11;}
  else { tempM -= 1; }
  updateCal();
});

// Calendar to next month
$("#next").click(() => {
  $(".displayMonth").empty();
  currentMonth = currentMonth.nextMonth();
  if (tempM == 11) { tempM = 0;}
  else { tempM += 1; }
  updateCal();
});

// Logout button is clicked
$("#logoutButton").click(() => {
  sessionStorage.removeItem("username");
  updateUser("");
  $("#logoutButton").hide();
  $(".newEvent").hide();
  $(".login").show();
  $('#userInfo').text("");
  returnText = "";
  $("#username").val("");
  $("#password").val("");
});

// Add new user
$("#newUserBtn").click(() => {
  var userName = $("#username").val();
  var password = $("#password").val();
  if (userName!="" && password!=""){
    addNewUser(userName,password);
  }else{
    alert("empty userName or PW ")
  }

});

// Delete button
$("#deleteEvent").click(() => {
  if(!deleting || editing) {
    deleting = true;
    editing = false
    $("#deleteEvent").css("background-color", "red");
    $("#deleteEvent").text("Deleting");

    $("#editEvent").css("background-color", "white");
    $("#editEvent").text("Edit event");

    alert("Delete mode... Click any calendar event to delete. Cannot be undone!");
  } else {
    deleting = false;
    $("#deleteEvent").css("background-color", "white");
    $("#deleteEvent").text("Delete event");
  }
});

// Edit button
$("#editEvent").click(() => {
  if(!editing || deleting) {
    editing = true;
    deleting = false;
    sharing = false;
    $("#editEvent").css("background-color", "red");
    $("#editEvent").text("Editing");

    $("#deleteEvent").css("background-color", "white");
    $("#deleteEvent").text("Delete event");

    alert("Edit mode... Click any calendar event to edit, then enter information into event box.");
  } else {
    editing = false;
    $("#editEvent").css("background-color", "white");
    $("#editEvent").text("Edit event");
  }
});

//Share button
$("#shareEvent").click(() => {
  if (sharing == false){
    editing = false;
    deleting = false;
    sharing = true;
    $("#editEvent").css("background-color", "white");
    $("#editEvent").text("Edit Event");
    $("#deleteEvent").css("background-color", "white");
    $("#deleteEvent").text("Delete event");
    $("#shareEvent").css("background-color", "red");
    alert("Click on event to share and enter username.");
  }else{
    sharing = false;
    $("#editEvent").css("background-color", "white");
    $("#editEvent").text("Editing");
    $("#deleteEvent").css("background-color", "white");
    $("#deleteEvent").text("Delete event");
    $("#shareEvent").css("background-color", "white");
  }

});

// Initalizes the calendar to current date.
function initalize() {
  tempM = currDate.getMonth();
  tempY = currDate.getFullYear();
  currentMonth = new Month(currDate.getFullYear(), currDate.getMonth());
}

// Whenever user clicks an event, get the ID to edit or delete
$(document).on("click", ".eventLink", function(event) {
  const theEventID = this.id - 100;
  if (deleting) { deleteEvent(theEventID); }
  else if (sharing){
    var theFriend = document.getElementById('friendUser').value;
    shareEvent(theEventID,theFriend);
  }
  else if (editing) {
    eventTime = String(document.getElementById('eventTime').value);
    eventDate = String(document.getElementById('eventDate').value);
    eventText = document.getElementById('newEventText').value;
    editEvent(eventText, username, eventTime, eventDate, theEventID);
  }
});

// Initalizes the calendar to current date. Repsonsible for redrawing calendar
function updateCal() {
  //Draws the calendar
  let weeks = currentMonth.getWeeks();
  if (weeks.length == 5) { $(".displayMonth").css("grid-template-rows", "repeat(5, 14vh)"); }
  else if (weeks.length == 4) { $(".displayMonth").css("grid-template-rows", "repeat(4, 14vh)"); }
  else { $(".displayMonth").css("grid-template-rows", "repeat(6, 14vh)"); }
  let dayTracker = 1;
  for (let i in weeks) {
    let days = weeks[i].getDates();
    for(let d in days){
      if (days[d].getMonth() != tempM) { $(".displayMonth").append("<div class=day></div>"); }
      else {
        let temporaryDayID = String(days[d].getDate());
        if (days[d].getDate()<10){
            temporaryDayID = "0"+temporaryDayID;
        }
        $(".displayMonth").append("<div class=day><strong>" + days[d].getDate() + "</strong><div class=subDay id=" + temporaryDayID + "></div></div>");
        $("header").html("<h1>" + months[days[d].getMonth()] + " " + days[d].getFullYear() + "</h1>");
        dayTracker =dayTracker+1;
      }
      // Focuses on updating the calendar from server
      let stringDay = String(dayTracker);
      if (dayTracker<10){
          stringDay = "0"+stringDay;
      }

      let tempMonth = String(tempM+1);
      if((tempM+1)<10){
          tempMonth = "0"+tempMonth;
      }

      let sqlDate = String(tempY)+"-"+String(tempMonth)+"-"+stringDay;

      if(currentUser!=""){ getEvents(currentUser, sqlDate); }
  	}
  }
  checkAlert();
}

// Adds a new user
function addNewUser(username, password){
    var load = JSON.stringify({username:username, pwd:password});
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","newUser.php?q="+load,true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.onreadystatechange = function(){
        if (this.status = 200 && this.readyState == 4){
            if (this.responseText.substr(-1) == "0"){
                alert("User already exists");
            } else {
              alert("User created, please login");
            }
        }
    }
    xmlhttp.send(null);
}

// Deletes the selected event
function deleteEvent(eventID){
  var load = JSON.stringify({id:eventID});
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","deleteEvent.php?q="+load,true);
  xmlhttp.setRequestHeader("Content-type", "application/json");
  xmlhttp.onreadystatechange = function(){
    if (this.status = 200 && this.readyState == 4){
      if (this.responseText.substr(-1) == "1") {
        alert("error deleting");
      }
      $(".displayMonth").empty();
      updateCal();
    }
  }
  xmlhttp.send(null);
}

// Shares the selected event
function shareEvent(eventID, theFriend){
  var load = JSON.stringify({id:eventID, username:theFriend});
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","shareEvent.php?q="+load,true);
  xmlhttp.setRequestHeader("Content-type", "application/json");
  xmlhttp.onreadystatechange = function(){
    if (this.status = 200 && this.readyState == 4){
      if (this.responseText == "0"){
        alert("Shared event to "+theFriend);
      }
    }
  }
  xmlhttp.send(null);
}
