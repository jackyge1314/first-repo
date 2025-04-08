from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

def load_files():
    with open("example/example.txt", "r", encoding="utf-8") as f:
        example_text = f.read()
    with open("example/example.json", "r", encoding="utf-8") as f:
        example_json = json.load(f)
    with open(".output/944037/944037.txt", "r", encoding="utf-8") as f:
        text = f.read()
    return example_text, example_json, text

def process_medical_report():
    example_text, example_json, text = load_files()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是专业的医疗报告结构化助手，请将输入的医疗报告按照示例的格式进行结构化处理。"),
            ("human", f"""
                请参考以下示例，将医疗报告结构化：

                示例报告：
                {example_text}

                示例结构：
                {json.dumps(example_json, ensure_ascii=False, indent=2)}

                待处理报告：
                {text}
            """)
        ]
    )
    print(prompt.messages)

    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({})
    return result

if __name__ == "__main__":
    result = process_medical_report()
    print(result)
