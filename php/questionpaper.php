<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
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

    // Loop through each question
    for ($i = 1; $i <= 22; $i++) {
        @$userInput = $_POST["q$i"];
        $words = explode(" ", $userInput);

        $sqlColumns = "SHOW COLUMNS FROM keywords1";
        $resultColumns = $conn->query($sqlColumns);

        $matchedColumn = null;

        if ($resultColumns->num_rows > 0) {
            while ($rowColumn = $resultColumns->fetch_assoc()) {
                $columnName = $rowColumn["Field"];

                $sql = "SELECT * FROM keywords1 WHERE $columnName = ?";
                $stmt = $conn->prepare($sql);

                foreach ($words as $word) {
                    $word = trim($word);
                    if ($word != '') {
                        $stmt->bind_param("s", $word);
                        $stmt->execute();
                        $result = $stmt->get_result();

                        if ($result->num_rows > 0) {
                            $matchedColumn = $columnName;
                            break;
                        }
                    }
                }

                $stmt->close();

                if ($matchedColumn) {
                    echo "<h3 id='column$i' style='display:none'>$matchedColumn</h3>";
                    break;
                }
            }

            if (!$matchedColumn) {
                echo "<h3 id='column$i' style='display:none'>No bloom word Matched</h3>";
            }
        }
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html>

<head>
    <style>
        .cen {
            text-align: center;
        }

        body {
            font-family: 'Arial', sans-serif;
            background-color: #f2f2f2;
            margin: 20px;
        }

        form {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }

        table,
        th {
            border: 1px solid #ddd;
        }

        th,
        td {
            padding: 10px;
            text-align: left;
        }


        th {
            background-color: #3498db;
            color: #fff;
        }

        textarea {
            height: 50px;
            width: 100%;
            padding: 3px;
            font-size: 1rem;

        }


        input[type='text'],
        input[type='number'],
        select {
            height: 35px;
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 16px;
            font-size: 1rem;
        }

        select {
            cursor: pointer;
        }

        button {
            background-color: #4caf50;
            color: #fff;
            border: none;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }

        button:hover {
            background-color: #45a049;
        }

        button[type='submit'] {
            background-color: #008CBA;
        }

        button[type='submit']:hover {
            color: black;
            background-color: lightblue;
        }

        a {
            color: #008CBA;
            text-decoration: none;
            font-weight: bold;
            margin-left: 10px;
        }

        a:hover {
            color: white;
            background-color: greenyellow;
            border-radius: 10px;
        }

        #insert {
            margin-left: 50%
        }

        * {
            text-align: center;
        }
    </style>
</head>

<body>
    
