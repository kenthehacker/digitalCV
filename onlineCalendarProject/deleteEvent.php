<?php
// Responsible for deleting the event from the database.
ini_set("session.cookie_httponly", 1);
session_start();
require 'database.php';

$q = $_GET['q'];
$decodedJSON = json_decode($q);
$id = $decodedJSON->id;

$qry = "delete from events where id=".$id;
if ($externalSQL->query($qry)){
    echo "0"; //Success
}else{
    echo "1"; //Failed
}
?>
