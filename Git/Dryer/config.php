<?php 

  
	$dir = (__DIR__."/configfolder/config.ini");

	$ini_array = parse_ini_file($dir, true);
	//print_r($ini_array['DEFAULT']['factor b']);
	$sm=$ini_array['DEFAULT']['set moisture %'];
	$offset=$ini_array['DEFAULT']['offset'];
	$factorA=$ini_array['DEFAULT']['factor a'];
	$factorB=$ini_array['DEFAULT']['factor b'];
	$minspeed=$ini_array['DEFAULT']['min motor speed'];
	$maxspeed=$ini_array['DEFAULT']['max motor speed'];
	$interval=$ini_array['DEFAULT']['reading interval'];
	$alertlow=$ini_array['DEFAULT']['limit alert low'];
	$alerthigh=$ini_array['DEFAULT']['limit alert high'];
    $HforGraph=$ini_array['DEFAULT']['hours for graphs'];
	$ITime=$ini_array['DEFAULT']['integration time'];


?>
<!DOCTYPE html><html lang="en-GB">
	<head> 
        <LINK REL="shortcut icon" HREF="/sechoirflavi.ico">
		<title>Sechoir - Other Settings</title>
		<link href="css/bootstrap.css" rel="stylesheet" id="bootstrap-css">
	<link href="css/style_main.css" rel="stylesheet" id="main-css">
	



	</head>
<body>  
	<div class="container">
<?php include "./menu.php"; ?>
		<h2>Parameters settings</h2> 
		<div class="grpbtn">

		    <form action="/setdb.php" method="post">
			
				
			<label for="sm">Set Moisture (% Humidity):</label>
			<input class="inputother" type="text" name="sm" value="<?php echo $sm;?>"> 
			
			
			<label for="offset">Offset:</label>
			<input class="inputother" type="text" name="offset" value="<?php echo $offset;?>">
			
			<label for="factorA">Factor A:</label>
			<input class="inputother"  type="text" name="factorA" value="<?php echo $factorA;?>">
			
			<label for="factorB" >Factor B:</label>
			<input class="inputother"  type="text" name="factorB" value="<?php echo $factorB;?>"> 
			
			<label for="minspeed">Motor minimum speed (Hz):</label>
			<input class="inputother"  type="text" name="minspeed" value="<?php echo $minspeed;?>"> 
			
			<label for="maxspeed">Motor maximum speed (Hz):</label>
			<input class="inputother"  type="text" name="maxspeed" value="<?php echo $maxspeed;?>"> 
			
			<label for="interval">Reading interval (minutes):</label>
			<input class="inputother"  type="text" name="interval" value="<?php echo $interval;?>"> 
			
			<label for="alertlow">Email alert when humidity is lower than (% Humidity):</label>
			<input class="inputother"  type="text" name="alertlow" value="<?php echo $alertlow;?>"> 
			
			<label for="alerthigh">Email alert when humidity is higher than (% Humidity):</label>
			<input class="inputother"  type="text" name="alerthigh" value="<?php echo $alerthigh;?>"> <br />
            
            <label for="HforGraph">Time to show on Graphs (hours):</label>
			<input class="inputother"  type="text" name="HforGraph" value="<?php echo $HforGraph;?>"> <br />
            
            <label for="ITime">Integration Time for the dryer (hours)</label>
			<input class="inputother"  type="text" name="ITime" value="<?php echo $ITime;?>"> <br />
            
			<input type="submit" name="Cancel" class="buttonp" id="button1" value="Cancel"/>
			   
		   
				
				<input type="submit" name="SubmitButton" class="buttonp" id="button2" value="Submit"/>
		
		</form> 
	</div>  
	</div>
	</div>
	  
</body>
</html>