<a href="faculty.html" style="margin-right:62%">Back</a>  
    <form method="post" action="" onsubmit="return validateForm();" id="myForm">
        <h3>Exam Details</h3>
        <table align="center" border="5">
            <tr>
                <td class='cen'>Subject Code:</td>
                <td>
                    <input type="text" required name="subject_code" id="subject_code" oninput="convertToUpperCase(this)"
                        value="<?php echo isset($_POST['subject_code']) ? htmlspecialchars($_POST['subject_code']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Subject Name:</td>
                <td>
                    <input type="text" required name="subject_name" id="subject_name" oninput="capitalizeEachWord(this)"
                        value="<?php echo isset($_POST['subject_name']) ? htmlspecialchars($_POST['subject_name']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Semester:</td>
                <td>
                    <input type="text" required name="semester" id="semester" placeholder="EX:3rd"
                        value="<?php echo isset($_POST['semester']) ? htmlspecialchars($_POST['semester']) : ''; ?>">
                </td>
            </tr>

            <tr>
                <td class='cen'>Year of Student:</td>
                <td>
                    <input type="text" required name="year_of_student" id="year_of_student" placeholder="EX:2nd"
                        value="<?php echo isset($_POST['year_of_student']) ? htmlspecialchars($_POST['year_of_student']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Academic Year:</td>
                <td><input type="text" required name="academic_year" id="academic_year" placeholder="EX:2020-2021"
                        value="<?php echo isset($_POST['academic_year']) ? htmlspecialchars($_POST['academic_year']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Faculty ID:</td>
                <td><input type="number" required name="faculty_id" id="faculty_id" class="num"
                        value="<?php echo isset($_POST['faculty_id']) ? htmlspecialchars($_POST['faculty_id']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Question Paper ID:</td>
                <td><input type="number" required name="questionpaperid" id="questionpaperid" class="num"
                        value="<?php echo isset($_POST['questionpaperid']) ? htmlspecialchars($_POST['questionpaperid']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Exam Type:</td>
                <td>
                    <select name="examtype" id="examtype" required>
                        <option value=''>TYPE</option>
                        <option value='INTERNAL ASSESMENT-I' <?php echo (isset($_POST['examtype']) && $_POST['examtype'] === 'INTERNAL ASSESMENT-I') ? 'selected' : ''; ?>>INTERNAL ASSESMENT-I
                        </option>
                        <option value='INTERNAL ASSESMENT-II' <?php echo (isset($_POST['examtype']) && $_POST['examtype'] === 'INTERNAL ASSESMENT-II') ? 'selected' : ''; ?>>INTERNAL ASSESMENT-II
                        </option>
                        <option value='SEMESTER EXAMINATION' <?php echo (isset($_POST['examtype']) && $_POST['examtype'] === 'SEMESTER EXAMINATION') ? 'selected' : ''; ?>>SEMESTER EXAMINATION
                        </option>
                    </select>
                </td>
            </tr>
            <tr>
                <td class='cen'>Department:</td>
                <td><input type="text" required name="dep" id="dep" oninput="capitalizeEachWord(this)"
                        placeholder="EX:B.Tech Information Technology"
                        value="<?php echo isset($_POST['dep']) ? htmlspecialchars($_POST['dep']) : ''; ?>">
                </td>
            </tr>
            <tr>
                <td class='cen'>Date of Exam:</td>
                <td><input type="text" required name="dateofexam" id="dateofexam" placeholder="dd/mm/yyyy"
                        value="<?php echo isset($_POST['dateofexam']) ? htmlspecialchars($_POST['dateofexam']) : ''; ?>">
                </td>
            </tr>
        </table>
        <br>
        <hr>
        <br>
        <table border="1" align="center">
            <tr>
                <th class='cen' style='padding: 0%;'>Q.NO</th>
                <th class='cen' style='width: 50%;'>Question</th>
                <th class="cen" style='width: 10%;'>Unit No</th>
                <th class='cen' style='width: 10%;'>Mark</th>
                <th class='cen' style='width: 13%;'>Course<br>Outcome</th>
                <th class='cen' style='width: 23%;'>Bloom Level</th>
            </tr>
            <?php
            for ($i = 1; $i <= 10; $i++) {
                echo "<tr>
            <td>$i</td>
            <td>
                <textarea rows='3' cols='8' required class='cen' style='width: 100%;' name='q$i' id='q$i'>" . (isset($_POST["q$i"]) ? htmlspecialchars($_POST["q$i"]) : '') . "</textarea>
            </td>
            <td>
                <input type='number' required style='width:100%;' name='u$i' id='u$i'
                    value='" . (isset($_POST["u$i"]) ? htmlspecialchars($_POST["u$i"]) : '') . "'>
            </td>
            <td>
                <input type='number' required style='width:100%;' name='m$i' id='m$i'
                    value='" . (isset($_POST["m$i"]) ? htmlspecialchars($_POST["m$i"]) : '') . "'>
            </td>


            <td>
                <select name='co$i' id='co$i' required>
                    <option value=''>CO</option>
                    <option value='CO1' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO1' ? 'selected' : '') . ">CO1</option>
                    <option value='CO2' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO2' ? 'selected' : '') . ">CO2</option>
                    <option value='CO3' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO3' ? 'selected' : '') . ">CO3</option>
                    <option value='CO4' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO4' ? 'selected' : '') . ">CO4</option>
                    <option value='CO5' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO5' ? 'selected' : '') . ">CO5</option>
                    <option value='CO6' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO6' ? 'selected' : '') . ">CO6</option>
                </select>
            </td>
            <td>
                <input type='text' id='b$i' class='font' name='b$i' required readonly >
            </td>
        </tr>";
            }

              for ($i = 21; $i <= 32; $i++) {
                $numeric_suffix = ceil($i / 2);
                $alphabetic_suffix = ($i % 2 == 0) ? 'b' : 'a';

                // Combine both suffixes for the desired pattern
                $combined_suffix = $numeric_suffix . $alphabetic_suffix;
                $i = $i - 10;
                

                echo "<tr>
                <td>$combined_suffix</td>
                <td>
                <textarea rows='3' cols='8' required class='cen' style='width: 100%;' name='q$i' id='q$i'>" . (isset($_POST["q$i"]) ? htmlspecialchars($_POST["q$i"]) : '') . "</textarea>
            </td>
                <td>
    <input type='number' required style='width:100%;' name='u$i' id='u$i' value='" . (isset($_POST["u$i"]) ?
                    htmlspecialchars($_POST["u$i"]) : '') . "'>
