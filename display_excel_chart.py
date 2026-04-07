from spire.xls import *
from spire.xls.common import *
import os
from IPython.display import display, HTML
from PIL import Image
import time

def display_images_row(*image_paths, width=300, gap=10):
    html_content = f'<div style="display: flex; gap: {gap}px; flex-wrap: wrap; align-items: flex-start;">'
    for path in image_paths:
        html_content += f'<img src="{path}" style="width: {width}px; border: 1px solid #ddd; border-radius: 4px;">'
    html_content += '</div>'
    display(HTML(html_content))


def concatenate_images(image_paths, output_path='tmp.png', direction='horizontal'):
    """
    水平或垂直拼接多张图片
    :param image_paths: 图片路径列表
    :param output_path: 输出图片路径
    :param direction: 'horizontal' 或 'vertical'
    """
    # 1. 打开所有图片
    images = [Image.open(path) for path in image_paths]
    
    # 2. 获取所有图片的宽度和高度
    widths, heights = zip(*(img.size for img in images))

    # 3. 根据方向计算新画布的尺寸
    if direction == 'horizontal':
        total_width = sum(widths)
        max_height = max(heights)
        new_image = Image.new('RGB', (total_width, max_height))
        
        # 4. 依次将图片粘贴到新画布上
        x_offset = 0
        for img in images:
            new_image.paste(img, (x_offset, 0))
            x_offset += img.width
    else:  # vertical
        max_width = max(widths)
        total_height = sum(heights)
        new_image = Image.new('RGB', (max_width, total_height))
        
        y_offset = 0
        for img in images:
            new_image.paste(img, (0, y_offset))
            y_offset += img.height

    # 5. 保存结果
    new_image.save(output_path)
    # print(f"成功！图片已保存至: {output_path}")
    display(Image.open(output_path))
    os.remove(output_path)

# image_files = ['image1.png', 'image2.png', 'image3.png']
# concatenate_images(image_files, 'result_horizontal.png', 'horizontal')

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
                # display_images_row(*[f'tmp{k+1}.png' for k in range(cols)], width=width, gap=2)
                concatenate_images([f'tmp{k+1}.png' for k in range(cols)])
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
