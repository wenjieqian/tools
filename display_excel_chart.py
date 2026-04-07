from spire.xls import *
from spire.xls.common import *
import os
from IPython.display import display, HTML, Image
import time

def display_images_row(*image_paths, width=300, gap=10):
    html_content = f'<div style="display: flex; gap: {gap}px; flex-wrap: wrap; align-items: flex-start;">'
    for path in image_paths:
        html_content += f'<img src="{path}" style="width: {width}px; border: 1px solid #ddd; border-radius: 4px;">'
    html_content += '</div>'
    display(HTML(html_content))

def display_batch(fp,bs=20,bi=1,cols=3,width=400):
    workbook = Workbook()
    workbook.LoadFromFile(fp) # 替换为你的文件路径
    for i in range(workbook.Worksheets.Count):
        sheet = workbook.Worksheets.get_Item(i)
        k=0
        cc=sheet.Charts.Count
        for j in range(cols*bs*(bi-1),cols*bs*bi):
            if j>=cc:
                break
            chart = sheet.Charts.get_Item(j)
            k=k+1
            image_path = f"tmp{k}.png"
            chart_image = workbook.SaveChartAsImage(sheet, j)
            chart_image.Save(image_path)
            if k==cols:
                k=0
                print(f'{(j+1)/cols:.0f}/{cc/cols:.0f}',chart.ChartTitle.split()[0])
                display_images_row(*[f'tmp{k+1}.png' for k in range(cols)], width=width, gap=2)
                time.sleep(0.3)
            if j==cc-1:
                print('*'*100)
                print('*'*10,'打印完毕，再见','*'*10)
                print('*'*100)
    for k in range(1,cols+1):
        try:
            os.remove(f"tmp{k}.png")
        except:
            pass
    workbook.Dispose()
fp='test.xlsx'
display_batch(fp,bs=3,bi=1,cols=3,width=400)
