import os
import pyautogui
import pyperclip
import cv2
import numpy as np
import time

button_dir = 'buttons/'


def __find_button(template_path, threshold=0.8, x_percentage=0.5, y_percentage=0.5):
    """
    在屏幕截图中查找指定模板图像的位置。
    :param y_percentage:
    :param x_percentage:
    :param template_path: 模板图像的文件路径。
    :param threshold: 匹配阈值，默认为 0.8。
    :return:
    """
    # 截取屏幕截图
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2HSV)

    # 加载模板图像
    if not os.path.exists(template_path):
        print(template_path)
        print("模板图像文件不存在，程序终止")
        raise SystemExit
    template = cv2.imread(template_path)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2HSV)

    # 在屏幕截图中匹配模板图像
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        h, w = template.shape[:2]
        button_center_x = max_loc[0] + w * x_percentage
        button_center_y = max_loc[1] + h * y_percentage
        return button_center_x, button_center_y

    return None


def find_button(template_path, threshold=0.8, x_percentage=0.5, y_percentage=0.5):
    res = __find_button(template_path, threshold, x_percentage, y_percentage)
    trytimes = 5
    while not res and trytimes > 0:
        trytimes -= 1
        print("未找到按钮，等待2秒后重试")
        time.sleep(5)
        res = __find_button(template_path, threshold, x_percentage, y_percentage)
    return res


def click_button(x, y):
    """
    点击指定坐标的按钮。
    :param x: 按钮中心的 x 坐标。
    :param y: 按钮中心的 y 坐标。
    :return:
    """
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.click()
    # 防止后续操作太快，页面未加载完成
    time.sleep(0.5)


def input_text(text):
    """
    输入文本
    :param text: 输入的文本
    :return:
    """
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)


def clear_input_box():
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('delete')
    time.sleep(0.5)


def click_space():
    # 点击空白区域
    items_path = os.path.join(button_dir, 'items.png')
    space_pos = find_button(items_path)
    while not space_pos:
        print("未找到空白区域，等待5秒后重试")
        time.sleep(5)
        space_pos = find_button(items_path)
    click_button(*space_pos)


def student(student_id):
    """
    输入学号
    :param student_id: 学号
    :return:
    """

    # 点击加号按钮
    plus_button_path = os.path.join(button_dir, 'plus.png')
    plus_button_pos = find_button(plus_button_path)
    if not plus_button_pos:
        print("未找到加号按钮，跳过此行数据")
        return False
    click_button(*plus_button_pos)

    # 在新页面中输入学号并点击检索
    # 根据检索按钮定位
    search_button_path = os.path.join(button_dir, 'check.png')
    input_box_pos = find_button(search_button_path, y_percentage=-2)
    if not input_box_pos:
        print("未找到学号输入框，跳过此行数据")
        return False
    click_button(*input_box_pos)
    input_text(str(student_id))
    search_button_pos = find_button(search_button_path)
    if not search_button_pos:
        print("未找到检索按钮，跳过此行数据")
        return False
    click_button(*search_button_pos)

    # 点击第一个搜索结果，并点击确定
    time.sleep(2)
    first_result_pos = find_button(search_button_path, x_percentage=0.75, y_percentage=4.5)
    if not first_result_pos:
        print("未找到检索结果，跳过此行数据")
        return False
    click_button(*first_result_pos)
    confirm_button_path = os.path.join(button_dir, 'confirm.png')
    confirm_button_pos = find_button(confirm_button_path)
    if not confirm_button_pos:
        print("未找到右下角确定按钮，跳过此行数据")
        return False
    click_button(*confirm_button_pos)

    return True


type2index = {
    '学业发展': 1,
    '思想动态': 2,
    '心理健康': 3,
    '升学就业': 4,
    '个人情感': 5,
    '班级建设': 6,
}


def types(type_names):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.17)
    if not inputbox_pos:
        print("未找到谈话类型输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)

    for type_name in type_names:
        if type_name not in type2index:
            print("不存在的类型：", type_name, "，跳过此行数据")
            return False

        type_index = type2index[type_name]
        type_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.3 + 0.0867 * (type_index - 1))
        if not type_pos:
            print("未找到谈话类型，跳过此行数据")
            return False
        click_button(*type_pos)

    click_space()
    return True


mode2index = {
    '平静': 1,
    '欢愉': 2,
    '失望': 3,
    '忧郁': 4,
    '愤怒': 5,
    '担心': 6,
    '乐观': 7,
}


def mode(mode_name='平静'):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.3)
    if not inputbox_pos:
        print("未找到学生状态输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)

    if mode_name not in mode2index:
        print("不存在的类型：", mode_name, "，跳过此行数据")
        return False

    mode_index = mode2index[mode_name]
    mode_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.43 + 0.0867 * (mode_index - 1))
    if not mode_pos:
        print("未找到学生状态类型，跳过此行数据")
        return False
    click_button(*mode_pos)

    return True


def starttime(date, time):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.43)
    if not inputbox_pos:
        print("未找到开始时间输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)

    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.56)
    if not inputbox_pos:
        print("未找到日期输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)
    input_text(date)

    inputbox_pos = find_button(items_path, x_percentage=3, y_percentage=0.56)
    if not inputbox_pos:
        print("未找到时间输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)
    clear_input_box()
    input_text(time)

    click_space()
    return True


def timespan(span='15'):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.56)
    if not inputbox_pos:
        print("未找到谈话时长输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)

    clear_input_box()
    input_text(span)
    return True


def place(pl='新主楼G833'):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.69)
    if not inputbox_pos:
        print("未找到谈话地点输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)
    input_text(pl)
    return True


def subject(sbj):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.82)
    if not inputbox_pos:
        print("未找到谈话主题输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)
    input_text(sbj)
    return True


def content(ctt):
    items_path = os.path.join(button_dir, 'items.png')
    inputbox_pos = find_button(items_path, x_percentage=1.5, y_percentage=0.95)
    if not inputbox_pos:
        print("未找到谈话内容输入框，跳过此行数据")
        return False
    click_button(*inputbox_pos)
    input_text(ctt)
    return True
