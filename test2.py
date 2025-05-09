import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import threading
import time
import random
import os

class UndistortDialog(tk.Toplevel):
    """Undistort处理对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("视频去畸变处理")
        self.geometry("700x500")
        self.parent = parent
        
        # 输入MP4文件
        tk.Label(self, text="输入MP4文件:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input_mp4 = tk.Entry(self, width=50)
        self.input_mp4.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_input_mp4).grid(row=0, column=2, padx=5)
        
        # 中间图片输出路径
        tk.Label(self, text="中间图片输出路径:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.intermediate_path = tk.Entry(self, width=50)
        self.intermediate_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_intermediate_path).grid(row=1, column=2, padx=5)
        
        # 转换后视频输出路径
        tk.Label(self, text="转换后视频输出路径:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.output_video = tk.Entry(self, width=50)
        self.output_video.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_output_video).grid(row=2, column=2, padx=5)
        
        # CPP可执行文件路径
        tk.Label(self, text="CPP可执行文件路径:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cpp_executable = tk.Entry(self, width=50)
        self.cpp_executable.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_cpp_executable).grid(row=3, column=2, padx=5)
        
        # 转换角度
        tk.Label(self, text="转换角度:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.angle_var = tk.StringVar(value="0")
        angles = ["0", "90", "180", "270"]
        tk.OptionMenu(self, self.angle_var, *angles).grid(row=4, column=1, sticky=tk.W)
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 执行按钮
        execute_btn = tk.Button(button_frame, text="执行", command=self.execute_undistort)
        execute_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, pady=10)
        
        # 进度标签
        self.progress_label = tk.Label(self, text="准备就绪")
        self.progress_label.grid(row=7, column=0, columnspan=3)
        
        # 日志区域
        tk.Label(self, text="处理日志:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.NE)
        self.log_text = scrolledtext.ScrolledText(self, width=80, height=8)
        self.log_text.grid(row=8, column=1, columnspan=2, padx=5, pady=5)
        self.log_text.insert(tk.END, "等待开始处理...\n")
    
    def browse_input_mp4(self):
        """选择输入MP4文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("MP4视频文件", "*.mp4"), ("所有文件", "*.*")])
        if file_path:
            self.input_mp4.delete(0, tk.END)
            self.input_mp4.insert(0, file_path)
    
    def browse_intermediate_path(self):
        """选择中间图片输出路径"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.intermediate_path.delete(0, tk.END)
            self.intermediate_path.insert(0, dir_path)
    
    def browse_output_video(self):
        """选择转换后视频输出路径"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4视频文件", "*.mp4"), ("所有文件", "*.*")])
        if file_path:
            self.output_video.delete(0, tk.END)
            self.output_video.insert(0, file_path)
    
    def browse_cpp_executable(self):
        """选择CPP可执行文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")])
        if file_path:
            self.cpp_executable.delete(0, tk.END)
            self.cpp_executable.insert(0, file_path)
    
    def validate_inputs(self):
        """验证输入是否有效"""
        required_fields = [
            ("输入MP4文件", self.input_mp4.get()),
            ("中间图片输出路径", self.intermediate_path.get()),
            ("转换后视频输出路径", self.output_video.get()),
            ("CPP可执行文件路径", self.cpp_executable.get())
        ]
        
        for field_name, field_value in required_fields:
            if not field_value:
                messagebox.showerror("错误", f"请填写{field_name}")
                return False
            
            if field_name.endswith("路径") and not os.path.exists(field_value):
                messagebox.showerror("错误", f"{field_name}不存在")
                return False
        
        return True
    
    def execute_undistort(self):
        """执行去畸变处理"""
        if not self.validate_inputs():
            return
        
        # 禁用按钮防止重复点击
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)
        
        # 获取参数
        params = {
            "input_mp4": self.input_mp4.get(),
            "intermediate_path": self.intermediate_path.get(),
            "output_video": self.output_video.get(),
            "cpp_executable": self.cpp_executable.get(),
            "angle": self.angle_var.get()
        }
        
        # 记录开始处理
        self.log_text.insert(tk.END, f"开始处理: {params['input_mp4']}\n")
        self.log_text.see(tk.END)
        self.parent.output_area.insert(tk.END, f"开始Undistort处理: {params['input_mp4']}\n")
        self.parent.output_area.see(tk.END)
        
        # 在新线程中执行处理
        threading.Thread(
            target=self.run_undistort_process,
            args=(params,),
            daemon=True
        ).start()
    
    def run_undistort_process(self, params):
        """执行去畸变处理（模拟）"""
        steps = [
            ("正在提取视频帧", 20),
            ("正在运行去畸变算法", 40),
            ("正在处理角度旋转", 60),
            ("正在重新编码视频", 80),
            ("正在清理临时文件", 95),
            ("处理完成", 100)
        ]
        
        for step_name, progress in steps:
            time.sleep(random.uniform(1, 3))  # 模拟处理时间
            
            # 更新UI
            self.after(0, lambda n=step_name, p=progress: self.update_progress(n, p))
            
            # 记录日志
            self.after(0, lambda n=step_name: self.log_text.insert(tk.END, f"{n}...\n"))
            self.after(0, lambda: self.log_text.see(tk.END))
            self.after(0, lambda n=step_name: self.parent.output_area.insert(tk.END, f"Undistort: {n}...\n"))
            self.after(0, lambda: self.parent.output_area.see(tk.END))
        
        # 处理完成
        self.after(0, lambda: messagebox.showinfo("完成", "视频去畸变处理已完成!"))
        self.after(0, self.enable_buttons)
    
    def update_progress(self, step_name, progress):
        """更新进度条和标签"""
        self.progress['value'] = progress
        self.progress_label.config(text=step_name)
    
    def enable_buttons(self):
        """重新启用所有按钮"""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)

class Application(tk.Tk):
    """主应用程序"""
    def __init__(self):
        super().__init__()
        self.title("视频处理系统")
        self.geometry("900x700")
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建输出区域
        self.create_output_area()
        
        # 状态栏
        self.create_status_bar()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self)
        
        # 功能1菜单
        func1_menu = tk.Menu(menubar, tearoff=0)
        func1_menu.add_command(label="远程服务器连接", command=self.open_server_connection)
        func1_menu.add_command(label="视频检测", command=self.open_video_detection)
        menubar.add_cascade(label="功能1", menu=func1_menu)
        
        # 预处理菜单
        preprocess_menu = tk.Menu(menubar, tearoff=0)
        preprocess_menu.add_command(label="Undistort", command=self.open_undistort)
        menubar.add_cascade(label="预处理", menu=preprocess_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=lambda: messagebox.showinfo("关于", "视频处理系统 v1.0"))
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.config(menu=menubar)
    
    def create_output_area(self):
        """创建输出区域"""
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 输出标签
        label = tk.Label(frame, text="系统输出:")
        label.pack(anchor=tk.NW)
        
        # 滚动文本框
        self.output_area = scrolledtext.ScrolledText(
            frame, 
            wrap=tk.WORD, 
            width=100, 
            height=30,
            font=('Arial', 10)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # 示例文本
        self.output_area.insert(tk.INSERT, "系统已启动，等待操作...\n")
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_server_connection(self):
        """打开服务器连接对话框"""
        ServerConnectionDialog(self)
    
    def open_video_detection(self):
        """打开视频检测对话框"""
        VideoDetectionDialog(self)
    
    def open_undistort(self):
        """打开Undistort对话框"""
        UndistortDialog(self)

if __name__ == "__main__":
    app = Application()
    app.mainloop()