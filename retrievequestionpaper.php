<?php
$conn = new mysqli('localhost:3307', 'root', '', 'test');

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
@$sub = $_POST["subject_code"];
@$Academic = $_POST["academic_year"];
@$Faculty = $_POST["faculty_id"];
@$questionpaperid = $_POST["questionpaperid"];
@$examtype = $_POST["examtype"];
$sql = "SELECT *
        FROM questionpaperdetails
        JOIN partA ON questionpaperdetails.questionpaperid = partA.questionpaperid
        JOIN partBandC ON questionpaperdetails.questionpaperid = partBandC.questionpaperid
        WHERE questionpaperdetails.subject_code=? AND questionpaperdetails.academic_year=? AND questionpaperdetails.faculty_id=? AND questionpaperdetails.questionpaperid=? AND questionpaperdetails.examtype=?";

$stmt = $conn->prepare($sql);

?>
<html>

<head>
    <style>
        fieldset {
            display: inline-block;
            width: 65%;
            padding: 3%;
        }

        a {
            display: block;
            text-decoration: none;
            color: blue;
            font-size: 20px;
            margin-right: 95%;

        }

        * {
            text-align: center;
            margin: 0%;
        }

        .co {
            font-size: small;
            text-align: left;
        }

        .left {
            text-align: left;
        }

        td {
            padding: 10px;
            text-align: left;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px;
        }

        @media print {
            table {
                width: 100%;
                page-break-before: always;
                /* Ensure each table starts on a new page */
                margin-bottom: 20px;
                /* Additional margin at the bottom for better spacing */
            }
        }


        .right {
            text-align: right;
        }


        .displayinline {
            display: inline-block;
        }

        td {
            padding: 10px;
            text-align: center;
        }

        .pad {
            width: 5px;
        }

        .pad2 {
            padding: 0%;
            width: auto;
        }


        .up {
            margin: 2%;
        }

        .left2 {
            text-align: left;
        }
    </style>

</head>

