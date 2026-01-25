import tkinter as tk
import tkinter.ttk as ttk

class MainWindow(tk.Toplevel):
    def __init__(self, main='Debug'):
        '''
        这个类向用户展示许可证信息，随主窗口一起使用。

        __init__函数说明：
        这个函数负责初始化窗口，不会负责其他操作（像控件、文本等），不归这个函数管。
        '''
        super().__init__()
        self.title('软件许可证')
        self._winfo_geometry(700, 500)
        self._dpi_fix()
        self.attributes('-alpha', 0.8) #设置窗口基本参数
        
        #self.transient(main)
        #self.grab_set()
        #self.focus_set() #设置弹窗（Debug：暂时禁用）

        self._set_components()

    def _set_components(self):
        pass

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
        解决窗口在高DPI下错位问题
        这个函数特别解决150DPI下错位问题（针对希沃大屏等特殊设备）
        靠，Tkinter的代码真的够老，修复DPI的函数都没有，技术债是吗？
        '''
        pixels = self.winfo_fpixels('72p') / 72.0 #计算像素位置
        if pixels > 1.7: #如果DPI大于125
            scaling = pixels * 0.8
            self.call('tk', 'scaling', scaling) #在过高DPI下调整缩放

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()