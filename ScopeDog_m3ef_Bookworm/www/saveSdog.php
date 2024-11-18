<!DOCTYPE html>
<html>
<head>
	<title>Scope Dog</title>
	
</head>
<body bgcolor="#000000" text="#FFFFFF">
<?php
$html = "";
$Az_Gear_Ratio1 = $_POST['1_Az_Gear_Ratio:'];
$Alt_Gear_Ratio1 = $_POST['1_Alt_Gear_Ratio:'];
$Alt_Gear1 = $_POST['1_Alt_Gear:'];
$Az_Direction1 = $_POST['1_Az_Direction:'];
$Current_Limit1 = $_POST['1_Current_Limit:'];
$azVelocity1 = $_POST['1_azVelocity:'];
$altVelocity1 = $_POST['1_altVelocity:'];
$SlewSpeedSlow1 = $_POST['1_SlewSpeedSlow:'];
$SlewSpeedMed1 = $_POST['1_SlewSpeedMed:'];
$AutoStart1 = $_POST['1_AutoStart:'];
$Backlash1 = $_POST['1_Backlash:'];
$flip_AltF1 = $_POST['1_flip_AltF:'];
$flip_AltS1 = $_POST['1_flip_AltS:'];
$flip_AzF1 = $_POST['1_flip_AzF:'];
$flip_AzS1 = $_POST['1_flip_AzS:'];
$Az_Gear_Ratio2 = $_POST['2_Az_Gear_Ratio:'];
$Alt_Gear_Ratio2 = $_POST['2_Alt_Gear_Ratio:'];
$Alt_Gear2 = $_POST['2_Alt_Gear:'];
$Az_Direction2 = $_POST['2_Az_Direction:'];
$Current_Limit2 = $_POST['2_Current_Limit:'];
$azVelocity2 = $_POST['2_azVelocity:'];
$altVelocity2 = $_POST['2_altVelocity:'];
$SlewSpeedSlow2 = $_POST['2_SlewSpeedSlow:'];
$SlewSpeedMed2 = $_POST['2_SlewSpeedMed:'];
$AutoStart2 = $_POST['2_AutoStart:'];
$Backlash2 = $_POST['2_Backlash:'];
$flip_AltF2 = $_POST['2_flip_AltF:'];
$flip_AltS2 = $_POST['2_flip_AltS:'];
$flip_AzF2 = $_POST['2_flip_AzF:'];
$flip_AzS2 = $_POST['2_flip_AzS:'];
$fp = fopen("/home/scopedog/ScopeDog.config", "w") or die("Unable to open file!");
$txt = "1_AutoStart: " . $AutoStart1 . "\n";
fwrite($fp, $txt);
$txt = "1_Az_Gear_Ratio: " . $Az_Gear_Ratio1 . "\n";
fwrite($fp, $txt);
$txt = "1_Alt_Gear_Ratio: " . $Alt_Gear_Ratio1 . "\n";
fwrite($fp, $txt);
$txt = "1_Alt_Gear: " . $Alt_Gear1 . "\n";
fwrite($fp, $txt);
$txt = "1_Az_Direction: " . $Az_Direction1 . "\n";
fwrite($fp, $txt);
$txt = "1_Current_Limit: " . $Current_Limit1 . "\n";
fwrite($fp, $txt);
$txt = "1_azVelocity: " . $azVelocity1 . "\n";
fwrite($fp, $txt);
$txt = "1_altVelocity: " . $altVelocity1 . "\n";
fwrite($fp, $txt);
$txt = "1_SlewSpeedSlow: " . $SlewSpeedSlow1 . "\n";
fwrite($fp, $txt);
$txt = "1_SlewSpeedMed: " . $SlewSpeedMed1 . "\n";
fwrite($fp, $txt);
$txt = "1_Backlash: " . $Backlash1 . "\n";
fwrite($fp, $txt);
$txt = "1_flip_AltF: " . $flip_AltF1 . "\n";
fwrite($fp, $txt);
$txt = "1_flip_AltS: " . $flip_AltS1 . "\n";
fwrite($fp, $txt);
$txt = "1_flip_AzF: " . $flip_AzF1 . "\n";
fwrite($fp, $txt);
$txt = "1_flip_AzS: " . $flip_AzS1 . "\n";
fwrite($fp, $txt);
$txt = "2_AutoStart: " . $AutoStart2 . "\n";
fwrite($fp, $txt);
$txt = "2_Az_Gear_Ratio: " . $Az_Gear_Ratio2 . "\n";
fwrite($fp, $txt);
$txt = "2_Alt_Gear_Ratio: " . $Alt_Gear_Ratio2 . "\n";
fwrite($fp, $txt);
$txt = "2_Alt_Gear: " . $Alt_Gear2 . "\n";
fwrite($fp, $txt);
$txt = "2_Az_Direction: " . $Az_Direction2 . "\n";
fwrite($fp, $txt);
$txt = "2_Current_Limit: " . $Current_Limit2 . "\n";
fwrite($fp, $txt);
$txt = "2_azVelocity: " . $azVelocity2 . "\n";
fwrite($fp, $txt);
$txt = "2_altVelocity: " . $altVelocity2 . "\n";
fwrite($fp, $txt);
$txt = "2_SlewSpeedSlow: " . $SlewSpeedSlow2 . "\n";
fwrite($fp, $txt);
$txt = "2_SlewSpeedMed: " . $SlewSpeedMed2 . "\n";
fwrite($fp, $txt);
$txt = "2_Backlash: " . $Backlash2 . "\n";
fwrite($fp, $txt);
$txt = "2_flip_AltF: " . $flip_AltF2 . "\n";
fwrite($fp, $txt);
$txt = "2_flip_AltS: " . $flip_AltS2 . "\n";
fwrite($fp, $txt);
$txt = "2_flip_AzF: " . $flip_AzF2 . "\n";
fwrite($fp, $txt);
$txt = "2_flip_AzS: " . $flip_AzS2 . "\n";
fwrite($fp, $txt);
fclose($fp);

