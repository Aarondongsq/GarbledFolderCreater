'''
    乱码文件夹生成器 - GUI主代码
    Copyright (C) 2026 Chung Chai Aaron Dong

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    --- 特别补充说明 ---
    1. 严禁倒卖本代码（包括其中的一部分）或将其用于商业洗稿。
    2. 严禁 Gitee、GitCode 等平台在未经作者书面许可的情况下，私自镜像、克隆
       或通过爬虫抓取本项目用于增加平台KPI等。
    3. 任何违反 GPL v3 协议的行为，作者保留在开源社区公示及追究法律责任的权利。
'''

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as fileask

import sys
from threading import Thread
from os.path import join, exists, abspath
from os import makedirs
from time import sleep

from random import randint, choice #Python自带模块

import LICENSE
import aboutwindow
import supportwindow #导入外部模块

#==================== 全局函数 ====================
def winfo_geometry(master:tk.Tk, x:int, y:int):
    '''
    如果使用该函数，在窗口设置大小的时候，默认居中在窗口中央。
    （Tips：默认设置最小窗口伸展为你输入的数值）
    '''
    screenwidth = (master.winfo_screenwidth() - x)/2
    screenheight = (master.winfo_screenheight() - y)/2
    master.geometry(f'{x}x{y}+{int(screenwidth)}+{int(screenheight)}')
    master.minsize(x, y)

def resource_path(relative_path) -> str:
    '''
    针对软件打包的情况生成路径，然后返回str值，可以直接使用。
    特别关照“VS”这个狗屎调试器，能自动检测是否在调试模式

    relative_path：以这个代码文件为基准，定位到文件的路径。
    '''
    try:
        # PyInstaller创建临时文件夹,将路径存储于_MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path =abspath(".")

    #↓返回拼接结果
    if exists(join(base_path, relative_path)): #检查是否在VS调试环境下
        return join(base_path, relative_path) 
    else:
        return join(base_path, 'GUI', relative_path)

def dpi_fix(master:tk.Tk):
    '''
    解决窗口在高DPI下错位问题，针对Windows的狗屎代码的优化
    这个函数特别解决150DPI下错位问题（针对希沃大屏等特殊设备）
    靠，Tkinter的代码真的够老，修复DPI的函数都没有，技术债是吗？
    '''
    pixels = master.winfo_fpixels('72p') / 72.0 #计算当前DPI
    if pixels > 1.7 and sys.platform == 'win32':  #如果DPI大于125
        scaling = pixels*0.8
        #下方发放设置参数，让其全局生效
        master.call('tk', 'scaling', scaling)
    elif pixels < 1.34 and sys.platform == 'win32': #如果DPI是100
        scaling = pixels*1.3
        #下方发放设置参数，让其全局生效
        master.call('tk', 'scaling', scaling)
