'''
    关于软件 - 乱码文件夹生成器 模块组件
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
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import sys
from os.path import join, abspath

#==================== 全局函数 ====================
def resource_path(relative_path) -> str:
    '''
    针对软件打包的情况生成路径，然后返回str值，可以直接使用。

    relative_path：以这个代码文件为基准，定位到文件的路径。
    '''
    try:
        # PyInstaller创建临时文件夹,将路径存储于_MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path =abspath(".")

    #↓返回拼接结果
    return join(base_path, relative_path) 

#==================== 类定义 ====================
class MainWindow(tk.Toplevel):
    def __init__(self, main='Debug'):
        '''
        展示乱码文件夹生成器的关于信息界面。

        __init__函数说明：
        负责窗口初始化、菜单基本创建，其他的是归其他函数管。
        main：需要被置顶的窗口。
        '''
        super().__init__()
        self.title('乱码文件夹 生成器 - 关于该软件')
        self._winfo_geometry(600, 400)
        self.attributes('-alpha', 0.8)
        self._dpi_fix() #初始化窗口参数

        #self.transient(main)
        #self.grab_set()
        #self.focus_set() #负责将窗口变弹窗（Debug：暂时禁用）

        #----- 菜单创建 -----
        self.menu = tk.Menu() #主菜单
        self.filemenu = tk.Menu(tearoff=0)
        self.moremenu = tk.Menu(tearoff=0)

        self.filemenu.alphamenu = tk.Menu(tearoff=0) #透明度菜单（子菜单）

        # ----- 一级菜单设置 -----
        self.menu.add_cascade(label='文件', menu=self.filemenu)
        self.menu.add_cascade(label='更多', menu=self.moremenu)

        self._child_menu_create() #拼接菜单
        self._set_components() #放置控件

        self.config(menu=self.menu)
        
    def _child_menu_create(self):
        '''
        负责创建软件菜单，为宝贵的__init__函数节省空间。
        '''
        # ----- Filemenu子菜单 - 透明度调整菜单 -----
        alpha_options = [('0.2 （不建议）', 0.2), ('0.4', 0.4), ('0.6', 0.6), ('0.8 （默认）', 0.8),
                         ('不透明', 1)]
        for text, number in alpha_options: #循环创建
            self.filemenu.alphamenu.add_command(label=text, 
                                                command=lambda num=number: self.attributes('-alpha', num))

        # ----- Filemenu设置 -----
        self.filemenu.add_cascade(label='窗口透明度', menu=self.filemenu.alphamenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='关闭该窗口', foreground='red', command=self.destroy)

        # ----- Moremenu设置 -----
        self.moremenu.add_command(label='❤ 支持该软件 ❤',  background='#fc7aab', 
                                  foreground='#f31c0a', font=('', 15, 'bold'))
        self.moremenu.add_command(label='小提示...', command=lambda: msgbox.showinfo('这个夜景好美啊', '我希望我也能去那里...'))

    def _set_components(self):
        '''
        负责窗口控件的创建。
        '''
        #----- 图片展示部分 -----
        try:
            self.image = self._load_picture(r'assets\image\show.png') #加载图片
            self.picture = tk.Label(self, image=self.image, bg='red')
            self.picture.place(x=-5, y=-5, width=610, height=120) #放置图片
        except Exception as e:
            '''
            即便上面图片因为不可抗力导致无法创建，下面的控件也可以照样用
            即：如果遇极端情况无法创建（与代码无关系的致命错误），
            那么跳过这一步，其他控件要创建
            '''
            pass

        #----- 文字部分 -----
        tk.Label(self, text='版本 1.0', fg='#57628C', 
                 font=('', 20, 'bold')).place(x=40, y=140, width=150, height=45) #展示版本号
        infotext = [('作者：小松果', 195, 100), ('开发时间：2026.1.8', 220, 157),
                    ('说明：本软件及其插画均使用GPL V3协议开源。', 245, 360)] #信息文本：(文本, y，width)]
        for text, y, width in infotext: #循环创建，节省代码开销
            tk.Label(self, text=text, font=('', 10)).place(x=45, y=y, width=width, height=20)

        #----- 按钮部分 -----
        ok_button = tk.Button(self, text='了解了！', bg='green', fg='white', activebackground='#FCB827',
                              activeforeground='white', border=0, relief='flat', font=('', 15, 'bold'),
                              command=self.destroy) #确认按钮
        ok_button.place(x=55, y=280, width=220, height=50)
        support_project_button = tk.Button(self, text='❤ 支持该项目 ❤', bg='#fc7aab', fg='#f31c0a', activebackground='#FCB827',
                              activeforeground='white', border=0, relief='flat', font=('', 15, 'bold')) #支持项目按钮
        support_project_button.place(x=326, y=280, width=220, height=50)  

    def _winfo_geometry(self, x:int, y:int):
        '''
        如果使用该函数，在窗口设置大小的时候，默认居中在窗口中央。
        （Tips：默认设置最小窗口伸展为你输入的数值）
        '''
        screenwidth = (self.winfo_screenwidth() - x)/2
        screenheight = (self.winfo_screenheight() - y)/2
        self.geometry(f'{x}x{y}+{int(screenwidth)}+{int(screenheight)}')
        self.minsize(x, y)

    def _dpi_fix(self:tk.Tk):
        '''
        解决窗口在高DPI下错位问题，针对Windows的狗屎代码的优化
        这个函数特别解决150DPI下错位问题（针对希沃大屏等特殊设备）
        靠，Tkinter的代码真的够老，修复DPI的函数都没有，技术债是吗？
        '''
        pixels = self.winfo_fpixels('72p') / 72.0 #计算像素位置
        if pixels > 1.7 and sys.platform == 'win32':  #如果DPI大于125并且是Windows
            scaling = pixels * 0.8
            #↓在过高DPI下调整缩放
            self.call('tk', 'scaling', scaling)

    def _load_picture(self, path:int) -> ImageTk.PhotoImage:
        '''
        选取指定位置的图片，然后返回能让Tk识别到的Image文本。

        path：图片所在路径。
        '''
        get_image = Image.open(resource_path('GUI\\' + path)) #Debug
        #↓返回tk图片数据
        return ImageTk.PhotoImage(get_image) 
        

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()