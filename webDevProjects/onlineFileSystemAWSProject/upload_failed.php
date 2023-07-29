<?php
session_start();

$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){ //sends user back to login if not logged in
  header("Location: login.php");
  exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>File upload failed</title>
</head>
<body>
  <h3>Uploading Failed!</h3>
  <p>Confirm the file's name, size, and type then try again later</p>
  <div>
    <form action="upload.php" method="GET">
      <button>
        Try again
      </button>
    </form>
  </div>
  <br />
  <div>
    <form action="fileList.php" method="GET">
      <button>
        Return to file list
      </button>
    </form>
  </div>
  <br />
  <div>
    <form action="logout.php" method="GET">
      <button>
        Logout and return to sign-in screen
      </button>
    </form>
  </div>
</body>
