<!DOCTYPE html>
<html>
<head>
    <title>Hotel Recommendation</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            background-image: url('images/bgimage2.webp'); /* Replace 'path/to/your/image.jpg' with the actual path to your image */
            background-size: cover;
        }
        h1 {
            text-align: center;
            color: black; /* Optional: Set text color to white for better visibility on the background image */
        }
        #city{
            padding:3px 20px 3px 20px;
        }

        form {
            display: flex;
            flex-direction: column;
            align-items: center; /* Updated alignment to left */
            margin-left: 20px; /* Add margin to create space from the left side */
            background-color: rgba(255, 255, 255, 0.8); /* Optional: Add a semi-transparent white background to the form for better visibility */
            padding: 20px; /* Optional: Add padding to the form for better appearance */
            border-radius: 20px; /* Set border radius to create curved corners */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <form action="" method="POST">
        <h1>Hotel Recommendation</h1>
        <label for="cities">Select City:</label>
        <select id="city" name="city">
            <option value="Select">Please Select city</option>
            <option value="Las_Vegas">Las Vegas</option>
            <option value="Boston">Boston</option>
            <option value="Miami_Beach">Miami Beach</option>
            <option value="Chicago">Chicago</option>
        
            <option value="San_Francisco">San_Francisco</option>
            <option value="New_Orleans">New_Orleans</option>
            <option value="Baltimore">Baltimore</option>
            <option value="Atlanta">Atlanta</option>
            <option value="Springfield">Springfield</option>
        </select><br><br>
        <label for="longitude">Longitude:</label>
        <input type="text" id="longitude" name="longitude"><br><br>
        <label for="latitude">Latitude:</label>
        <input type="text" id="latitude" name="latitude"><br><br>
        <input type="submit" value="Submit" name="submit">
    </form>
</body>
</html>

<?php
if (isset($_POST['submit'])) {
    $city = $_POST['city'];
    $longitude = $_POST['longitude'];
    $latitude = $_POST['latitude'];
    
    // Pass the input data to the Python file using the `exec` function
    exec("python3 main.py $city $longitude $latitude", $rest);
    
    // Display the output from the Python file

    
    echo '<style>
    table {
        display: flex
        border-collapse: collapse;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.8);; 
        border-radius: 10px; 
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
    }
    
    th, td {
        padding: 8px;
        text-align: left;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
</style>';

echo '<table>';

    foreach ($rest as $row) {
        $columns = explode('|', $row);
        echo '<tr>';
        foreach ($columns as $column) {
            echo '<td>' . $column . '</td>';
        }
        echo '</tr>';
    }

    echo '</table>';
}
?> 
