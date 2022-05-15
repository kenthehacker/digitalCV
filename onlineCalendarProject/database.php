<?php

$sqlUserName = "kk";
$sqlPassword = "toor";
//$sqlUserName = "admin5";
//$sqlPassword = "admin";
$externalSQL = new mysqli('localhost', $sqlUserName, $sqlPassword, 'calendarDB');

if ($externalSQL->connect_errno){
    printf("connection failed ",$externalSQL->connect_error);
    exit;
}
?>
