<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Make New User</title>
    </head>
    <body>
        <form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="POST">
            <input type="text" name="newUserName" id="newUsername">
            <input type="submit" value="Add">
        </form>

        <?php
            if (isset($_POST['newUserName'])){
              $readfile = fopen("/srv/Module2/userName.txt", "r");
              $userFound = FALSE;
              $userName = $_POST["newUserName"];
              while( !feof($readfile) ){
                $currentText = trim(fgets($readfile));
                if ($currentText == $userName && $currentText != ""){
                  $userFound=TRUE;
                }
              }
              fclose($readfile);
              if ($userFound) {
                echo htmlentities("User already present! Try a different username");
                exit;
              }

                $fileToEdit = fopen("/srv/Module2/userName.txt", "a+");
                $whiteSpace = "\r\n";
                //$newString = trim($whiteSpace.$_POST["newUserName"]);
                $trimmedUser = trim($_POST["newUserName"]);
                //$newString = $whiteSpace.$trimmedUser;
                $newString = $trimmedUser.$whiteSpace;
                //$newString = $newString . PHP_EOL;
                $newString = $newString;
                fwrite($fileToEdit,$newString);
                fclose($fileToEdit);
                header("Location: login.php");
            }
        ?>
    </body>
</html>
