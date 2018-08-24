<?php
$dir = (__DIR__."/configfolder/config.ini");
$ini_array = parse_ini_file($dir, true);
$HforGraph=$ini_array['DEFAULT']['hours for graphs'];

$Ti=date("Y-m-d H:i:s");
$TiRange=date('Y-m-d H:i:s', strtotime('-'.$HforGraph.' hour', strtotime($Ti)));

//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', '127.0.0.1');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', '');
define('DB_NAME', 'Sechoirdb');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);



if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

//query to get data from the table
$query = sprintf("SELECT * FROM Data WHERE Time BETWEEN \"".$TiRange."\" AND \"".$Ti."\"");

//execute query
$result = $mysqli->query($query);

//loop through the returned data
$data = array();
foreach ($result as $row) {
	$data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

//now print the data
print json_encode($data);

