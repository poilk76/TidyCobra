import wx
import wx.dataview
from pubsub import pub
from src.GUI import edit, settings
from src.functions.config import getRuleSets
from src.functions.sort import SORTER
from src.functions.locale import getLocale
import os

class MAINWINDOW(wx.Frame):

    def onTimer(self, *args) -> None:
        self.sorter.sort()

    def reload(self):
        self.Show()
        self.dataViewReset()
        self.sorter.getConfigurations()
        self.locale = getLocale()
        self.SetStatusText(self.locale["RELOAD"])

    def dataViewReset(self) -> None:
        self.dataView.DeleteAllItems()
        for rule in getRuleSets():
            self.dataView.AppendItem([rule])
        self.SetStatusText(self.locale["RESETDATAVIEW"])

    # ADD
    def addFunc(self, *args) -> None:
        edit.EDITWINDOWS("VN5XQuBIr3")
        self.SetStatusText(self.locale["OPENADD"])

    #REMOVE
    def removeFunc(self, *args) -> None:
        if self.dataView.GetSelectedRow() != -1:
            text = self.dataView.GetTextValue(self.dataView.GetSelectedRow(), 0)
            dlg = wx.MessageDialog(self, self.locale["QUESTIONREMOVE"]+f"{text}.", "Question", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == 5103:
                os.remove(f'src/rules/{text}.json')
                self.dataViewReset()
                self.SetStatusText(self.locale["DONEREMOVE"]+f"{text}.")
            else:
                self.SetStatusText(self.locale["CANCELREMOVE"])
        else: 
            self.SetStatusText(self.locale["STOPREMOVE"])

    #MODIFY
    def modifyFunc(self, *args) -> None:
        if self.dataView.GetSelectedRow() != -1:
            edit.EDITWINDOWS(self.dataView.GetTextValue(self.dataView.GetSelectedRow(), 0))
            self.SetStatusText(self.locale["OPENMODIFY"])
        else: 
            self.SetStatusText(self.locale["STOPMODIFY"])

    #SETTINGS
    def settingsFunc(self, *args) -> None:
        settings.SETINGSWINDOW()
        self.SetStatusText("Settings window opened")

    def buttons(self) -> wx.BoxSizer:

        horizontalSizer= wx.BoxSizer(wx.HORIZONTAL)

        self.addBtn = wx.Button(self.panel, label=self.locale["ADD"])
        self.addBtn.Bind(wx.EVT_BUTTON, self.addFunc)

        self.deleteBtn = wx.Button(self.panel, label=self.locale["REMOVE"])
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.removeFunc)

        self.modifyBtn = wx.Button(self.panel, label=self.locale["MODIFY"])
        self.modifyBtn.Bind(wx.EVT_BUTTON, self.modifyFunc)

        bitmap = wx.Bitmap("resources/settings.svg")
        bitmap.Rescale(bitmap, (25,25))
        self.settingsBtn = wx.Button(self.panel,size=(45,45))
        self.settingsBtn.Bind(wx.EVT_BUTTON, self.settingsFunc)
        self.settingsBtn.SetBitmap(bitmap)

        horizontalSizer.AddStretchSpacer()

        horizontalSizer.Add(self.addBtn ,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)
        horizontalSizer.Add(self.deleteBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)
        horizontalSizer.Add(self.modifyBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)
        horizontalSizer.Add(self.settingsBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)

        return horizontalSizer



    def __init__(self) -> None:

        super().__init__(None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetMinSize((300,600))
        self.CreateStatusBar()
        self.locale = getLocale()

        self.sorter = SORTER()
        self.sorter.getConfigurations()

        self.panel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.dataView = wx.dataview.DataViewListCtrl(self.panel, size=(280, 480))
        self.dataView.AppendTextColumn(self.locale["RULESET"], width=280)
        
        self.mainSizer.Add(self.dataView, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)
        self.mainSizer.Add(self.buttons(), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)

        pub.subscribe(self.reload, "reload")

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.timer.Start(5000)

        self.panel.SetSizer(self.mainSizer)
        self.Center()
        self.dataViewReset()
        self.SetStatusText(self.locale["READY"])
        self.Show()


def renderGui() -> None:

    app = wx.App()
    frame = MAINWINDOW()
    app.MainLoop()