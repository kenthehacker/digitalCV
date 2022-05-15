<?php
ini_set("session.cookie_httponly", 1);
session_start();

$q = $_GET['q'];
require 'database.php';
$decodedJSON = json_decode($q);
$username = $decodedJSON->username;
$pwd = sha1(hash('ripemd160',$decodedJSON->pwd));
$comma = "','";

//check if username already exists
$qry0 = "select exists(select * from userName where userName='".$username."')";
$stmt_checkUser = $externalSQL->prepare($qry0);
$stmt_checkUser->execute();
$stmt_checkUser->bind_result($checker);
while($stmt_checkUser->fetch()){
    if ($checker == 1) {
        echo "0";
        //user already exists
        exit;
    }
}
$stmt_checkUser->close();

$qry = "insert into userName (userName, password) values ('".$username.$comma.$pwd."')";
if ($externalSQL->query($qry)){
    echo "1";
    //good insert of username
}else{
    echo "2";
    //bad insert of username
}
?>
