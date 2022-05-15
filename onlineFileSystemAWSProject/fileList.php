<?php
session_start();

//Confirms user is signed in - returns to login screen if not
$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){
  echo htmlentities("Username invalid, try again!");
  header("Location: login.php");
  exit;
}
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>User Directory</title>
  </head>

  <body>
    <header>
      <h1>List of uploaded files for <?php echo htmlentities($username); ?> </h1>
    </header>
    <form action="logout.php" method="POST">
      <input type="submit" value="Logout" name="logout">
    </form>
    <form action="deleteUser.php" method="POST">
      <input type="submit" value="Delete this account" name="deleteUser">
    </form>
    <hr>

    <?php
    //we want to list the user uploaded files
      $path = "/srv/Module2";
      $path = sprintf("%s/%s", $path, $username);
      $_SESSION['fileListDir']=$path;
      $files = scandir($path);

      //iterate through files in scanned user directory
      for ($i = 2; $i < count($files); $i++) {//first 2 "files" lead back to directory
        $f = $files[$i];
        $file_path = sprintf("%s/%s", $path, $f);
    ?>

        <form action="viewFile.php" method="POST">
          <input type="hidden" name="filename" value="<?php echo $file_path;?>"/>
          <input type="submit" name="submit" value="<?php echo $f; ?>"/>
        </form>
        <form action="deleteScript.php" method="POST">
          <input type="hidden" name="filename" value="<?php echo $file_path;?>"/>
          <input type="submit" name="delete" value="delete" />
        </form>
        <br />

    <?php } ?>

    <div>
      <hr>
      <form action="upload.php" class='link'>
        <button>
          Upload Page
        </button>
      </form>
    </div>
  </body>
</html>
