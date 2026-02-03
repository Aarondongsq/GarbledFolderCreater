'''
    支持本软件 - 乱码文件夹生成器 模块组件
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
import sys
from os.path import abspath, join, exists

from PIL import Image, ImageTk

#====================全局函数 ====================
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

#==================== 类定义 ====================
class MainWindow(tk.Toplevel):
    def __init__(self, main:tk.Tk):
        '''
        展示“支持本软件”窗口

        __init__函数说明：
        负责窗口的创建工作，其他事归其他函数管，而不是这个函数。
        main：指定被置顶在下的窗口。
        '''
        super().__init__()
        self.title('支持该软件')
        self._winfo_geometry(450, 450)
        self.resizable(0, 0)
        self.attributes('-alpha', 0.8) #初始化窗口

        self.transient(main)
        self.grab_set()
        self.focus_set() #将其变为弹窗

        self._set_components()

    def _set_components(self):
        '''
        负责“支持该软件”窗口的控件摆放
        不过我说个实话，这个控件就放寥寥几个控件而已，居然要开一个函数

        由于放的控件太少了，所以这个函数还负责图片加载
        '''
        get_image = Image.open(resource_path(join('assets','image','support.png')))#获取图片
        self.image = ImageTk.PhotoImage(get_image) #图片转换成可被Tk识别到的类型

        self.show_image = tk.Label(self, image=self.image) #展示图片
        self.show_image.place(x=-10, y=-10, width=470, height=470)

    def _winfo_geometry(self, x:int, y:int):
        '''
        将窗口剧中在中间，同时设定该窗口的大小（包括该窗口的最小值）。

        x：指定窗口长度。
        y：指定窗口宽度。
        '''
        width = (self.winfo_screenwidth() - x) / 2
        height = (self.winfo_screenheight() - y) / 2 #获取屏幕长宽，并决定位置。

        self.geometry(f'{x}x{y}+{int(width)}+{int(height)}')