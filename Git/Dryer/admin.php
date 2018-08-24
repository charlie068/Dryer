<!DOCTYPE html>
<html lang="en-GB">
	<head>
		<title>Sechoir</title>
		<link href="css/style_main.css" rel="stylesheet">
		<link href="css/bootstrap.css" rel="stylesheet">
        <LINK REL="shortcut icon" HREF="/sechoirflavi.ico">
		<style>
			.chart-container {
				width: auto;
				height: auto;
			}
		</style>
	</head>
	<body>
	
	<div class="container">
		
		<?php include "./menu.php"; ?>
		
		
<?php

#sleep(2);	
$output=shell_exec("pgrep -f '[s]echoirD.py'");
$outputarr=preg_split('/\s+/', $output); 
#echo $output;
$progstarted=True;
if (count($outputarr)>1){
		$progstarted=True;
	}
	else {
		$progstarted=False;
	}
?>
		
		<h2>Parameters settings</h2> 
		<div class="grpbtn">
			

		    <form action="/prog.php" method="post">
			<label for="attente" <?php if ($progstarted) { ?> hidden <?php   } ?> >Time before start (min) </label>
			<input class="inputother"  type="text" name="attente" <?php if ($progstarted) { ?> hidden <?php   } ?> value="0">
		    <input type="submit" name="prog" <?php if ($progstarted) { ?> disabled <?php   } ?> class="buttonp" id="button1" value="Start Program"/>
		    <input type="submit" name="prog" <?php if ($progstarted) { ?> disabled <?php   } ?> class="buttonp" id="button1" value="Record only"/>
			<input type="submit"  name="prog" <?php if (!$progstarted) { ?> disabled <?php   } ?> class="buttonp" id="button2" value="Stop Program"/>
			<input type="submit"  name="prog" <?php if ($progstarted) { ?> disabled <?php   } ?> class="buttonp" id="button1" value="Reset DB"/>
			
		
		</form> 
	</div>  
		</div>
	</body>
</html>
