'''
description: Extract PDF Text directly and transform it into TXT file 直接抽取pdf正文 转化成txt文件
author: jtx
data: 2021_01_20
'''

import pdfplumber
from tqdm import tqdm
import re

f = "3.pdf"
out = open("3_2.txt", "w", encoding="utf-8")
pdf = pdfplumber.open(f)

for num, page in enumerate(pdf.pages):
    content = ""
    for char in page.objects["char"]:
        content += char["text"]

    # 判断每段的长度
    content_list = content.split(' ')
    content_result = ''
    for each_content in content_list:
        chinese_in_content = ''
        regex_str = ".*?([\u4E00-\u9FA5]+).*?"
        match_obj = re.findall(regex_str, each_content)
        for each_obj in match_obj:
            chinese_in_content += each_obj
        if len(chinese_in_content) > 36:
            content_result += each_content + '\n\n'
    out.write(content_result)
    break

