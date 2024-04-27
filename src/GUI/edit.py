import wx
import wx.dataview
from pubsub import pub
from src.functions.config import CONFIGURATIONRULE, saveConfig
from src.GUI.add import ADDWINDOW
import os

class EDITWINDOWS(wx.Frame):

    def getExtensions(self) -> list:

        extensions = []

        for row in range(self.view.GetItemCount()):
            temp_row = []
            for col in range(2):
                temp_row.append(self.view.GetTextValue(row, col))

            extensions.append(temp_row)

        return extensions

    def addListener(self,path:str, extensions:str) -> None:
        self.view.AppendItem([path,extensions])
        self.Show()
        self.SetStatusText(f"Set move rule for {path}.")

    def addFunc(self, *args) -> None:
        ADDWINDOW()

    def removeFunc(self, *args) -> None:
        if self.view.GetSelectedRow() != -1:
            self.SetStatusText(f'Removed {self.view.GetSelectedRow()}.')
            self.view.DeleteItem(self.view.GetSelectedRow())
        else:
            self.SetStatusText(f'Not selected row.')

    def browseFunc(self, *args) -> None:
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.pathTextBox.SetValue(dlg.GetPath())
            self.SetStatusText(f"Set {dlg.GetPath()} to text box.")
        dlg.Destroy()

    def closeFunc(self, *args) -> None:
        self.Destroy()

    def saveFunc(self, *args) -> None:
        if self.file != "VN5XQuBIr3":
            os.remove(f'src/rules/{self.conf.name}.json')
        saveConfig(self.nameTextBox.Value, self.pathTextBox.Value, self.getExtensions())
        pub.sendMessage('reload')
        self.Destroy()

    def buttons(self) -> wx.BoxSizer:

        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.saveBtn = wx.Button(self.panel, label="SAVE")
        self.saveBtn.Bind(wx.EVT_BUTTON, self.saveFunc)

        self.closeBtn = wx.Button(self.panel, label="CANCEL")
        self.closeBtn.Bind(wx.EVT_BUTTON, self.closeFunc)

        horizontalSizer.AddStretchSpacer()
        horizontalSizer.Add(self.saveBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)
        horizontalSizer.Add(self.closeBtn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=2)

        return horizontalSizer
    
    def dataView(self) -> wx.BoxSizer:

        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.view = wx.dataview.DataViewListCtrl(self.panel, size=(300, 200))
        self.view.AppendTextColumn("Rule", width=280)
        self.view.AppendTextColumn("Extensions")

        self.addBtn = wx.Button(self.panel, label="ADD")
        self.addBtn.Bind(wx.EVT_BUTTON, self.addFunc)

        self.removeBtn = wx.Button(self.panel, label="REMOVE")
        self.removeBtn.Bind(wx.EVT_BUTTON, self.removeFunc)

        horizontalSizer.Add(self.addBtn, wx.SizerFlags().Proportion(1))
        horizontalSizer.Add(self.removeBtn, wx.SizerFlags().Proportion(1))

        verticalSizer.Add(self.view, flag=wx.EXPAND)
        verticalSizer.Add(horizontalSizer, flag=wx.EXPAND)

        return verticalSizer

    def __init__(self, file):

        super().__init__(None, title="Add set of rules", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetMinSize((300,600))
        self.CreateStatusBar()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        
        nameLabel = wx.StaticText(self.panel, label="Rule set name:")
        self.nameTextBox = wx.TextCtrl(self.panel, size=(-1, -1))

        pathLabel = wx.StaticText(self.panel, label="Sort in path:")
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pathTextBox = wx.TextCtrl(self.panel, size=(280, -1))

        self.browseBtn = wx.Button(self.panel, label="BROWSE")
        self.browseBtn.Bind(wx.EVT_BUTTON, self.browseFunc)
        horizontalSizer.Add(self.pathTextBox)
        horizontalSizer.Add(self.browseBtn, flag=wx.EXPAND | wx.LEFT, border=10)

        self.mainSizer.Add(nameLabel, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.mainSizer.Add(self.nameTextBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)
        self.mainSizer.Add(pathLabel, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.mainSizer.Add(horizontalSizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)
        self.mainSizer.Add(self.dataView(), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)
        self.mainSizer.AddStretchSpacer()
        self.mainSizer.Add(self.buttons(), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.panel.SetSizer(self.mainSizer)
        self.Center()

        self.file = file
        if self.file != "VN5XQuBIr3":
            self.conf = CONFIGURATIONRULE(file+".json")
            self.nameTextBox.SetValue(self.conf.name)
            self.pathTextBox.SetValue(self.conf.mainPath)
            for item in self.conf.rules:
                self.view.AppendItem(item)

        pub.subscribe(self.addListener, "add")

        self.SetStatusText("Conf loaded.")
        self.Show()