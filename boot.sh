#!/bin/sh
#
# gordon.sh (c) gutemine 2023 
#
VERSION="V1.0"
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
VERBOSE=""
LINE="======================================================================"
DREAMBOX=""
GORDON="/data/gordon"
GORDONCONFIG="/data/bootconfig.txt"
GORDONTMP="/tmp/gordon.txt"
HELP=false
SHOWBOOT=false
VERBOSE=""

function gordonExit() {
exit 0
}

setCmdLine() {
   CMDLINE=""
   if [ $DREAMBOX == "dreamone" ]; then
      CMDLINE="logo=osd0,loaded,0x7f800000 vout=1080p50hz,enable hdmimode=1080p50hz fb_width=1280 fb_height=720 console=ttyS0,1000000 root=$ROOT rootwait rootfstype=ext4 no_console_suspend panel_type=lcd_4"
   else
      if [ $DREAMBOX == "dreamtwo" ]; then
         CMDLINE="logo=osd0,loaded,0x0 vout=1080p50hz,enable hdmimode=1080p50hz fb_width=1280 fb_height=720 console=ttyS0,1000000 root=$ROOT rootwait rootfstype=ext4 no_console_suspend panel_type=lcd_4"
      else
         echo "only dreamone | dreamtwo supported"
         echo $LINE
         gordonExit
      fi
   fi
}

addCommand() {
   if [ ! -e /usr/bin/gordon ]; then
      ln -sfn $GORDON/gordon.sh /usr/bin/gordon
   fi
}

showHeader() {
   echo $LINE
   echo -e "    ************ gordon.sh $VERSION (c) gutemine 2023 **************"
   echo $LINE
}

showUsage() {
   echo "Usage: gordon.sh [OPTIONS]..."
   echo ""
   echo "OPTIONS:"
   echo ""
   echo "    -b, -boot      boot partition 0,1,2,.. default is 0"
   echo $LINE
}

getModel() {
   if [ -z $DREAMBOX ]; then
      if [ `cat /proc/stb/info/model | grep one | wc -l` -gt 0 ]; then
         DREAMBOX="dreamone"
      fi
      if [ `cat /proc/stb/info/model | grep two | wc -l` -gt 0 ]; then
         DREAMBOX="dreamtwo"
      fi
   fi
   if [ $DREAMBOX == "dreamone" -o $DREAMBOX == "dreamtwo" ]; then
      true
   else
      echo "ERROR: only dreamone | dreamtwo supported"
      echo $LINE
      false
   fi
}

checkGPT() {
   PARTITION_SIZE=$(cat /proc/partitions | grep mmcblk0p1 | awk '{print $3}')
   if [ ! $PARTITION_SIZE -eq 114688 ];then
      echo "NO GPT in Flash"
      echo $LINE
      false
   else  
      true
   fi		
}
   
checkBooted() {
   if [ `grep /dev/mmcblk0p5 /proc/cmdline | wc -l` -gt 0 ]; then
      BOOTED=`cat /proc/cmdline | awk '{print $8}'`
      echo "INFO: booted from $BOOTED"
      echo $LINE
      false
   else
      echo "INFO: NOT booted from Flash image 0"
      echo $LINE
      true
   fi
}

setBoot() {
   if [ $BOOTDEVICE != "0" -a $BOOTDEVICE != "1" -a $BOOTDEVICE != "2" -a $BOOTDEVICE != "3" -a $BOOTDEVICE != "4" ]; then
      echo "'$BOOTDEVICE' is not a valid boot partition option - only 0,1,2... accepted"
      echo $LINE
      gordonExit
   fi
   echo "set default boot to $BOOTDEVICE"
   BOOTPART=`expr $BOOTDEVICE "+" 5`
   ROOT="/dev/mmcblk0p$BOOTPART"
   grep -v "default=" $GORDONCONFIG > $GORDONTMP
   echo "default=$BOOTDEVICE" > $GORDONCONFIG
   cat $GORDONTMP >> $GORDONCONFIG
   echo $LINE
}

showBootconfig() {
   if [ -e $GORDONCONFIG ]; then
      echo $LINE
      cat $GORDONCONFIG
      echo $LINE
   else
      echo "$GORDONCONFIG not found"
   fi
   # make setBoot work ...
   BOOTDEVICE=$TARGETDEVICE
}

#
# check command line arguments
#
if [ -z $1 ]; then
    HELP=true
fi
while [ $# -gt 0 ] ; do
    case $1 in	
        -b | -boot | --b | --boot)
           BOOTDEVICE="$2"
           ;;
    esac
    shift
done

if ! getModel; then
   gordonExit
fi

if ! checkGPT; then
   gordonExit
fi

if [ ! -z $BOOTDEVICE ]; then
   showHeader
   setBoot
   gordonExit
  fi
fi

setCmdLine

#
# here comes the main action ...
#

showHeader

addCommand

if $HELP; then
   showUsage
   gordonExit
fi

if $SHOWBOOT; then
   showBootconfig
   doFinish
   gordonExit
fi

if checkBooted; then
   gordonExit
fi
#
# Done, see you next time, but why did it take you so long to show up ?
#
