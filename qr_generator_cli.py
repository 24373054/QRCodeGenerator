#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
二维码生成器 - 命令行版本
QR Code Generator - CLI Version

功能：将网址转换为二维码，扫描后自动跳转到相应网页或应用
Feature: Convert URLs to QR codes that redirect to webpages or apps when scanned
"""

import qrcode
import os
import sys
from datetime import datetime


def generate_qr_code(url, filename=None, save_dir="qr_codes"):
    """
    生成二维码
    
    参数:
        url: 要转换的网址
        filename: 保存的文件名（可选）
        save_dir: 保存目录（默认为 qr_codes）
    
    返回:
        保存的文件路径
    """
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 如果没有指定文件名，使用时间戳
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qrcode_{timestamp}.png"
    
    # 确保文件名以 .png 结尾
    if not filename.endswith('.png'):
        filename += '.png'
    
    # 完整的保存路径
    filepath = os.path.join(save_dir, filename)
    
    # 创建二维码实例
    qr = qrcode.QRCode(
        version=1,  # 控制二维码的大小，1是最小的，40是最大的
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容错率
        box_size=10,  # 每个格子的像素大小
        border=4,  # 边框的格子宽度
    )
    
    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)
    
    # 创建图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存图片
    img.save(filepath)
    
    return filepath


def batch_generate(urls, save_dir="qr_codes"):
    """
    批量生成二维码
    
    参数:
        urls: URL列表或包含URL的文件路径
        save_dir: 保存目录
    
    返回:
        生成的文件路径列表
    """
    filepaths = []
    
    # 如果是文件路径，读取文件内容
    if isinstance(urls, str) and os.path.isfile(urls):
        with open(urls, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    
    # 批量生成
    for i, url in enumerate(urls, 1):
        try:
            filename = f"qrcode_{i}.png"
            filepath = generate_qr_code(url, filename, save_dir)
            filepaths.append(filepath)
            print(f"✓ 已生成: {filepath} -> {url}")
        except Exception as e:
            print(f"✗ 生成失败 ({url}): {str(e)}")
    
    return filepaths


def main():
    """
    主函数 - 命令行交互
    """
    print("="*60)
    print("二维码生成器 | QR Code Generator")
    print("="*60)
    print()
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        url = sys.argv[1]
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        
        try:
            filepath = generate_qr_code(url, filename)
            print(f"✓ 二维码已生成: {filepath}")
            print(f"✓ 网址: {url}")
        except Exception as e:
            print(f"✗ 生成失败: {str(e)}")
            sys.exit(1)
    else:
        # 交互模式
        print("请选择模式:")
        print("1. 单个网址生成")
        print("2. 批量生成（从文件读取）")
        print("3. 批量生成（手动输入）")
        print()
        
        choice = input("请输入选项 (1/2/3): ").strip()
        
        if choice == '1':
            url = input("\n请输入网址: ").strip()
            filename = input("请输入文件名（直接回车使用时间戳）: ").strip()
            filename = filename if filename else None
            
            try:
                filepath = generate_qr_code(url, filename)
                print(f"\n✓ 二维码已生成: {filepath}")
                print(f"✓ 网址: {url}")
            except Exception as e:
                print(f"\n✗ 生成失败: {str(e)}")
        
        elif choice == '2':
            file_path = input("\n请输入包含URL的文件路径: ").strip()
            
            if os.path.isfile(file_path):
                filepaths = batch_generate(file_path)
                print(f"\n✓ 共生成 {len(filepaths)} 个二维码")
            else:
                print(f"\n✗ 文件不存在: {file_path}")
        
        elif choice == '3':
            print("\n请输入网址（每行一个，输入空行结束）:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                filepaths = batch_generate(urls)
                print(f"\n✓ 共生成 {len(filepaths)} 个二维码")
            else:
                print("\n✗ 没有输入任何网址")
        
        else:
            print("\n✗ 无效的选项")
    
    print("\n" + "="*60)
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
