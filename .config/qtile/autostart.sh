#!/bin/sh

redshift &
picom -b
# light-locker &
dunst &

xinput set-prop 12 305 0
