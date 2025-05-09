import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import threading
import time
import random

class ServerConnectionDialog(tk.Toplevel):
    """服务器连接对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("远程服务器连接")
        self.geometry("400x250")
        self.parent = parent
        
        # 服务器地址
        tk.Label(self, text="服务器地址:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.server_address = tk.Entry(self, width=30)
        self.server_address.grid(row=0, column=1, padx=5, pady=5)
        
        # 端口
        tk.Label(self, text="端口:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.port = tk.Entry(self, width=30)
        self.port.grid(row=1, column=1, padx=5, pady=5)
        self.port.insert(0, "22")  # 默认SSH端口
        
        # 用户名
        tk.Label(self, text="用户名:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.username = tk.Entry(self, width=30)
        self.username.grid(row=2, column=1, padx=5, pady=5)
        
        # 密码
        tk.Label(self, text="密码:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.password = tk.Entry(self, width=30, show="*")
        self.password.grid(row=3, column=1, padx=5, pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 连接按钮
        connect_btn = tk.Button(button_frame, text="连接", command=self.connect_server)
        connect_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def connect_server(self):
        """连接服务器逻辑"""
        server = self.server_address.get()
        port = self.port.get()
        username = self.username.get()
        password = self.password.get()
        
        if not all([server, port, username, password]):
            messagebox.showerror("错误", "请填写所有字段")
            return
        
        # 这里应该是实际的服务器连接逻辑
        # 示例中只是模拟连接过程
        self.parent.output_area.insert(tk.END, f"尝试连接到服务器: {username}@{server}:{port}\n")
        self.parent.output_area.see(tk.END)
        
        # 模拟连接过程
        threading.Thread(target=self.simulate_connection, args=(server, port, username)).start()
        
    def simulate_connection(self, server, port, username):
        """模拟服务器连接过程"""
        time.sleep(2)  # 模拟连接延迟
        success = random.choice([True, False])  # 随机成功或失败
        
        self.after(0, lambda: self.connection_result(success, server, username))
    
    def connection_result(self, success, server, username):
        if success:
            messagebox.showinfo("成功", f"已成功连接到服务器 {username}@{server}")
            self.parent.output_area.insert(tk.END, "服务器连接成功!\n")
        else:
            messagebox.showerror("失败", "服务器连接失败，请检查参数")
            self.parent.output_area.insert(tk.END, "服务器连接失败!\n")
        
        self.parent.output_area.see(tk.END)
        self.destroy()

class VideoDetectionDialog(tk.Toplevel):
    """视频检测对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("视频检测设置")
        self.geometry("600x400")
        self.parent = parent
        self.tasks = []
        
        # 输入文件夹
        tk.Label(self, text="输入文件夹:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input_dir = tk.Entry(self, width=50)
        self.input_dir.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_input_dir).grid(row=0, column=2, padx=5)
        
        # 输出文件夹
        tk.Label(self, text="输出文件夹:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.output_dir = tk.Entry(self, width=50)
        self.output_dir.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5)
        
        # 模型选择
        tk.Label(self, text="检测模型:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.model_var = tk.StringVar(value="YOLOv5")
        models = ["YOLOv5", "Faster R-CNN", "SSD", "自定义模型"]
        tk.OptionMenu(self, self.model_var, *models).grid(row=2, column=1, sticky=tk.W)
        
        # 任务列表
        tk.Label(self, text="任务列表:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.NE)
        self.task_listbox = tk.Listbox(self, width=60, height=8)
        self.task_listbox.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 添加任务按钮
        add_btn = tk.Button(button_frame, text="添加任务", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=10)
        
        # 开始检测按钮
        start_btn = tk.Button(button_frame, text="开始检测", command=self.start_detection)
        start_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 进度标签
        self.progress_label = tk.Label(self, text="准备就绪")
        self.progress_label.grid(row=6, column=0, columnspan=3)
    
    def browse_input_dir(self):
        """选择输入文件夹"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.input_dir.delete(0, tk.END)
            self.input_dir.insert(0, dir_path)
    
    def browse_output_dir(self):
        """选择输出文件夹"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, dir_path)
    
    def add_task(self):
        """添加检测任务"""
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        model = self.model_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        task_id = len(self.tasks) + 1
        task_info = {
            "id": task_id,
            "input": input_dir,
            "output": output_dir,
            "model": model
        }
        self.tasks.append(task_info)
        
        display_text = f"任务{task_id}: {model}模型 - 输入: {input_dir} -> 输出: {output_dir}"
        self.task_listbox.insert(tk.END, display_text)
        
        self.parent.output_area.insert(tk.END, f"已添加任务: {display_text}\n")
        self.parent.output_area.see(tk.END)
    
    def start_detection(self):
        """开始视频检测"""
        if not self.tasks:
            messagebox.showwarning("警告", "没有可执行的任务")
            return
        
        self.parent.output_area.insert(tk.END, f"开始执行 {len(self.tasks)} 个检测任务...\n")
        self.parent.output_area.see(tk.END)
        
        # 禁用按钮防止重复点击
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)
        
        # 在新线程中执行检测任务
        threading.Thread(target=self.run_detection_tasks, daemon=True).start()
    
    def run_detection_tasks(self):
        """执行检测任务（模拟）"""
        total_tasks = len(self.tasks)
        
        for i, task in enumerate(self.tasks, 1):
            # 更新进度
            progress = int((i / total_tasks) * 100)
            self.after(0, lambda p=progress: self.update_progress(p, f"正在处理任务 {i}/{total_tasks}"))
            
            # 模拟任务执行
            self.parent.output_area.insert(tk.END, f"开始处理任务 {i}: {task['model']}模型\n")
            self.parent.output_area.see(tk.END)
            
            # 模拟处理时间
            time.sleep(random.uniform(2, 5))
            
            # 模拟任务完成
            self.parent.output_area.insert(tk.END, f"任务 {i} 完成!\n")
            self.parent.output_area.see(tk.END)
        
        # 所有任务完成
        self.after(0, lambda: self.update_progress(100, "所有任务已完成!"))
        self.after(0, lambda: messagebox.showinfo("完成", "所有视频检测任务已完成!"))
        
        # 重新启用按钮
        self.after(0, self.enable_buttons)
    
    def update_progress(self, value, text):
        """更新进度条和标签"""
        self.progress['value'] = value
        self.progress_label.config(text=text)
    
    def enable_buttons(self):
        """重新启用所有按钮"""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)

class Application(tk.Tk):
    """主应用程序"""
    def __init__(self):
        super().__init__()
        self.title("视频检测系统")
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
        
        # 其他菜单（示例）
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="设置", command=lambda: print("设置"))
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=lambda: messagebox.showinfo("关于", "视频检测系统 v1.0"))
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

if __name__ == "__main__":
    app = Application()
    app.mainloop()