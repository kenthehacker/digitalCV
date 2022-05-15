function getEvents(username, dateNoTime){

    if (username!=""){
        var load = JSON.stringify({name:username, date:dateNoTime});
        //load is a json string sent to PHP to get parsed
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","getEvents.php?q="+load,true); 
        xmlhttp.setRequestHeader("Content-type", "application/json");
        xmlhttp.onreadystatechange = function(){
            if (this.status = 200 && this.readyState == 4){ //checks if process is done on the php side
                tempID = "#"+dateNoTime.substring(8,10);
                //above parses the time and that's how we extract our postID
                $(tempID).append("<p>" + this.responseText + "</p>");
                //adds the response text to the specified eventID on the HTML side 
            }
        }
        xmlhttp.send(null);
    }
}
