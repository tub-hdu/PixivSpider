#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from PixivSpider import *
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('P站爬虫')
        self.master.geometry('350x250')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.ProgressBar1Var = StringVar(value='')
        self.ProgressBar1 = Progressbar(self.top, orient='horizontal', maximum=100, variable=self.ProgressBar1Var)
        self.ProgressBar1.place(relx=0.026, rely=0.796, relwidth=0.952, relheight=0.077)

        self.List1Var = StringVar(value='List1')
        self.List1Font = Font(font=('宋体',9))
        self.List1 = Listbox(self.top, listvariable=self.List1Var, font=self.List1Font)
        self.List1.place(relx=0.513, rely=0.036, relwidth=0.465, relheight=0.700)

        self.style.configure('TCommand1.TButton', font=('宋体',9))
        self.Command1 = Button(self.top, text='下载今日美图', command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.place(relx=0.026, rely=0.036, relwidth=0.465, relheight=0.689)

        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体',9))
        self.Label1 = Label(self.top,text="",style='TLabel1.TLabel')
        self.Label1.place(relx=0.026, rely=0.905, relwidth=0.926, relheight=0.090)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)


    def Command1_Cmd(self, event=None):
        #TODO, Please finish the function here!

        self.__output_info('准备启动P站爬虫')
        x=PixivSpider(self.__output_info,self.ProgressBar1Var,self.List1)
        x.start()
        

    def __output_info(self,message):

        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体',9))
        self.Label1 = Label(self.top,text=message,style='TLabel1.TLabel')
        self.Label1.place(relx=0.026, rely=0.905, relwidth=0.926, relheight=0.090)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()

