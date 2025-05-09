#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

def main():
    # 源PDF文件和输出目录
    source_pdf = "source/EN-CNt2.pdf"
    output_dir = "source/EN-CNt2-pages"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 使用系统命令获取页数
    try:
        result = subprocess.run(
            ["mdls", source_pdf], 
            capture_output=True, 
            text=True, 
            check=True
        )
        for line in result.stdout.splitlines():
            if "kMDItemNumberOfPages" in line:
                page_count = int(line.split("=")[1].strip())
                break
        else:
            print("无法确定PDF页数")
            return
    except Exception as e:
        print(f"获取页数时出错: {e}")
        return
    
    print(f"PDF页数: {page_count}")
    
    # 使用系统命令拆分PDF
    for i in range(1, page_count + 1):
        output_file = f"{output_dir}/page-{i}.pdf"
        
        # 使用系统默认的PDF查看器（预览应用）进行打印到PDF操作
        # 使用macOS的系统命令（需要用户交互，所以改用其他方法）
        
        # 使用pdftocairo命令拆分PDF（如果存在）
        try:
            # 尝试使用pdftocairo（如果安装了poppler工具)
            subprocess.run(
                ["pdftocairo", "-pdf", "-f", str(i), "-l", str(i), source_pdf, output_file.replace(".pdf", "")],
                check=True
            )
            print(f"已提取页面 {i} 到 {output_file}")
            continue
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # 尝试使用gs（Ghostscript）如果安装了
        try:
            subprocess.run([
                "gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-dSAFER",
                f"-dFirstPage={i}", f"-dLastPage={i}",
                f"-sOutputFile={output_file}", source_pdf
            ], check=True, stderr=subprocess.PIPE)
            print(f"已提取页面 {i} 到 {output_file}")
            continue
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # 如果都失败了，使用系统命令
        try:
            print(f"尝试使用系统命令拆分页面 {i}...")
            # 使用印象笔记的命令行工具（如果安装了）
            subprocess.run([
                "textutil", "-convert", "txt", "-output", f"{output_dir}/page-{i}.txt",
                source_pdf
            ], check=True)
            print(f"已提取页面 {i} 内容到文本文件 {output_dir}/page-{i}.txt")
        except (subprocess.SubprocessError, FileNotFoundError):
            print(f"无法提取页面 {i}，请手动拆分")
    
    print(f"操作完成！请检查 {output_dir} 目录")

if __name__ == "__main__":
    main() 