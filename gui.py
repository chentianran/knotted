import os
import wx
import threading
import homcomplex
 
class Viewer(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Homology Viewer')
        self.panel = wx.Panel(self.frame)
 
        self.PhotoMaxSize = 240
 
        self.createWidgets()

        self.H = homcomplex.HomComplex()

        self.frame.Show()
 
    def createWidgets(self):
        img = wx.EmptyImage(600,500)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
 
        self.cmd_input = wx.TextCtrl(self.panel, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.cmd_input.Bind(wx.EVT_TEXT_ENTER, self.onCmd)

        browseBtn = wx.Button(self.panel, label='Browse')
        #browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.cmd_input, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onCmd(self, event):
        cmd = self.cmd_input.GetValue().strip()
        if len(cmd) > 0:
            key, sep, line = cmd.partition(' ')
            if 'B' == key:
                arg = line.partition('=')
                if arg[1] == '=':
                    name = arg[0].strip()
                    terms = arg[2].split('+')
                    for t in terms:
                        self.H.bound (name, t.strip())
                self.onView()

            elif 'ker' == key:
                print self.H.ker()

            elif 'img' == key:
                print self.H.img()

            elif 'hom' == key:
                print self.H.hom_string()

            self.cmd_input.SetValue('')

    def onView(self):
        self.H.draw_png('hom.png')
        filepath = "hom.png"
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
viewer = Viewer()
viewer.MainLoop()

