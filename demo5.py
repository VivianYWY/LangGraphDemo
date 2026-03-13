def random_poem(title: str) -> str:
    """
    写诗函数
    根据用户输入的主题写诗
    :param title: 诗的主题
    :return 发送结果的字符串
    """
    # print(title)
    llm = Ollama(model="qwen2:7b")
    text = """
    基于下面的主题写一首诗,主题是'{0}', 诗是:
    """.format(title)
    return llm(text)

class PromptTitleInput(BaseModel):
    title: str = Field(description="这是诗的主题")

import os
from pydantic import BaseModel, Field

def save_text(content: str, path: str) -> str:
    """
    保存文本的函数

    :param content: 要保存的内容
    :param path: 保存目录
    :return: 提示字符串
    """
    with open(os.path.join(path, "test.txt"), "w") as file:
        file.write(content)
    return "保存成功，在{0} 下".format(os.path.join(path, "test.txt"))

result = agent.run("给1780105****@163.com写个请假邮件，我肚子疼要去医院")
class PromptSaveInput(BaseModel):
    content: str = Field(description="需要保存的内容")
    path: str = Field(description="保存内容的目录")

# 定义发送电子邮件的函数
def post_message(title: str, content: str, address: str) -> str:
    """
    发送电子邮件的函数
    :param title: 邮件的主题
    :param content: 邮件的内容
    :param address: 邮箱地址
    :return: 发送结果的字符串
    """
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "1780105****@163.com"  # 用户名
    mail_pass = "****"  # 授权密码, 非登录密码 写自己的

    sender = '1780105****@163.com'  # 发件人邮箱(最好写全, 不然会失败)
    receivers = [,address]  # 接收邮件, 可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtp_obj.login(mail_user, mail_pass)  # 登录验证
        smtp_obj.sendmail(sender, receivers, message.as_string())  # 发送
        smtp_obj.quit()
        print("邮件发送成功。")
        return "邮件发送成功。"
    except smtplib.SMTPException as e:
        return f"邮件发送失败: {str(e)}"

# 定义输入模型类
class PostInput(BaseModel):
    title: str = Field(description="这是邮件的主题")
    content: str = Field(description="这是邮件的内容")
    address: str = Field(description="这是邮箱地址")

tools = [
    StructuredTool.from_function(
        func=random_poem,
        name="写诗",
        description="根据用户输入的主题",
        args_schema=PromptTitleInput
    ),
    StructuredTool.from_function(
        func=save_text,
        name="保存文本",
        description="将内容保存到用户指定的目录下",
        args_schema=PromptSaveInput
    ),
    StructuredTool.from_function(
        func=post_message,
        name="发送邮件",
        description="根据用户输入的主题和内容发送邮件",
        args_schema=PostInput
    )
]
