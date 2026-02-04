'''
    彩蛋 - 乱码文件夹生成器 模块组件
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
import sys
from os.path import join, exists, abspath #Python自带模块

from module.EasterString import TEXT

from PIL import Image, ImageTk #第三方模块

#==================== 全局变量====================
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
    if exists(join(base_path, relative_path)): #确实是否在VS调试环境下
        return join(base_path, relative_path) 
    else:
        return join(base_path, 'GUI', relative_path)

def winfo_geometry(master:tk.Toplevel, x:int, y:int):
    '''
    设定窗口在中央，但是使用前请先填写长宽。
    在设定好窗口位置和长宽后的同时，也会确定窗口的最小大小。
    这玩意，我都是坚持直打，而不是《面向CV编程》，所以注释有时候会不同很正常

    master：指定窗口。
    x：窗口的长度。
    y：窗口的宽度。
    '''
    width = (master.winfo_screenwidth() - x) / 2
    height = (master.winfo_screenheight() - y) / 2 #获取窗口剧中所需要在的位置
    master.geometry(f'{x}x{y}+{int(width)}+{int(height)}') #设置长宽和位置
    #确定窗口最小值↓
    master.minsize(x, y)

#==================== 类定义 ====================
class MainWindow(tk.Toplevel):
    def __init__(self, main):
        r'''
        \(@^0^@)/ 生成一个有趣的彩蛋窗口！
        包含了很多有趣的东西，看下有没有你熟悉的片段～
        本来想弄鸡你太美的，但是人家爱发绿尸寒的，那就搞不了了
        不过，有趣的东西，当然是越多越好，搞不了鸡你太美，那就搞别的

        __init__函数说明：
        建立一个有趣的窗口，但是仅初始化，因此你可以看到这一块代码就是初始化占大头
        main：需要被置顶的窗口。
        '''
        super().__init__()
        self.title('点开看看里面是什么？')
        winfo_geometry(self, 700, 450)
        self.resizable(0, 0)
        self.attributes('-alpha', 0.95) #初始化窗口配置
        self._set_icon(resource_path(join('assets', 'icon', 'egg.ico')))

        self.transient(main)
        self.grab_set()
        self.focus_set() #将窗口变成弹窗

        self._set_components() #放置控件

    def _set_components(self):
        '''
        给最有趣的窗口添加有意思的控件（不然窗口就没意思了）
        图片的加载是归其他函数管，跟我有何关系？
        '''
        #----- 彩条创建 -----
        background_options = [(0, 0.12), (0.24, 0.36), (0.48, 0.6), (0.72, 0.84), (0.96, 1)] #放置彩条：（粉彩条y轴,蓝彩条t轴）
        for pink_y, blue_y in background_options: #循环放置彩条（上粉色，下蓝色）
            tk.Label(self, bg='#FB46AE').place(rely=pink_y, relwidth=1.01, relheight=0.12)
            tk.Label(self, bg='#45C0FC').place(rely=blue_y, relwidth=1.01, relheight=0.12)

        #----- 按钮创建 -----
        self.image = self._load_picture(
            resource_path(join('assets', 'image', 'button.png')), (72, 72)) #获取图片内容

        self.whatinside_1 = tk.Button(self, border=0, relief='flat', 
                                      image=self.image, activebackground='#FFBF00', 
                                      command=lambda: self.click_button_(0))
        self.whatinside_1.place(x=60, y=140, width=150, height=150) #神秘内容按钮1
        self.whatinside_2 = tk.Button(self, border=0, relief='flat', 
                                      image=self.image, activebackground='#FFBF00', 
                                      command=lambda: self.click_button_(1))
        self.whatinside_2.place(x=270, y=140, width=150, height=150) #神秘内容按钮2
        #↓神秘内容按钮3
        self.whatinside_3 = tk.Button(self, border=0, relief='flat', 
                                      image=self.image, activebackground='#FFBF00', 
                                      command=lambda: self.click_button_(2))
        self.whatinside_3.place(x=485, y=140, width=150, height=150) 

    def click_button_(self, wordtype:int):
        '''
        点击按钮时，出现的小剧场文本。

        type：选择的小剧场文本类型。
        '''
        msgbox.showinfo(TEXT[wordtype][0], TEXT[wordtype][1], parent=self) #展示有意思的东西

    def _load_picture(self, path:str, resize:tuple=(0,0)) -> ImageTk.PhotoImage:
        '''
        加载图片内容，并返回可供Tkinter阅读的图片内容。

        path：指定图片路径。
        resize：缩放图片大小，默认为(0, 0)
        '''
        image_data = Image.open(path)
        image_data.resize(resize) #获取，缩放图片

        #↓加工并返回可供Tkinter阅读的图片
        return ImageTk.PhotoImage(image_data)

    def _set_icon(self, icon:str):
        '''
        设定软件窗口栏图标。
        如果遇到极端情况，导致图标无法放置，那么将跳过这一步。

        icon：图标位置。
        '''
        try:
            self.iconbitmap(icon)
        except: #若是遇到极端情况，将不会创建图标
            pass