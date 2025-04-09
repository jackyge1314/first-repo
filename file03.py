# 直接解析.docx的 XML（终极方法）
import zipfile
from xml.etree.ElementTree import fromstring

with zipfile.ZipFile("example/test.doc") as z:
    with z.open('word/document.xml') as f:
        xml_content = f.read()
        root = fromstring(xml_content)
        
        # 提取所有文本（包括隐藏内容）
        all_text = ' '.join([elem.text for elem in root.iter() if elem.text])
        print("原始XML中的文本:", all_text)