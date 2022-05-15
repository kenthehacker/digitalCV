<?php
ini_set("session.cookie_httponly", 1);
session_start();
$q = $_GET['q'];

require 'database.php';
$decodedJSON = json_decode($q);

$user = $decodedJSON->username;
$event = ($decodedJSON->event)." ";
$eventTime = $decodedJSON->time;
$eventDate = $decodedJSON->date;

$dateNoTime = $eventDate;
$date = $eventDate." ".$eventTime;
$comma = "','";
$qry = "insert into events (username, title, date, dateNoTime) values ('".$user.$comma.$event.$comma.$date.$comma.$dateNoTime."')";

if ($externalSQL->query($qry)){
    echo "inserted new event correctly";
}else{
    echo "bad insert";
}
?>
