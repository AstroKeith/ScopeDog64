<!DOCTYPE html>
<html>
<head>
	<title>Scope Dog</title>
	
</head>
<body bgcolor="#000000" text="#FFFFFF">
	<h3 align="center">runScopeDog</h3><br>
<?php 

$command = escapeshellcmd('sudo /home/scopedog/StartScope.py run');
shell_exec($command);
//echo $output;

?>
</body>
</html>
