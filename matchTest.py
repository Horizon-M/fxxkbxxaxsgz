import time

from input import find_button


if __name__ == '__main__':
    filename = 'buttons/plus.png'

    button = find_button(filename)
    while not button:
        print("未找到按钮，等待5秒后重试")
        time.sleep(5)
        button = find_button(filename)

    print(button)
