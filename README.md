# 二维码生成器 | QR Code Generator

一个功能完整的二维码生成工具，支持将网址转换为二维码。扫描生成的二维码后，可以自动跳转到相应的网页或应用程序。

## 功能特点

- ✅ 支持任何URL（网页、应用深链接等）
- ✅ 命令行界面（CLI）和图形界面（GUI）两种模式
- ✅ 批量生成二维码
- ✅ 可自定义二维码大小和容错率
- ✅ 高质量PNG输出
- ✅ 实时预览
- ✅ 打包为独立exe程序，无需Python环境

## 快速开始（使用exe）

直接双击运行：
- `二维码生成器_GUI.exe` - 图形界面版本（推荐）
- `二维码生成器_CLI.exe` - 命令行版本

## 开发环境安装

如果需要从源码运行或修改：

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

**图形界面版本（推荐）：**
```bash
python qr_generator_gui.py
```

**命令行版本：**
```bash
python qr_generator_cli.py
```

## 使用方法

### 图形界面版本

1. 输入网址（或点击快速示例按钮）
2. 自定义文件名、大小和容错率（可选）
3. 点击"生成二维码"按钮
4. 查看预览并保存

功能：
- 实时预览生成的二维码
- 自定义文件名、大小和容错率
- 快速示例按钮
- 另存为功能
- 打开文件夹功能

### 命令行版本

#### 交互模式

```bash
python qr_generator_cli.py
```

然后按照提示选择：
1. 单个网址生成
2. 批量生成（从文件读取）
3. 批量生成（手动输入）

#### 命令行参数模式

```bash
# 基本用法
python qr_generator_cli.py "https://www.example.com"

# 指定文件名
python qr_generator_cli.py "https://www.example.com" "my_qrcode.png"
```

## 支持的URL类型

### 网页链接
```
https://www.baidu.com
https://github.com
https://www.google.com
```

### 应用深链接
```
weixin://          # 打开微信
alipay://          # 打开支付宝
taobao://          # 打开淘宝
```

### 其他
```
mailto:example@email.com    # 发送邮件
tel:+8613800138000         # 拨打电话
sms:+8613800138000         # 发送短信
```

## 输出说明

- 生成的二维码保存在 `qr_codes/` 目录下
- 默认格式为PNG
- 默认使用高容错率（30%），即使部分损坏也能扫描

## 批量生成示例

创建一个 `urls.txt` 文件：
```
https://www.baidu.com
https://www.google.com
https://github.com
```

然后运行命令行版本，选择选项 2，输入 `urls.txt`

## 打包为exe

如果需要重新打包：

### GUI版本
```bash
pyinstaller --onefile --windowed --name "二维码生成器_GUI" --icon=icon.ico qr_generator_gui.py
```

### CLI版本
```bash
pyinstaller --onefile --name "二维码生成器_CLI" --icon=icon.ico qr_generator_cli.py
```

打包后的exe文件在 `dist/` 目录下。

## 技术说明

- 使用 `qrcode` 库生成二维码
- 使用 `Pillow (PIL)` 处理图像
- GUI使用 `tkinter` 构建
- 支持高容错率（最高30%）
- 自动调整二维码版本以适应数据长度
- 使用 `PyInstaller` 打包为独立exe

## 文件结构

```
二维码/
├── qr_generator_gui.py      # GUI版本源码
├── qr_generator_cli.py      # CLI版本源码
├── requirements.txt         # 依赖列表
├── README.md               # 说明文档
├── qr_codes/               # 生成的二维码保存目录
└── dist/                   # 打包后的exe文件
    ├── 二维码生成器_GUI.exe
    └── 二维码生成器_CLI.exe
```

## 常见问题

**Q: 扫描二维码后无法跳转？**
A: 请确保输入的URL格式正确，以 `http://` 或 `https://` 开头。

**Q: 如何生成应用深链接的二维码？**
A: 直接输入应用的URL Scheme，如 `weixin://`、`alipay://` 等。

**Q: 二维码太小扫不出来？**
A: 在设置中增加"大小"参数，推荐使用10-15。

**Q: exe文件太大？**
A: PyInstaller打包会包含Python运行时，这是正常的。如果需要减小体积，可以使用虚拟环境打包。

## 许可证

MIT License

## 作者

Created with ❤️ for easy QR code generation
