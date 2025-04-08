








请参考file07.py代码，并将 prompt 修改如下，修改完的代码写入 file09.py：
    prompt = f"""系统：你是专业的医疗报告结构化助手
        用户：{example_text}
        系统：{example_json}
        用户：{text}"""
    其中 {example_text}为example/example.txt文件内容，{example_json}为example/example.json的文件内容，{text}为.output/944037/944037.txt的文件内容