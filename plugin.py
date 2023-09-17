# -*- coding: iso-8859-1 -*-

import os
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox

import subprocess
import time

version_txt = "0.1-r1"

def Plugins(**kwargs):
    return [PluginDescriptor(
        name=_("GPT Boot Plugin"),
        description=_("GPT Boot Plugin"),
        where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
        fnc=main,
        icon="logo.png"
    )]

def main(session, **kwargs):
    session.open(MainScreen)

class MainScreen(Screen):
    skin = """
    <screen position="center,center" size="660,550" title="GPT Boot Plugin" >
        <widget name="list" position="10,10" size="640,455" enableWrapAround="1" scrollbarMode="showOnDemand" />
        <widget name="helptext" font="Regular;35" position="25,475" size="640,45" valign="top" render="Label" />
    </screen>"""

    def __init__(self, session, args=None):
        Screen.__init__(self, session)
        self.session = session
        
        self["helptext"]=Label("Selection an option an press OK!")
        
        option_list = []
        option_list.append(("Set boot-device","boot"))
        option_list.append(("Flash Image to device","flash"))
        option_list.append(("Option 3","option3"))
        option_list.append(("Option 4","option4"))
        self["list"] = MenuList(option_list)
        self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.run, "cancel": self.close}, -1)
        
        self.setTitle("GPT Boot Plugin - v%s" % version_txt)

    def run(self):
        entry = self["list"].getCurrent()
        if entry:
            print("=== entry", entry[1])
            if entry[1] == "flash":
                print("=== code for flash")
                self.session.open(MessageBox, "you have selected 'flash'. But there is yet not a running code", MessageBox.TYPE_INFO)
                #...
            elif entry[1] == "boot":
                print("=== code for boot")
                device_list = []
                device_list.append(("Flash",0))
                device_list.append(("Slot1",1))
                device_list.append(("Slot2",2))
                self.session.openWithCallback(
                    self.boot_device_callback,
                    ChoiceBox,
                    "Select the boot device",
                    device_list,
                )
            elif entry[1] == "option3":
                print("=== code for option3")
                self.session.open(MessageBox, "you have selected 'option3'. But there is yet not a running code", MessageBox.TYPE_INFO)
                #...
            elif entry[1] == "option4":
                print("=== code for option4")
                self.session.open(MessageBox, "you have selected 'option4'. But there is yet not a running code", MessageBox.TYPE_INFO)
                #...
            else:
                print("=== unknown option")

    def boot_device_callback(self, retValue=""):
        print("=== retValue", retValue)
        if retValue:
            print("=== entry", retValue[1])
            self.session.open(MessageBox, "the bootdevice will be changed and reboot the box", MessageBox.TYPE_INFO)
            self.change_boot(slot=retValue[1])

    def change_boot(self, slot):
        print("=== change_boot", slot)
        device = "%s" % slot
        print("=== cmd", "./boot.sh", "-b", device)
        
        os.chdir("/usr/lib/enigma2/python/Plugins/Extensions/GPT-Boot-Plugin")
        subprocess.call(["./boot.sh", "-b", device])
        time.sleep(1)
        subprocess.call(["reboot"])
        

