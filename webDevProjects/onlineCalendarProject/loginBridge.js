var returnText = "";
if (sessionStorage.getItem("username")) {
  returnText = sessionStorage.getItem("username");
  checkUser(returnText);
  $('.login').hide();
  $(".displayMonth").empty();
  updateUser(returnText);
}
//if user logs in then we have to modify the page to reflect that user is indeed logged in
//by removing and adding some HTML elements

$("#submit").click(() => {
  var user = $("#username").val();
  var pwd = $("#password").val();
  if (user!="" && pwd!="" && returnText == ""){
    loginBridge(user,pwd);
  } else if (user == "" || pwd == "") { alert("empty field!"); }
});
//if user hits submit then enter login bridge 

function updateUser(newUserName){
  currentUser = newUserName;
  $("#logoutButton").show();
  $(".newEvent").show();
  $(".displayMonth").empty();
  updateCal();
}

function loginBridge(user, pwd){
  //AJAX request to check if user exists
  var xmlhttp = new XMLHttpRequest();
  var load = JSON.stringify({username:user, password:pwd});
  xmlhttp.open("POST","login.php?q="+load,true); //or is it get??
      xmlhttp.setRequestHeader("Content-type", "application/json");
      xmlhttp.onreadystatechange = function(){
      if (this.status = 200 && this.readyState == 4){
          returnText = this.responseText.trim()
          //responseText either "" or a fullblown username
          if (returnText == ""){
              alert("Wrong username or password");
          }else{
              $('#userInfo').text("Logged in as " + returnText);
              $('.login').hide();
              sessionStorage.setItem("username", returnText);
              updateUser(returnText);
          }
      }
  }
  xmlhttp.send(null);
}

//Prevents against abuse of functionality attacks
function checkUser(user){
  //AJAX request to check if user exists
  var xmlhttp = new XMLHttpRequest();
  var load = JSON.stringify({username:user});
  xmlhttp.open("POST","checkUser.php?q="+load,true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.onreadystatechange = function(){
    if (this.status === 200 && this.readyState === 4){
      tempText = this.responseText.trim();
      if (returnText != tempText){
        alert("Unexpected username. Logout and try again.");
        $(".displayMonth").empty();
      }
    }
  }
  xmlhttp.send(null);
}
