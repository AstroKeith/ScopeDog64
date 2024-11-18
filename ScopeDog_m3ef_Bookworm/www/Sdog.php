<!DOCTYPE html>
<html>
<head>
	<title>Scope Dog</title>
	
</head>
<body bgcolor="#000000" text="#FFFFFF">
	<h3 align="center">ScopeDog.config file</h3><br>
	
	<table><tr><td>
	<zform action='saveSdog.php' method='post'>
	</td><td> </td></tr>
<?php


$filename = "/home/scopedog/ScopeDog.config";
if (file_exists($filename)) {
    chmod($filename, 0777);
} else {
    echo "The file $filename does not exist";
}
$html = "";
$fp=fopen("/home/scopedog/ScopeDog.config", "r");
print_r($myVar);
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
			//$html .= " Is the Alt drive gear Left of stepper motor or Right of stepper motor";
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
		case "1_Backlash:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Altitude backlash in arcmin";
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
			$html .= " If true....next restart Scope Dog will automatically start";
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
		case "2_Az_Gear_Ratio:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			$azVelStart= ($sdValue/360)*10000;
			break;
		case "2_Alt_Gear_Ratio:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " ver mk3_14 Final Drive Ratio, ver mk3_15 Total Drive Ratio";
			$altVelStart=($sdValue/360)*10000;
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
			//$html .= " Is the Alt drive gear Left of stepper motor or Right of stepper motor";
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
		case "2_Backlash:":
			$html .= "<tr><td>$sdType</td><td><input type=text Name=$sdType Value=$sdValue ></td><td>";
			$html .= " Altitude backlash in arcmin";
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
</td></zform><td> 
<!-- 
<form action="runScopeDog.php" method="post">
<INPUT type="submit" value="Run ScopeDog">
</form>
 -->
</td></tr>

</table>
</body>
</html>
