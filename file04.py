import os
import sys

def print_environment_info():
    """打印环境信息用于诊断"""
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")

# 打印环境信息
print_environment_info()

# 设置文件的完整路径
file_path = os.path.abspath("/home/jackyge/code/git-learn/my-repo/.output/20231205_165237/20231205_165237.txt")

# 检查文件是否存在
if not os.path.exists(file_path):
    print(f"错误：文件不存在：{file_path}")
else:
    try:
        # 使用基本的文件读取
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except Exception as e:
        print(f"处理文件时出错：{str(e)}")