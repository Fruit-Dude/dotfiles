#!/bin/sh
dunst &
nitrogen --restore &
picom --experimental-backends --backend glx --xrender-sync-fence &
flameshot &
 
