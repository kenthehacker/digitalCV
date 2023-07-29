<?php
// PHP file for checking an alert
ini_set("session.cookie_httponly", 1);
session_start();
require 'database.php';
$q = trim($_GET['q']);
$messages = array();

$decodedJSON = json_decode($q);
$currHour = $decodedJSON->hour;
$currMin = $decodedJSON->minute;
$currDay = $decodedJSON->day;
$currYear = $decodedJSON->year;
$currMonth = $decodedJSON->month;
$username = $decodedJSON->username;

$sqlDate = $currYear."-".$currMonth."-".$currDay;

$qry = "select * from events where username='".$username."' and dateNoTime='".$sqlDate."'";
if (!$result = $externalSQL->query($qry)) {
    echo "100";
    //bad fetch method
    exit;
}
while ($row = $result->fetch_assoc()){
    $sqlTime = strval(htmlentities($row['date']));
    $sqlMessage = htmlentities($row['title']);
    $sqlYear = intval(substr($sqlDate, 0,4));
    $sqlDay = intval(substr($sqlDate, 8,10));
    $sqlMonth = intval(substr($sqlDate, 5,7));
    $sqlHour = substr($sqlTime, 11,2);
    if ($sqlHour>12){
        $sqlHour = $sqlHour-12;
    }
    $sqlMinute = intval(substr($sqlDate, -4,-2));

    if ($sqlYear == $currYear && $sqlDay == $currDay){
        if ($sqlHour == $currHour){
            //for now check if it's within the hour
            array_push($messages,$sqlMessage);
        }
    }
}
echo json_encode($messages);

?>
