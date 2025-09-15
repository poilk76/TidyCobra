import wx
import wx.dataview
from pubsub import pub
from Sorter.config import Config
from Sorter.sorter import Sorter
from GUI import viewModifyRule,viewRemove

class MainWindow(wx.Frame):

    def onBtnDownloadFolder(self, event) -> None:

        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.textBoxDownloadFolder.SetValue(dlg.GetPath())
            self.config.rulesList[0]["sourceFolder"] = dlg.GetPath()
        dlg.Destroy()

    def onBtnAddItem(self, event) -> None:

        self.dataView.AppendItem(["",""])
        self.config.rulesList[0]["destinationFolders"].append({})
        addRuleWindow = viewModifyRule.ModifyRuleWindow(len(self.config.rulesList[0]["destinationFolders"])-1)
        addRuleWindow.Show()

    def onBtnRemoveItem(self, event) -> None:

        selectedItem = self.dataView.GetSelectedRow()
        removeRuleWindow = viewRemove.RemoveRule(selectedItem)
        removeRuleWindow.Show()

    def onBtnModifyItem(self, event) -> None:
        
        selectedItem = self.dataView.GetSelectedRow()
        modifyRuleWindow = viewModifyRule.ModifyRuleWindow(selectedItem,self.config.rulesList[0]["destinationFolders"][selectedItem])
        modifyRuleWindow.Show()

    def onBtnSaveConfig(self, event) -> None:

        self.config.saveConfig()

    def onBtnRunManual(self, event) -> None:
        
        self.sorter.ruleList = self.config.rulesList
        self.sorter.sortAll()

    def onClose(self,event) -> None:
        self.config.saveConfig()
        self.Destroy()

    def listenerModifyRule(self, message) -> None:
        
        if message["id"] != -1:
            data = message["data"]
            self.dataView.SetValue(data["destinationPath"],message["id"],0)
            self.dataView.SetValue(" ".join(data["extensions"]),message["id"],1)
            self.config.rulesList[0]["destinationFolders"][message["id"]] = data
        elif self.config.rulesList[0]["destinationFolders"][-1] == {}:
            lastIndex = len(self.config.rulesList[0]["destinationFolders"])-1
            self.dataView.DeleteItem(lastIndex)
            self.config.rulesList[0]["destinationFolders"].pop(lastIndex)
    
    def listenerRemoveRule(self, id) -> None:

        self.dataView.DeleteItem(id)
        self.config.rulesList[0]["destinationFolders"].pop(id)
    
    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER
                                                                                           | wx.MAXIMIZE_BOX))
        
        self.config = Config()
        self.sorter = Sorter(self.config)

        self.payload = []
        self.SetMinSize(self.GetSize())
        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")
        pub.subscribe(self.listenerModifyRule, "modifyRuleListener")
        pub.subscribe(self.listenerRemoveRule, "removeRuleListener")

        ''' Text labels '''
        self.textStep1 = wx.StaticText(self.panel, label="Step 1: Choose your Downloads folder")
        self.textStep2 = wx.StaticText(self.panel, label="Step 2: Set up destination folders and their extensions")
        self.textStep3 = wx.StaticText(self.panel, label="Step 3: Save/Run")

        ''' Dividers '''
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)  # main sizer

        ''' Horizontal boxes '''
        self.hboxDownloads = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxDataViewControls = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxSaveControls = wx.BoxSizer(wx.HORIZONTAL)

        ''' Dialogs '''
        self.dialogStep1 = wx.DirDialog(None, "Choose input directory", "", wx.DD_DIR_MUST_EXIST)

        ''' Buttons '''
        self.btnDownloadFolder = wx.Button(self.panel, label="Browse")
        self.btnDownloadFolder.Bind(wx.EVT_BUTTON, self.onBtnDownloadFolder)

        self.btnAddItem = wx.Button(self.panel, label="Add")
        self.btnAddItem.Bind(wx.EVT_BUTTON, self.onBtnAddItem)

        self.btnRemoveItem = wx.Button(self.panel, label="Remove")
        self.btnRemoveItem.Bind(wx.EVT_BUTTON, self.onBtnRemoveItem)

        self.btnImportConfig = wx.Button(self.panel, label="Modify")
        self.btnImportConfig.Bind(wx.EVT_BUTTON, self.onBtnModifyItem)

        self.btnSaveConfig = wx.Button(self.panel, label="Save configuration file")
        self.btnSaveConfig.Bind(wx.EVT_BUTTON, self.onBtnSaveConfig)

        self.btnRunManual = wx.Button(self.panel, label="Run sorter")
        self.btnRunManual.Bind(wx.EVT_BUTTON, self.onBtnRunManual)

        self.btnRunAuto = wx.Button(self.panel, label="Run on startup")
        #self.btnRunAuto.Bind(wx.EVT_BUTTON, self.onBtnRunAuto)

        ''' Textboxes '''
        self.textBoxDownloadFolder = wx.TextCtrl(self.panel)

        ''' DataView '''
        self.dataView = wx.dataview.DataViewListCtrl(self.panel, size=(200, 200))
        self.dataView.AppendTextColumn("Folder Path", width=225)
        self.dataView.AppendTextColumn("Extensions")

        ''' Step 1 : Select download folder'''
        self.sizerMain.Add(self.textStep1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        self.hboxDownloads.Add(self.textBoxDownloadFolder, proportion=1)
        self.hboxDownloads.Add(self.btnDownloadFolder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))
        self.sizerMain.Add(self.hboxDownloads, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        ''' Step 2: Set up rules '''
        self.sizerMain.Add(self.textStep2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.dataView, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.hboxDataViewControls.Add(self.btnAddItem, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxDataViewControls.Add(self.btnRemoveItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxDataViewControls.Add(self.btnImportConfig, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxDataViewControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        ''' Step 3: Save/Run '''
        self.sizerMain.Add(self.textStep3, wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.BOTTOM, 10))
        self.hboxSaveControls.Add(self.btnSaveConfig, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxSaveControls.Add(self.btnRunManual, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxSaveControls.Add(self.btnRunAuto, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxSaveControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.Center()
        self.SetSize(self.GetBestSize())
        self.sizerMain.Fit(self)
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Center()

        for destinationFolder in self.config.rulesList[0]["destinationFolders"]:
            self.dataView.AppendItem([destinationFolder["destinationPath"]," ".join(destinationFolder["extensions"])])

        self.textBoxDownloadFolder.SetValue(self.config.rulesList[0]["sourceFolder"])

        self.Show(True)

def renderGui():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()

if __name__ == "__main__":

    renderGui()
