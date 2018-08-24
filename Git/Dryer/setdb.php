<?php 
function config_set($config_file, $section, $key, $value) {
    $config_data = parse_ini_file($config_file, true);
    $config_data[$section][$key] = $value;
        $new_content = '';
    foreach ($config_data as $section => $section_content) {
        $section_content = array_map(function($value, $key) {
            return "$key=$value";
        }, array_values($section_content), array_keys($section_content));
        $section_content = implode("\n", $section_content);
        $new_content .= "[$section]\n$section_content\n";
    }
    //echo $new_content;
    file_put_contents($config_file, $new_content);
    //echo 'file written';
}

if(isset($_POST['SubmitButton'])){       //check if form was submitted
	$dir = (__DIR__."/configfolder/config.ini");
if(isset($_POST['sm'])){
config_set($dir, "DEFAULT",  "set moisture %",  $_POST['sm']);}
if(isset($_POST['offset'])){
config_set($dir, "DEFAULT",  "offset",  $_POST['offset']);}
if(isset($_POST['factorA'])){
config_set($dir, "DEFAULT",  "factor a",  $_POST['factorA']);}
if(isset($_POST['factorB'])){
config_set($dir, "DEFAULT",  "factor b",  $_POST['factorB']);}
if(isset($_POST['minspeed'])){
config_set($dir, "DEFAULT",  "min motor speed",  $_POST['minspeed']);}
if(isset($_POST['maxspeed'])){
config_set($dir, "DEFAULT",  "max motor speed",  $_POST['maxspeed']);}
if(isset($_POST['interval'])){
config_set($dir, "DEFAULT",  "reading interval",  $_POST['interval']);}
if(isset($_POST['alertlow'])){
config_set($dir, "DEFAULT",  "limit alert low",  $_POST['alertlow']);}
if(isset($_POST['alerthigh'])){
config_set($dir, "DEFAULT",  "limit alert high",  $_POST['alerthigh']);}
if(isset($_POST['HforGraph'])){
config_set($dir, "DEFAULT",  "hours for graphs",  $_POST['HforGraph']);}
if(isset($_POST['ITime'])){
config_set($dir, "DEFAULT",  "integration time",  $_POST['ITime']);}

echo "
<script>
alert('Settings were changed successfully');
 window.location=document.referrer;
</script> ";


} else {
	
?>
<script>
alert("Settings were NOT changed! \nPrevious settings will be reloaded...");
 window.location=document.referrer;
</script> ";
<?php
}
?>
