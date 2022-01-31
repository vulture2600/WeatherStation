<?php
//updated for bullsye. gpio command replaced with raspi-gpio
echo '{"doorSensors" : [{"sideDoorLock": ';
$status4 = shell_exec("./getIO.sh 23");
echo $status4;

echo ', "sideDoor": ';
$status3 = shell_exec('./getIO.sh 22');
echo $status3;

echo ', "mainDoor": ';
$status2 = shell_exec('./getIO.sh 27');
echo $status2;
echo '}]}'
?>

