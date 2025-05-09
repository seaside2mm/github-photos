import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import threading
import time
import random
import os
from datetime import datetime

class CreateWorkspaceDialog(tk.Toplevel):
    """创建工作目录对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("创建工作目录")
        self.geometry("600x400")
        self.parent = parent
        
        # 视频文件路径
        tk.Label(self, text="视频文件路径:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.video_path = tk.Entry(self, width=50)
        self.video_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_video_path).grid(row=0, column=2, padx=5)
        
        # 配置文件路径
        tk.Label(self, text="配置文件路径:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.config_path = tk.Entry(self, width=50)
        self.config_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_config_path).grid(row=1, column=2, padx=5)
        
        # 工作空间路径
        tk.Label(self, text="工作空间路径:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.workspace_path = tk.Entry(self, width=50)
        self.workspace_path.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_workspace_path).grid(row=2, column=2, padx=5)
        
        # 工作空间名称
        tk.Label(self, text="工作空间名称:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.workspace_name = tk.Entry(self, width=50)
        self.workspace_name.grid(row=3, column=1, padx=5, pady=5)
        self.workspace_name_default = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workspace_name.insert(0, self.workspace_name_default)
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 创建按钮
        create_btn = tk.Button(button_frame, text="创建", command=self.create_workspace)
        create_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 日志区域
        tk.Label(self, text="操作日志:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.NE)
        self.log_text = scrolledtext.ScrolledText(self, width=70, height=10)
        self.log_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        self.log_text.insert(tk.END, "准备创建工作目录...\n")
    
    def browse_video_path(self):
        """浏览视频文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.avi"), ("所有文件", "*.*")])
        if file_path:
            self.video_path.delete(0, tk.END)
            self.video_path.insert(0, file_path)
    
    def browse_config_path(self):
        """浏览配置文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("配置文件", "*.json *.yaml *.xml"), ("所有文件", "*.*")])
        if file_path:
            self.config_path.delete(0, tk.END)
            self.config_path.insert(0, file_path)
    
    def browse_workspace_path(self):
        """浏览工作空间路径"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.workspace_path.delete(0, tk.END)
            self.workspace_path.insert(0, dir_path)
    
    def validate_inputs(self):
        """验证输入是否有效"""
        required_fields = [
            ("视频文件路径", self.video_path.get()),
            ("配置文件路径", self.config_path.get()),
            ("工作空间路径", self.workspace_path.get()),
            ("工作空间名称", self.workspace_name.get())
        ]
        
        for field_name, field_value in required_fields:
            if not field_value:
                messagebox.showerror("错误", f"请填写{field_name}")
                return False
            
            if field_name.endswith("路径") and not os.path.exists(field_value):
                messagebox.showerror("错误", f"{field_name}不存在")
                return False
        
        return True
    
    def create_workspace(self):
        """创建工作目录"""
        if not self.validate_inputs():
            return
        
        # 获取参数
        video_path = self.video_path.get()
        config_path = self.config_path.get()
        workspace_root = self.workspace_path.get()
        workspace_name = self.workspace_name.get()
        
        # 完整工作空间路径
        workspace_path = os.path.join(workspace_root, workspace_name)
        
        # 记录开始处理
        self.log_text.insert(tk.END, f"开始创建工作目录: {workspace_path}\n")
        self.log_text.see(tk.END)
        self.parent.output_area.insert(tk.END, f"开始创建工作目录: {workspace_path}\n")
        self.parent.output_area.see(tk.END)
        
        # 在新线程中执行处理
        threading.Thread(
            target=self.run_workspace_creation,
            args=(video_path, config_path, workspace_path),
            daemon=True
        ).start()
    
    def run_workspace_creation(self, video_path, config_path, workspace_path):
        """执行工作目录创建（模拟）"""
        try:
            # 模拟创建过程
            steps = [
                ("正在创建工作目录结构", 20),
                ("正在复制视频文件", 40),
                ("正在复制配置文件", 60),
                ("正在初始化评价环境", 80),
                ("工作目录创建完成", 100)
            ]
            
            for step_name, progress in steps:
                time.sleep(random.uniform(0.5, 1.5))  # 模拟处理时间
                
                # 更新日志
                self.after(0, lambda n=step_name: self.log_text.insert(tk.END, f"{n}...\n"))
                self.after(0, lambda: self.log_text.see(tk.END))
                self.after(0, lambda n=step_name: self.parent.output_area.insert(tk.END, f"创建工作目录: {n}...\n"))
                self.after(0, lambda: self.parent.output_area.see(tk.END))
            
            # 创建完成
            self.after(0, lambda: messagebox.showinfo("完成", f"工作目录创建成功:\n{workspace_path}"))
        
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"创建工作目录失败:\n{str(e)}"))
            self.after(0, lambda: self.log_text.insert(tk.END, f"错误: {str(e)}\n"))
            self.after(0, lambda: self.log_text.see(tk.END))

