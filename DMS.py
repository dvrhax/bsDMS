import wx, os, dSQLite, shutil, webbrowser, myDialogs

class SQLMod():
    def __init__(self, dbPath):
        self.dbPath=dbPath
        self.tableName='DocManSys'
        self.conn=self.connectSQL()
        self.cur=self.conn.cursor()
        try:
            self.cur.execute('select * from DocManSys')
        except dSQLite.OperationalError:
            self.cur.execute('create table DocManSys (name text, link text, desc text, tags list)')
        except dSQLite.DatabaseError:
            print('Database Error')
        
        
    def connectSQL(self):
        return dSQLite.connect(self.dbPath, detect_types=dSQLite.PARSE_DECLTYPES)
        
    def closeSQL(self):
        self.cur.close()
        self.conn.close()
        
    def fetchLink(self,name):
        self.cur.execute('select link from DocManSys where name=?',(name,))
        return self.cur.fetchall()[0][0]
        
    def fetchDesc(self,name):
        self.cur.execute('select desc from DocManSys where name=?',(name,))
        return self.cur.fetchall()[0][0]
        
    def fetchTags(self,name):
        self.cur.execute('select tags from DocManSys where name=?',(name,))
        return self.cur.fetchall()[0][0]
        
    def delRecord(self,name,commit=False):
        self.cur.execute('delete from DocManSys where name=?',(name,))
        if commit: self.conn.commit()
    
    def executeInsRepl(self,info,replace):
        if replace:
            self.delRecord(info[0])
        self.cur.execute('insert into DocManSys values (?,?,?,?)',tuple(info))
        self.conn.commit()
        
    def replaceInsert(self, iDict):
        tag2pos={'name':0,'link':1,'desc':2,'tags':3}
        if self.nameExists(iDict['name']):
            info=list(self.fetchRow(iDict['name']))
            for k,v in iDict.items():
                info[tag2pos[k]]=v
            self.executeInsRepl(info,True)
        else:
            info = ['','','',[]]
            for k,v in iDict.items():
                info[tag2pos[k]]=v
            self.executeInsRepl(info,False)

    def nameExists(self, findName):
        return findName in self.retAllNames()
        
    def retAllNames(self):
        #Returns a list of all names in the database
        self.cur.execute('select name from DocManSys')
        return self.compactReturn(self.cur.fetchall())
        
    def subLists(self,iList):
        x={}
        for tup in iList:
            for i,v in enumerate(tup):
                try:
                    x[i].append(v)
                except:
                    x[i]=[v]
        out=[]
        for k,v in x.items():
            out.append(v)
        return tuple(out)
        
    def fetchRow(self,name):
        self.cur.execute('select * from DocManSys where name=?',(name,))
        return self.cur.fetchall()[0]
        
    def retNameTags(self):
        self.cur.execute('select name, tags from DocManSys')
        return self.cur.fetchall()
        
    def retFiltNameTags(self, tagList):
        temp=self.retNameTags()
        for t in tagList:
            ntTup=temp
            temp=[]
            for nt in ntTup:
                if t in nt[1]:
                    temp.append(nt)
        if len(temp)==0: return [],[]
        name,tags = self.subLists(temp)
        return name, list(set(self.compactList(tags))-set(tagList))
    
    def compactList(self, iList):
        oList = []
        for e in iList:
            try:
                oList += e
            except TypeError:
                pass
        oList=list(set(oList))
        try:
            oList.remove('')
        except:
            pass
        return oList
    
    def compactReturn(self,obj):
        oList=[]
        for subObj in obj:
            oList+=list(subObj)
        return list(set(oList))
        
    def updateNameLink(self, oldName, newName, newLink):
        #Helper function to facilitate conversions to office 2007
        #and other name replacement operations
        tag2pos={'name':0,'link':1,'desc':2,'tags':3}
        if self.nameExists(oldName):
            info = list(self.fetchRow(oldName))
            info[tag2pos['name']] = newName
            info[tag2pos['link']] = newLink
            self.executeInsRepl(info, False)
            self.delRecord(oldName, True)
            return True
        else:
            return False
        

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent, savePath, relPath):
        wx.FileDropTarget.__init__(self)
        self.parent = parent
        self.savePath = savePath
        self.relPath = relPath

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            if self.parent.readOnly:
                self.parent.onDrop(fileCopy(file,self.savePath,self.relPath))
            
