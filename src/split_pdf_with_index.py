# 指定索引进行切分
# 参考：https://blog.51cto.com/u_16213336/8944825
import os.path

import numpy as np

import PyPDF2

import fitz  # 导入pymupdf库


def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        return pdf_reader


def get_total_pages(pdf_reader):
    return len(pdf_reader.pages)


def specify_split_position(total_pages):
    start_page = int(input("请输入切分的起始页码："))
    end_page = int(input("请输入切分的结束页码："))

    if start_page < 1 or end_page > total_pages or start_page > end_page:
        print("输入的页码无效，请重新输入。")
        specify_split_position(total_pages)
    else:
        return (start_page, end_page)


def split_pdf(pdf_reader, start_page, end_page):
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(start_page - 1, end_page):
        # pdf_writer.addPage(pdf_reader.pages(page_num))
        pdf_writer.add_page(pdf_reader.pages[page_num])
        # pdf_writer.add_page(pdf_reader.pages(page_num))

    return pdf_writer


def save_pdf(pdf_writer, output_path):
    with open(output_path, 'wb') as file:
        pdf_writer.write(file)


if __name__ == '__main__':
    file_path = '../neuro.pdf'

    # pdf_reader = read_pdf(file_path)
    # print(pdf_reader.pages)
    output_dir = "../docs/pdf"

    # 根据书签获取切分点
    doc = fitz.open(file_path)
    toc = doc.get_toc()
    section_info = np.empty((64 + 2, 2), dtype=int)
    section_info[0, 0] = 1
    split_num = 1
    is_first = False
    for i in range(len(toc)):
        indent_level, bookmark_name, redirect_page = toc[i]  # [缩进级别, 书签名, 书签跳转的页码]
        if indent_level <= 2:
            if indent_level == 1:  # 如果是某一部分，则这部分的第一章不作为切分点，而是这一部分的开始作为切分点
                section_info[split_num, 0] = redirect_page
                split_num = split_num + 1
                is_first = True
            else:
                if is_first == True:
                    is_first = False
                    continue
                else:
                    section_info[split_num, 0] = redirect_page
                    split_num = split_num + 1
    section_info[65, 0] = doc.page_count + 1  # 用于控制结束

    # 切分PDF
    # 一旦离开with块，该文件句柄就会关闭，所以不能用read_file()函数
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for chap_i in range(len(section_info)-1):
            pdf_writer = split_pdf(pdf_reader, section_info[chap_i, 0], section_info[chap_i+1, 0]-1)  # 55
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            save_pdf(pdf_writer, "%s/%02d.pdf" % (output_dir, chap_i))
            pass
    print('Split PDF success!')


