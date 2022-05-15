<?php
ini_set("session.cookie_httponly", 1);
session_start();
$q = $_GET['q'];
require 'database.php';
$decodedJSON = json_decode($q);
//fetches JSON from JS and spits out the username event time and date into variable
$user = $decodedJSON->username;
$event = ($decodedJSON->event)." ";
$eventTime = $decodedJSON->time;
$eventDate = $decodedJSON->date;
$id = $decodedJSON->id;

$dateNoTime = $eventDate;
$date = $eventDate." ".$eventTime;
//given the SQL values we update SQL row entry
$stmt = $externalSQL->prepare("UPDATE events SET title=?, date=?, dateNoTime=? WHERE id=?");
if(!$stmt){
	printf("Query Prep Failed for putting post: %s\n", $externalSQL->error);
	exit;
}
$stmt->bind_param('sssi', $event, $date, $dateNoTime, $id);
$stmt->execute();
$stmt->close();
?>
