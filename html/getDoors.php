<?php

echo '{"doorSensors" : [{"sideDoorLock": ';
$setmode4 = shell_exec("/usr/local/bin/gpio -g mode 4 in");
$status = shell_exec('gpio read 4');
echo $status;
echo ', "sideDoor": ';
$setmode3 = shell_exec("/usr/local/bin/gpio -g mode 3 in");
$status = shell_exec('gpio read 3');
echo $status;
echo ', "mainDoor": ';
$setmode2 = shell_exec("/usr/local/bin/gpio -g mode 2 in");
$status = shell_exec('gpio read 2');
echo $status;
echo '}]}'
?>
