import os
import wx
import threading
 
from mathtex.mathtex_main import Mathtex
from mathtex.fonts import BakomaFonts

from homformat  import *
from homcomplex import *

class Viewer(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Homology Viewer')
        self.panel = wx.Panel(self.frame)
 
        self.createWidgets()

        self.H = HomComplex()
        self.mathfont = BakomaFonts()
        self.result_tex = ''

        self.cmd_input.SetFocus()
        self.frame.Show()
 
    def createWidgets(self):
        img1 = wx.EmptyImage(600,500)
        img2 = wx.EmptyImage(600,100)
        self.img_graph  = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img1))
        self.img_result = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img2))
 
        self.cmd_input = wx.TextCtrl(self.panel, size=(600,-1), style=wx.TE_PROCESS_ENTER)
        self.cmd_input.Bind(wx.EVT_TEXT_ENTER, self.onCmd)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.img_graph,  0, wx.ALL, 5)
        self.mainSizer.Add(self.img_result, 0, wx.ALL, 5)
        self.mainSizer.Add(self.cmd_input, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onCmd(self, event):
        cmd = self.cmd_input.GetValue().strip()
        if 'ker' == cmd:
            self.result_tex = r'$Ker=' + set2tex(self.H.ker()) + '$'
            self.onResult()

        elif 'img' == cmd:
            self.result_tex = r'$Im=' + set2tex(self.H.img()) + '$'
            self.onResult()

        elif 'hom' == cmd:
            ker, img = self.H.hom()
            self.result_tex = hom2tex (ker, img)
            self.onResult()

        else:
            src, sep, line = cmd.partition('~')
            if '~' == sep:
                name = src.strip()
                terms = line.split('+')
                for t in terms:
                    s, sep, v = t.partition('*')
                    if '*' == sep:
                        self.H.bound_with (name, v.strip(), scalar=s.strip())
                    else:
                        self.H.bound (name, t.strip())
                self.onView()

        self.cmd_input.SetValue('')

    def onView(self):
        self.H.draw_png('hom.png')
        filepath = "hom.png"
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
 
        self.img_graph.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
    def onResult(self):
        m = Mathtex (self.result_tex, self.mathfont, 26)
        m.save('result.png', 'png')
        img = wx.Image('result.png', wx.BITMAP_TYPE_ANY)
        self.img_result.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 

viewer = Viewer()
viewer.MainLoop()

