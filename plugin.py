# -*- coding: iso-8859-1 -*-

import os
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Screens.Console import Console

def Plugins(**kwargs):
    return [PluginDescriptor(
        name=_("GPT Boot Plugin"),
        description=_("GPT Boot Plugin"),
        where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
        fnc=main,
        icon="logo.png"
    )]

def main(session, **kwargs):
    session.open(Scripts)

class Scripts(Screen):
    skin = """
    <screen position="center,center" size="660,475" title="GPT Boot Plugin" >
        <widget name="list" position="10,10" size="640,455" scrollbarMode="showOnDemand" />
    </screen>"""

    def __init__(self, session, args=None):
        Screen.__init__(self, session)
        self.session = session
        try:
            scripts_dir = "/usr/lib/enigma2/python/Plugins/Extensions/GPT-Boot-Plugin/scripts/"
            script_list = [x[:-3] for x in os.listdir(scripts_dir) if x.endswith('.py')]
            script_list.sort()
        except Exception as e:
            script_list = []
        self["list"] = MenuList(script_list)
        self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.run, "cancel": self.close}, -1)

    def run(self):
        script = self["list"].getCurrent()
        if script is not None:
            script_path = "/usr/lib/enigma2/python/Plugins/Extensions/GPT-Boot-Plugin/scripts/" + script + ".py"
            os.popen("python2.7 " + script_path)

    def boot_flash_image(self):
        os.popen("python2.7 Boot-Flash-Image.py")

    def slot1(self):
        os.popen("python2.7 slot1.py")

    def slot2(self):
        os.popen("python2.7 slot2.py")

    def slot3(self):
        os.popen("python2.7 slot3.py")

    def auswahl(self):
        print("Wählen Sie ein Programm aus:")
        print("1. Boot-Flash-Image")
        print("2. Slot 1")
        print("3. Slot 2")
        print("4. Slot 3")
        
        auswahl = input("Geben Sie die Nummer des gewünschten Programms ein: ")
        
        if auswahl == "1":
            self.boot_flash_image()
        elif auswahl == "2":
            self.slot1()
        elif auswahl == "3":
            self.slot2()
        elif auswahl == "4":
            self.slot3()
        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine der verfügbaren Optionen.")
