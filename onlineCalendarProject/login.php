<?php
ini_set("session.cookie_httponly", 1);
session_start();
/*
strategy:
username and pw on upper right corner, if entered then sends string to PHP
via AJAX and checks for numRows and returns a bool
*/
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require "database.php";
$q = trim($_GET['q']);

$decodedJSON = json_decode($q);

$username = $decodedJSON->username;
$password = $decodedJSON->password;

$hashedPassword = sha1(hash('ripemd160', $password));
//double hash
$qry = "select * from userName where userName='$username' and password ='$hashedPassword'";
$result = $externalSQL->query($qry);
$numberOfRows = intval($result->num_rows);
if($numberOfRows!=1){
    echo "";
    //the reason why we print a blank is because on the JS side we check if its an empty string or not
    //if it is empty, then we print error message, else its the username
}else{
    $_SESSION['username'] = $username;
    echo trim($username);
    $_SESSION['token'] = bin2hex(random_bytes(32));
}

?>
