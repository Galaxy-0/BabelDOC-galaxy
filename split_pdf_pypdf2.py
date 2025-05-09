#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfReader, PdfWriter

def main():
    # 源PDF文件和输出目录
    source_pdf = "source/EN-CNt2.pdf"
    output_dir = "source/EN-CNt2-pages"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开PDF文件
    try:
        reader = PdfReader(source_pdf)
        total_pages = len(reader.pages)
        print(f"PDF页数: {total_pages}")
        
        # 遍历每一页并保存到单独的文件
        for i in range(total_pages):
            # 创建一个新的PdfWriter对象
            writer = PdfWriter()
            
            # 添加当前页到writer
            writer.add_page(reader.pages[i])
            
            # 保存到输出文件
            output_file = f"{output_dir}/page-{i+1}.pdf"
            with open(output_file, "wb") as fp:
                writer.write(fp)
            
            print(f"已提取页面 {i+1} 到 {output_file}")
            
        print(f"拆分完成！所有页面已保存到 {output_dir} 目录")
        
    except Exception as e:
        print(f"处理PDF时出错: {e}")

if __name__ == "__main__":
    main() 