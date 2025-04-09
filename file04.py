from docx2python import docx2python
import json

doc = docx2python("example/test.doc")

# 手动构建字典
data = {
    "body": doc.body,
    "header": doc.header,
    "footer": doc.footer,
    "text": doc.text  # 所有文本合并后的字符串
}

print(json.dumps(data, indent=2, ensure_ascii=False))
