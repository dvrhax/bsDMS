#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Tue Oct 13 16:46:49 2009
#
#Version 1.0.0 Initial Production ready release
#Version 1.1.0 Release implementing readonly and right click close from taskbar
#Version 1.1.2 Release implementing stay on top selection and No Taskbar
#Version 1.1.4 Release setting default selection in list box and fixing bug that causes filter on empty dropdown to empty list. 10/27/2009
#Version 1.2.0 Released with several changes: All paths are now stored relative so moving directory structures won't break the open functionality
#               Changed the upload and download functions to remember last path used per session
#               Changed all the fetchone() to fetchall() and related list comprehensions to avoid database locked issues
#               Added functionality to onUpload and onDrop to add the filtered tag set as a default to the uploaded/dropped file
#               Added functionality to open a file with a double click on its entry in the fileSelBox
#Version 1.2.1 Added additional error trapping for starting empty databases. 6/24/2011
#Version 1.3.0 Added 'Email -> Send To' incorporating the simplemapi module to send selected file as an email attachment
#Version 1.4.0 Tweaks for Python3 and wxPhoenix

import wx

# begin wxGlade: extracode
import os, sys, DMS, TankIcon, tBarIconify
if sys.platform == 'win32': import simplemapi
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR 
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER|wx.SP_LIVE_UPDATE)
        self.window_1_pane_2 = wx.Panel(self.window_1, -1)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1)
        self.filterBox = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.filterButton = wx.Button(self, -1, "Filter")
        self.resetButton = wx.Button(self, -1, "Reset")
        self.uploadButton = wx.Button(self, -1, "Upload")
        self.DownloadButton = wx.Button(self, -1, "Download")
        self.openButton = wx.Button(self, -1, "Open File")
        self.fileSelBox = wx.ListBox(self.window_1_pane_1, -1, choices=[], style=wx.LB_SINGLE|wx.LB_SORT)
        self.label_1 = wx.StaticText(self.window_1_pane_2, -1, "Name", style=wx.ALIGN_CENTRE)
        self.nameBox = wx.TextCtrl(self.window_1_pane_2, -1, "",style=wx.TE_READONLY)
        self.label_2 = wx.StaticText(self.window_1_pane_2, -1, "Description", style=wx.ALIGN_CENTRE)
        self.descBox = wx.TextCtrl(self.window_1_pane_2, -1, "", style=wx.TE_PROCESS_TAB|wx.TE_MULTILINE)
        self.label_3 = wx.StaticText(self.window_1_pane_2, -1, "Tags", style=wx.ALIGN_CENTRE)
        self.tagInputBox = wx.TextCtrl(self.window_1_pane_2, -1, "", style=wx.TE_MULTILINE)
        
        self.__setVariables()
        
        dt = DMS.MyFileDropTarget(self,self.storagePath,self.relativeStorage)
        self.SetDropTarget(dt)

        ico = TankIcon.getTankIcon()
        self.SetIcon(ico)
        self.trayIcon=tBarIconify.trayIcon(ico,'bsDMS',self,kwds["style"])
        self.__createMenuBar()
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onFilter, self.filterButton)
        self.Bind(wx.EVT_BUTTON, self.onReset, self.resetButton)
        self.Bind(wx.EVT_BUTTON, self.onUpload, self.uploadButton)
        self.Bind(wx.EVT_BUTTON, self.onDownload, self.DownloadButton)
        self.Bind(wx.EVT_BUTTON, self.onOpen, self.openButton)
        ###------------My Bind Events---------------###
        self.Bind(wx.EVT_LISTBOX, self.selectionChange, self.fileSelBox)
        self.descBox.Bind(wx.EVT_KILL_FOCUS, self.infoChange)
        self.tagInputBox.Bind(wx.EVT_KILL_FOCUS, self.infoChange)
        self.Bind(wx.EVT_ICONIZE, self.on_iconify)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.fileSelBox.Bind(wx.EVT_LEFT_DCLICK, self.onOpen)
        ###-----------MenuBar Bindings---------------###
        self.Bind(wx.EVT_MENU, self.onOpenDB, id=self.ID_oDB)
        self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_oFile)
        self.Bind(wx.EVT_MENU, self.onUpload, id=self.ID_uFile)
        self.Bind(wx.EVT_MENU, self.onDownload, id=self.ID_dFile)
        self.Bind(wx.EVT_MENU, self.onRemove, id=self.ID_rFile)
        self.Bind(wx.EVT_MENU, self.onSearch, id=self.ID_search)
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onReadOnly, id=self.ID_readOnly)
        self.Bind(wx.EVT_MENU, self.onEmail, id=self.ID_email)
        # end wxGlade
        self.onReadOnly('')
        
    def __createMenuBar(self):
        self.ID_oFile = wx.NewId()
        self.ID_oDB = wx.NewId()
        self.ID_uFile = wx.NewId()
        self.ID_dFile = wx.NewId()
        self.ID_rFile = wx.NewId()
        self.ID_search = wx.NewId()
        self.ID_readOnly = wx.NewId()
        self.ID_email = wx.NewId()
            
        self.topMenuBar = wx.MenuBar()
        ###-----------File MenuBar---------------###
        tmpMenu = wx.Menu()
        tmpMenu.Append(self.ID_oDB, "Open Database", "", wx.ITEM_NORMAL)
        tmpMenu.Append(self.ID_search, "Search","",wx.ITEM_NORMAL)
        tmpMenu.AppendSeparator()
        tmpMenu.Append(wx.ID_ABOUT, "About","",wx.ITEM_NORMAL)
        tmpMenu.AppendSeparator()
        tmpMenu.Append(wx.ID_EXIT,'E&xit',"",wx.ITEM_NORMAL)
        self.topMenuBar.Append(tmpMenu, "&File")
        ###-----------Tools MenuBar---------------###
        tmpMenu = wx.Menu()
        tmpMenu.Append(self.ID_oFile, "Open File", "", wx.ITEM_NORMAL)
        self.uploadMenu=tmpMenu.Append(self.ID_uFile, "Upload File", "", wx.ITEM_NORMAL)
        tmpMenu.Append(self.ID_dFile, "Download File", "", wx.ITEM_NORMAL)
        self.removeMenu=tmpMenu.Append(self.ID_rFile, "Remove File", "", wx.ITEM_NORMAL)
        #append method of wx.Menu() returns a wx.MenuItem obj which can then be used to set the default state
        self.readOnlyMenu=tmpMenu.Append(self.ID_readOnly, "Read Only", "", wx.ITEM_CHECK)
        self.readOnlyMenu.Check(True)
        self.topMenuBar.Append(tmpMenu, "Tools")
        ###-----------Email MenuBar---------------###
        tmpMenu = wx.Menu()
        tmpMenu.Append(self.ID_email, "Send To...", "", wx.ITEM_NORMAL)
        self.topMenuBar.Append(tmpMenu, "Email")
        
        self.SetMenuBar(self.topMenuBar)
        
    def __setVariables(self):
        self.Version='1.3.0'
        self.rootPath=os.path.split(sys.argv[0])[0]
        self.relativeStorage='DocArchive'
        self.storagePath=os.path.join(self.rootPath,self.relativeStorage)
        self.dbFile=os.path.join(self.rootPath,'.DMSSQLdb')
        self.downloadDefault=os.path.expanduser('~\\My Documents')
        self.uploadDefault=os.path.expanduser('~\\My Documents')

        self.SQLMod=DMS.SQLMod(self.dbFile)
        self.preFilterTags=[]
        
        self.updateValues()
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("betascheme Document Managment System")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 2, 5, 5)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.filterBox, 0, 0, 0)
        sizer_4.Add(self.filterButton, 0, 0, 0)
        sizer_4.Add(self.resetButton, 0, 0, 0)
        sizer_4.Add((100, 20), 0, 0, 0)
        sizer_4.Add(self.uploadButton, 0, 0, 0)
        sizer_4.Add(self.DownloadButton, 0, 0, 0)
        sizer_4.Add(self.openButton, 0, 0, 0)
        sizer_3.Add(sizer_4, 0, 0, 0)
        sizer_6.Add(self.fileSelBox, 1, wx.ALL|wx.EXPAND, 5)
        self.window_1_pane_1.SetSizer(sizer_6)
        grid_sizer_1.Add(self.label_1, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.nameBox, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_2, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.descBox, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_3, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.tagInputBox, 0, wx.ALL|wx.EXPAND, 5)
        self.window_1_pane_2.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableRow(2)
        grid_sizer_1.AddGrowableCol(1)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)
        sizer_3.Add(self.window_1, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        
    def onEmail(self, event):
        name = self.nameBox.GetValue()
        try:
            link = self.SQLMod.fetchLink(name)
            subject = 'Emailing: %s'%name
            simplemapi.SendMail(subject=subject, attachfiles=link)
        except IndexError:
            print('No file Selected')
        
    def onReadOnly(self, event):
        self.readOnly=not self.readOnlyMenu.IsChecked()
        for textControl in [self.descBox,self.tagInputBox]:
            textControl.SetEditable(self.readOnly)
        for b in [self.uploadMenu, self.removeMenu, self.uploadButton]:
            b.Enable(self.readOnly)        
        
    def onAbout(self, event):
        DMS.showAbout(self.Version)
        
    def onSearch(self, event):
        DMS.underConstruction(self)
        
    def onOpenDB(self,event):
        DMS.underConstruction(self)
        
    def onRemove(self, event):
        name=self.nameBox.GetValue()
        link=self.SQLMod.fetchLink(name)
        if DMS.removeDoc(self,name,link):
            self.SQLMod.delRecord(name,True)
            self.updateValues()
        
    def on_iconify(self, e):
        """
        Being minimized, hide self, which removes the program from the taskbar.
        """
        self.Hide()

    def OnCloseWindow(self, event):
        # tell the window to kill itself
        self.SQLMod.closeSQL()
        self.trayIcon.kill()
        self.Destroy()


    def infoChange(self,event):
        if self.isDirty():
            name=self.nameBox.GetValue()
            desc=self.descBox.GetValue()
            tags=DMS.string2list(self.tagInputBox.GetValue())
            self.SQLMod.replaceInsert({'name':name,'desc':desc,'tags':tags})
            self.updateValues(name)
        
    def selectionChange(self, event):
        if self.fileSelBox.GetStringSelection() != '': self.selectionHandler()
        
    def onFilter(self, event): # wxGlade: MyFrame.<event_handler>
        filter = bytes(self.filterBox.GetStringSelection(),'utf-8')
        if filter !='':
            self.preFilterTags.append(filter)
            self.updateValues()

    def onReset(self, event): # wxGlade: MyFrame.<event_handler>
        self.preFilterTags=[]
        self.updateValues()
        event.Skip()
        
    def onUpload(self, event):
        returnDict,self.uploadDefault = DMS.uploadFile(self,self.storagePath,self.relativeStorage,self.uploadDefault)
        if returnDict: 
            returnDict['tags']=self.preFilterTags
            self.SQLMod.replaceInsert(returnDict)
            self.updateValues(returnDict['name'])

    def onDownload(self, event): # wxGlade: MyFrame.<event_handler>
        link=self.SQLMod.fetchLink(self.nameBox.GetValue())
        self.downloadDefault=DMS.downloadFile(self,os.path.join(self.rootPath,link),self.downloadDefault)

    def onOpen(self, event): # wxGlade: MyFrame.<event_handler>
        link=self.SQLMod.fetchLink(self.nameBox.GetValue())
        DMS.openLink(os.path.join(self.rootPath,link))
        
    def onDrop(self,returnDict):
        returnDict['tags']=self.preFilterTags
        self.SQLMod.replaceInsert(returnDict)
        self.updateValues(returnDict['name'])
                
    def isDirty(self):
        #protect from writing an empty name file
        if self.nameBox.GetValue()=='': return False
        #Check to see if the text control fields have changed
        temp=[self.descBox, self.tagInputBox]
        for obj in temp:
            if obj.IsModified():
                return True
        return False
        
    def selectionHandler(self):
        sel=self.fileSelBox.GetStringSelection()
        self.nameBox.ChangeValue(sel)
        self.descBox.ChangeValue(self.SQLMod.fetchDesc(sel))
        self.tagInputBox.ChangeValue(b'\n'.join(self.SQLMod.fetchTags(sel)))
            
    def updateValues(self,select=False):
        #Error checking added at the bottom to catch problems with opening a brand new database.  May try something else seems kind of clunky
        filterName, filterTags = self.SQLMod.retFiltNameTags(self.preFilterTags)
        temp=((self.filterBox,filterTags),(self.fileSelBox,filterName))
        for obj, oList in temp:
            obj.Items=oList
        if select:
            self.fileSelBox.SetStringSelection(select)
        else:
            try:#Tried:  wx._core.PyAssertionError: but got a Syntax Error
                self.fileSelBox.SetSelection(0)
            except:
                pass
        try:    
            self.selectionHandler()
        except (TypeError, IndexError):
            pass

# end of class MyFrame


if __name__ == "__main__":
    #app = wx.PySimpleApp(0)
    app = wx.App()
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()