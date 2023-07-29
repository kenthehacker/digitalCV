<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>File upload</title>
</head>
<body>
  <div>
    <h2>WARNING!</h2>
    <br />
    <p>This irreversibly deletes this user and all uploaded files!</p>
    <p>You will be returned to sign in page on account deletion</p>
  </div>
  <form action="deleteUser.php" method="POST">
    <input type="submit" value="No, take me back." name="deleteUser">
    <input type="submit" value="DELETE ACCOUNT" name="deleteUser">
  </form>
</body>
</html>

<?php
//Checks if user is signed in - returns to login page if not
$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){
  echo htmlentities("Username invalid, try again!");
  header("Location: login.php");
  exit;
}

//User changes mind and doesn't want to delete account - returns to file list
if ($_POST['deleteUser'] == "No, take me back.") {
  header("Location: fileList.php");
  exit;
}

if ($_POST['deleteUser'] == "DELETE ACCOUNT") {
  //deletes user from userName.txt
  $filePath = "/srv/Module2/userName.txt";
  $contents = file_get_contents($filePath);
  $newContents = preg_replace("/$username/", '', $contents);
  file_put_contents($filePath, $newContents);

  //deletes files from directory
  $directoryPath = "/srv/Module2/" . $username;
  $files = scandir($directoryPath);
  foreach ($files as $f) {
    $file_path = sprintf("%s/%s", $directoryPath, $f);
    unlink($file_path);
  }
  //deletes directory
  rmdir($directoryPath);
  header("Location: logout.php");
}
?>