?>

	<h3 align="center">ScopeDog.config file</h3><br>
	
	<table><tr><td>
	<form action='saveSdog.php' method='post'>
	</td><td> </td></tr>
<?php
$html = "";
$fp=fopen('/home/scopedog/ScopeDog.config', 'r');
while(!feof($fp)) {
	$line = fgets($fp);
	$sp =  strpos($line," ");
	$sdType= substr($line, 0, $sp);
	$sdValue= substr($line, $sp+1);
	
	switch ($sdType) {
		case "1_flip_AltF:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Alt directions on joystick at Medium and Fast slew speeds";
			break;
		case "1_flip_AltS:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Alt directions on joystick at Slow speeds";
			break;
		case "1_flip_AzF:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Az directions on joystick at Medium and Fast slew speeds";
			break;
		case "1_flip_AzS:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Az directions on joystick at Slow speeds";
			break;
		case "1_Backlash:":
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='text' value='$sdValue'></td><td>";
			$html .= " Altitude backlash in arcmin";
			break;
		case "1_Az_Gear_Ratio:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			$azVelStart= ($sdValue/360)*10000;
			break;
		case "1_Alt_Gear_Ratio:":
			$altVelStart=($sdValue/360)*10000;
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			break;
		case "1_Alt_Gear:":
			$lCheck="";
			$rCheck="";

 			if(strcmp($sdValue,"Left\n")==0)
			{
				$lCheck="checked";
			}
			else
			{
				$rCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>A<input name=$sdType type=radio value='Left' $lCheck />
											  B<input name=$sdType type=radio value='Right' $rCheck /></td><td>";
			$html .= " If your Alt direction is wrong change this";
			break;
		case "1_Az_Direction:":
			$lCheck="";
			$rCheck="";

 			if(strcmp($sdValue,"A\n")==0)
			{
				$lCheck="checked";
			}
			else
			{
				$rCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>A<input name=$sdType type=radio value='A' $lCheck />
											  B<input name=$sdType type=radio value='B' $rCheck /></td><td>";
			$html .= " If your AZ direction is wrong change this";
			break;
		case "1_Current_Limit:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Max Amps Motors allowed to draw...3.0 is maximum but only set this as high as necessary or motors will get very very hot and reduce the life of the motor";
			break;
		case "1_azVelocity:":
			$iVal=intval ($azVelStart);
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " As a starting point change value to $iVal. The larger the value the faster the max Az speed. 
				Starting Value will change if you have changed gear ratio above. Save to refresh.";
			break;
		case "1_altVelocity:":
			$iVal=intval ($altVelStart);
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " As a starting point change value to $iVal. The larger the value the faster the max Alt speed. 
				Starting Value will change if you have changed gear ratio above. Save to refresh.";
			break;
		case "1_SlewSpeedSlow:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " If when centering object the slew is too fast increase this number...too slow decrease it";
			break;
		case "1_SlewSpeedMed:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " If when moving to object the medium slew is too fast increase this number...too slow decrease it";
			break;
		case "1_AutoStart:":
			$tCheck="";
			$fCheck="";

 			if(strcmp($sdValue,"True\n")==0)
			{
				$tCheck="checked";
			}
			else
			{
				$fCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>True<input name=$sdType type=radio value='True' $tCheck />
											  False<input name=$sdType type=radio value='False' $fCheck /></td><td>";
			$html .= " If true...next restart Scope Dog will automatically start";
			break;
		case "2_flip_AltF:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Alt directions on joystick at Medium and Fast slew speeds";
			break;
		case "2_flip_AltS:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Alt directions on joystick at Slow speeds";
			break;
		case "2_flip_AzF:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Az directions on joystick at Medium and Fast slew speeds";
			break;
		case "2_flip_AzS:":
			$faCheck="";
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='checkbox' value='checked' $sdValue > Flip</td><td>";
			$html .= " Flip Az directions on joystick at Slow speeds\n";
			break;
		case "2_Backlash:":
			$html .= "<tr><td>$sdType</td><td><input name='$sdType' type='text' value='$sdValue' ></td><td>";
			$html .= " Altitude backlash in arcmin";
			break;
		case "2_Az_Gear_Ratio:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			$azVelStart= ($sdValue/360)*10000;
			break;
		case "2_Alt_Gear_Ratio:":
			$altVelStart=($sdValue/360)*10000;
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			break;
		case "2_Alt_Gear:":
			$lCheck="";
			$rCheck="";

				if(strcmp($sdValue,"Left\n")==0)
			{
				$lCheck="checked";
			}
			else
			{
				$rCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>A<input name=$sdType type=radio value='Left' $lCheck />
												B<input name=$sdType type=radio value='Right' $rCheck /></td><td>";
			$html .= " If your Alt direction is wrong change this";
			break;
		case "2_Az_Direction:":
			$lCheck="";
			$rCheck="";

				if(strcmp($sdValue,"A\n")==0)
			{
				$lCheck="checked";
			}
			else
			{
				$rCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>A<input name=$sdType type=radio value='A' $lCheck />
												B<input name=$sdType type=radio value='B' $rCheck /></td><td>";
			$html .= " If your AZ direction is wrong change this";
			break;
		case "2_Current_Limit:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Max Amps Motors allowed to draw...3.0 is maximum but only set this as high as necessary or motors will get very very hot and reduce the life of the motor";
			break;
		case "2_azVelocity:":
			$iVal=intval ($azVelStart);
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " As a starting point change value to $iVal. The larger the value the faster the max Az speed. 
				Starting Value will change if you have changed gear ratio above. Save to refresh.";
			break;
		case "2_altVelocity:":
			$iVal=intval ($altVelStart);
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " As a starting point change value to $iVal. The larger the value the faster the max Alt speed. 
				Starting Value will change if you have changed gear ratio above. Save to refresh.";
			break;
		case "2_SlewSpeedSlow:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " If when centering object the slew is too fast increase this number...too slow decrease it";
			break;
		case "2_SlewSpeedMed:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " If when moving to object the medium slew is too fast increase this number...too slow decrease it";
			break;
		case "2_AutoStart:":
			$tCheck="";
			$fCheck="";

				if(strcmp($sdValue,"True\n")==0)
			{
				$tCheck="checked";
			}
			else
			{
				$fCheck="checked";			
			}
			$html .= "<tr><td>$sdType</td><td>True<input name=$sdType type=radio value='True' $tCheck />
												False<input name=$sdType type=radio value='False' $fCheck /></td><td>";
			$html .= " If true...next restart Scope Dog will automatically start";
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
