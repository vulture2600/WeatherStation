
#!/bin/bash


#run "sudo chmod +s /bin/raspi-gpio" first for file permissions
#set pullups for the inputs youre using:
#"raspi-gpio set XX pu"
#gets gpio state of pin passed from getDoors.php
#returns 0 or 1

status=$(raspi-gpio get $1)

value=${status:15:1}

echo $value

exit 0


