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


class PromptSaveInput(BaseModel):
    content: str = Field(description="需要保存的内容")
    path: str = Field(description="保存内容的目录")
