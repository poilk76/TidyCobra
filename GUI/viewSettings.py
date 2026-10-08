import wx
import wx.dataview
from pubsub import pub
from Utils.config import Config
from GUI import viewRemove, viewRule

class SettingsWindow(wx.Frame):

    def render(self) -> None:

        self.panel.DestroyChildren()

        self.config = Config()

        # Dividers
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerOption = wx.BoxSizer(wx.HORIZONTAL)
        
        # Title
        self.title = wx.StaticText(self.panel,label="Settings")

        # Interval
        self.intervalText = wx.StaticText(self.panel,label="Interval [s]:")
        self.intervalInput = wx.TextCtrl(self.panel,value=str(self.config.interval//1000))

        # Options
        self.btnSave = wx.Button(self.panel,label="Save")
        self.btnCancel = wx.Button(self.panel,label="Cancel")

        self.sizerMain.Add(self.title, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.intervalText, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.intervalInput, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        
        self.sizerOption.Add(self.btnSave, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.sizerOption.Add(self.btnCancel, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        
        self.sizerMain.AddStretchSpacer()
        self.sizerMain.Add(self.sizerOption, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.Center()

    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.SetMinSize((200,300))

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")
        
        self.render()
        
        self.Show(True)

def renderGui():
    app = wx.App()
    frame = SettingsWindow()
    app.MainLoop()

if __name__ == "__main__":

    renderGui()
