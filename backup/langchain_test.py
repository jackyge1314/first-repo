from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}. Don't say any others!",
        ),
        ("human", "{input}"),
    ]
)

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

#chain = prompt | llm
chain = prompt | llm | StrOutputParser()
result = chain.invoke(
    {
        "input_language": "English",
        "output_language": "Chinese",
        "input": "I love programming. My name is jackyge, remember me!",
    }
)
print(result)