def underConstruction(parent):
    myDialogs.ConstructionDialog(parent)
            
def showAbout(vers):
    name='betascheme Document Management System'
    version=vers
    copyright='GPL 3.0'
    desc='An internal DMS built on Python and SQLite3'
    website=''
    developers=['DVRHax']
    license=''
    myDialogs.aboutDLG(name, version, copyright, desc, website, developers, license)
    
def removeDoc(parent,name,link):
    msg='Are you sure you want to remove %s' % name
    if myDialogs.msgDialog(parent,msg):
        try:
            os.remove(link)
            return True
        except:
            return removeDocFail(parent,name)
    
def removeDocFail(parent,name):
    msg='%s could not be removed.  Would you still like to remove the database record?' % name
    return myDialogs.msgDialog(parent,msg)
    
        
def downloadFile(parent, fromPath, dDir):
    # Create the dialog. In this case the current directory is forced as the starting
    # directory for the dialog, and no default file name is forced. This can easilly
    # be changed in your program. This is an 'save' dialog.
    #
    # Unlike the 'open dialog' example found elsewhere, this example does NOT
    # force the current working directory to change if the user chooses a different
    # directory than the one initially set.
    dFile=os.path.split(fromPath)[-1]
    dlg = wx.FileDialog(
        parent, message="Save file as ...", defaultDir=dDir, 
        defaultFile=dFile, wildcard="All files (*.*)|*.*", style=wx.SAVE
        )

    # This sets the default filter that the user will initially see. Otherwise,
    # the first filter in the list will be used by default.
    dlg.SetFilterIndex(2)

    # Show the dialog and retrieve the user response. If it is the OK response, 
    # process the data.
    if dlg.ShowModal() == wx.ID_OK:
        toPath = dlg.GetPath()
        shutil.copy2(fromPath, toPath)

    # Destroy the dialog. Don't do this until you are done with it!
    # BAD things can happen otherwise!
    dlg.Destroy()
    try:
        return os.path.split(toPath)[0]
    except:
        return dDir
            
def uploadFile(parent,savePath,relPath,uDir):
    # Create the dialog. In this case the current directory is forced as the starting
    # directory for the dialog, and no default file name is forced. This can easilly
    # be changed in your program. This is an 'open' dialog, and allows multitple
    # file selections as well.
    #
    # Finally, if the directory is changed in the process of getting files, this
    # dialog is set up to change the current working directory to the path chosen.
    canceled=True
    dlg = wx.FileDialog(
        parent, message="Choose a file",
        defaultDir=uDir, 
        defaultFile="",
        wildcard="All files (*.*)|*.*",
        style=wx.FD_OPEN | wx.FD_CHANGE_DIR
        )

    # Show the dialog and retrieve the user response. If it is the OK response, 
    # process the data.
    if dlg.ShowModal() == wx.ID_OK:
        # This returns a Python list of files that were selected.
        paths = dlg.GetPaths()[0]
        canceled=False

    try:
        newDefault=os.path.split(paths)[0]
    except:
        newDefault=uDir
    # Destroy the dialog. Don't do this until you are done with it!
    # BAD things can happen otherwise!
    dlg.Destroy()
    try:
        return fileCopy(paths,savePath,relPath), newDefault
    except UnboundLocalError:
        return False, newDefault
        
def fileCopy(fromPath, toPath, relPath):
    if not os.path.isdir(toPath):
        os.mkdir(toPath)
    shutil.copy2(fromPath, toPath)
    fName=os.path.split(fromPath)[-1]
    link=os.path.join(relPath,fName)
    return {'name':fName,'link':link}
    
def openLink(link):
    webbrowser.open(link)
    
def string2list(iString):
    tList = list(set(iString.splitlines()))
    tList.sort()
    try:
        tList.remove('')
    except:
        pass
    return tList
