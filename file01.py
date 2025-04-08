from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# 1. 初始化 DeepSeek 模型
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024
)

# 2. 定义对话历史
chat_history = [
    HumanMessage(content="你好！你是谁？"),
    AIMessage(content="我是DeepSeek AI助手，很高兴为您服务！")
]

# 3. 创建提示模板（包含对话历史）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的AI助手"),
    *chat_history,  # 注入历史对话
    ("human", "{user_input}")  # 用户最新输入
])

# 4. 创建处理链（链式调用）
chain = prompt | llm | StrOutputParser()

# 5. 调用链（传入用户最新输入）
user_input = "你能帮我做什么？"
response = chain.invoke({"user_input": user_input})

# 6. 输出结果
print("用户输入:", user_input)
print("AI回复:", response)