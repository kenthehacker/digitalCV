<?php
ini_set("session.cookie_httponly", 1);
header('Access-Control-Allow-Headers: Access-Control-Allow-Origin, Origin, Content-Type, Accept, Authorization, X-Request-With');

session_start();
require 'database.php';

$q = trim($_GET['q']);

$decodedJSON = json_decode($q);

$user = $decodedJSON->name;

$time = $decodedJSON->date;
//takes username and the date and time specified and constructs SQL query
$qry = "select * from events where username= '".$user."' and dateNoTime='".$time."' order by date";

$stmt = $externalSQL->prepare($qry);
if(!$stmt){
    //if SQL query didnt work then we print error
    printf("Query Prep Failed: %s\n", $externalSQL->error);
    exit;
}
$stmt->execute();
$result = $stmt->get_result();

//multiple results may come out, iterate through each row
while ($row = $result->fetch_assoc()){
    $temp = number_format(htmlentities($row['id'])) + 100; //setting ID to +100 to avoid conflict w date ID
    echo "<p><a class=eventLink href='#' id=".$temp.">";
    //echos out HTML elements and JS will stick the echo'ed out values into HTML
    echo htmlentities($row['title'])." at ".htmlentities($row['date']);
    echo "</a></p>";
}
?>
