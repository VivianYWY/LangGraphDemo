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
