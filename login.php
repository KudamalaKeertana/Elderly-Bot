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
$password = $_POST['password'];

// Prepare SQL query to fetch user data
$sql = "SELECT * FROM login WHERE username='$username' AND password='$password'";
$result = $conn->query($sql);

// Check if user exists
if ($result->num_rows > 0) {
    // User exists, fetch user data
    $row = $result->fetch_assoc();
    $medicines = $row['medicines'];

    // Close connection
    $conn->close();

    // Return user data along with medicines data
    echo $medicines;
} else {
    // Invalid credentials
    header("HTTP/1.1 401 Unauthorized");
    exit;
}
?>