#==================== 类定义 ====================
class CreateFolder:
    def __init__(self, main:tk.Tk, path:str, number:str):
        '''
        这个类负责创建文件夹。
        main：主窗口
        path：用户选择的路径
        number：用户希望生成的文件夹。
        
        __init__说明：
        这个函数仅负责走流程这个核心操作。
        涉及其他方面（如文件夹存在检查、数字合法检查等），将会交给其他函数处理。
        '''
        main.tiplabel.place_forget() #清空状态
        foldercheck_result = self._check_folder_exists(main, path)
        numbercheck_result = self._check_number_exists(main, number) #获取目录和数字合规性
        if foldercheck_result and numbercheck_result: 
            #检查是否通过两个条件，通过才执行下面的代码
            loadwin = LoadingWindow(main)
            createfolder_thread = Thread(target=self._execute, daemon=True,
                                         args=(path, number, loadwin)) #创建线程（用于生成文件夹）
            createfolder_thread.start()

    def _choose_letter(self, how_long:int) -> str:
        '''
        负责随机生成一段乱码，也是乱码文件夹生成器的一个重要零件。
        不过开始之前，你先给我输入一个数字，决定我到底要生成多长的乱文
        我生成好了后会给你
        '''
        letter = 'abcdefghijklmnopqrstuvwxyz1234567890' #字符串
        #↓返回已经搞定的乱码
        return ''.join(choice(letter) for _ in range(how_long)) 

    def _set_folder_name(self) -> str:
        '''
        负责乱码文件夹的命名。
        不需要向该函数提供任何名称，可以直接调用。
        当工作完成时，返回乱码文件夹的值。
        '''
        template = ['%s-%s-%s-%s','%s-%s-%s',
                    '%s-%s','%s'] #乱码文件夹名称的名称模板
        choosed_template = choice(template) #选择一个模板
        word_temp = [] #乱码的暂存列表
        for i in range(choosed_template.count('%s')):
            word_temp.append(self._choose_letter(randint(5, 10)))
        #下方的return将会现场组合好乱码文件夹的名称，然后返回
        return choosed_template%tuple(word_temp)
    
    def _execute(self, path:str, number:str, window:tk.Toplevel):
        '''
        这个函数负责创建文件夹。
        至于其他的活？这是其他函数干的事情
        '''
        try:
            for _ in range(int(number)): #循环，创建文件夹，循环多少次那么创建文件夹多少次
                fullpath = join(path, self._set_folder_name()) #生成文件夹的路径
                if not exists(fullpath): # 只有不存在才创建，防止崩溃
                    makedirs(fullpath)
                sleep(0.01) #延时，针对低配电脑
            window.after(0, lambda: msgbox.showinfo('提示', '文件夹创建完成啦！')) #创建成功提示
        except Exception as e:
            window.after(0,lambda error=e: self._show_error(window, '''1) 你选择的文件夹所在磁盘下线或者故障。
2) 你选择的文件夹所在磁盘空间已满。
3) 你没有给该软件相应权限去操作你选择的文件夹（如果你想在受限文件夹创建乱码文件夹，这个是有必要的）
4) 你试图在只读的网络驱动器内通过软件创建乱码文件夹。
5) 你选择的文件夹所在的网络驱动器由于一些原因下线了。''', error)) #抛出窗口错误
        finally:
            #↓销毁窗口并关闭，防止内存残留
            window.after(50, window.destroy) #延时50ms，防止抢占资源

    def _check_folder_exists(self, main:tk.Tk, path:str) -> bool:
        '''
        检查用户输入的文件夹路径是否存在。
        如果不存在，那么将会提示用户，返回False。
        如果存在，那么放行，返回True。
        '''
        if not exists(path): #检查文件夹是否存在
            main.tiplabel.config(text='必须指定一个存在的文件夹。')
            main.tiplabel.place(x=20, y=200, width=510, height=30) #提示用户
            return False
        else:
            return True
    
    def _check_number_exists(self, main:tk.Tk, number:str) -> bool:
        '''
        检查用户输入的数字是否合规的阿拉伯整数。
        如果不合规甚至报错的，那么提示用户，返回False
        如果合规，那么放行，返回True。
        '''
        try:
            if int(number) <= 0: #判断输入的数是否小于等于0
                main.tiplabel.config(text='生成的文件夹不能小于等于0。')
                main.tiplabel.place(x=20, y=200, width=510, height=30) 
            else:
                return True
        except ValueError: #在int过程中如果出错那么不合规
            main.tiplabel.config(text='必须输入阿拉伯整数。')
            main.tiplabel.place(x=20, y=200, width=510, height=30) 

    def _show_error(self, topwindow, tipinfo, errorinfo):
        '''
        当创建文件夹遇到致命错误时，将会执行这个函数。

        topwindow：希望在选定窗口上置顶的变量。
        tipinfo：展示排查信息。
        errorinfo：错误信息。
        '''
        Errorwin = ErrorWindow()
        Errorwin.window_set(topwindow) #置顶窗口
        Errorwin.set_error_info(tipinfo, errorinfo)

class LoadingWindow(tk.Toplevel):
    def __init__(self, main):
        '''
        此模块负责在创建文件夹时弹出窗口。
        在此窗口弹出期间，用户无法在弹窗以外的窗口做任何事情，直到任务完成后消失。
        '''
        super().__init__()
        self.title('创建文件夹中，请稍等...')
        winfo_geometry(self, 400, 150)
        self.attributes('-alpha', 0.8)
        self.protocol('WM_DELETE_WINDOW', lambda: None)
        self.resizable(0, 0) #窗口初始化设置

        self._set_components() #设置控件

        self.transient(main)
        self.grab_set() #由于该窗口的性质，故这样设置，使其变成一个弹窗。
        self.focus_set() 
    
    def _set_components(self):
        '''
        此函数负责在Loading窗口中创建控件。
        '''
        self.showtips = tk.Label(self, text='正在创建文件夹\n请稍安勿躁', 
                                 font=('', 12, 'bold'))
        self.showtips.place(x=100, y=25, width=200, height=50)
        self.process = ttk.Progressbar(self, orient='horizontal', mode='indeterminate')
        self.process.place(x=70, y=90, width=265, height=25) 
        #进度条，指示软件正在运行中，但是不具有进度功能↑
        self.process.start(5)

