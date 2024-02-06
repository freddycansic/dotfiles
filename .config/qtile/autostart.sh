#!/bin/sh

/usr/bin/redshift -c /home/freddy/.config/redshift.conf &
#picom -b &
feh --bg-scale /home/freddy/Pictures/Backgrounds/debian-background.png 

# enable keyboard while using trackpad
xinput --set-prop 13 313 0

# enable tapping on trackpad to click
xinput --set-prop 21 317 1
