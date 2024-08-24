<?php
$servername = "localhost";
$username = "root";
$password = ""; // Enter your MySQL password here
$dbname = "database2";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve form data
$username = $_POST['username'];
$password = ($_POST['password']); // Hash the password for security
$medicines = $_POST['medicines'];

// Prepare and execute SQL query to insert user data
$stmt = $conn->prepare("INSERT INTO login (username, password, medicines) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $username, $password, $medicines);

if ($stmt->execute()) {
    echo $medicines;
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
