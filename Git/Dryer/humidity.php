<?php 

  
	$dir = (__DIR__."/configfolder/config.ini");

	$ini_array = parse_ini_file($dir, true);
	//print_r($ini_array['DEFAULT']['factor b']);
	$sm=number_format($ini_array['DEFAULT']['set moisture %'],2);



?>
<!DOCTYPE html>
<html lang="en-GB">

	<head> 
		<title>Sechoir - Humidity Setting</title>
        <LINK REL="shortcut icon" HREF="/sechoirflavi.ico">
<link href="css/bootstrap.css" rel="stylesheet" id="bootstrap-css">
<link href="css/style_main.css" rel="stylesheet" id="main-css">
<script src="js/jquery-2.1.4.min.js"></script>
<script src="js/bootstrap.min.js"></script>



</head>
<body> 
	 <div class="container">
 

  
<?php include "./menu.php"; ?>

	<h2>Humidity settings</h2> 

		  <form action="/setdb.php" method="post">
			<form method="post" action="/setdb.php"> 
	
      <div class="input-group">	
          <span class="input-group-btn">
              <button type="button" class="btn btn-danger btn-number"  data-type="minus" data-field="sm">
                <span class="glyphicon glyphicon-minus"></span>
              </button>
          </span>
          <input type="text" name="sm" class="form-control input-number" type="number" value="<?php echo $sm;?>" min="5" max="30">
          <span class="input-group-btn">
              <button type="button" class="btn btn-success btn-number" data-type="plus" data-field="sm">
                  <span class="glyphicon glyphicon-plus"></span>
              </button>
          </span>
       
          </div>
 
		
          <div class="input-group">
		
            <input type="submit" name="Cancel" class="buttonp" id="button1" value="Cancel"/>
		  
		  <input type="submit" name="SubmitButton" class="buttonp" id="button2" value="Submit"/>
		
      </div>
	<p></p>
	

</div>
	
	</form> 	

    

	
	</div>
		<script>
//plugin bootstrap minus and plus
//http://jsfiddle.net/laelitenetwork/puJ6G/

$('.btn-number').click(function(e){
    e.preventDefault();
    
    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseFloat(input.val()); 
    if (!isNaN(currentVal)) {
        if(type == 'minus') {
            
            if(currentVal > input.attr('min')) {
                input.val((parseFloat(currentVal)- 0.1).toFixed(2)).change();
               
            } 
            if(parseFloat(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(parseFloat(currentVal + 0.1).toFixed(2)).change();
            }
            if(parseFloat(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});
$('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});
$('.input-number').change(function() {
    
    minValue =  parseFloat($(this).attr('min'));
    maxValue =  parseFloat($(this).attr('max'));
    valueCurrent = parseFloat($(this).val());
    
    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val(minValue);
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val(maxValue);
    }
    
    
});
$(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
    
    </script>	
	  
</body>
</html>


