<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Delete file</title>
</head>

<?php
session_start();

//Checks if user is signed in - returns to login screen if not
$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){
  echo htmlentities("Username invalid, try again!");
  header("Location: login.php");
  exit;
}

//Deletes specified file
$filename = $_POST['filename'];
if(unlink($filename)) {
  header("Location: fileList.php");
} else {
  echo htmlentities("Failed! Go back and try again later.");
}
?>
