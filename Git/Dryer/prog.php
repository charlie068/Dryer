<?php
#$username = posix_getpwuid(posix_geteuid())['name'];
#echo $username;
#putenv('PYTHONPATH=/home/pi/.local/lib/python3.5/site-packages');
if(isset($_POST['prog'])){  

    if(($_POST['prog'])=='Start Program'){ 
        #echo ("A");
        $command = escapeshellcmd('python/sechoirD.py ');
        echo ($_POST['attente']);
        $output = shell_exec($command . " " .$_POST['attente']. " E > /dev/null &");
        #$output = shell_exec($command);
        #echo ($output);
        
        ?>
        <script>
            
        alert('Program started');
        window.location=document.referrer;
        </script>
        <?php


    } else if (($_POST['prog'])=='Record only'){ 
		#echo ("A");
        $command = escapeshellcmd('python/sechoirD.py ');
        
        $output = shell_exec($command . " " .$_POST['attente']. " R > /dev/null &");
        #$output = shell_exec($command);
        #echo ($output);
        
        ?>
        <script>
            
        alert('Program started');
        window.location=document.referrer;
        </script>
        <?php
    
    
    
    
    } else if (($_POST['prog'])=='Stop Program'){  
        
        
        $command = escapeshellcmd('pkill -9 -f [p]ython');
        $output = shell_exec($command. " > /dev/null &");
        #exec('pkill -9 -f [p]ython');
         
        
        echo ($output);
        ?>
        <script>
        alert('Program Stopped');
        window.location=document.referrer;
        </script>
        <?php
      }
      
      else if (($_POST['prog'])=='Reset DB'){ 
          
          $command = escapeshellcmd('python/sechoirD.py delete');
          $output = shell_exec($command . " > /dev/null &");
          ?>
        <script>
        alert('Database has been reset');
        window.location=document.referrer;
        </script>
        <?php
          
      } 
}
      
?>




