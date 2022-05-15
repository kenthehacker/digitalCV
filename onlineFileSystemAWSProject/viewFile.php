<?php
session_start();

//Confirms user is signed in - returns to login screen if not
$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){
  echo htmlentities("Username invalid, try again!");
  header("Location: login.php");
  exit;
}

//Opens or downloads file in browser depending on mime type
$file_path = $_POST['filename'];
$filename = basename($file_path);
$finfo = new finfo(FILEINFO_MIME_TYPE);
$mime = $finfo->file($file_path);

header("Content-Type: ".$mime);
header('Content-Disposition: inline; filename="'.$filename.'";');
readfile($file_path);
?>
