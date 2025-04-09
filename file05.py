# 修改记录
# 将原来固定路径的 待处理报告文件路径 修改为 传参方式  jackyge 2025-04-09

import json
from pathlib import Path
from typing import Tuple, Dict, Any

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def load_files(input_path: str) -> Tuple[str, Dict[str, Any], str]:
    """加载示例文件和待处理的医疗报告
    
    Args:
        input_path: 待处理的医疗报告文件路径
        
    Returns:
        Tuple[str, Dict[str, Any], str]: 返回(示例文本, 示例JSON, 待处理文本)
    """
    try:
        # 使用Path处理路径，更安全且跨平台
        example_text = Path("example/example.txt").read_text(encoding="utf-8")
        example_json = json.loads(Path("example/example.json").read_text(encoding="utf-8"))
        text = Path(input_path).read_text(encoding="utf-8")

        return example_text, example_json, text
    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件加载失败: {str(e)}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {str(e)}")


def process_medical_report(input_path: str) -> str:
    """处理医疗报告并返回结构化结果
    
    Args:
        input_path: 待处理的医疗报告文件路径

    Returns:
        str: 结构化后的医疗报告
    """
    # 1. 加载文件
    example_text, example_json, text = load_files(input_path)
    
    # 2. 构建对话历史
    chat_history = [
        ("user", f"这是一份示例报告:\n{example_text}"),
        ("assistant", f"明白了，这份报告的结构化格式是:\n{json.dumps(example_json, ensure_ascii=False, indent=2).replace('{', '{{').replace('}', '}}')}"),
    ]
    
    # 3. 构建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是专业的医疗报告结构化助手，请将输入的医疗报告按照示例的格式进行结构化处理。"),
        *chat_history,  # 注入历史对话
        ("human", f"请按照这个格式处理这份新报告，不要增加特殊标识（如```json ```等):\n{text}")  # 用户最新输入
    ])
    print(prompt.messages)

    # 4. 初始化模型和流水线
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        max_tokens=4096,  # 明确设置最大token数
        timeout=30,       # 设置合理超时
        max_retries=3     # 适当增加重试次数
    )
    
    # 5. 构建处理链并执行
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({})
        return result
    except Exception as e:
        raise RuntimeError(f"医疗报告处理失败: {str(e)}")


if __name__ == "__main__":
    try:
        print("starting...")
        input_path = ".output/_20231205_165237/_20231205_165237.txt"
        result = process_medical_report(input_path)
        print(result)
        # 使用传入的输入路径
        output_path = Path(input_path).with_suffix('.json')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        print("处理成功，结果已保存到:", output_path)
    except Exception as e:
        print(f"处理失败: {str(e)}")