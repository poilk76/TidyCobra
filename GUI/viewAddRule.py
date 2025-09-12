import wx
from pubsub import pub

class AddRuleWindow(wx.Frame):

    def onBtnBrowse(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.textboxFolderPath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onBtnSave(self, event):

        extensions = [
            extension if extension.startswith(".") else "." + extension
            for extension in self.textboxExtensions.GetValue().split(" ")
        ]

        data = { 
            "extensions": extensions, 
            "destinationPath": self.textboxFolderPath.GetValue()
        }
        
        pub.sendMessage("addRuleListener", message=data)
        self.Destroy()

    def __init__(self):
        wx.Frame.__init__(self, None, title="Add rule", style=wx.DEFAULT_DIALOG_STYLE & ~wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)

        '''Sizers'''
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hboxPath = wx.BoxSizer(wx.HORIZONTAL)

        '''Labels'''
        self.labelFolderPath = wx.StaticText(self.panel, label="Select folder path:")
        self.labelExtensions = wx.StaticText(self.panel, label="Specify file extensions to reroute: (separated by spaces)")

        '''Textboxes'''
        self.textboxFolderPath = wx.TextCtrl(self.panel, size=(300, -1))
        self.textboxExtensions = wx.TextCtrl(self.panel)

        '''Buttons'''
        self.btnBrowseFolder = wx.Button(self.panel, label="Browse")
        self.btnBrowseFolder.Bind(wx.EVT_BUTTON, self.onBtnBrowse)
        self.btnSave = wx.Button(self.panel, label="Save")
        self.btnSave.Bind(wx.EVT_BUTTON, self.onBtnSave)

        '''Layout'''
        # Select path
        self.vbox.Add(self.labelFolderPath, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.hboxPath.Add(self.textboxFolderPath, proportion=1)
        self.hboxPath.Add(self.btnBrowseFolder, wx.SizerFlags().Border(wx.LEFT, 5))
        self.vbox.Add(self.hboxPath, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        # Set extensions
        self.vbox.Add(self.labelExtensions, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.vbox.Add(self.textboxExtensions, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        # Save
        self.vbox.Add(self.btnSave, flag=wx.CENTER|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        self.panel.SetSizer(self.vbox)
        self.Center()
        self.SetSize(self.GetBestSize())
        self.vbox.Fit(self)
        self.vbox.Layout()
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

        self.Show(True)