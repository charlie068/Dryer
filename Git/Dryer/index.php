<!DOCTYPE html><html lang="en-GB">
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
		<div id="Humidity"> 
		<h2>Seed Humidity</h2>
		<div class="chart-container">
			<canvas id="mycanvas"></canvas>
		</div>
        </div>
        <div id="Temperature"> 
		<h2>Seed Temperature</h2>
		<div class="chart-container">
			<canvas id="mycanvas2"></canvas>
		</div>
        </div>
        <div id="Air"> 
        <h2>Air Parameters</h2>
		<div class="chart-container">
			<canvas id="mycanvas3"></canvas>
		</div>
        </div>
		
		<!-- javascript -->
		</div>
		<script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>
		<script type="text/javascript" src="js/Chart.bundle.min.js"></script>
		<script type="text/javascript" src="js/linegraph.js"></script>
		<script>
		window.setInterval(function(){
		refreshgraph();
		}, 30000);
		</script>
	</body>
</html>
