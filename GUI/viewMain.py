import wx
import wx.dataview
from pubsub import pub
from Utils.config import Config
from Utils.sorter import Sorter
from GUI import viewModifyRule,viewRemove,viewAddRule

class MainWindow(wx.Frame):

    def render(self) -> None:

        self.panel.DestroyChildren()

        # Dividers
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerModify = wx.BoxSizer(wx.HORIZONTAL)
        
        # Title
        self.title = wx.StaticText(self.panel,label="TidyCobra")

        # DataView
        self.dataView = wx.dataview.DataViewListCtrl(self.panel, size=(400, 200))
        self.dataView.AppendTextColumn("Folder", width=225)
        self.dataView.AppendTextColumn("Active")
        for rule in self.config.rulesList:
            self.dataView.AppendItem([rule['sourceFolder'],"yes" if rule['isIntervalRunning'] else 'no'])
            
        # Modify
        self.btnRemoveItem = wx.Button(self.panel, label="Remove")
        self.btnAddItem = wx.Button(self.panel,label="Add")
        self.btnModifyItem = wx.Button(self.panel,label="Modify")

        # Settings
        self.btnSettings = wx.Button(self.panel,label="Settings")

        self.sizerModify.Add(self.btnAddItem, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.sizerModify.Add(self.btnRemoveItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.sizerModify.Add(self.btnModifyItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))

        self.sizerMain.Add(self.title, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.dataView, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.sizerMain.Add(self.sizerModify, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.sizerMain.Add(self.btnSettings, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.Center()

    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.SetMinSize((200,300))
        
        self.config = Config()

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")
        
        self.render()
        
        self.Show(True)

def renderGui():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()

if __name__ == "__main__":

    renderGui()
