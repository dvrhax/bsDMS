import wx
import wx.adv

class trayIcon(wx.adv.TaskBarIcon):
    def __init__(self, icon, tooltip, frame, baseStyles):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(icon, tooltip)
        self.frame = frame
        self.baseStyles=baseStyles
        #
        # At the very least, restore the frame if double clicked.  Addother
        # events later.
        #
        self.CreatePopupMenu()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP,self.onRightUp)
        
    def on_left_dclick(self, e):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def onRightUp(self, event):
        self.PopupMenu(self.menu)
        
    def checkOnTop(self, event):
        if self.onTop.IsChecked():
            newStyle=self.baseStyles | wx.STAY_ON_TOP
        else:
            newStyle=self.baseStyles
        self.frame.SetWindowStyle(newStyle)
        
    def CreatePopupMenu(self):
        self.ID_Restore=wx.NewId()
        self.menu=wx.Menu()  
        self.menu.Append(self.ID_Restore, "Restore")
        self.onTop=self.menu.Append(wx.NewId(), "Always On Top","", wx.ITEM_CHECK)
        self.menu.AppendSeparator()  
        self.menu.Append(wx.ID_EXIT, "Close App")
        self.Bind(wx.EVT_MENU, self.frame.OnCloseWindow, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_left_dclick, id=self.ID_Restore)
        self.Bind(wx.EVT_MENU, self.checkOnTop, self.onTop)

	
    def kill(self):
        self.Destroy()
