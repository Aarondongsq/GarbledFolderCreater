'''
    LICENSE - 乱码文件夹生成器 模块组件
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
import sys

from module.LString import GPL_V3

class MainWindow(tk.Toplevel):
    def __init__(self, main:tk.Toplevel):
        '''
        这个类向用户展示许可证信息，随主窗口一起使用。

        __init__函数说明：
        这个函数负责初始化窗口，不会负责其他操作（像控件、文本等），不归这个函数管。

        main：填写主窗口名称。
        '''
        super().__init__()
        self.title('乱码文件夹 - 软件许可证')
        self._winfo_geometry(700, 500)
        self.attributes('-alpha', 0.8) #设置窗口基本参数
        
        self.transient(main)
        self.grab_set()
        self.focus_set() #设定这个窗口为一个弹窗

        #↓创建控件
        self._set_components()

    def _set_components(self):
        #----- 控件参数创建 -----
        self.scrollbar = ttk.Scrollbar(self, orient='vertical') #先创建滚动条
        self.scrollbar.pack(side='right', fill='y')
        self.license_text = tk.Text(self, font=('', 10), wrap='none') #再然后才是许可证创建
        self.license_text.pack(side='top', fill='both', expand=True)
        
        #----- 控件参数调整 -----
        self.license_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.license_text.yview) #确定滚动条滑动命令

        #----- 加入内容 -----
        self.license_text.insert('1.0', GPL_V3) #注入许可证内容
        self.license_text.config(state='disabled')

    def _winfo_geometry(self, x:int, y:int):
        '''
        如果使用该函数，在窗口设置大小的时候，默认居中在窗口中央。
        （Tips：默认设置最小窗口伸展为你输入的数值）
        '''
        screenwidth = (self.winfo_screenwidth() - x)/2
        screenheight = (self.winfo_screenheight() - y)/2 #获取屏幕长度，计算应在位置

        self.geometry(f'{x}x{y}+{int(screenwidth)}+{int(screenheight)}') #确定位置和长宽，确定最小值
        self.minsize(x, y)
