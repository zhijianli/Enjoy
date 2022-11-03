# 版本为python3，如果为python2需要在字符串前面加上u
import re
def cut_sent(para):
    para = re.sub('([。！？；：\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？；：\?][”’])([^，。！？；\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def sentence_break(para):
    para = re.sub('([。！？；：\?])([^”’])', r"\1\n\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\n\2", para)  # 中文省略号
    para = re.sub('([。！？；：\?][”’])([^，。！？；\?])', r'\1\n\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = re.sub(r"(.{26})", "\\1\r\n\n", para)
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。

    return para


def sub(str):
    str = re.sub(r"(.{18})", "\\1\r\n\n", str)
    return str

def cut_end(str):
    str = re.sub('([》\?])([^”’])', r"\1\n\n     \2", str)
    return str

if __name__ == "__main__":
    para = "第一段第一行||－－弗洛伊德&第二段第一行||－－黑塞&第二段第一行||－－弗洛姆"
    # sents = cut_sent(para)
    sents = para.split('&')
    print(sents)
    for inx,val in enumerate(sents):

        text_str = sents[inx]
        saying = text_str.split('||')[0]
        source = text_str.split('||')[1]
        print(saying,source)


    # s = "如果我们不花时间去思考自己想要什么样的成功，以及自己的成功版本。那么，我们就很容易陷入一种基于他人期待的生活之中。"
    # s = sub(s)
    # s = sentence_break(s)
    # print(s)
    # s = "《爱的艺术》－－弗洛姆"
    #
    # s = cut_end(s)
    # print(s)


