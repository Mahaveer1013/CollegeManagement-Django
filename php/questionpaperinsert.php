<?php
$servername = "localhost:3307";
$username = "root";
$password = "";
$dbname = "test";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Initialize arrays to hold values
$questions = [];
$marks = [];
$co = [];
$b = [];
$u = [];

// Loop through each question
for ($i = 1; $i <= 22; $i++) {
    // Get question, mark, and co values using variable variables
    @$questions[$i] = ($_POST["q$i"]);
    @$marks[$i] = $_POST["m$i"];
    @$co[$i] = $_POST["co$i"];
    @$b[$i] = $_POST["b$i"];
    @$u[$i] = $_POST["u$i"];
}

if (empty($b[$i])) {
    $b[$i] = 'No.';
}
// Get other values
@$subject_code = $_POST["subject_code"];
@$subject_name = $_POST["subject_name"];
@$semester = $_POST["semester"];
@$year_of_student = $_POST["year_of_student"];
@$academic_year = $_POST["academic_year"];
@$faculty_id = $_POST["faculty_id"];
@$questionpaperid = $_POST["questionpaperid"];
@$Semester = $_POST["Semester"];
@$examtype = $_POST["examtype"];
@$dep = $_POST["dep"];
@$dateofexam = $_POST["dateofexam"];

$sql = "INSERT INTO questionpaperdetails (subject_code, subject_name,
 semester,year_of_student,academic_year,faculty_id,questionpaperid,examtype,dep,dateofexam)
VALUES ('$subject_code', '$subject_name',
'$semester','$year_of_student','$academic_year','$faculty_id','$questionpaperid','$examtype','$dep','$dateofexam')";

if ($conn->query($sql) === TRUE) {
    echo "Exam Details,";
} else {
    die("Error: " . $conn->error);
}


// Insert values into the database or perform other actions as needed
$sql1 = "INSERT INTO parta (
question1,mark1,co1,b1,
question2,mark2,co2,b2,
question3,mark3,co3,b3,
question4,mark4,co4,b4,
question5,mark5,co5,b5,
question6,mark6,co6,b6,
question7,mark7,co7,b7,
question8,mark8,co8,b8,
question9,mark9,co9,b9,
question10,mark10,co10,b10,questionpaperid,u1,u2,u3,u4,u5,u6,u7,u8,u9,u10) VALUES (
'$questions[1]','$marks[1]','$co[1]','$b[1]',
'$questions[2]','$marks[2]','$co[2]','$b[2]',
'$questions[3]','$marks[3]','$co[3]','$b[3]',
'$questions[4]','$marks[4]','$co[4]','$b[4]',
'$questions[5]','$marks[5]','$co[5]','$b[5]',
'$questions[6]','$marks[6]','$co[6]','$b[6]',
'$questions[7]','$marks[7]','$co[7]','$b[7]',
'$questions[8]','$marks[8]','$co[8]','$b[8]',
'$questions[9]','$marks[9]','$co[9]','$b[9]',
'$questions[10]','$marks[10]','$co[10]','$b[10]','$questionpaperid',
'$u[1]','$u[2]','$u[3]','$u[4]','$u[5]','$u[6]','$u[7]','$u[8]','$u[9]','$u[10]')";

if ($conn->query($sql1) === TRUE) {
    echo "2 marks,";
} else {
    die("Error: " . $conn->error);
}


$sql2 = "INSERT INTO partbandc (questionpaperid,question11a,mark11a,co11a,b11a,question11b ,mark11b ,co11b ,b11b ,
question12a ,mark12a ,co12a,b12a,question12b ,mark12b ,co12b ,b12b,
question13a ,mark13a ,co13a ,b13a ,question13b,mark13b ,co13b,b13b,
question14a,mark14a,co14a,b14a,question14b ,mark14b ,co14b,b14b,
question15a ,mark15a ,co15a,b15a,question15b,mark15b,co15b,b15b,
question16a,mark16a,co16a,b16a,question16b,mark16b,co16b,b16b,
u11a,u11b,u12a,u12b,u13a,u13b,u14a,u14b,u15a,u15b,u16a,u16b) VALUES (
    '$questionpaperid',
    '$questions[11]','$marks[11]','$co[11]','$b[11]',
    '$questions[12]','$marks[12]','$co[12]','$b[12]',
    '$questions[13]','$marks[13]','$co[13]','$b[13]',
    '$questions[14]','$marks[14]','$co[14]','$b[14]',
    '$questions[15]','$marks[15]','$co[15]','$b[15]',
    '$questions[16]','$marks[16]','$co[16]','$b[16]',
    '$questions[17]','$marks[17]','$co[17]','$b[17]',
    '$questions[18]','$marks[18]','$co[18]','$b[18]',
    '$questions[19]','$marks[19]','$co[19]','$b[19]',
    '$questions[20]','$marks[20]','$co[20]','$b[20]',
    '$questions[21]','$marks[21]','$co[21]','$b[21]',
    '$questions[22]','$marks[22]','$co[22]','$b[22]',
    '$u[11]','$u[12]','$u[13]','$u[14]','$u[15]','$u[16]','$u[17]','$u[18]','$u[19]','$u[20]','$u[21]','$u[22]'

    )";

if ($conn->query($sql2) === TRUE) {
    echo "13 marks and 15 marks are Uploaded Successfully into DataBase!!<br>";
    echo "<a href='faculty.html'>Go Back Faculty Page</a><br>";
    echo "<a href='questionpaperinsert.php>Upload Another Question Paper</a>";
} else {
    die("Error: " . $conn->error);
}

mysqli_close($conn);
?>