class ErrorWindow(tk.Toplevel):
    def __init__(self):
        '''
        这是一个错误窗口类，在软件遇到错误的时候，还无法解决，那么将会调用。

        __init__函数说明：
        仅负责窗口的创建，其他的话是由其他函数负责，保持简洁。

        main：软件主窗口变量。
        '''
        super().__init__()
        self.title('哎呀！出错了！')
        winfo_geometry(self, 550, 400)
        self.resizable(0, 0) #窗口参数初始化
        self.attributes('-alpha', 0.8) 

    def window_set(self, topwindow):
        '''
        此函数负责窗口的置顶，并且初始化一些东西。

        topwindow：希望置顶的窗口。
        '''
        self.transient(topwindow) #核心出装
        self.grab_set()
        self.focus_set()

        #↓设置控件
        self._set_components() 
    
    def set_error_info(self, tipstext:str, errortext:any):
        '''
        设置用户排查提示文本、错误信息。

        tipstext：给予用户提示的信息文本。
        errortext：软件报错时的信息。
        '''
        self.tipstext.insert('1.0', tipstext)
        self.tipstext.config(state='disabled')
        self.errorinfo.insert('1', errortext)
        self.errorinfo.config(state='disabled')

    def _set_components(self):
        '''
        此函数负责控件的创建。
        这个函数是作为__init__函数没创建控件的补充。
        '''
        #-----文本设置-----
        label_options = [('出错了...通常，这是由于以下原因造成的：', 28),
                         ('若排查完仍然出现该窗口，请联系作者解决。', 270)] #Label的模板设置：（文本， y）
        for text, y in label_options:
            tk.Label(self, text=text, font=('', 12)).place(x=20, y=y, 
                                                           width=420, height=23) #创建文本

        #-----提示阅览控件----
        self.tipstext = tk.Text(self, relief='flat', font=('楷体', 10))
        self.tipstext.place(x=30, y=60, width=475, height=200)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tipstext.yview)
        self.scrollbar.place(x=500, y=60, width=20, height=200) #滚动条创建
        self.tipstext.config(yscrollcommand=self.scrollbar.set) #设置好滚动条的状态

        #-----LabelFrame内控件-----
        self.labelframe = ttk.Labelframe(self, text='报错信息', labelanchor='n')
        self.labelframe.place(x=30, y=300, width=490, height=60) #labelframe控件
        self.errorinfo = ttk.Entry(self.labelframe, font=('楷体', 10)) #报错详细信息会显示在这个控件上
        self.errorinfo.place(x=10, y=0, width=465, height=26)

