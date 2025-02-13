# 指定索引进行切分
# 参考：https://blog.51cto.com/u_16213336/8944825
import os.path

import numpy as np

import PyPDF2


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

    section_info = np.array([
        [1,  -1],   # 0
        [30, -1],  # 1
        [48, -1],  # 2
        [74, 117],  # 3
        [90, 141],  # 4
        [113, 155],  # 5
        [125, 172],  # 6
        [138, 209],  # 7
        [170, 234],  # 8
        [190, 255],  # 9
        [211, 280],  # 10
        [233, 298],  # 11
        [247, 317],  # 12
        [265, 345],  # 13
        [293, 368],  # 14
        [314, 402],  # 15
        [342, 423],  # 16
        [358, 452],  # 17
        [380, 479],  # 18
        [405, 514],  # 19
        [436, 540],  # 20
        [462, 565],  # 21
        [484, 589],  # 22
        [507, 608],  # 23
        [527, 626],  # 24
        [543, 642],  # 25
        [558, 673],  # 26
        [587, 695],  # 27
        [608, 726],  # 28
        [634, 751],  # 29
        [656, 781],  # 30
        [681, 805],  # 31
        [703, 827],  # 32
        [723, 859],  # 33
        [750, 904],  # 34
        [791, 927],  # 35
        [813, 952],  # 36
        [837, 976],  # 37
        [858, 997],  # 38
        [876, 1018],  # 39
        [894, 1054],  # 40
        [923, 1089],  # 41
        [954, 1109],  # 42
        [970, 1124],  # 43
        [983, 1144],  # 44
        [1001, 1174],  # 45
        [1028, 1200],  # 46
        [1053, 1225],  # 47
        [1076, 1254],  # 48
        [1103, 1280],  # 49
        [1128, 1304],  # 50
        [1152, 1329],  # 51
        [1173, 1356],  # 52
        [1194, 1383],  # 53
        [1217, 1414],  # 54
        [1244, 1436],  # 55
        [1262, 1461],  # 56
        [1284, 1491],  # 57
        [1309, 1517],  # 58
        [1333, 1532],  # 59
        [1347, 1545],  # 60
        [1359, 1567],  # 61
        [1376, 1588],  # 62
        [1392, -1],  # 63
        [1406, -1],  # 64
        [1426, -1],  # 中英文对照表
        [1500, -1],  # 参考文献
        [1528+1, -1],  # 用于控制结束
    ])

    # pdf_reader = read_pdf(file_path)
    # print(pdf_reader.pages)
    output_dir = "../docs/pdf"

    # seek of closed file
    # 一旦离开with块，该文件句柄就会关闭，所以不能用read_file()函数
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for chap_i in range(len(section_info)-1):
            pdf_writer = split_pdf(pdf_reader, section_info[chap_i, 0], section_info[chap_i+1, 0]-1)  # 55
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            save_pdf(pdf_writer, "%s/%02d.pdf" % (output_dir, chap_i))
            pass


