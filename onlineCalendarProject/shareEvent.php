<?php
ini_set("session.cookie_httponly", 1);
session_start();
require 'database.php';
$q = trim($_GET['q']);
$decodedJSON = json_decode($q);
$username = $decodedJSON->username; //their friend
$eventID = $decodedJSON->id;

//check if the username exists if not then exit
$qry0 = "select * from userName where userName='".$username."'";

$rslt = $externalSQL->query($qry0);
$numberOfRows = intval($rslt->num_rows);
if ($numberOfRows==0){
    echo "1";
    //user does not exist
    exit;
}

$qry = "select * from events where id=".$eventID;
$stmt = $externalSQL->prepare($qry);
if(!$stmt){
    printf("Query Prep Failed: %s\n", $externalSQL->error);
    exit;
}
$stmt->execute();
$result = $stmt->get_result();

$comma = "','";
while ($row = $result->fetch_assoc()){
    $event = htmlentities($row['title']);
    $date = htmlentities($row['date']);
    $dateNoTime = htmlentities($row['dateNoTime']);
    $qry2 = "insert into events (username, title, date, dateNoTime) values('".$username.$comma.$event.$comma.$date.$comma.$dateNoTime."')";
    if ($externalSQL->query($qry2)){
        echo "0";
    }else{
        echo "bad insert";
    }

}
?>