class MainWindow(tk.Tk):
    def __init__(self):
        '''
        这里会初始化窗口的设置，至于控件？会交给set_components负责
        主菜单的配置会在这里配置，但是子菜单和孙菜单会在_child_menu_create配置
        '''
        super().__init__()
        self.title('乱码文件夹 生成器')
        winfo_geometry(self, 550, 380)
        self.resizable(0, 0)
        self.attributes('-alpha', 0.8)
        self.protocol('WM_DELETE_WINDOW', sys.exit)
        self._set_icon(resource_path(join('assets', 'icon', 'mainicon.ico')))
        dpi_fix(self) #解决DPI问题，全局应用
        
        self._set_components() #开始创建控件

        #-----菜单：创建----
        self.menu = tk.Menu() 
        self.filemenu = tk.Menu(tearoff=0)
        self.gerenatemenu = tk.Menu(tearoff=0)
        self.aboutmenu = tk.Menu(tearoff=0)
        
        #-----子菜单：创建----
        self.filemenu.alpha = tk.Menu(tearoff=0)

        self._child_menu_create() #拼接，启动！

        #-----主菜单：菜单项目部分&设置窗口-----
        self.menu.add_cascade(label='文件', menu=self.filemenu)
        self.menu.add_cascade(label='生成', menu=self.gerenatemenu)
        self.menu.add_cascade(label='关于', menu=self.aboutmenu)

        self.config(menu=self.menu)

    def _child_menu_create(self):
        '''
        负责组装菜单，给宝贵的__init__函数留点空间
        '''

        #-----filemenu子菜单：透明度调节-----
        alpha_options = [
            ('0.2 （不建议）', 0.2),
            ('0.4', 0.4),
            ('0.6', 0.6),
            ('0.8 （默认）', 0.8),
            ('不透明', 1.0)
        ] #透明度选项：（标注文本，输入的值）
        for label, opinions in alpha_options:
            self.filemenu.alpha.add_command(label=label, 
                 command=lambda v=opinions: self.attributes('-alpha', v))

        #-----filemenu菜单-----
        self.filemenu.add_cascade(label='窗口透明度', menu=self.filemenu.alpha)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='退出软件（确定吗？）', foreground='red', 
                                  activebackground='#8f3636', 
                                  activeforeground='white', command=sys.exit)
        #-----generatemenu菜单---
        generate_options = [10, 20, 30, 50, 
                            100, 200, 300, 500, 
                            1000, 5000, 10000] #生成多少个文件夹，数字指要生成多少个
        for number in generate_options:
            self.gerenatemenu.add_command(label=f'生成{str(number)}个乱码文件夹...',
                                          command=lambda num=number: self.confirmed_numfolder_(num))

        #-----aboutmenu菜单-----
        self.aboutmenu.add_command(label='关于该软件', command=lambda: aboutwindow.MainWindow(self))
        self.aboutmenu.add_command(label='开源许可证...', 
                                   command=lambda: LICENSE.MainWindow(self))
        self.aboutmenu.add_separator()
         #↓支持软件窗口
        self.aboutmenu.add_command(label='❤ 支持该软件 ❤', background='#fc7aab',  foreground='#f31c0a',  
                                   font=('', 15, 'bold'), command=lambda: supportwindow.MainWindow(self))

    def _set_components(self):
        '''
        负责创建窗口内的控件。
        光有窗口没啥用，如果只有窗口的软件那叫做空壳子，而不是GUI。
        要变成GUI，先要窗口，其次控件。
        '''
        ##########Labelframe内控件##########
        #---frame初始化&文本设置---
        framesettings = [('生成位置：', 20, 10),
                         ('生成数量：', 20, 45),
                         ('个', 430, 45)]#设置文本输入参数：(文本, X, Y)
        self.labelframe = ttk.Labelframe(self, text='生成设置', width=490, height=160)
        self.labelframe.place(x=30, y=20)
        for text,x,y in framesettings: #设置文本（针对Labelframe内）
            tk.Label(self.labelframe, text=text, font=('', 10, 'bold')).place(x=x, y=y)

        #---输入框部分---
        self.putwhere_entry = ttk.Entry(self.labelframe, font=('楷体', 12))
        self.putwhere_entry.place(x=115, y=9, width=340, height=25) #生成位置 输入框
        self.howmany_entry = ttk.Entry(self.labelframe, font=('楷体', 12))
        self.howmany_entry.place(x=115, y=45, width=310, height=25) #生成数量 输入框
        
        #---按钮部分---
        self.btn_storage = tk.Button(self.labelframe, text='让我选择存放位置！' ,
         bg='green', fg='white', border=0, relief='flat', font=('', 10, 'bold'),
        activebackground='#FCB827', activeforeground='white', 
        command=self.askwheretostroge_)
        self.btn_storage.place(x=25, y=83, width=200, height=33) #选择存放位置 按钮
        self.btn_ramdom = tk.Button(self.labelframe, text='文件夹数量随机' ,
        bg='#9200d0', fg='white', border=0,  relief='flat', font=('', 10, 'bold'),
        activebackground='#FCB827', activeforeground='white',
        command=self.random_numfolder_)
        self.btn_ramdom.place(x=260, y=83, width=200, height=33) #文件夹数量随机 按钮

        ##########self直接创建##########
        #-----提示文本-----
        self.tiplabel = tk.Label(self, text='测试内容，此文本不该在正常运作时出现',
                                 fg='red' , font=('楷体', 14, 'bold')) #这个控件不显示，在用户做出错误操作时才会显示

        #-----按钮部分-----
        self.actionbutton = tk.Button(self, text='开始生成！', bg='green', fg='white',
                                      relief='flat', border=0, width=20, height=2,
                                      font=('', 10, 'bold'), 
                                      activebackground='#FCB827', activeforeground='white',
                                      command=lambda: CreateFolder(self, self.putwhere_entry.get(), self.howmany_entry.get())) #开始按钮生成
        self.actionbutton.place(x=175, y=250)

    def _set_icon(self, icon:str):
        '''
        设定软件窗口栏图标。
        如果遇到极端情况，导致图标无法放置，那么将跳过这一步。

        icon：图标位置。
        '''
        try: #设定图标
            self.iconbitmap(icon)
        except: #若是遇到极端情况，将不会设定图标
            pass

    def askwheretostroge_(self):
        '''
        负责询问用户需要把乱码文件夹存储到哪里。
        如果用户选择好了，那么将会修改生成位置输入框内的东西，变成用户选择好的目录。
        与按钮“让我选择存放位置！”联系。
        '''
        path = fileask.askdirectory(title='请选择保存的位置')
        if len(path) > 0: #检查用户到底选择了没有
            self.putwhere_entry.delete('0','end')
            self.putwhere_entry.insert('0', path)

    def random_numfolder_(self):
        '''
        这个函数将会随机抽取一个数，然后修改生成数量输入框内的东西。
        与按钮“文件夹数量随机”有联系。
        '''
        self.howmany_entry.delete('0','end')
        #↓ 随机抽取100~1000的数
        self.howmany_entry.insert('0',randint(100, 1000))

    def confirmed_numfolder_(self, number:int):
        '''
        这个函数将会根据填入的数值（取决于number填的是啥），修改生成数量文件夹的输入框。
        与菜单中generatemenu中“生成XXX个文件夹...”有关系。
        '''
        self.howmany_entry.delete('0', 'end')
        self.howmany_entry.insert('0', str(number))

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()