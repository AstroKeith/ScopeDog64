<!DOCTYPE html>
<html>
<head>
	<title>eFinder</title>
	
</head>
<body bgcolor="#000000" text="#FFFFFF">
<?php
$html = "";
$d_x = $_POST['d_x'];
$d_y = $_POST['d_y'];
$Brightness = $_POST['Brightness'];
$Exposure = $_POST['Exposure'];
$Gain = $_POST['Gain'];
$Ramdisk = $_POST['Ramdisk'];
$Camera = $_POST['Camera'];
$Flip = $_POST['Flip'];
$Array_size = $_POST['Array_size'];
$Pixel_size =$_POST['Pixel_size'];
$Drive = $_POST['Drive'];
$Test_mode = $_POST['Test_mode'];
$Goto_mode = $_POST['Goto++_mode'];
$Lens = $_POST['Lens_focal_length'];
$volt_alarm = $_POST['volt_alarm'];

$filename = "/home/scopedog/eFinderSd.config";
chmod($filename, 0777);

$fp = fopen("/home/scopedog/eFinderSd.config", "w") or die("Unable to open file!");
$txt = "d_x:" . $d_x . "\n";
fwrite($fp, $txt);
$txt = "d_y:" . $d_y . "\n";
fwrite($fp, $txt);
$txt = "Brightness:" . $Brightness . "\n";
fwrite($fp, $txt);
$txt = "Exposure:" . $Exposure . "\n";
fwrite($fp, $txt);
$txt = "Gain:" . $Gain . "\n";
fwrite($fp, $txt);
$txt = "Ramdisk:" . $Ramdisk . "\n";
fwrite($fp, $txt);
$txt = "Camera:" . $Camera . "\n";
fwrite($fp, $txt);
$txt = "Flip:" . $Flip . "\n";
fwrite($fp, $txt);
$txt = "Array_size:" . $Array_size . "\n";
fwrite($fp, $txt);
$txt = "Pixel_size:" . $Pixel_size . "\n";
fwrite($fp, $txt);
$txt = "Drive:" . $Drive . "\n";
fwrite($fp, $txt);
$txt = "Test_mode:" . $Test_mode . "\n";
fwrite($fp, $txt);
$txt = "Goto++_mode:" . $Goto_mode . "\n";
fwrite($fp, $txt);
$txt = "Lens_focal_length:" . $Lens . "\n";
fwrite($fp, $txt);
$txt = "volt_alarm:" . $volt_alarm . "\n";
fwrite($fp, $txt);
fclose($fp);

?>

	<h3 align="center">efinderSd.config file</h3><br>
	
	<table><tr><td>
	<form action='saveEf.php' method='post'>
	</td><td> </td></tr>
<?php
$html = "";
$fp=fopen('/home/scopedog/eFinderSd.config', 'r');
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
</td><td> </td></tr>
</form>
</table>

</body>
</html>

