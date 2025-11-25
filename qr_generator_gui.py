#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
二维码生成器 - 图形界面增强版
QR Code Generator - Enhanced GUI Version

功能：支持网址、邮件、电话、短信等多种类型的二维码生成
Features: Support URL, Email, Phone, SMS and other QR code types
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import qrcode
from PIL import Image, ImageTk
import os
from datetime import datetime
from urllib.parse import quote


class QRCodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("二维码生成器 增强版 | QR Code Generator Pro")
        self.root.geometry("800x850")
        self.root.resizable(True, True)  # 允许调整窗口大小
        self.root.minsize(700, 700)  # 设置最小窗口尺寸
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 当前生成的二维码路径
        self.current_qr_path = None
        self.current_url = None
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        style.configure('Title.TLabel', font=('Microsoft YaHei UI', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Microsoft YaHei UI', 10), foreground='#7f8c8d')
        style.configure('TButton', font=('Microsoft YaHei UI', 10), padding=10)
        style.configure('Generate.TButton', font=('Microsoft YaHei UI', 12, 'bold'), padding=15)
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建Canvas和滚动条
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # 创建可滚动的Frame
        scrollable_frame = ttk.Frame(canvas, padding="20")
        
        # 绑定配置事件
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # 创建窗口并使其宽度自适应
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # 当Canvas大小改变时，调整内部Frame的宽度
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 鼠标滚轮支持
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 布局Canvas和滚动条
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 主容器（现在在scrollable_frame中）
        main_frame = scrollable_frame
        
        # 标题
        title_label = ttk.Label(main_frame, text="二维码生成器 增强版", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="支持网址、邮件、电话、短信等多种类型", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 15))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 创建各个选项卡
        self.create_url_tab()
        self.create_email_tab()
        self.create_phone_tab()
        self.create_sms_tab()
        self.create_other_tab()
        
        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="二维码设置", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 文件名
        filename_frame = ttk.Frame(settings_frame)
        filename_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filename_frame, text="文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.filename_entry = ttk.Entry(filename_frame, font=('Microsoft YaHei UI', 10))
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.filename_entry.insert(0, f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # 大小和容错率
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X)
        
        ttk.Label(options_frame, text="大小:").pack(side=tk.LEFT, padx=(0, 5))
        self.size_var = tk.StringVar(value="10")
        size_combo = ttk.Combobox(options_frame, textvariable=self.size_var, 
                                 values=["5", "10", "15", "20"], width=8, state='readonly')
        size_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(options_frame, text="容错率:").pack(side=tk.LEFT, padx=(0, 5))
        self.error_correction_var = tk.StringVar(value="H")
        error_combo = ttk.Combobox(options_frame, textvariable=self.error_correction_var,
                                   values=["L (7%)", "M (15%)", "Q (25%)", "H (30%)"], 
                                   width=12, state='readonly')
        error_combo.current(3)
        error_combo.pack(side=tk.LEFT)
        
        # 生成按钮
        generate_btn = ttk.Button(main_frame, text="生成二维码", 
                                 style='Generate.TButton',
                                 command=self.generate_qr_code)
        generate_btn.pack(fill=tk.X, pady=(0, 15))
        
        # 预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="二维码预览", padding="15")
        preview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 使用tk.Label而不是ttk.Label，因为需要height参数
        self.preview_label = tk.Label(preview_frame, text="二维码将在这里显示", 
                                      background='#ecf0f1', relief=tk.SUNKEN, 
                                      width=40, height=15,
                                      font=('Microsoft YaHei UI', 10))
        self.preview_label.pack(pady=5)
        
        # 显示当前URL
        self.url_display = ttk.Label(preview_frame, text="", foreground='#3498db', 
                                    font=('Microsoft YaHei UI', 9), wraplength=700)
        self.url_display.pack(pady=(5, 0))
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.save_btn = ttk.Button(button_frame, text="另存为", 
                                   command=self.save_as, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        self.open_folder_btn = ttk.Button(button_frame, text="打开文件夹", 
                                         command=self.open_folder, state=tk.DISABLED)
        self.open_folder_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_url_tab(self):
        """创建网址选项卡"""
        url_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(url_tab, text="🌐 网址")
        
        ttk.Label(url_tab, text="请输入网址 (URL):", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(url_tab, font=('Microsoft YaHei UI', 11))
        self.url_entry.pack(fill=tk.X, pady=(0, 15))
        self.url_entry.insert(0, "https://")
        
        # 快速示例
        ttk.Label(url_tab, text="快速示例:", font=('Microsoft YaHei UI', 9)).pack(anchor=tk.W, pady=(0, 5))
        
        examples_frame = ttk.Frame(url_tab)
        examples_frame.pack(fill=tk.X)
        
        examples = [
            ("GitHub", "https://github.com"),
            ("百度", "https://www.baidu.com"),
            ("Google", "https://www.google.com"),
            ("微信", "weixin://"),
            ("支付宝", "alipay://"),
        ]
        
        for i, (name, url) in enumerate(examples):
            btn = ttk.Button(examples_frame, text=name, 
                           command=lambda u=url: self.set_url(u))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='ew')
        
        for i in range(3):
            examples_frame.columnconfigure(i, weight=1)
    
    def create_email_tab(self):
        """创建邮件选项卡"""
        email_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(email_tab, text="📧 邮件")
        
        # 收件人
        ttk.Label(email_tab, text="收件人 (To):", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.email_to = ttk.Entry(email_tab, font=('Microsoft YaHei UI', 11))
        self.email_to.pack(fill=tk.X, pady=(0, 15))
        self.email_to.insert(0, "example@email.com")
        
        # 抄送
        ttk.Label(email_tab, text="抄送 (CC) - 可选:", font=('Microsoft YaHei UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.email_cc = ttk.Entry(email_tab, font=('Microsoft YaHei UI', 10))
        self.email_cc.pack(fill=tk.X, pady=(0, 15))
        
        # 主题
        ttk.Label(email_tab, text="主题 (Subject):", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.email_subject = ttk.Entry(email_tab, font=('Microsoft YaHei UI', 11))
        self.email_subject.pack(fill=tk.X, pady=(0, 15))
        self.email_subject.insert(0, "")
        
        # 正文
        ttk.Label(email_tab, text="正文 (Body) - 可选:", font=('Microsoft YaHei UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.email_body = scrolledtext.ScrolledText(email_tab, font=('Microsoft YaHei UI', 10), height=6)
        self.email_body.pack(fill=tk.BOTH, expand=True)
        
        # 提示
        ttk.Label(email_tab, text="💡 扫描后将打开邮件应用，收件人和内容已自动填写", 
                 foreground='#7f8c8d', font=('Microsoft YaHei UI', 9)).pack(pady=(10, 0))
    
    def create_phone_tab(self):
        """创建电话选项卡"""
        phone_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(phone_tab, text="📞 电话")
        
        ttk.Label(phone_tab, text="请输入电话号码:", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.phone_number = ttk.Entry(phone_tab, font=('Microsoft YaHei UI', 14))
        self.phone_number.pack(fill=tk.X, pady=(0, 15))
        self.phone_number.insert(0, "+86")
        
        # 说明
        info_frame = ttk.LabelFrame(phone_tab, text="使用说明", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        info_text = """
📱 电话号码格式：
  • 国内号码：+86 13800138000 或 13800138000
  • 国际号码：+1 234-567-8900
  • 固定电话：010-12345678

✨ 扫描后效果：
  • 手机会自动打开拨号界面
  • 号码已自动填入，点击拨打即可

💡 应用场景：
  • 名片二维码
  • 客服热线
  • 紧急联系方式
        """
        
        ttk.Label(info_frame, text=info_text, font=('Microsoft YaHei UI', 9), 
                 foreground='#2c3e50', justify=tk.LEFT).pack(anchor=tk.W)
        
        # 快速示例
        example_frame = ttk.Frame(phone_tab)
        example_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(example_frame, text="快速示例:", font=('Microsoft YaHei UI', 9)).pack(side=tk.LEFT, padx=(0, 10))
        
        phone_examples = [
            ("客服热线", "10086"),
            ("示例号码", "+8613800138000"),
        ]
        
        for name, number in phone_examples:
            btn = ttk.Button(example_frame, text=name, 
                           command=lambda n=number: self.set_phone(n))
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_sms_tab(self):
        """创建短信选项卡"""
        sms_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(sms_tab, text="💬 短信")
        
        # 收件人
        ttk.Label(sms_tab, text="收件人号码:", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.sms_number = ttk.Entry(sms_tab, font=('Microsoft YaHei UI', 11))
        self.sms_number.pack(fill=tk.X, pady=(0, 15))
        self.sms_number.insert(0, "+86")
        
        # 短信内容
        ttk.Label(sms_tab, text="短信内容 (可选):", font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.sms_body = scrolledtext.ScrolledText(sms_tab, font=('Microsoft YaHei UI', 10), height=8)
        self.sms_body.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 说明
        info_text = "💡 扫描后将打开短信应用，收件人和内容已自动填写，点击发送即可"
        ttk.Label(sms_tab, text=info_text, foreground='#7f8c8d', 
                 font=('Microsoft YaHei UI', 9), wraplength=700).pack()
        
        # 应用场景
        scenario_frame = ttk.LabelFrame(sms_tab, text="应用场景", padding="10")
        scenario_frame.pack(fill=tk.X, pady=(10, 0))
        
        scenarios = "• 活动报名（扫码发送指定内容到号码）\n• 验证码获取\n• 快速反馈"
        ttk.Label(scenario_frame, text=scenarios, font=('Microsoft YaHei UI', 9), 
                 foreground='#2c3e50', justify=tk.LEFT).pack(anchor=tk.W)
    
    def create_other_tab(self):
        """创建其他类型选项卡"""
        other_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(other_tab, text="⚡ 其他")
        
        ttk.Label(other_tab, text="其他类型的二维码", font=('Microsoft YaHei UI', 12, 'bold')).pack(pady=(0, 15))
        
        # WiFi
        wifi_frame = ttk.LabelFrame(other_tab, text="📶 WiFi 连接", padding="10")
        wifi_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(wifi_frame, text="网络名称 (SSID):").pack(anchor=tk.W, pady=(0, 5))
        self.wifi_ssid = ttk.Entry(wifi_frame, font=('Microsoft YaHei UI', 10))
        self.wifi_ssid.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(wifi_frame, text="密码:").pack(anchor=tk.W, pady=(0, 5))
        self.wifi_password = ttk.Entry(wifi_frame, font=('Microsoft YaHei UI', 10), show="*")
        self.wifi_password.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(wifi_frame, text="加密类型:").pack(anchor=tk.W, pady=(0, 5))
        self.wifi_encryption = ttk.Combobox(wifi_frame, values=["WPA/WPA2", "WEP", "无"], state='readonly')
        self.wifi_encryption.current(0)
        self.wifi_encryption.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(wifi_frame, text="生成 WiFi 二维码", 
                  command=self.generate_wifi_qr).pack(fill=tk.X, pady=(10, 0))
        
        # 地理位置
        geo_frame = ttk.LabelFrame(other_tab, text="📍 地理位置", padding="10")
        geo_frame.pack(fill=tk.X, pady=(10, 0))
        
        coord_frame = ttk.Frame(geo_frame)
        coord_frame.pack(fill=tk.X)
        
        ttk.Label(coord_frame, text="纬度:").pack(side=tk.LEFT, padx=(0, 5))
        self.geo_lat = ttk.Entry(coord_frame, font=('Microsoft YaHei UI', 10), width=15)
        self.geo_lat.pack(side=tk.LEFT, padx=(0, 20))
        self.geo_lat.insert(0, "39.9042")
        
        ttk.Label(coord_frame, text="经度:").pack(side=tk.LEFT, padx=(0, 5))
        self.geo_lng = ttk.Entry(coord_frame, font=('Microsoft YaHei UI', 10), width=15)
        self.geo_lng.pack(side=tk.LEFT)
        self.geo_lng.insert(0, "116.4074")
        
        ttk.Button(geo_frame, text="生成位置二维码", 
                  command=self.generate_geo_qr).pack(fill=tk.X, pady=(10, 0))
    
    def set_url(self, url):
        """设置URL"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
    
    def set_phone(self, number):
        """设置电话号码"""
        self.phone_number.delete(0, tk.END)
        self.phone_number.insert(0, number)
    
    def build_url_from_tab(self):
        """根据当前选项卡构建URL"""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # 网址
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning("警告", "请输入网址！")
                return None
            return url
        
        elif current_tab == 1:  # 邮件
            to = self.email_to.get().strip()
            if not to:
                messagebox.showwarning("警告", "请输入收件人邮箱！")
                return None
            
            cc = self.email_cc.get().strip()
            subject = self.email_subject.get().strip()
            body = self.email_body.get("1.0", tk.END).strip()
            
            # 构建 mailto URL
            url = f"mailto:{to}"
            params = []
            
            if cc:
                params.append(f"cc={quote(cc)}")
            if subject:
                params.append(f"subject={quote(subject)}")
            if body:
                params.append(f"body={quote(body)}")
            
            if params:
                url += "?" + "&".join(params)
            
            return url
        
        elif current_tab == 2:  # 电话
            number = self.phone_number.get().strip()
            if not number:
                messagebox.showwarning("警告", "请输入电话号码！")
                return None
            return f"tel:{number}"
        
        elif current_tab == 3:  # 短信
            number = self.sms_number.get().strip()
            if not number:
                messagebox.showwarning("警告", "请输入收件人号码！")
                return None
            
            body = self.sms_body.get("1.0", tk.END).strip()
            
            if body:
                return f"sms:{number}?body={quote(body)}"
            else:
                return f"sms:{number}"
        
        else:
            messagebox.showwarning("警告", "请使用对应选项卡的生成按钮！")
            return None
    
    def generate_wifi_qr(self):
        """生成WiFi二维码"""
        ssid = self.wifi_ssid.get().strip()
        password = self.wifi_password.get().strip()
        
        if not ssid:
            messagebox.showwarning("警告", "请输入WiFi名称！")
            return
        
        encryption_map = {
            "WPA/WPA2": "WPA",
            "WEP": "WEP",
            "无": "nopass"
        }
        
        encryption = encryption_map[self.wifi_encryption.get()]
        
        # WiFi 二维码格式
        if encryption == "nopass":
            wifi_string = f"WIFI:T:nopass;S:{ssid};;"
        else:
            wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        
        self.current_url = wifi_string
        self._generate_qr_from_string(wifi_string)
    
    def generate_geo_qr(self):
        """生成地理位置二维码"""
        lat = self.geo_lat.get().strip()
        lng = self.geo_lng.get().strip()
        
        if not lat or not lng:
            messagebox.showwarning("警告", "请输入经纬度！")
            return
        
        try:
            float(lat)
            float(lng)
        except ValueError:
            messagebox.showerror("错误", "经纬度必须是数字！")
            return
        
        geo_string = f"geo:{lat},{lng}"
        self.current_url = geo_string
        self._generate_qr_from_string(geo_string)
    
    def generate_qr_code(self):
        """生成二维码"""
        url = self.build_url_from_tab()
        
        if url:
            self.current_url = url
            self._generate_qr_from_string(url)
    
    def _generate_qr_from_string(self, data):
        """从字符串生成二维码"""
        try:
            # 获取设置
            box_size = int(self.size_var.get())
            error_correction_map = {
                "L (7%)": qrcode.constants.ERROR_CORRECT_L,
                "M (15%)": qrcode.constants.ERROR_CORRECT_M,
                "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
                "H (30%)": qrcode.constants.ERROR_CORRECT_H,
            }
            error_correction = error_correction_map[self.error_correction_var.get()]
            
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction,
                box_size=box_size,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 保存文件
            save_dir = "qr_codes"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            filename = self.filename_entry.get().strip()
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(save_dir, filename)
            img.save(filepath)
            
            self.current_qr_path = filepath
            
            # 显示预览
            self.show_preview(img)
            
            # 显示URL
            self.url_display.config(text=f"内容: {data}")
            
            # 启用按钮
            self.save_btn.config(state=tk.NORMAL)
            self.open_folder_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("成功", f"二维码已生成！\n保存位置: {filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")
    
    def show_preview(self, img):
        """显示预览"""
        # 调整图片大小以适应预览区域
        img_copy = img.copy()
        img_copy.thumbnail((280, 280), Image.Resampling.LANCZOS)
        
        # 转换为 PhotoImage
        photo = ImageTk.PhotoImage(img_copy)
        
        # 更新标签
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo  # 保持引用
    
    def save_as(self):
        """另存为"""
        if not self.current_qr_path:
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("所有文件", "*.*")]
        )
        
        if filepath:
            try:
                img = Image.open(self.current_qr_path)
                img.save(filepath)
                messagebox.showinfo("成功", f"已保存到: {filepath}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def open_folder(self):
        """打开文件夹"""
        if self.current_qr_path:
            folder = os.path.dirname(os.path.abspath(self.current_qr_path))
            os.startfile(folder)


def main():
    root = tk.Tk()
    app = QRCodeGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
