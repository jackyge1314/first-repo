from fastapi import FastAPI, File, UploadFile, HTTPException
from pdfminer.high_level import extract_text
import Levenshtein
import json
import os
from typing import Dict
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="医疗报告结构化服务")

def load_example():
    with open("example/example.txt", "r", encoding="utf-8") as f:
        example_text = f.read()
    with open("example/example.json", "r", encoding="utf-8") as f:
        example_json = json.load(f)
    return example_text, example_json

def validate_report_type(text: str, example_text: str) -> bool:
    similarity = Levenshtein.ratio(text, example_text)
    return similarity >= 0.7

def process_with_llm(text: str, example_text: str, example_json: Dict) -> Dict:
    # 1. 传参获取文件
    # 2. 构建对话历史
    chat_history = [
        ("user", f"这是一份示例报告:\n{example_text}"),
        #("assistant", f"明白了，这份报告的结构化格式是:\n{json.dumps(example_json, ensure_ascii=False, indent=2)}"),   # langchain的 ChatPromptTemplate 中{}默认用于标识占位符（如{variable_name}），所以必须添加.replace...
        ("assistant", f"明白了，这份报告的结构化格式是:\n{json.dumps(example_json, ensure_ascii=False, indent=2).replace('{', '{{').replace('}', '}}')}"),
    ]
    
    # 3. 构建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是专业的医疗报告结构化助手，请将输入的医疗报告按照示例的格式进行结构化处理。"),
        *chat_history,  # 注入历史对话
        ("human", f"请按照这个格式处理这份新报告，不要增加特殊标识（如```json ```等):\n{text}")  # 用户最新输入
    ])

    # 打印{json.dumps(example_json, ensure_ascii=False, indent=2).replace('{', '{{').replace('}', '}}')}")内容
    #print(f"提示模板内容: {prompt.messages}")

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
        logger.info(f"PROMPT内容为: {prompt.messages}")
        result = chain.invoke({})
        logger.info(f"LLM返回的原始内容: {result}") # jackyge tst 2025-04-08
        #return result
        return json.loads(result)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"输出结果解析失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型处理失败: {str(e)}")

@app.post("/api/v1/report/process")
async def process_report(file: UploadFile = File(...)):
    try:
        logger.info(f"开始处理文件: {file.filename}")
        
        if not file.filename.endswith('.pdf'):
            logger.warning(f"不支持的文件类型: {file.filename}")
            raise HTTPException(status_code=400, detail={"code": 1001, "message": "仅支持PDF文件"})
        
        # 保存上传的PDF文件
        temp_path = f".output/{file.filename}"
        logger.info(f"保存临时文件到: {temp_path}")
        os.makedirs(".output", exist_ok=True)
        
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # 提取PDF文本
        logger.info("开始提取PDF文本")
        text = extract_text(temp_path)
        logger.info(f"提取的文本长度: {len(text)}")
        os.remove(temp_path)  # 清理临时文件
        
        # 加载示例数据
        logger.info("加载示例数据")
        example_text, example_json = load_example()
        
        # 验证报告类型
        logger.info("验证报告类型")
        if not validate_report_type(text, example_text):
            logger.warning("报告类型不匹配")
            raise HTTPException(status_code=400, detail={
                "code": 1002,
                "message": "报告类型不匹配"
            })
        
        logger.info("开始LLM处理")
        result = process_with_llm(text, example_text, example_json)
        logger.info("LLM处理完成")
        
        response = {
            "code": 0,
            "message": "success",
            "data": result
        }
        logger.info("处理成功")
        return response
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={
            "code": 1003,
            "message": f"结构化失败：{str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)