#!/bin/bash
status=$(raspi-gpio get $1)
value=${status:15:1}
echo $value
exit 0