<?php
// Responsible for confirming the user exists in the database.
ini_set("session.cookie_httponly", 1);
session_start();
$q = $_GET['q'];
require 'database.php';
$decodedJSON = json_decode($q);

$user = $decodedJSON->username;

$stmt = $externalSQL->prepare("SELECT userName FROM userName WHERE userName=?");
if(!$stmt){
	printf("Query Prep Failed for putting post: %s\n", $externalSQL->error);
	exit;
}
$stmt->bind_param('s', $user);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()){
  if ($_SESSION['username'] == $row['userName']) {
    echo htmlentities($row["userName"]);
  }
}
$stmt->close();
?>
