import subprocess
from pathlib import Path

def read_doc_file(file_path):
    """
    读取 .doc 文件内容（使用 antiword）
    
    参数:
        file_path (str): .doc 文件路径
        
    返回:
        str: 文件文本内容
    """
    # 检查文件是否存在
    if not Path(file_path).exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 检查文件扩展名
    if not file_path.lower().endswith('.doc'):
        raise ValueError("仅支持 .doc 文件")
    
    try:
        # 使用 antiword 提取文本
        result = subprocess.run(
            ['antiword', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"antiword 执行失败: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("请先安装 antiword: sudo apt-get install antiword")

# 示例使用
if __name__ == "__main__":
    try:
        text = read_doc_file("example/test.doc")
        print("文件内容:")
        print(text)
    except Exception as e:
        print(f"错误: {e}")