<body>


    <?php
    if ($stmt) {
        $stmt->bind_param("sssss", $sub, $Academic, $Faculty, $questionpaperid, $examtype);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {

            while ($row = $result->fetch_assoc()) {


                echo "
                   <fieldset>
    
    
   
    <h2 style='display:inline; margin-left:0%; '>PANIMALAR ENGINEERING COLLEGE</h2> 
    <h5>An Autonomous Insititution,Affilated to Anna University, Chennai</h5>
    <p>(JAISAKTHI EDUCATIONAL TRUST)</p>
    <p>Approved by All India Council of Technical Education</p>
    <p>Bangalore Trunk Road, Varadharajapuram, Poonamallee, chennai - 600123</p><hr>
    <h3 class='displayinline'>" . $row['dep'] . "</h3><hr>
    <h3 class='displayinline'> " . $row['examtype'] . "</h3><hr>";


                echo "
                <center>
    <table>
        <tr>
            <td colspan='2'><h3 class='left' >Subject Name: " . $row['subject_name'] . "</h3></td>
          
        
        </tr>
        <tr>
            <td><h4 class='left'>Academic Year : " . $row['academic_year'] . " </h4></td>
         
             <td><h4 class='right'>Year/Semester: " . $row['year_of_student'] . "/" . $row['semester'] . "</h4></td>
        </tr>
        <tr>
            <td><h4 class='left'>Subject Code: " . $row['subject_code'] . "</h4></td>
          
            <td><h4 class='right'>Date:" . $row["dateofexam"] . "</h4></td>
        </tr>
        <tr>
            <td><h4 class='left'>Maxium Marks:100</h4></td>
           
            <td><h4 class='right'>Duration:3.00Hours</h4></td>
        </tr>
    </table>
<hr>
<p class='co'><b>Course Outcome:</b><br>
<b>CO1:</b> Identify and select suitable Process Model for the given problem and have a thorough understanding of variousSoftware Life Cycle models.
<br><b>CO2:</b> Analyze the requirements of the given software project and produce requirement specifications
<br><b>CO3:</b> Apply the knowledge of object-oriented modelling concepts and design methods with a clear emphasison Unified Modelling Language 
<br>for a moderately realistic object oriented system
<br><b>CO4:</b> Apply various software architectures, including frameworks and design patterns, when developing
<br>software projects
strategies of the software project
<br><b>CO5:</b> Evaluate the software project using various testing Technique.
<br><b>CO6:</b> recognise the deployment started g and configuration management strategies of software project
<br><b>Blooms Level: 1</b> - Remembering,<b> 2</b> - Understanding,<b> 3</b> - Applying,<b> 4</b> - Analysing,<b> 5</b> - Evaluating<b> 6</b> - Creating.</p>
<hr>
       <h3 class='displayinline'>Answer All the Question</h3>
       <hr>
       <h3 class='displayinline'>Part-A (10*2=20)</h3>
       <table border='1'>
            
            <tr>
                    <th><b>Q.NO</b></th>
                    <th><b>Question</b></th>
                    <th><b>Bloom Level</b></th>
                    <th><b>course<br>Outcome</b></th>
                    <th><b>Max Mark</b></th>
            </tr>
            <tr >
                    <td>1</td>
                    <td class='left'>" . nl2br($row['question1']) . "</td>
                    <td>" . $row['b1'] . "</td>
                    <td>" . $row['co1'] . "</td>
                    <td>" . $row['mark1'] . "</td>
            </tr>
            <tr>
                    <td>2</td>
                    <td class='left'>" . nl2br($row['question2']) . "</td>
                    <td>" . $row['b2'] . "</td>
                    <td>" . $row['co2'] . "</td>
                    <td>" . $row['mark2'] . "</td>
            </tr>
            <tr>
                    <td>3</td>
                    <td class='left'>" . nl2br($row['question3']) . "</td>
                    <td>" . $row['b3'] . "</td>
                    <td>" . $row['co3'] . "</td>
                    <td>" . $row['mark3'] . "</td>
            </tr>
            <tr>
                    <td>4</td>
                    <td class='left'>" . nl2br($row['question4']) . "</td>
                    <td>" . $row['b4'] . "</td>
                    <td>" . $row['co4'] . "</td>
                    <td>" . $row['mark4'] . "</td>
            </tr>
            <tr>
                    <td>5</td>
                    <td class='left'>" . nl2br($row['question5']) . "</td>
                    <td>" . $row['b5'] . "</td>
                    <td>" . $row['co5'] . "</td>
                    <td>" . $row['mark5'] . "</td>
            </tr>
            <tr>
                    <td>6</td>
                    <td class='left'>" . nl2br($row['question6']) . "</td>
                    <td>" . $row['b6'] . "</td>
                    <td>" . $row['co6'] . "</td>
                    <td>" . $row['mark6'] . "</td>
            </tr>
            <tr>
                    <td>7</td>
                    <td class='left'>" . nl2br($row['question7']) . "</td>
                    <td>" . $row['b7'] . "</td>
                    <td>" . $row['co7'] . "</td>
                    <td>" . $row['mark7'] . "</td>
            </tr>
            <tr>
                    <td>8</td>
                    <td class='left'>" . nl2br($row['question8']) . "</td>
                    <td>" . $row['b8'] . "</td>
                    <td>" . $row['co8'] . "</td>
                    <td>" . $row['mark8'] . "</td>
            </tr>
            <tr>
                    <td>9</td>
                    <td class='left'>" . nl2br($row['question9']) . "</td>
                    <td>" . $row['b9'] . "</td>
                    <td>" . $row['co9'] . "</td>
                    <td>" . $row['mark9'] . "</td>
            </tr><tr>
                    <td>10</td>
                    <td class='left'>" . nl2br($row['question10']) . "</td>
                    <td>" . $row['b10'] . "</td>
                    <td>" . $row['co10'] . "</td>
                    <td>" . $row['mark10'] . "</td>
            </tr>
      
</table>
        </fieldset>  <br><br><br>";
                echo "
        <fieldset>
            <h3>Part-B (5*13=65)</h3>
       <table border='1' style='display:inline-block;'>
             <tr>
                    <th><b>Q.NO</b></th>
                    <th><b>option</b></th>
                    <th><b>Question</b></th>
                    <th><b>Bloom Level</b></th>
                    <th><b>course<br>Outcome</b></th>
                    <th><b>Max Mark</b></th>
            </tr>
       
            <tr >
                    <td rowspan='3'>11</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question11a']) . "</td>
                    <td>" . $row['b11a'] . "</td>
                    <td>" . $row['co11a'] . "</td>
                    <td>" . $row['mark11a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr>   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question11b']) . "</td>
                    <td>" . $row['b11b'] . "</td>
                    <td>" . $row['co11b'] . "</td>
                    <td>" . $row['mark11b'] . "</td>
            </tr>
            <tr>
            <td colspan='7'></td>
            </tr>
             <tr class='up'>
                    <td rowspan='3'>12</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question12a']) . "</td>
                    <td>" . $row['b12a'] . "</td>
                    <td>" . $row['co12a'] . "</td>
                    <td>" . $row['mark12a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr >   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question12b']) . "</td>
                    <td>" . $row['b12b'] . "</td>
                    <td>" . $row['co12b'] . "</td>
                    <td>" . $row['mark12b'] . "</td>
            </tr>
            </tr>
            <tr>
            <td colspan='7'></td>
            </tr>
            <tr class='up'>
                    <td rowspan='3'>13</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question13a']) . "</td>
                    <td>" . $row['b13a'] . "</td>
                    <td>" . $row['co13a'] . "</td>
                    <td>" . $row['mark13a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr>   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question13b']) . "</td>
                    <td>" . $row['b13b'] . "</td>
                    <td>" . $row['co13b'] . "</td>
                    <td>" . $row['mark13b'] . "</td>
            </tr>
            </tr>
            <tr>
            <td colspan='7'></td>
            </tr>
            <tr >
                    <td rowspan='3'>14</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question14a']) . "</td>
                    <td>" . $row['b14a'] . "</td>
                    <td>" . $row['co14a'] . "</td>
                    <td>" . $row['mark14a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr>   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question14b']) . "</td>
                    <td>" . $row['b14b'] . "</td>
                    <td>" . $row['co14b'] . "</td>
                    <td>" . $row['mark14b'] . "</td>
            </tr>
            </tr>
            <tr>
            <td colspan='7'></td>
            </tr>
            <tr >
                    <td rowspan='3'>15</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question15a']) . "</td>
                    <td>" . $row['b15a'] . "</td>
                    <td>" . $row['co15a'] . "</td>
                    <td>" . $row['mark15a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr>   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question15b']) . "</td>
                    <td>" . $row['b15b'] . "</td>
                    <td>" . $row['co15b'] . "</td>
                    <td>" . $row['mark15b'] . "</td>
            </tr>
            
            
      
</table>
<br><br>
            <h3>Part-C (1*15=15)</h3>
       <table border='1'>
       <tr>
                    <th><b>Q.NO</b></th>
                    <th><b>option</b></th>
                    <th><b>Question</b></th>
                    <th><b>Bloom Level</b></th>
                    <th><b>course<br>Outcome</b></th>
                    <th><b>Max Mark</b></th>
            </tr>

            <tr >
                    <td rowspan='3'>16</td>
                    <td>a</td>
                    <td class='left'>" . nl2br($row['question16a']) . "</td>
                    <td>" . $row['b16a'] . "</td>
                    <td>" . $row['co16a'] . "</td>
                    <td>" . $row['mark16a'] . "</td>
            </tr>
            <tr>
            <td colspan='6' class='pad2'>OR</td>
            </tr>
            <tr>   
                   <td>b</td>
                    <td class='left'>" . nl2br($row['question16b']) . "</td>
                    <td>" . $row['b16b'] . "</td>
                    <td>" . $row['co16b'] . "</td>
                    <td>" . $row['mark16b'] . "</td>
            </tr>
            

</table>
        </fieldset>";
                echo "
                <br><br><br>
                <fieldset style='display:inline; '>

        <table border='1' >
            <tr>
                <td><b>Q.No</b></td>
                <td><b>Unit<br>No</b></td>
                <td colspan='5'><b>Marks of Course Outcome</b></td>
                <td rowspan='2'><b>Total<br>Marks</b></td>
                <td colspan='6'><b>Marks of Blooms Level<b></td>
            </tr>
            <tr>
                <td><b>CO/BL</b></td>
                <td></td>
                <td ><b>CO1</b></td>
                <td><b>CO2</b></td>
                <td><b>CO3</b></td>
                <td><b>CO4</b></td>
                <td><b>CO5</b></td>
                <td><b>BL1</b></td>
                <td><b>BL2</b></td>
                <td><b>BL3</b></td>
                <td><b>BL4</b></td>
                <td><b>BL5</b></td>
                <td><b>BL6</b></td>
            </tr>
            <tr>
                <td>1</td>
                <td id='1u'>" . $row['u1'] . "</td>
                <td id='1co1'></td>
                <td id='1co2'></td>
                <td id='1co3'></td>
                <td id='1co4'></td>
                <td id='1co5'></td>
                <td><b>2</b></td>
                <td id='1bl1'></td>
                <td id='1bl2'></td>
                <td id='1bl3'></td>
                <td id='1bl4'></td>
                <td id='1bl5'></td>
                <td id='1bl6'></td>
            </tr>
            <tr>
                <td>2</td>
                <td id='2u'>" . $row['u2'] . "</td>
                <td id='2co1'></td>
                <td id='2co2'></td>
                <td id='2co3'></td>
                <td id='2co4'></td>
                <td id='2co5'></td>
                <td><b>2</b></td>
                <td id='2bl1'></td>
                <td id='2bl2'></td>
                <td id='2bl3'></td>
                <td id='2bl4'></td>
                <td id='2bl5'></td>
                <td id='2bl6'></td>
            </tr>
            <tr>
                <td>3</td>
                <td id='3u'>" . $row['u3'] . "</td>
                <td id='3co1'></td>
                <td id='3co2'></td>
                <td id='3co3'></td>
                <td id='3co4'></td>
                <td id='3co5'></td>
                <td><b>2</b></td>
                <td id='3bl1'></td>
                <td id='3bl2'></td>
                <td id='3bl3'></td>
                <td id='3bl4'></td>
                <td id='3bl5'></td>
                <td id='3bl6'></td>
            </tr>
            <tr>
                <td>4</td>
                <td id='4u'>" . $row['u4'] . "</td>
                <td id='4co1'></td>
                <td id='4co2'></td>
                <td id='4co3'></td>
                <td id='4co4'></td>
                <td id='4co5'></td>
                <td><b>2</b></td>
                <td id='4bl1'></td>
                <td id='4bl2'></td>
                <td id='4bl3'></td>
                <td id='4bl4'></td>
                <td id='4bl5'></td>
                <td id='4bl6'></td>
            </tr>
            <tr>
                <td>5</td>
                <td id='5u'>" . $row['u5'] . "</td>
                <td id='5co1'></td>
                <td id='5co2'></td>
                <td id='5co3'></td>
                <td id='5co4'></td>
                <td id='5co5'></td>
                <td><b>2</b></td>
                <td id='5bl1'></td>
                <td id='5bl2'></td>
                <td id='5bl3'></td>
                <td id='5bl4'></td>
                <td id='5bl5'></td>
                <td id='5bl6'></td>
            </tr>
            <tr>
                <td>6</td>
                <td id='6u'>" . $row['u6'] . "</td>
                <td id='6co1'></td>
                <td id='6co2'></td>
                <td id='6co3'></td>
                <td id='6co4'></td>
                <td id='6co5'></td>
                <td><b>2</b></td>
                <td id='6bl1'></td>
                <td id='6bl2'></td>
                <td id='6bl3'></td>
                <td id='6bl4'></td>
                <td id='6bl5'></td>
                <td id='6bl6'></td>
            </tr>
            <tr>
                <td>7</td>
                <td id='7u'>" . $row['u7'] . "</td>
                <td id='7co1'></td>
                <td id='7co2'></td>
                <td id='7co3'></td>
                <td id='7co4'></td>
                <td id='7co5'></td>
                <td><b>2</b></td>
                <td id='7bl1'></td>
                <td id='7bl2'></td>
                <td id='7bl3'></td>
                <td id='7bl4'></td>
                <td id='7bl5'></td>
                <td id='7bl6'></td>
            </tr>
            <tr>
                <td>8</td>
                <td id='8u'>" . $row['u8'] . "</td>
                <td id='8co1'></td>
                <td id='8co2'></td>
                <td id='8co3'></td>
                <td id='8co4'></td>
                <td id='8co5'></td>
                <td><b>2</b></td>
                <td id='8bl1'></td>
                <td id='8bl2'></td>
                <td id='8bl3'></td>
                <td id='8bl4'></td>
                <td id='8bl5'></td>
                <td id='8bl6'></td>
            </tr>
            <tr>
                <td>9</td>
                <td id='9u'>" . $row['u9'] . "</td>
                <td id='9co1'></td>
                <td id='9co2'></td>
                <td id='9co3'></td>
                <td id='9co4'></td>
                <td id='9co5'></td>
                <td><b>2</b></td>
                <td id='9bl1'></td>
                <td id='9bl2'></td>
                <td id='9bl3'></td>
                <td id='9bl4'></td>
                <td id='9bl5'></td>
                <td id='9bl6'></td>
            </tr>
            <tr>
                <td>10</td>
                <td id='10u'>" . $row['u10'] . "</td>
                <td id='10co1'></td>
                <td id='10co2'></td>
                <td id='10co3'></td>
                <td id='10co4'></td>
                <td id='10co5'></td>
                <td><b>2</b></td>
                <td id='10bl1'></td>
                <td id='10bl2'></td>
                <td id='10bl3'></td>
                <td id='10bl4'></td>
                <td id='10bl5'></td>
                <td id='10bl6'></td>
            </tr>
            <tr>
                <td>11a</td>
                <td id='11au'>" . $row['u11a'] . "</td>
                <td id='11aco1'></td>
                <td id='11aco2'></td>
                <td id='11aco3'></td>
                <td id='11aco4'></td>
                <td id='11aco5'></td>
                <td><b>13</b></td>
                <td id='11abl1'></td>
                <td id='11abl2'></td>
                <td id='11abl3'></td>
                <td id='11abl4'></td>
                <td id='11abl5'></td>
                <td id='11abl6'></td>
            </tr>
            <tr>
                <td>11b</td>
                <td id='11bu'>" . $row['u11b'] . "</td>
                <td id='11bco1'></td>
                <td id='11bco2'></td>
                <td id='11bco3'></td>
                <td id='11bco4'></td>
                <td id='11bco5'></td>
                <td><b>13</b></td>
                <td id='11bbl1'></td>
                <td id='11bbl2'></td>
                <td id='11bbl3'></td>
                <td id='11bbl4'></td>
                <td id='11bbl5'></td>
                <td id='11bbl6'></td>
            </tr>
            <tr>
                <td>12a</td>
                <td id='12au'>" . $row['u12a'] . "</td>
                <td id='12aco1'></td>
                <td id='12aco2'></td>
                <td id='12aco3'></td>
                <td id='12aco4'></td>
                <td id='12aco5'></td>
                <td><b>13</b></td>
                <td id='12abl1'></td>
                <td id='12abl2'></td>
                <td id='12abl3'></td>
                <td id='12abl4'></td>
                <td id='12abl5'></td>
                <td id='12abl6'></td>
            </tr>
            <tr>
                <td>12b</td>
                <td id='12bu'>" . $row['u12b'] . "</td>
                <td id='12bco1'></td>
                <td id='12bco2'></td>
                <td id='12bco3'></td>
                <td id='12bco4'></td>
                <td id='12bco5'></td>
                <td><b>13</b></td>
                <td id='12bbl1'></td>
                <td id='12bbl2'></td>
                <td id='12bbl3'></td>
                <td id='12bbl4'></td>
                <td id='12bbl5'></td>
                <td id='12bbl6'></td>
            </tr>
            <tr>
                <td>13a</td>
                <td id='13au'>" . $row['u13a'] . "</td>
                <td id='13aco1'></td>
                <td id='13aco2'></td>
                <td id='13aco3'></td>
                <td id='13aco4'></td>
                <td id='13aco5'></td>
                <td><b>13</b></td>
                <td id='13abl1'></td>
                <td id='13abl2'></td>
                <td id='13abl3'></td>
                <td id='13abl4'></td>
                <td id='13abl5'></td>
                <td id='13abl6'></td>
            </tr>
            <tr>
                <td>13b</td>
                <td id='13bu'>" . $row['u13b'] . "</td>
                <td id='13bco1'></td>
                <td id='13bco2'></td>
                <td id='13bco3'></td>
                <td id='13bco4'></td>
                <td id='13bco5'></td>
                <td><b>13</b></td>
                <td id='13bbl1'></td>
                <td id='13bbl2'></td>
                <td id='13bbl3'></td>
                <td id='13bbl4'></td>
                <td id='13bbl5'></td>
                <td id='13bbl6'></td>
            </tr>
            <tr>
                <td>14a</td>
                <td id='14au'>" . $row['u14a'] . "</td>
                <td id='14aco1'></td>
                <td id='14aco2'></td>
                <td id='14aco3'></td>
                <td id='14aco4'></td>
                <td id='14aco5'></td>
                <td><b>13</b></td>
                <td id='14abl1'></td>
                <td id='14abl2'></td>
                <td id='14abl3'></td>
                <td id='14abl4'></td>
                <td id='14abl5'></td>
                <td id='14abl6'></td>
            </tr>
            <tr>
                <td>14b</td>
                <td id='14bu'>" . $row['u14b'] . "</td>
                <td id='14bco1'></td>
                <td id='14bco2'></td>
                <td id='14bco3'></td>
                <td id='14bco4'></td>
                <td id='14bco5'></td>
                <td><b>13</b></td>
                <td id='14bbl1'></td>
                <td id='14bbl2'></td>
                <td id='14bbl3'></td>
                <td id='14bbl4'></td>
                <td id='14bbl5'></td>
                <td id='14bbl6'></td>
            </tr>
            <tr>
                <td>15a</td>
                <td id='15au'>" . $row['u15a'] . "</td>
                <td id='15aco1'></td>
                <td id='15aco2'></td>
                <td id='15aco3'></td>
                <td id='15aco4'></td>
                <td id='15aco5'></td>
                <td><b>13</b></td>
                <td id='15abl1'></td>
                <td id='15abl2'></td>
                <td id='15abl3'></td>
                <td id='15abl4'></td>
                <td id='15abl5'></td>
                <td id='15abl6'></td>
            </tr>
            <tr>
                <td>15b</td>
                <td id='15bu'>" . $row['u15b'] . "</td>
                <td id='15bco1'></td>
                <td id='15bco2'></td>
                <td id='15bco3'></td>
                <td id='15bco4'></td>
                <td id='15bco5'></td>
                <td><b>13</b></td>
                <td id='15bbl1'></td>
                <td id='15bbl2'></td>
                <td id='15bbl3'></td>
                <td id='15bbl4'></td>
                <td id='15bbl5'></td>
                <td id='15bbl6'></td>
            </tr>
            <tr>
                <td>16a</td>
                <td id='16au'>" . $row['u16a'] . "</td>
                <td id='16aco1'></td>
                <td id='16aco2'></td>
                <td id='16aco3'></td>
                <td id='16aco4'></td>
                <td id='16aco5'></td>
                <td><b>15</b></td>
                <td id='16abl1'></td>
                <td id='16abl2'></td>
                <td id='16abl3'></td>
                <td id='16abl4'></td>
                <td id='16abl5'></td>
                <td id='16abl6'></td>
            </tr>
            <tr>
                <td>16b</td>
                <td id='16bu'>" . $row['u16b'] . "</td>
                <td id='16bco1'></td>
                <td id='16bco2'></td>
                <td id='16bco3'></td>
                <td id='16bco4'></td>
                <td id='16bco5'></td>
                <td><b>15</b></td>
                <td id='16bbl1'></td>
                <td id='16bbl2'></td>
                <td id='16bbl3'></td>
                <td id='16bbl4'></td>
                <td id='16bbl5'></td>
                <td id='16bbl6'></td>
            </tr>
            <tr>
                    <td><b>Total</b></td>
                    <td></td>
                    <td id='co1total'></td>
                    <td id='co2total'></td>
                    <td id='co3total'></td>
                    <td id='co4total'></td>
                    <td id='co5total'></td>
                    <td>180</td>
                    <td colspan='2'><p id='b1b2total'></p></td>
                    <td colspan='2'><p id='b3b4total'></p></td>
                    <td colspan='2'><p id='b5b6total'></p></td>
                </tr>
                <tr>
                    <td colspan='2' style='font-size:14px;'><b>Mark Distribution in %</b></td>
                    <td id='ptco1'></td>
                    <td id='ptco2'></td>
                    <td id='ptco3'></td>
                    <td id='ptco4'></td>
                    <td id='ptco5'></td>
                    <td></td>
                    <td colspan='2' id='ptbl1bl2'></td>
                    <td colspan='2' id='ptbl3bl4'></td>
                    <td colspan='2' id='ptbl5bl6'></td>
                </tr>

            <tr>
                    <td colspan='2'>Recommendation</td>
                    <td colspan='5' style='font-size:13px;'>Based on the Syllabus of the Examinations, the Distribution of Course Outcome should be Uniform.</td>
                    <td></td>
                    <td colspan='2'>20-35%</td>
                    <td colspan='2'>Minimum 40%</td>
                    <td colspan='2'>15-25%</td>
                </tr>
        </table>
    </center>

<b>
                <p style='text-align:left'>It is ensured that:</p>
            </b>
            <ol>
                <li style='text-align:left'>The Questions are from Text Books and Reference Books provided in the
                    syllabus
                    and
                    Test the skills suggested in Blooms taxonomy.</li>
                <li style='text-align:left'>The Cognitive Level and Course Outcome mentioned are appropriate.</li>
                <li style='text-align:left'>The Distribution of Questions, Distribution of Course Outcomes and
                    Percentage of
                    Distribution of Blooms Level are Appropriate.</li>
            </ol>
            <br><br>
            <table style='display:inline-block;'>
                <tr>
                    <td></td>
                    <td>Prepared by</td>
                    <td style='padding: 18px;'></td>
                    <td></td>
                    <td>Verified by</td>
                    <td style='padding: 18px;'></td>
                    <td>Approved by</td>
                </tr>
                <tr>
                    <td></td>
                    <td ><b>Course Instructor</b></td>
                    <td></td>
                    <td></td>
                    <td><b>Course Co-ordinator</b></td>
                    <td></td>
                    <td><b>Head of the Department</b></td>
                </tr>
                <tr>
                    <td style='text-align: right;'>Name:</td>
                    <td></td>
                    <td></td>
                    <td style='text-align: right;'>Name:</td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td style='text-align: right;'>Designation:</td>
                    <td></td>
                    <td></td>
                    <td style='text-align: right;'>Designation:</td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </table><button onclick='window.print();' style='background-color:lightgreen;'>Print</button>
            

            </fieldset>
            <br><br><br>";
                for ($i = 1; $i <= 10; $i++) {
                    $coKey = 'co' . $i;
                    $markKey = 'mark' . $i;

                    if ($row[$coKey]) {
                        for ($j = 1; $j <= 5; $j++) {
                            $coIndex = 'co' . $j;
                            $coId = $i . $coIndex;

                            if ($row[$coKey] === 'CO' . $j) {
                                echo "<script>document.getElementById('$coId').innerText = '" . $row[$markKey] . "';</script>";
                            }
                        }
                    }
                }


                for ($i = 11; $i <= 16; $i++) {
                    $coa = $row['co' . $i . 'a'];
                    $cob = $row['co' . $i . 'b'];

                    for ($j = 1; $j <= 5; $j++) {
                        $coaId = "{$i}aco{$j}";
                        $cobId = "{$i}bco{$j}";

                        if ($coa && $coa === 'CO' . $j) {
                            echo "<script>document.getElementById('{$coaId}').innerText = '{$row['mark' . $i . 'a']}';</script>";
                        }

                        if ($cob && $cob === 'CO' . $j) {
                            echo "<script>document.getElementById('{$cobId}').innerText = '{$row['mark' . $i . 'b']}';</script>";
                        }
                    }
                }
                echo "
    <script>


        var co11 = parseInt(document.getElementById('1co1').innerText) || 0;
        var co21 = parseInt(document.getElementById('2co1').innerText) || 0;
        var co31 = parseInt(document.getElementById('3co1').innerText) || 0;
        var co41 = parseInt(document.getElementById('4co1').innerText) || 0;
        var co51 = parseInt(document.getElementById('5co1').innerText) || 0;
        var co61 = parseInt(document.getElementById('6co1').innerText) || 0;
        var co71 = parseInt(document.getElementById('7co1').innerText) || 0;
        var co81 = parseInt(document.getElementById('8co1').innerText) || 0;
        var co91 = parseInt(document.getElementById('9co1').innerText) || 0;
        var co101 = parseInt(document.getElementById('10co1').innerText) || 0;
        var co11a1 = parseInt(document.getElementById('11aco1').innerText) || 0;
        var co11b1 = parseInt(document.getElementById('11bco1').innerText) || 0;
        var co12a1 = parseInt(document.getElementById('12aco1').innerText) || 0;
        var co12b1 = parseInt(document.getElementById('12bco1').innerText) || 0;
        var co13a1 = parseInt(document.getElementById('13aco1').innerText) || 0;
        var co13b1 = parseInt(document.getElementById('13bco1').innerText) || 0;
        var co14a1 = parseInt(document.getElementById('14aco1').innerText) || 0;
        var co14b1 = parseInt(document.getElementById('14bco1').innerText) || 0;
        var co15a1 = parseInt(document.getElementById('15aco1').innerText) || 0;
        var co15b1 = parseInt(document.getElementById('15bco1').innerText) || 0;
        var co16a1 = parseInt(document.getElementById('16aco1').innerText) || 0;
        var co16b1 = parseInt(document.getElementById('16bco1').innerText) || 0;
        var totalco1 = co11 + co21 + co31 + co41 + co51 + co61 + co71 + co81 + co91 + co101 + co11a1 + co11b1 + co12a1 + co12b1 + co13a1 + co13b1 + co14a1 + co14b1 + co15a1 + co15b1 + co16a1 + co16b1;
        document.getElementById('co1total').innerText=totalco1;


        var co12 = parseInt(document.getElementById('1co2').innerText) || 0;
        var co22 = parseInt(document.getElementById('2co2').innerText) || 0;
        var co32 = parseInt(document.getElementById('3co2').innerText) || 0;
        var co42 = parseInt(document.getElementById('4co2').innerText) || 0;
        var co52 = parseInt(document.getElementById('5co2').innerText) || 0;
        var co62 = parseInt(document.getElementById('6co2').innerText) || 0;
        var co72 = parseInt(document.getElementById('7co2').innerText) || 0;
        var co82 = parseInt(document.getElementById('8co2').innerText) || 0;
        var co92 = parseInt(document.getElementById('9co2').innerText) || 0;
        var co102 = parseInt(document.getElementById('10co2').innerText) || 0;
        var co11a2 = parseInt(document.getElementById('11aco2').innerText) || 0;
        var co11b2 = parseInt(document.getElementById('11bco2').innerText) || 0;
        var co12a2 = parseInt(document.getElementById('12aco2').innerText) || 0;
        var co12b2 = parseInt(document.getElementById('12bco2').innerText) || 0;
        var co13a2 = parseInt(document.getElementById('13aco2').innerText) || 0;
        var co13b2 = parseInt(document.getElementById('13bco2').innerText) || 0;
        var co14a2 = parseInt(document.getElementById('14aco2').innerText) || 0;
        var co14b2 = parseInt(document.getElementById('14bco2').innerText) || 0;
        var co15a2 = parseInt(document.getElementById('15aco2').innerText) || 0;
        var co15b2 = parseInt(document.getElementById('15bco2').innerText) || 0;
        var co16a2 = parseInt(document.getElementById('16aco2').innerText) || 0;
        var co16b2 = parseInt(document.getElementById('16bco2').innerText) || 0;
        var totalco2 = co12 + co22 + co32 + co42 + co52 + co62 + co72 + co82 + co92 + co102 + co11a2 + co11b2 + co12a2 + co12b2 + co13a2 + co13b2 + co14a2 + co14b2 + co15a2 + co15b2 + co16a2 + co16b2 ;
        document.getElementById('co2total').innerText=totalco2;

        var co13 = parseInt(document.getElementById('1co3').innerText) || 0;
        var co23 = parseInt(document.getElementById('2co3').innerText) || 0;
        var co33 = parseInt(document.getElementById('3co3').innerText) || 0;
        var co43 = parseInt(document.getElementById('4co3').innerText) || 0;
        var co53 = parseInt(document.getElementById('5co3').innerText) || 0;
        var co63 = parseInt(document.getElementById('6co3').innerText) || 0;
        var co73 = parseInt(document.getElementById('7co3').innerText) || 0;
        var co83 = parseInt(document.getElementById('8co3').innerText) || 0;
        var co93 = parseInt(document.getElementById('9co3').innerText) || 0;
        var co103 = parseInt(document.getElementById('10co3').innerText) || 0;
        var co11a3 = parseInt(document.getElementById('11aco3').innerText) || 0;
        var co11b3 = parseInt(document.getElementById('11bco3').innerText) || 0;
        var co12a3 = parseInt(document.getElementById('12aco3').innerText) || 0;
        var co12b3 = parseInt(document.getElementById('12bco3').innerText) || 0;
        var co13a3 = parseInt(document.getElementById('13aco3').innerText) || 0;
        var co13b3 = parseInt(document.getElementById('13bco3').innerText) || 0;
        var co14a3 = parseInt(document.getElementById('14aco3').innerText) || 0;
        var co14b3 = parseInt(document.getElementById('14bco3').innerText) || 0;
        var co15a3 = parseInt(document.getElementById('15aco3').innerText) || 0;
        var co15b3 = parseInt(document.getElementById('15bco3').innerText) || 0;
        var co16a3 = parseInt(document.getElementById('16aco3').innerText) || 0;
        var co16b3 = parseInt(document.getElementById('16bco3').innerText) || 0;
        var totalco3 = co13 + co23 + co33 + co43 + co53 + co63 + co73 + co83 + co93 + co103 + co11a3 + co11b3 + co12a3 + co12b3 + co13a3 + co13b3 + co14a3 + co14b3 + co15a3 + co15b3 + co16a3 + co16b3 ;
        document.getElementById('co3total').innerText=totalco3;
        
        var co14 = parseInt(document.getElementById('1co4').innerText) || 0;
        var co24 = parseInt(document.getElementById('2co4').innerText) || 0;
        var co34 = parseInt(document.getElementById('3co4').innerText) || 0;
        var co44 = parseInt(document.getElementById('4co4').innerText) || 0;
        var co54 = parseInt(document.getElementById('5co4').innerText) || 0;
        var co64 = parseInt(document.getElementById('6co4').innerText) || 0;
        var co74 = parseInt(document.getElementById('7co4').innerText) || 0;
        var co84 = parseInt(document.getElementById('8co4').innerText) || 0;
        var co94 = parseInt(document.getElementById('9co4').innerText) || 0;
        var co104 = parseInt(document.getElementById('10co4').innerText) || 0;
        var co11a4 = parseInt(document.getElementById('11aco4').innerText) || 0;
        var co11b4 = parseInt(document.getElementById('11bco4').innerText) || 0;
        var co12a4 = parseInt(document.getElementById('12aco4').innerText) || 0;
        var co12b4 = parseInt(document.getElementById('12bco4').innerText) || 0;
        var co13a4 = parseInt(document.getElementById('13aco4').innerText) || 0;
        var co13b4 = parseInt(document.getElementById('13bco4').innerText) || 0;
        var co14a4 = parseInt(document.getElementById('14aco4').innerText) || 0;
        var co14b4 = parseInt(document.getElementById('14bco4').innerText) || 0;
        var co15a4 = parseInt(document.getElementById('15aco4').innerText) || 0;
        var co15b4 = parseInt(document.getElementById('15bco4').innerText) || 0;
        var co16a4 = parseInt(document.getElementById('16aco4').innerText) || 0;
        var co16b4 = parseInt(document.getElementById('16bco4').innerText) || 0;
        var totalco4 = co14 + co24 + co34 + co44 + co54 + co64 + co74 + co84 + co94 + co104 + co11a4 + co11b4 + co12a4 + co12b4 + co13a4 + co13b4 + co14a4 + co14b4 + co15a4 + co15b4 + co16a4 + co16b4 ;
        document.getElementById('co4total').innerText=totalco4;

        var co15 = parseInt(document.getElementById('1co5').innerText) || 0;
        var co25 = parseInt(document.getElementById('2co5').innerText) || 0;
        var co35 = parseInt(document.getElementById('3co5').innerText) || 0;
        var co45 = parseInt(document.getElementById('4co5').innerText) || 0;
        var co55 = parseInt(document.getElementById('5co5').innerText) || 0;
        var co65 = parseInt(document.getElementById('6co5').innerText) || 0;
        var co75 = parseInt(document.getElementById('7co5').innerText) || 0;
        var co85 = parseInt(document.getElementById('8co5').innerText) || 0;
        var co95 = parseInt(document.getElementById('9co5').innerText) || 0;
        var co105 = parseInt(document.getElementById('10co5').innerText) || 0;
        var co11a5 = parseInt(document.getElementById('11aco5').innerText) || 0;
        var co11b5 = parseInt(document.getElementById('11bco5').innerText) || 0;
        var co12a5 = parseInt(document.getElementById('12aco5').innerText) || 0;
        var co12b5 = parseInt(document.getElementById('12bco5').innerText) || 0;
        var co13a5 = parseInt(document.getElementById('13aco5').innerText) || 0;
        var co13b5 = parseInt(document.getElementById('13bco5').innerText) || 0;
        var co14a5 = parseInt(document.getElementById('14aco5').innerText) || 0;
        var co14b5 = parseInt(document.getElementById('14bco5').innerText) || 0;
        var co15a5 = parseInt(document.getElementById('15aco5').innerText) || 0;
        var co15b5 = parseInt(document.getElementById('15bco5').innerText) || 0;
        var co16a5 = parseInt(document.getElementById('16aco5').innerText) || 0;
        var co16b5 = parseInt(document.getElementById('16bco5').innerText) || 0;
        var totalco5 = co15 + co25 + co35 + co45 + co55 + co65 + co75 + co85 + co95 + co105 + co11a5 + co11b5 + co12a5 + co12b5 + co13a5 + co13b5 + co14a5 + co14b5 + co15a5 + co15b5 + co16a5 + co16b5 ;
        document.getElementById('co5total').innerText=totalco5;
        
        
        </script>";

                for ($i = 1; $i <= 10; $i++) {
                    $bKey = 'b' . $i;
                    $markKey = 'mark' . $i;

                    if ($row[$bKey]) {
                        $category = '';
                        switch ($row[$bKey]) {
                            case 'Remember':
                                $category = 'bl1';
                                break;
                            case 'Understanding':
                                $category = 'bl2';
                                break;
                            case 'Applying':
                                $category = 'bl3';
                                break;
                            case 'Analyzing':
                                $category = 'bl4';
                                break;
                            case 'Evaluate':
                                $category = 'bl5';
                                break;
                            case 'Creating':
                                $category = 'bl6';
                                break;
                        }

                        echo "<script>document.getElementById('$i$category').innerText = '" . $row[$markKey] . "';</script>";
                    }
                }



                if ($row['b11a']) {
                    if ($row['b11a'] === 'Remember') {
                        echo "<script>document.getElementById('11abl1').innerText = '" . $row['mark11a'] . "';</script>";
                    } else if ($row['b11a'] === 'Understanding') {
                        echo "<script>document.getElementById('11abl2').innerText = '" . $row['mark11a'] . "';</script>";
                    } else if ($row['b11a'] === 'Applying') {
                        echo "<script>document.getElementById('11abl3').innerText = '" . $row['mark11a'] . "';</script>";
                    } else if ($row['b11a'] === 'Analyzing') {
                        echo "<script>document.getElementById('11abl4').innerText = '" . $row['mark11a'] . "';</script>";
                    } else if ($row['b11a'] === 'Evaluate') {
                        echo "<script>document.getElementById('11abl5').innerText = '" . $row['mark11a'] . "';</script>";
                    } else if ($row['b11a'] === 'Creating') {
                        echo "<script>document.getElementById('11abl6').innerText = '" . $row['mark11a'] . "';</script>";
                    }
                }
                if ($row['b11b']) {
                    if ($row['b11b'] === 'Remember') {
                        echo "<script>document.getElementById('11bbl1').innerText = '" . $row['mark11b'] . "';</script>";
                    } else if ($row['b11b'] === 'Understanding') {
                        echo "<script>document.getElementById('11bbl2').innerText = '" . $row['mark11b'] . "';</script>";
                    } else if ($row['b11b'] === 'Applying') {
                        echo "<script>document.getElementById('11bbl3').innerText = '" . $row['mark11b'] . "';</script>";
                    } else if ($row['b11b'] === 'Analyzing') {
                        echo "<script>document.getElementById('11bbl4').innerText = '" . $row['mark11b'] . "';</script>";
                    } else if ($row['b11b'] === 'Evaluate') {
                        echo "<script>document.getElementById('11bbl5').innerText = '" . $row['mark11b'] . "';</script>";
                    } else if ($row['b11b'] === 'Creating') {
                        echo "<script>document.getElementById('11bbl6').innerText = '" . $row['mark11b'] . "';</script>";
                    }
                }
                if ($row['b12a']) {
                    if ($row['b12a'] === 'Remember') {
                        echo "<script>document.getElementById('12abl1').innerText = '" . $row['mark12a'] . "';</script>";
                    } else if ($row['b12a'] === 'Understanding') {
                        echo "<script>document.getElementById('12abl2').innerText = '" . $row['mark12a'] . "';</script>";
                    } else if ($row['b12a'] === 'Applying') {
                        echo "<script>document.getElementById('12abl3').innerText = '" . $row['mark12a'] . "';</script>";
                    } else if ($row['b12a'] === 'Analyzing') {
                        echo "<script>document.getElementById('12abl4').innerText = '" . $row['mark12a'] . "';</script>";
                    } else if ($row['b12a'] === 'Evaluate') {
                        echo "<script>document.getElementById('12abl5').innerText = '" . $row['mark12a'] . "';</script>";
                    } else if ($row['b12a'] === 'Creating') {
                        echo "<script>document.getElementById('12abl6').innerText = '" . $row['mark12a'] . "';</script>";
                    }
                }
                if ($row['b12b']) {
                    if ($row['b12b'] === 'Remember') {
                        echo "<script>document.getElementById('12bbl1').innerText = '" . $row['mark12b'] . "';</script>";
                    } else if ($row['b12b'] === 'Understanding') {
                        echo "<script>document.getElementById('12bbl2').innerText = '" . $row['mark12b'] . "';</script>";
                    } else if ($row['b12b'] === 'Applying') {
                        echo "<script>document.getElementById('12bbl3').innerText = '" . $row['mark12b'] . "';</script>";
                    } else if ($row['b12b'] === 'Analyzing') {
                        echo "<script>document.getElementById('12bbl4').innerText = '" . $row['mark12b'] . "';</script>";
                    } else if ($row['b12b'] === 'Evaluate') {
                        echo "<script>document.getElementById('12bbl5').innerText = '" . $row['mark12b'] . "';</script>";
                    } else if ($row['b12b'] === 'Creating') {
                        echo "<script>document.getElementById('12bbl6').innerText = '" . $row['mark12b'] . "';</script>";
                    }
                }
                if ($row['b13a']) {
                    if ($row['b13a'] === 'Remember') {
                        echo "<script>document.getElementById('13abl1').innerText = '" . $row['mark13a'] . "';</script>";
                    } else if ($row['b13a'] === 'Understanding') {
                        echo "<script>document.getElementById('13abl2').innerText = '" . $row['mark13a'] . "';</script>";
                    } else if ($row['b13a'] === 'Applying') {
                        echo "<script>document.getElementById('13abl3').innerText = '" . $row['mark13a'] . "';</script>";
                    } else if ($row['b13a'] === 'Analyzing') {
                        echo "<script>document.getElementById('13abl4').innerText = '" . $row['mark13a'] . "';</script>";
                    } else if ($row['b13a'] === 'Evaluate') {
                        echo "<script>document.getElementById('13abl5').innerText = '" . $row['mark13a'] . "';</script>";
                    } else if ($row['b13a'] === 'Creating') {
                        echo "<script>document.getElementById('13abl6').innerText = '" . $row['mark13a'] . "';</script>";
                    }
                }
                if ($row['b13b']) {
                    if ($row['b13b'] === 'Remember') {
                        echo "<script>document.getElementById('13bbl1').innerText = '" . $row['mark13b'] . "';</script>";
                    } else if ($row['b13b'] === 'Understanding') {
                        echo "<script>document.getElementById('13bbl2').innerText = '" . $row['mark13b'] . "';</script>";
                    } else if ($row['b13b'] === 'Applying') {
                        echo "<script>document.getElementById('13bbl3').innerText = '" . $row['mark13b'] . "';</script>";
                    } else if ($row['b13b'] === 'Analyzing') {
                        echo "<script>document.getElementById('13bbl4').innerText = '" . $row['mark13b'] . "';</script>";
                    } else if ($row['b13b'] === 'Evaluate') {
                        echo "<script>document.getElementById('13bbl5').innerText = '" . $row['mark13b'] . "';</script>";
                    } else if ($row['b13b'] === 'Creating') {
                        echo "<script>document.getElementById('13bbl6').innerText = '" . $row['mark13b'] . "';</script>";
                    }
                }
                if ($row['b14a']) {
                    if ($row['b14a'] === 'Remember') {
                        echo "<script>document.getElementById('14abl1').innerText = '" . $row['mark14a'] . "';</script>";
                    } else if ($row['b14a'] === 'Understanding') {
                        echo "<script>document.getElementById('14abl2').innerText = '" . $row['mark14a'] . "';</script>";
                    } else if ($row['b14a'] === 'Applying') {
                        echo "<script>document.getElementById('14abl3').innerText = '" . $row['mark14a'] . "';</script>";
                    } else if ($row['b14a'] === 'Analyzing') {
                        echo "<script>document.getElementById('14abl4').innerText = '" . $row['mark14a'] . "';</script>";
                    } else if ($row['b14a'] === 'Evaluate') {
                        echo "<script>document.getElementById('14abl5').innerText = '" . $row['mark14a'] . "';</script>";
                    } else if ($row['b14a'] === 'Creating') {
                        echo "<script>document.getElementById('14abl6').innerText = '" . $row['mark14a'] . "';</script>";
                    }
                }
                if ($row['b14b']) {
                    if ($row['b14b'] === 'Remember') {
                        echo "<script>document.getElementById('14bbl1').innerText = '" . $row['mark14b'] . "';</script>";
                    } else if ($row['b14b'] === 'Understanding') {
                        echo "<script>document.getElementById('14bbl2').innerText = '" . $row['mark14b'] . "';</script>";
                    } else if ($row['b14b'] === 'Applying') {
                        echo "<script>document.getElementById('14bbl3').innerText = '" . $row['mark14b'] . "';</script>";
                    } else if ($row['b14b'] === 'Analyzing') {
                        echo "<script>document.getElementById('14bbl4').innerText = '" . $row['mark14b'] . "';</script>";
                    } else if ($row['b14b'] === 'Evaluate') {
                        echo "<script>document.getElementById('14bbl5').innerText = '" . $row['mark14b'] . "';</script>";
                    } else if ($row['b14b'] === 'Creating') {
                        echo "<script>document.getElementById('14bbl6').innerText = '" . $row['mark14b'] . "';</script>";
                    }
                }
                if ($row['b15a']) {
                    if ($row['b15a'] === 'Remember') {
                        echo "<script>document.getElementById('15abl1').innerText = '" . $row['mark15a'] . "';</script>";
                    } else if ($row['b15a'] === 'Understanding') {
                        echo "<script>document.getElementById('15abl2').innerText = '" . $row['mark15a'] . "';</script>";
                    } else if ($row['b15a'] === 'Applying') {
                        echo "<script>document.getElementById('15abl3').innerText = '" . $row['mark15a'] . "';</script>";
                    } else if ($row['b15a'] === 'Analyzing') {
                        echo "<script>document.getElementById('15abl4').innerText = '" . $row['mark15a'] . "';</script>";
                    } else if ($row['b15a'] === 'Evaluate') {
                        echo "<script>document.getElementById('15abl5').innerText = '" . $row['mark15a'] . "';</script>";
                    } else if ($row['b15a'] === 'Creating') {
                        echo "<script>document.getElementById('15abl6').innerText = '" . $row['mark15a'] . "';</script>";
                    }
                }
                if ($row['b15b']) {
                    if ($row['b15b'] === 'Remember') {
                        echo "<script>document.getElementById('15bbl1').innerText = '" . $row['mark15b'] . "';</script>";
                    } else if ($row['b15b'] === 'Understanding') {
                        echo "<script>document.getElementById('15bbl2').innerText = '" . $row['mark15b'] . "';</script>";
                    } else if ($row['b15b'] === 'Applying') {
                        echo "<script>document.getElementById('15bbl3').innerText = '" . $row['mark15b'] . "';</script>";
                    } else if ($row['b15b'] === 'Analyzing') {
                        echo "<script>document.getElementById('15bbl4').innerText = '" . $row['mark15b'] . "';</script>";
                    } else if ($row['b15b'] === 'Evaluate') {
                        echo "<script>document.getElementById('15bbl5').innerText = '" . $row['mark15b'] . "';</script>";
                    } else if ($row['b15b'] === 'Creating') {
                        echo "<script>document.getElementById('15bbl6').innerText = '" . $row['mark15b'] . "';</script>";
                    }
                }
                if ($row['b16a']) {
                    if ($row['b16a'] === 'Remember') {
                        echo "<script>document.getElementById('16abl1').innerText = '" . $row['mark16a'] . "';</script>";
                    } else if ($row['b16a'] === 'Understanding') {
                        echo "<script>document.getElementById('16abl2').innerText = '" . $row['mark16a'] . "';</script>";
                    } else if ($row['b16a'] === 'Applying') {
                        echo "<script>document.getElementById('16abl3').innerText = '" . $row['mark16a'] . "';</script>";
                    } else if ($row['b16a'] === 'Analyzing') {
                        echo "<script>document.getElementById('16abl4').innerText = '" . $row['mark16a'] . "';</script>";
                    } else if ($row['b16a'] === 'Evaluate') {
                        echo "<script>document.getElementById('16abl5').innerText = '" . $row['mark16a'] . "';</script>";
                    } else if ($row['b16a'] === 'Creating') {
                        echo "<script>document.getElementById('16abl6').innerText = '" . $row['mark16a'] . "';</script>";
                    }
                }
                if ($row['b16b']) {
                    if ($row['b16b'] === 'Remember') {
                        echo "<script>document.getElementById('16bbl1').innerText = '" . $row['mark16b'] . "';</script>";
                    } else if ($row['b16b'] === 'Understanding') {
                        echo "<script>document.getElementById('16bbl2').innerText = '" . $row['mark16b'] . "';</script>";
                    } else if ($row['b16b'] === 'Applying') {
                        echo "<script>document.getElementById('16bbl3').innerText = '" . $row['mark16b'] . "';</script>";
                    } else if ($row['b16b'] === 'Analyzing') {
                        echo "<script>document.getElementById('16bbl4').innerText = '" . $row['mark16b'] . "';</script>";
                    } else if ($row['b16b'] === 'Evaluate') {
                        echo "<script>document.getElementById('16bbl5').innerText = '" . $row['mark16b'] . "';</script>";
                    } else if ($row['b16b'] === 'Creating') {
                        echo "<script>document.getElementById('16bbl6').innerText = '" . $row['mark16b'] . "';</script>";
                    }
                }
                echo "
                <script>
                var b11 = parseInt(document.getElementById('1bl1').innerText) || 0;
                var b21 = parseInt(document.getElementById('2bl1').innerText) || 0;
                var b31 = parseInt(document.getElementById('3bl1').innerText) || 0;
                var b41 = parseInt(document.getElementById('4bl1').innerText) || 0;
                var b51 = parseInt(document.getElementById('5bl1').innerText) || 0;
                var b61 = parseInt(document.getElementById('6bl1').innerText) || 0;
                var b71 = parseInt(document.getElementById('7bl1').innerText) || 0;
                var b81 = parseInt(document.getElementById('8bl1').innerText) || 0;
                var b91 = parseInt(document.getElementById('9bl1').innerText) || 0;
                var b101 = parseInt(document.getElementById('10bl1').innerText) || 0;
                var b11a1 = parseInt(document.getElementById('11abl1').innerText) || 0;
                var b11b1 = parseInt(document.getElementById('11bbl1').innerText) || 0;
                var b12a1 = parseInt(document.getElementById('12abl1').innerText) || 0;
                var b12b1 = parseInt(document.getElementById('12bbl1').innerText) || 0;
                var b13a1 = parseInt(document.getElementById('13abl1').innerText) || 0;
                var b13b1 = parseInt(document.getElementById('13bbl1').innerText) || 0;
                var b14a1 = parseInt(document.getElementById('14abl1').innerText) || 0;
                var b14b1 = parseInt(document.getElementById('14bbl1').innerText) || 0;
                var b15a1 = parseInt(document.getElementById('15abl1').innerText) || 0;
                var b15b1 = parseInt(document.getElementById('15bbl1').innerText) || 0;
                var b16a1 = parseInt(document.getElementById('16abl1').innerText) || 0;
                var b16b1 = parseInt(document.getElementById('16bbl1').innerText) || 0;
        
                var b12 = parseInt(document.getElementById('1bl2').innerText) || 0;
                var b22 = parseInt(document.getElementById('2bl2').innerText) || 0;
                var b32 = parseInt(document.getElementById('3bl2').innerText) || 0;
                var b42 = parseInt(document.getElementById('4bl2').innerText) || 0;
                var b52 = parseInt(document.getElementById('5bl2').innerText) || 0;
                var b62 = parseInt(document.getElementById('6bl2').innerText) || 0;
                var b72 = parseInt(document.getElementById('7bl2').innerText) || 0;
                var b82 = parseInt(document.getElementById('8bl2').innerText) || 0;
                var b92 = parseInt(document.getElementById('9bl2').innerText) || 0;
                var b102 = parseInt(document.getElementById('10bl2').innerText) || 0;
                var b11a2 = parseInt(document.getElementById('11abl2').innerText) || 0;
                var b11b2 = parseInt(document.getElementById('11bbl2').innerText) || 0;
                var b12a2 = parseInt(document.getElementById('12abl2').innerText) || 0;
                var b12b2 = parseInt(document.getElementById('12bbl2').innerText) || 0;
                var b13a2 = parseInt(document.getElementById('13abl2').innerText) || 0;
                var b13b2 = parseInt(document.getElementById('13bbl2').innerText) || 0;
                var b14a2 = parseInt(document.getElementById('14abl2').innerText) || 0;
                var b14b2 = parseInt(document.getElementById('14bbl2').innerText) || 0;
                var b15a2 = parseInt(document.getElementById('15abl2').innerText) || 0;
                var b15b2 = parseInt(document.getElementById('15bbl2').innerText) || 0;
                var b16a2 = parseInt(document.getElementById('16abl2').innerText) || 0;
                var b16b2 = parseInt(document.getElementById('16bbl2').innerText) || 0;
        
                var b1b2total = b11 + b21 + b31 + b41 + b51 + b61 + b71 + b81 + b91 + b101 + b11a1 + b11b1 + b12a1 + b12b1 + b13a1 + b13b1 + b14a1 + b14b1 + b15a1 + b15b1 + b16a1 + b16b1 + b12+ b22 + b32 + b42 + b52 + b62 + b72 + b82 + b92 + b102 + b11a2 + b11b2 + b12a2 + b12b2 + b13a2 + b13b2 + b14a2 + b14b2 + b15a2 + b15b2 + b16a2 + b16b2 ;
                document.getElementById('b1b2total').innerText='BL1+BL2='+b1b2total;
        
                var b13 = parseInt(document.getElementById('1bl3').innerText) || 0;
                var b23 = parseInt(document.getElementById('2bl3').innerText) || 0;
                var b33 = parseInt(document.getElementById('3bl3').innerText) || 0;
                var b43 = parseInt(document.getElementById('4bl3').innerText) || 0;
                var b53 = parseInt(document.getElementById('5bl3').innerText) || 0;
                var b63 = parseInt(document.getElementById('6bl3').innerText) || 0;
                var b73 = parseInt(document.getElementById('7bl3').innerText) || 0;
                var b83 = parseInt(document.getElementById('8bl3').innerText) || 0;
                var b93 = parseInt(document.getElementById('9bl3').innerText) || 0;
                var b103 = parseInt(document.getElementById('10bl3').innerText) || 0;
                var b11a3 = parseInt(document.getElementById('11abl3').innerText) || 0;
                var b11b3 = parseInt(document.getElementById('11bbl3').innerText) || 0;
                var b12a3 = parseInt(document.getElementById('12abl3').innerText) || 0;
                var b12b3 = parseInt(document.getElementById('12bbl3').innerText) || 0;
                var b13a3 = parseInt(document.getElementById('13abl3').innerText) || 0;
                var b13b3 = parseInt(document.getElementById('13bbl3').innerText) || 0;
                var b14a3 = parseInt(document.getElementById('14abl3').innerText) || 0;
                var b14b3 = parseInt(document.getElementById('14bbl3').innerText) || 0;
                var b15a3 = parseInt(document.getElementById('15abl3').innerText) || 0;
                var b15b3 = parseInt(document.getElementById('15bbl3').innerText) || 0;
                var b16a3 = parseInt(document.getElementById('16abl3').innerText) || 0;
                var b16b3 = parseInt(document.getElementById('16bbl3').innerText) || 0;
        
                var b14 = parseInt(document.getElementById('1bl4').innerText) || 0;
                var b24 = parseInt(document.getElementById('2bl4').innerText) || 0;
                var b34 = parseInt(document.getElementById('3bl4').innerText) || 0;
                var b44 = parseInt(document.getElementById('4bl4').innerText) || 0;
                var b54 = parseInt(document.getElementById('5bl4').innerText) || 0;
                var b64 = parseInt(document.getElementById('6bl4').innerText) || 0;
                var b74 = parseInt(document.getElementById('7bl4').innerText) || 0;
                var b84 = parseInt(document.getElementById('8bl4').innerText) || 0;
                var b94 = parseInt(document.getElementById('9bl4').innerText) || 0;
                var b104 = parseInt(document.getElementById('10bl4').innerText) || 0;
                var b11a4 = parseInt(document.getElementById('11abl4').innerText) || 0;
                var b11b4 = parseInt(document.getElementById('11bbl4').innerText) || 0;
                var b12a4 = parseInt(document.getElementById('12abl4').innerText) || 0;
                var b12b4 = parseInt(document.getElementById('12bbl4').innerText) || 0;
                var b13a4 = parseInt(document.getElementById('13abl4').innerText) || 0;
                var b13b4 = parseInt(document.getElementById('13bbl4').innerText) || 0;
                var b14a4 = parseInt(document.getElementById('14abl4').innerText) || 0;
                var b14b4 = parseInt(document.getElementById('14bbl4').innerText) || 0;
                var b15a4 = parseInt(document.getElementById('15abl4').innerText) || 0;
                var b15b4 = parseInt(document.getElementById('15bbl4').innerText) || 0;
                var b16a4 = parseInt(document.getElementById('16abl4').innerText) || 0;
                var b16b4 = parseInt(document.getElementById('16bbl4').innerText) || 0;
        
                var b3b4total = b13 + b23 + b33 + b43 + b53 + b63 + b73 + b83 + b93 + b103 + b11a3 + b11b3 + b12a3 + b12b3 + b13a3 + b13b3 + b14a3 + b14b3 + b15a3 + b15b3 + b16a3 + b16b3 + b14+ b24 + b34 + b44 + b54 + b64 + b74 + b84 + b94 + b104 + b11a4 + b11b4 + b12a4 + b12b4 + b13a4 + b13b4 + b14a4 + b14b4 + b15a4 + b15b4 + b16a4 + b16b4 ;
                document.getElementById('b3b4total').innerText='BL3+BL4='+b3b4total;
                
                var b15 = parseInt(document.getElementById('1bl5').innerText) || 0;
                var b25 = parseInt(document.getElementById('2bl5').innerText) || 0;
                var b35 = parseInt(document.getElementById('3bl5').innerText) || 0;
                var b45 = parseInt(document.getElementById('4bl5').innerText) || 0;
                var b55 = parseInt(document.getElementById('5bl5').innerText) || 0;
                var b65 = parseInt(document.getElementById('6bl5').innerText) || 0;
                var b75 = parseInt(document.getElementById('7bl5').innerText) || 0;
                var b85 = parseInt(document.getElementById('8bl5').innerText) || 0;
                var b95 = parseInt(document.getElementById('9bl5').innerText) || 0;
                var b105 = parseInt(document.getElementById('10bl5').innerText) || 0;
                var b11a5 = parseInt(document.getElementById('11abl5').innerText) || 0;
                var b11b5 = parseInt(document.getElementById('11bbl5').innerText) || 0;
                var b12a5 = parseInt(document.getElementById('12abl5').innerText) || 0;
                var b12b5 = parseInt(document.getElementById('12bbl5').innerText) || 0;
                var b13a5 = parseInt(document.getElementById('13abl5').innerText) || 0;
                var b13b5 = parseInt(document.getElementById('13bbl5').innerText) || 0;
                var b14a5 = parseInt(document.getElementById('14abl5').innerText) || 0;
                var b14b5 = parseInt(document.getElementById('14bbl5').innerText) || 0;
                var b15a5 = parseInt(document.getElementById('15abl5').innerText) || 0;
                var b15b5 = parseInt(document.getElementById('15bbl5').innerText) || 0;
                var b16a5 = parseInt(document.getElementById('16abl5').innerText) || 0;
                var b16b5 = parseInt(document.getElementById('16bbl5').innerText) || 0;
        
                var b16 = parseInt(document.getElementById('1bl6').innerText) || 0;
                var b26 = parseInt(document.getElementById('2bl6').innerText) || 0;
                var b36 = parseInt(document.getElementById('3bl6').innerText) || 0;
                var b46 = parseInt(document.getElementById('4bl6').innerText) || 0;
                var b56 = parseInt(document.getElementById('5bl6').innerText) || 0;
                var b66 = parseInt(document.getElementById('6bl6').innerText) || 0;
                var b76 = parseInt(document.getElementById('7bl6').innerText) || 0;
                var b86 = parseInt(document.getElementById('8bl6').innerText) || 0;
                var b96 = parseInt(document.getElementById('9bl6').innerText) || 0;
                var b106 = parseInt(document.getElementById('10bl6').innerText) || 0;
                var b11a6 = parseInt(document.getElementById('11abl6').innerText) || 0;
                var b11b6 = parseInt(document.getElementById('11bbl6').innerText) || 0;
                var b12a6 = parseInt(document.getElementById('12abl6').innerText) || 0;
                var b12b6 = parseInt(document.getElementById('12bbl6').innerText) || 0;
                var b13a6 = parseInt(document.getElementById('13abl6').innerText) || 0;
                var b13b6 = parseInt(document.getElementById('13bbl6').innerText) || 0;
                var b14a6 = parseInt(document.getElementById('14abl6').innerText) || 0;
                var b14b6 = parseInt(document.getElementById('14bbl6').innerText) || 0;
                var b15a6 = parseInt(document.getElementById('15abl6').innerText) || 0;
                var b15b6 = parseInt(document.getElementById('15bbl6').innerText) || 0;
                var b16a6 = parseInt(document.getElementById('16abl6').innerText) || 0;
                var b16b6 = parseInt(document.getElementById('16bbl6').innerText) || 0;
        
                var b5b6total = b15 + b25 + b35 + b45 + b55 + b65 + b75 + b85 + b95 + b105 + b11a5 + b11b5 + b12a5 + b12b5 + b13a5 + b13b5 + b14a5 + b14b5+ b15a5 + b15b5 + b16a5 + b16b5 + b16+ b26 + b36 + b46 + b56 + b66 + b76 + b86 + b96 + b106 + b11a6 + b11b6 + b12a6 + b12b6 + b13a6 + b13b6 + b14a6 + b14b6 + b15a6 + b15b6 + b16a6 + b16b6 ;
                document.getElementById('b5b6total').innerText='BL5+BL6='+b5b6total;

               
                var pertco1 = (totalco1 / 180) * 100;
                var pertco1Formatted = pertco1.toFixed(2);
                document.getElementById('ptco1').innerText = pertco1Formatted+'%';
                
                var pertco2 = (totalco2 / 180) * 100;
                var pertco2Formatted = pertco2.toFixed(2);
                document.getElementById('ptco2').innerText = pertco2Formatted+'%';

                var pertco3 = (totalco3 / 180) * 100;
                var pertco3Formatted = pertco3.toFixed(2);
                document.getElementById('ptco3').innerText = pertco3Formatted+'%';

                var pertco4 = (totalco4 / 180) * 100;
                var pertco4Formatted = pertco4.toFixed(2);
                document.getElementById('ptco4').innerText = pertco4Formatted+'%';
                
                var pertco5 = (totalco5 / 180) * 100;
                var pertco5Formatted = pertco5.toFixed(2);
                document.getElementById('ptco5').innerText = pertco5Formatted+'%';
                
                var b1b2total = (b1b2total / 180) * 100;
                var pertbl1bl2Formatted = b1b2total.toFixed(2);
                document.getElementById('ptbl1bl2').innerText = pertbl1bl2Formatted+'%';
                
                var b3b4total = (b3b4total / 180) * 100;
                var pertbl3bl4Formatted = b3b4total.toFixed(2);
                document.getElementById('ptbl3bl4').innerText = pertbl3bl4Formatted+'%';
                
                var b5b6total = (b5b6total / 180) * 100;
                var pertbl5bl6Formatted = b5b6total.toFixed(2);
                document.getElementById('ptbl5bl6').innerText = pertbl5bl6Formatted+'%';
                
                

                
                
                </script>
                
                ";



            }



        } else {
            echo "<p>No data available for this details</p>";
            echo "<p>Please Check Once Again</p>";
            echo " <a href='retrievequestionpaper.html' style='margin-left:48%'>Back</a>";
        }

        $stmt->close();
    } else {
        die("Prepared statement failed: " . $conn->error);
    }





    $conn->close();
    ?>
</body>

</html>