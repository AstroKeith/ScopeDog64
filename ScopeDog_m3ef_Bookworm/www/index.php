<!DOCTYPE html>
<html>
<head>
<title>ScopeDog & Efinder</title>

</head>
<body bgcolor="#000000" text="#FFFFFF">
<h3 align="center">Select ScopeDog or eFinder</h3><br>
<form action='Sdog.php' method='post'>
<INPUT TYPE="submit"  value="ScopeDog">
</form>
<form action='eF.php' method='post'>
<INPUT TYPE="submit"  value="eFinder">
</form>

</body>
</html>

<?php

$image = '/home/scopedog/Solver/Stills/image.jpg';
$imageData = base64_encode(file_get_contents($image));
echo '<img src="data:image/jpg;base64,'.$imageData.'">';
?>
