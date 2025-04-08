# 山东某医院检查报告结构化项目

### 一、项目背景与目标
* 背景：医院检查报告需要从PDF格式转换为结构化的JSON数据，以便后续处理和分析
* 目标：构建一个稳定可靠的报告结构化服务

### 二、项目描述
* 目前支持1种类型的医疗检查报告
* 将PDF报告转换为标准化的JSON格式
* 确保输出结果的稳定性（JSON结构保持一致）

### 三、技术栈
* Web框架：FastAPI
* 服务器：Uvicorn
* PDF处理：pdfminer.six
* 文本相似度：python-Levenshtein
* 大模型集成：langchain + Deepseek
* Python版本要求：>=3.8

### 四、接口定义
#### 4.1 报告结构化接口
* 接口路径：`/api/v1/report/process`
* 请求方法：POST
* Content-Type: multipart/form-data
* 请求参数：
  ```json
  {
    "file": "PDF文件，必填"
  }
  ```
* 响应格式：
  ```json
  {
    "code": 0,          // 状态码：0成功，非0失败
    "message": "string", // 状态描述
    "data": {           // 结构化数据
      // 具体字段见example.json
    }
  }
  ```

### 五、处理流程
1. 报告模板准备
   * 创建example目录
   * 添加example.txt（报告文本样例）
   * 添加example.json（结构化结果样例）

2. PDF文本提取
   * 输入：file_xx.pdf
   * 输出：.output/file_xx.txt
   * 工具：pdfminer.six

3. 报告类型验证
   * 方法：计算编辑距离相似度
   * 阈值：>=0.7判定为同类报告
   * 验证失败返回错误信息

4. 内容结构化
   * 使用Qwen2.5:32b模型
   * 提示词模板：
   ```
   系统：你是专业的医疗报告结构化助手
   用户：<example.txt内容>
   系统：<example.json内容>
   用户：<待处理报告内容>
   ```

### 六、部署说明
1. 环境准备
   ```bash
   pip install -r requirements.txt
   ```

2. 启动服务
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. 接口测试
   * 访问 http://localhost:8000/docs
   * 使用Swagger UI测试接口

### 七、错误处理
| 错误类型 | 错误码 | 说明 |
|---------|--------|-----|
| 文件格式错误 | 1001 | 仅支持PDF文件 |
| 报告类型不匹配 | 1002 | 与模板相似度低于0.7 |
| 结构化失败 | 1003 | 模型处理异常 |
