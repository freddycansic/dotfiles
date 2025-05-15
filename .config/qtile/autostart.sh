#!/bin/sh

redshift &
picom -b
# light-locker &
dunst &

xinput set-prop 12 305 0

gnome-keyring-daemon --start

export XDG_CURRENT_DESKTOP=GTK

xmodmap ~/.Xmodmap
