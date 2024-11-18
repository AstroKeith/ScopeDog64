<!DOCTYPE html>
<html>
<head>
	<title>Efinder Lite</title>
	
</head>
<body bgcolor="#000000" text="#FFFFFF">
	<h3 align="center">efinderSd.config file</h3><br>
	
	<table><tr><td>
	<form action='saveEf.php' method='post'>
	</td><td> </td></tr>
<?php


$filename = "/home/scopedog/eFinderSd.config";
chmod($filename, 0777);

$html = "";
$fp=fopen("/home/scopedog/eFinderSd.config", "r");
print_r($myVar);
while(!feof($fp)) {
	$line = fgets($fp);
	$sp =  strpos($line,":");

	$sdType= substr($line, 0, $sp);
	$sdValue= substr($line, $sp+1);
	
	switch ($sdType) {

		case "d_x":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Finder to Main scope x offset, set automatically";
			break;
		case "d_y":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Finder to Main scope y offset, set automatically";
			break;
		case "Brightness":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " OLED display brightness, 1 to 255";
			break;
		case "Exposure":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Default camera exposure time";
			break;
		case "Gain":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Default camera gain";
			break;	
		case "Ramdisk":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " set to 'True' to use RAM for temporary image storage (recommended), else 'False'";
			break;
		case "Camera":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter 'ASI' or RPI' as appropriate";
			break;
		case "Flip":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter 'auto', 'right' or 'left' as appropriate";
			break;
		case "Array_size":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Format width x height as '1280x960'";
			break;
		case "Pixel_size":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter pix scale in arcseconds'";
			break;
		case "Drive":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter 'scopedog', 'servocat', 'sitech' or 'none'";
			break;
		case "Test_mode":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter '1' to cause eFinder to use test images for solving (ie not the camera), else '0'";
			break;
		case "Goto++_mode":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter '1' to enable automatic GoTo++ mode' else '0'";
			break;
		case "Lens_focal_length":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter camera lens focal length, in millimeters";
			break;
		case "volt_alarm":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Enter minimum voltage to trigger alarm";
			break;
	}
	$html .= "</td></tr>";
}
echo $html;

?>
<tr><td>
<INPUT TYPE="submit"  value="Save Config File">
</td></form><td> 
<!-- 
<form action="runScopeDog.php" method="post">
<INPUT type="submit" value="Run ScopeDog">
</form>
 -->

</td></tr>

</table>

</body>
</html>


