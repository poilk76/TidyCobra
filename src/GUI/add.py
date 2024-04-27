import wx
import wx.dataview
from pubsub import pub

class ADDWINDOW(wx.Frame):

    def parseExtensions(self) -> str:
        
        text = self.extensionTextBox.Value.replace('.', '')
        
        return text

    def saveFunc(self, *args) -> None:
        pub.sendMessage("add", path=self.pathTextBox.Value, extensions=self.parseExtensions())
        self.Destroy()

    def closeFunc(self, *args) -> None:
        self.Destroy()

    def browseFunc(self, *args) -> None:
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.pathTextBox.SetValue(dlg.GetPath())
            self.SetStatusText(f"Set {dlg.GetPath()} to text box.")
        dlg.Destroy()

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

    def choose(self) -> wx.BoxSizer:

        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        pathLabel = wx.StaticText(self.panel, label="Where to move:")
        self.pathTextBox = wx.TextCtrl(self.panel, size=(280, -1))

        self.browseBtn = wx.Button(self.panel, label="BROWSE")
        self.browseBtn.Bind(wx.EVT_BUTTON, self.browseFunc)

        horizontalSizer.Add(self.pathTextBox, flag=wx.EXPAND)
        horizontalSizer.Add(self.browseBtn, flag=wx.EXPAND | wx.LEFT, border=10)

        extensionLabel = wx.StaticText(self.panel, label="Extensions:")
        self.extensionTextBox = wx.TextCtrl(self.panel, size=(300, -1))

        verticalSizer.Add(pathLabel)
        verticalSizer.Add(horizontalSizer, flag=wx.EXPAND | wx.TOP, border=10)
        verticalSizer.Add(extensionLabel, flag=wx.EXPAND | wx.TOP, border=10)
        verticalSizer.Add(self.extensionTextBox, flag=wx.EXPAND | wx.TOP, border=10)

        return verticalSizer

    def __init__(self):

        super().__init__(None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetMinSize((200,300))
        self.CreateStatusBar()

        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(self.choose(), flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT | wx.LEFT, border=10)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(self.buttons(), flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT | wx.LEFT, border=10)
        self.panel.SetSizer(mainSizer)
        self.Center()
        self.SetStatusText("Ready!")
        self.Show()