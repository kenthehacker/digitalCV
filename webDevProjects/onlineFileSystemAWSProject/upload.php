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
  <h1>You are uploading your file as: <?php echo htmlentities($_SESSION['username']);?></h1>
  <p>You can upload files up to <em>2 MB</em> in size!</p>
  <br/>
  <form enctype="multipart/form-data" action="upload.php" method="POST">
    <p>
      <label for="uploadfile_input">Choose a file to upload:</label>
      <input type="file" name="uploaded_file" id="uploadfile_input" />
    </p>
    <input type="submit" value="Upload your file" name="uploaded"/>
  </form>
  <br />
  <hr>
  <div>
    <form action="fileList.php" method="GET">
      <button>
        Return to file list
      </button>
    </form>
    <form action="logout.php" method="GET">
      <button>
        Logout
      </button>
    </form>
  </div>
</body>
</html>

<?php
//Confirms user is signed in - returns to login page if not
$username = $_SESSION['username'];
if(!preg_match('/^[\w_\-]+$/', $username)){
  echo htmlentities("Username invalid, try again!");
  header("Location: login.php");
  exit;
}

if (isset($_POST['uploaded'])) {
  $filename = basename($_FILES['uploaded_file']['name']);
  $filename = str_replace(" ", "_", $filename);

  //Confirms characters are valid
  if(!preg_match('/^[\w_\.\-]+$/', $filename)){
  	echo htmlentities("Invalid filename, please try again with valid characters");
    exit;
  } else {
    $uploadPath = $_SESSION["fileListDir"];
    $full_path = sprintf("%s/%s", $uploadPath, $filename);

    //Attempts to move files, if upload failed will return to appropriate page
    if( move_uploaded_file($_FILES['uploaded_file']['tmp_name'], $full_path)){
      header("Location: upload_success.php");
      exit;
    } else {
        header("Location: upload_failed.php");
        exit;
    }
  }
}
?>