class EvaluationDialog(tk.Toplevel):
    """评价对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("视频评价")
        self.geometry("600x450")
        self.parent = parent
        
        # 工作空间路径
        tk.Label(self, text="工作空间路径:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.workspace_path = tk.Entry(self, width=50)
        self.workspace_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_workspace_path).grid(row=0, column=2, padx=5)
        
        # CPP可执行文件路径
        tk.Label(self, text="CPP可执行文件路径:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.cpp_executable = tk.Entry(self, width=50)
        self.cpp_executable.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_cpp_executable).grid(row=1, column=2, padx=5)
        
        # 线程数目
        tk.Label(self, text="同时运行线程数目:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.thread_count = ttk.Combobox(self, width=10, values=[str(i) for i in range(1, 17)])
        self.thread_count.grid(row=2, column=1, sticky=tk.W)
        self.thread_count.set("4")  # 默认4线程
        
        # 评价参数
        tk.Label(self, text="评价参数:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.NE)
        self.params_text = scrolledtext.ScrolledText(self, width=50, height=5)
        self.params_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        self.params_text.insert(tk.END, "--mode=eval\n--precision=high")
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 执行按钮
        execute_btn = tk.Button(button_frame, text="开始评价", command=self.start_evaluation)
        execute_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 进度标签
        self.progress_label = tk.Label(self, text="准备开始评价")
        self.progress_label.grid(row=6, column=0, columnspan=3)
        
        # 日志区域
        tk.Label(self, text="评价日志:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.NE)
        self.log_text = scrolledtext.ScrolledText(self, width=70, height=8)
        self.log_text.grid(row=7, column=1, columnspan=2, padx=5, pady=5)
        self.log_text.insert(tk.END, "等待开始评价...\n")
    
    def browse_workspace_path(self):
        """浏览工作空间路径"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.workspace_path.delete(0, tk.END)
            self.workspace_path.insert(0, dir_path)
    
    def browse_cpp_executable(self):
        """浏览CPP可执行文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")])
        if file_path:
            self.cpp_executable.delete(0, tk.END)
            self.cpp_executable.insert(0, file_path)
    
    def validate_inputs(self):
        """验证输入是否有效"""
        required_fields = [
            ("工作空间路径", self.workspace_path.get()),
            ("CPP可执行文件路径", self.cpp_executable.get())
        ]
        
        for field_name, field_value in required_fields:
            if not field_value:
                messagebox.showerror("错误", f"请填写{field_name}")
                return False
            
            if not os.path.exists(field_value):
                messagebox.showerror("错误", f"{field_name}不存在")
                return False
        
        try:
            thread_count = int(self.thread_count.get())
            if thread_count < 1 or thread_count > 16:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "线程数必须是1-16之间的整数")
            return False
        
        return True
    
    def start_evaluation(self):
        """开始评价"""
        if not self.validate_inputs():
            return
        
        # 获取参数
        workspace_path = self.workspace_path.get()
        cpp_executable = self.cpp_executable.get()
        thread_count = int(self.thread_count.get())
        eval_params = self.params_text.get("1.0", tk.END).strip()
        
        # 记录开始处理
        self.log_text.insert(tk.END, f"开始评价工作空间: {workspace_path}\n")
        self.log_text.insert(tk.END, f"使用线程数: {thread_count}\n")
        self.log_text.insert(tk.END, f"评价参数: {eval_params}\n")
        self.log_text.see(tk.END)
        
        self.parent.output_area.insert(tk.END, f"开始评价: {workspace_path}\n")
        self.parent.output_area.see(tk.END)
        
        # 在新线程中执行处理
        threading.Thread(
            target=self.run_evaluation,
            args=(workspace_path, cpp_executable, thread_count, eval_params),
            daemon=True
        ).start()
    
    def run_evaluation(self, workspace_path, cpp_executable, thread_count, eval_params):
        """执行评价（模拟）"""
        try:
            # 模拟评价过程
            total_steps = 10
            for step in range(1, total_steps + 1):
                progress = int((step / total_steps) * 100)
                time.sleep(random.uniform(0.5, 1.5))  # 模拟处理时间
                
                # 更新进度
                # self.after(0, lambda p=progress: self.progress['value'] = p)
                self.after(0, lambda s=step: self.progress_label.config(
                    text=f"正在处理 ({s}/{total_steps}) - {cpp_executable}"
                ))
                
                # 更新日志
                self.after(0, lambda s=step: self.log_text.insert(
                    tk.END, f"线程 {s % thread_count or thread_count}: 处理第 {s} 项...\n"
                ))
                self.after(0, lambda: self.log_text.see(tk.END))
                self.after(0, lambda s=step: self.parent.output_area.insert(
                    tk.END, f"评价进度: {s}/{total_steps}\n"
                ))
                self.after(0, lambda: self.parent.output_area.see(tk.END))
            
            # 评价完成
            self.after(0, lambda: messagebox.showinfo("完成", "视频评价已完成!"))
        
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"评价失败:\n{str(e)}"))
            self.after(0, lambda: self.log_text.insert(tk.END, f"错误: {str(e)}\n"))
            self.after(0, lambda: self.log_text.see(tk.END))

class ReportGenerationDialog(tk.Toplevel):
    """报告生成对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("生成评价报告")
        self.geometry("600x400")
        self.parent = parent
        
        # 工作空间路径
        tk.Label(self, text="工作空间路径:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.workspace_path = tk.Entry(self, width=50)
        self.workspace_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_workspace_path).grid(row=0, column=2, padx=5)
        
        # 模板文件路径
        tk.Label(self, text="模板文件路径:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.template_path = tk.Entry(self, width=50)
        self.template_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_template_path).grid(row=1, column=2, padx=5)
        
        # 报告输出路径
        tk.Label(self, text="报告输出路径:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.report_path = tk.Entry(self, width=50)
        self.report_path.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览...", command=self.browse_report_path).grid(row=2, column=2, padx=5)
        
        # 报告格式
        tk.Label(self, text="报告格式:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.report_format = ttk.Combobox(self, width=15, values=["PDF", "HTML", "Word", "Markdown"])
        self.report_format.grid(row=3, column=1, sticky=tk.W)
        self.report_format.set("PDF")  # 默认PDF格式
        
        # 按钮框架
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 生成按钮
        generate_btn = tk.Button(button_frame, text="生成报告", command=self.generate_report)
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 日志区域
        tk.Label(self, text="生成日志:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.NE)
        self.log_text = scrolledtext.ScrolledText(self, width=70, height=6)
        self.log_text.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
        self.log_text.insert(tk.END, "准备生成报告...\n")
    
    def browse_workspace_path(self):
        """浏览工作空间路径"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.workspace_path.delete(0, tk.END)
            self.workspace_path.insert(0, dir_path)
    
    def browse_template_path(self):
        """浏览模板文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("模板文件", "*.html *.docx *.md"), ("所有文件", "*.*")])
        if file_path:
            self.template_path.delete(0, tk.END)
            self.template_path.insert(0, file_path)
    
    def browse_report_path(self):
        """浏览报告输出路径"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf"), ("HTML文件", "*.html"), 
                      ("Word文件", "*.docx"), ("Markdown文件", "*.md")])
        if file_path:
            self.report_path.delete(0, tk.END)
            self.report_path.insert(0, file_path)
            # 根据文件扩展名自动设置格式
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".pdf":
                self.report_format.set("PDF")
            elif ext == ".html":
                self.report_format.set("HTML")
            elif ext == ".docx":
                self.report_format.set("Word")
            elif ext == ".md":
                self.report_format.set("Markdown")
    
    def validate_inputs(self):
        """验证输入是否有效"""
        required_fields = [
            ("工作空间路径", self.workspace_path.get()),
            ("模板文件路径", self.template_path.get()),
            ("报告输出路径", self.report_path.get())
        ]
        
        for field_name, field_value in required_fields:
            if not field_value:
                messagebox.showerror("错误", f"请填写{field_name}")
                return False
            
            if field_name != "报告输出路径" and not os.path.exists(field_value):
                messagebox.showerror("错误", f"{field_name}不存在")
                return False
        
        return True
    
    def generate_report(self):
        """生成报告"""
        if not self.validate_inputs():
            return
        
        # 获取参数
        workspace_path = self.workspace_path.get()
        template_path = self.template_path.get()
        report_path = self.report_path.get()
        report_format = self.report_format.get()
        
        # 记录开始处理
        self.log_text.insert(tk.END, f"开始生成报告: {report_path}\n")
        self.log_text.insert(tk.END, f"使用模板: {template_path}\n")
        self.log_text.insert(tk.END, f"格式: {report_format}\n")
        self.log_text.see(tk.END)
        
        self.parent.output_area.insert(tk.END, f"开始生成报告: {report_path}\n")
        self.parent.output_area.see(tk.END)
        
        # 在新线程中执行处理
        threading.Thread(
            target=self.run_report_generation,
            args=(workspace_path, template_path, report_path, report_format),
            daemon=True
        ).start()
    
    def run_report_generation(self, workspace_path, template_path, report_path, report_format):
        """执行报告生成（模拟）"""
        try:
            # 模拟报告生成过程
            steps = [
                ("正在收集评价数据", 20),
                ("正在处理模板", 40),
                ("正在生成图表", 60),
                ("正在格式化内容", 80),
                ("正在导出报告", 95),
                ("报告生成完成", 100)
            ]
            
            for step_name, progress in steps:
                time.sleep(random.uniform(0.5, 1.5))  # 模拟处理时间
                
                # 更新进度
                # self.after(0, lambda p=progress: self.progress['value'] =p)
                
                # 更新日志
                self.after(0, lambda n=step_name: self.log_text.insert(tk.END, f"{n}...\n"))
                self.after(0, lambda: self.log_text.see(tk.END))
                self.after(0, lambda n=step_name: self.parent.output_area.insert(tk.END, f"生成报告: {n}...\n"))
                self.after(0, lambda: self.parent.output_area.see(tk.END))
            
            # 报告生成完成
            self.after(0, lambda: messagebox.showinfo("完成", f"报告已生成:\n{report_path}"))
        
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"报告生成失败:\n{str(e)}"))
            self.after(0, lambda: self.log_text.insert(tk.END, f"错误: {str(e)}\n"))
            self.after(0, lambda: self.log_text.see(tk.END))

class Application(tk.Tk):
    """主应用程序"""
    def __init__(self):
        super().__init__()
        self.title("视频评价系统")
        self.geometry("1000x800")
        
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
        
        # 评价菜单
        evaluation_menu = tk.Menu(menubar, tearoff=0)
        evaluation_menu.add_command(label="工作目录创建", command=self.open_create_workspace)
        evaluation_menu.add_command(label="评价", command=self.open_evaluation)
        evaluation_menu.add_command(label="报告生成", command=self.open_report_generation)
        menubar.add_cascade(label="评价", menu=evaluation_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=lambda: messagebox.showinfo("关于", "视频评价系统 v1.0"))
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
            width=120, 
            height=35,
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
    
    def open_create_workspace(self):
        """打开创建工作目录对话框"""
        CreateWorkspaceDialog(self)
    
    def open_evaluation(self):
        """打开评价对话框"""
        EvaluationDialog(self)
    
    def open_report_generation(self):
        """打开报告生成对话框"""
        ReportGenerationDialog(self)

if __name__ == "__main__":
    app = Application()
    app.mainloop()