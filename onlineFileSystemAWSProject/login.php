<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <title>
        Eric and Ken file sharing
      </title>
    </head>

    <body>
        <form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="POST">
            <input type="text" name="username" id="username">
            <input type="submit" value="LogIn" name="userSubmit">
            <div>
                <input type="submit" value = "Click to make new Acc" name="newUser" id = "newUser">
            </div>
        </form>

        <?php
          $baseDirectory = getcwd();
          //append the userNames at the end of the baseDirectories
          $userNames = fopen("/srv/Module2/userName.txt", "r") or die("userName.txt not opened");

          //makes directory for all users
          while( !feof($userNames) ){
              $currentText = trim(fgets($userNames));
              $srv = "/srv";
              $module2="/Module2/";
              $tempDir = $srv.$module2.$currentText;
              if (is_dir($tempDir)==FALSE){
                  mkdir($tempDir) or die("Can't make user directory");
              }
          }
          fclose($userNames);

          //Checks user ID is valid
          if (isset($_POST['userSubmit'])){
              $h = fopen("/srv/Module2/userName.txt", "r");
              $validUser = FALSE;
              $userName = $_POST["username"];
              while( !feof($h) ){
                  $currentText = trim(fgets($h));
                  if ($currentText==$userName  && $currentText!=""){
                      $_SESSION['username'] = $currentText;
                      $validUser=TRUE;
                  }
              }
              fclose($h);
              if ($validUser==FALSE){
                  echo htmlentities("Incorrect UserID");
              }else{
                  $_SESSION["username"]=$userName;
                  header("Location: fileList.php");
                  exit;
              }
          }
          $userFile = fopen('/srv/Module2/userName.txt','a') or die("unable to access userName.txt");
          //if we want to make new user
          if (isset($_POST['newUser'])){
              $_SESSION['userFile']=$userFile;
              header("Location: newUser.php");
              exit;
          }
        ?>

    </body>
</html>