</td>       
            <td>
    <input type='number' required style='width:100%;' name='m$i' id='m$i' value='" . (isset($_POST["m$i"]) ?
                    htmlspecialchars($_POST["m$i"]) : '') . "'>
</td>

            <td>
                <select name='co$i' id='co$i' required style='width: 95%;'>
                    <option value=''>CO</option>
                    <option value='CO1' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO1' ? 'selected' : '') . ">CO1</option>
                    <option value='CO2' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO2' ? 'selected' : '') . ">CO2</option>
                    <option value='CO3' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO3' ? 'selected' : '') . ">CO3</option>
                    <option value='CO4' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO4' ? 'selected' : '') . ">CO4</option>
                    <option value='CO5' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO5' ? 'selected' : '') . ">CO5</option>
                    <option value='CO6' " . (isset($_POST["co$i"]) && $_POST["co$i"] == 'CO6' ? 'selected' : '') . ">CO6</option>
                </select>
            </td>
            <td>
                <input type='text' id='b$i' class='font' name='b$i' required readonly >
            </td>
        </tr>";
                $i = $i + 10;
            } ?>
        </table>
        <br>

        <button type="submit">Validate</button>
        <button type="button" onclick="return reload1();">Clear</button>
        <button type="button" onclick="return bloom();">bloom</button><br><br>
        <button type="submit" id="insert" style="display: none;" onclick="openSphp()">Insert</button>

    </form>



    <script>

        function reload1() {

            // Clearing values in input fields
            document.getElementsByName('subject_code')[0].value = '';
            document.getElementsByName('subject_name')[0].value = '';
            document.getElementsByName('semester')[0].value = '';
            document.getElementsByName('year_of_student')[0].value = '';
            document.getElementsByName('academic_year')[0].value = '';
            document.getElementsByName('faculty_id')[0].value = '';
            document.getElementsByName('questionpaperid')[0].value = '';


            // Clearing values in dynamic input fields
            for (var i = 1; i <= 22; i++) {
                document.getElementById('q' + i).value = '';
                document.getElementById('m' + i).value = '';
                document.getElementById('co' + i).value = '';
            }

            // Clearing the h3 elements
            for (var i = 1; i <= 22; i++) {
                document.getElementById('column' + i).innerText = '';
            }
            for (let i = 1; i <= 22; i++) {
                document.getElementById('b' + i).innerText = '';
            }
        }
        function bloom() {
            for (let i = 1; i <= 22; i++) {
                var columnElement = document.getElementById("column" + i);
                var inputElement = document.getElementById("b" + i);

                // Get the value of id="column$i"
                var columnValue = columnElement.innerText;

                // Update the value of the input element with the retrieved value
                inputElement.value = columnValue;
            }
            document.getElementById("insert").style.display = "block";
            return false;
        }


        function openSphp() {
            let isValid = true;

            for (let i = 1; i <= 22; i++) {
                const columnElement = document.getElementById("column" + i);
                const inputElement = document.getElementById("b" + i);

                if (columnElement.innerText.trim() === 'No bloom word Matched') {
                    isValid = false;
                    alert("Enter a valid keyword for Bloom Level in question " + i);
                    break;
                    return false;
                } else {
                    inputElement.value = columnElement.innerText;
                }
            }

            if (isValid) {
                document.forms[0].action = "questionpaperinsert.php";
                document.forms[0].submit();
            }
        }
        function convertToUpperCase(inputField) {
            // Get the user input value
            var userInput = inputField.value;

            // Convert to uppercase
            var uppercaseText = userInput.toUpperCase();

            // Update the input field with the uppercase value
            inputField.value = uppercaseText;
        }

        function capitalizeEachWord(inputField) {
            // Get the user input value
            var userInput = inputField.value.toLowerCase();

            // Capitalize each word
            var capitalizedText = userInput.replace(/\b\w/g, function (char) {
                return char.toUpperCase();
            });

            // Update the input field with the capitalized value
            inputField.value = capitalizedText;
        }






    </script>
</body>

</html>