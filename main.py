import os
import pandas as pd
import time
import input
from input import find_button, click_button, button_dir

data_path = 'data.xlsx'

if __name__ == '__main__':

    data = pd.read_excel(data_path, sheet_name='Sheet1')

    # 找 logo，找到时认为已经在起始页面
    logo_button_path = os.path.join(button_dir, 'logo.png')
    logo_button_pos = find_button(logo_button_path)
    while not logo_button_pos:
        print("未找到logo，等待5秒后重试")
        time.sleep(5)
        logo_button_pos = find_button(logo_button_path)

    for index, row in data.iterrows():
        new_button_path = os.path.join(button_dir, 'new.png')
        new_button_pos = find_button(new_button_path)
        if not new_button_pos:
            print("未找到新建按钮，程序终止")
            raise SystemExit
        click_button(*new_button_pos)

        if not input.student(row['学生学工号']):
            print("未完成学生检索，程序终止")
            raise SystemExit

        types = row['谈话类型'].split(',')
        if not input.types(types):
            print("未完成谈话类型输入，程序终止")
            raise SystemExit

        if not input.mode():
            print("未完成学生状态输入，程序终止")
            raise SystemExit

        times = row['谈话时间'].split(' ')
        if not input.starttime(times[0], times[1]):
            print("未完成开始时间输入，程序终止")
            raise SystemExit

        if not input.timespan():
            print("未完成谈话时长输入，程序终止")
            raise SystemExit

        if not input.place():
            print("未完成谈话地点输入，程序终止")
            raise SystemExit

        if not input.subject(row['谈话主题']):
            print("未完成谈话主题输入，程序终止")
            raise SystemExit

        if not input.content(row['谈心谈话内容']):
            print("未完成谈话内容输入，程序终止")
            raise SystemExit

        confirm_button_path = os.path.join(button_dir, 'confirm_out.png')
        confirm_button_pos = find_button(confirm_button_path)
        if not confirm_button_pos:
            print("未找到右下角确定按钮，程序终止")
            raise SystemExit
        click_button(*confirm_button_pos)
        time.sleep(2)

    print("全部完成")
