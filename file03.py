# aspose-words
# pip install aspose-words  # 安装相应包
import aspose.words as aw
doc = aw.Document(".output/_20231205_165237/_20231205_165237.doc")
print(doc.get_text())