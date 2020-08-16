# -*- coding: utf-8 -*-

import clr
clr.AddReferenceToFileAndPath(r"C:\Lib\dll\StdLib.dll")
clr.AddReferenceToFileAndPath(r"C:\Lib\dll\ezPyWpfLib.dll")
import ezPyWpfLib as ez

def onCreated():
    ez.DumpControlTable()

def onClosing(event):
    if not ez.YesNoDialog("Do you want to quie ?","Quit"):
        event.args.Cancel = True

app_content = [ # vbox  
    [ # hbox
        { "name" : "ComboBox", 'items' : ["늑대닷컴","여우코믹스","W툰"], "width" : 80, "expand" : False, 'border' : False},
        { "name" : "TextField", "expand" : True, 'border' : False},
        { "name" : "Button", "label" : "Get", 'width' : 40, "expand" : False, 'border' : False},
        { "expand" : False, 'border' : True  },
    ],       
    [
        { "name" : "TextArea", "expand" : True, 'border' : False},
        { "expand" : True, 'border' : True  },
    ],
]


def MakeWindow():
    win = ez.Window()
    win.SetTitle("WebTook Crawler")
    win.SetSize(640,400)
    win.SetContent(app_content)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    return win

if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()




