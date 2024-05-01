import wx
from src.functions.locale import getLocale
from src.functions.config import CONFIGURATIONMAIN
from pubsub import pub
import os

class SETINGSWINDOW(wx.Frame):

    def saveFunc(self, *args) -> None:
        self.conf.lang = self.choices[self.choice.GetSelection()]
        self.conf.saveConf()
        pub.sendMessage('reload')

    def closeFunc(self, *args) -> None:
        self.Destroy()

    def buttons(self) -> wx.BoxSizer:

            horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

            self.saveBtn = wx.Button(self.panel, label=self.locale["SAVE"])
            self.saveBtn.Bind(wx.EVT_BUTTON, self.saveFunc)

            self.closeBtn = wx.Button(self.panel, label=self.locale["CANCEL"])
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeFunc)

            horizontalSizer.AddStretchSpacer()
            horizontalSizer.Add(self.saveBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)
            horizontalSizer.Add(self.closeBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)

            return horizontalSizer

    def __init__(self):

        super().__init__(None, title="Settings", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetMinSize((300,600))
        self.CreateStatusBar()
        self.locale = getLocale()
        self.conf = CONFIGURATIONMAIN()

        self.panel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.choices = [x.split('.')[0] for x in os.listdir("src/locale")]

        langLabel = wx.StaticText(self.panel, label="Language:")

        self.choice = wx.Choice(self.panel, choices=self.choices)
        self.choice.SetSelection(self.choices.index(self.locale["lang"]))


        self.mainSizer.Add(langLabel,flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)
        self.mainSizer.Add(self.choice,flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=10)

        self.mainSizer.AddStretchSpacer()
        self.mainSizer.Add(self.buttons(), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.mainSizer)
        self.SetStatusText(self.locale["READY"])
        self.Show()