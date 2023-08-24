#########################################
# change promp here!!
#########################################
def askprompt(question,feed_content):
    message=f"从现在开始你是一个机器人客服，根据四重反引号分隔的文本中的内容，用中文回答三重中括号分隔的文本中的问题\n````{feed_content}````\n[[[{question}]]]"
    return message

def rejectprompt(question,feed_content):
    message=f"根据四重反引号分隔的文本中的内容，判断是否可以正确地回答三重中括号分隔的文本中的问题，不能涉及文本之外的知识，用一个字回答，只能回答是或否\n````{feed_content}````\n[[[{question}]]]"
    return message

def splitquestionprompt(question):
    message=f"根据下面的内容，将内容分为多个独立的问题，存储在一个python list中。\n你只需要输出python list，不要输出其他内容\n-----\n{question}"
    return message











def allinoneprompt(question,feed_content):
    message=f"根据提供的文件摘录列表（没有特定顺序），\
        使用领域专业知识通用工具为给定的问题提供最终答案。在回答中，始终包含一个“来源”部分，\
        仅包括回答问题所需的最小来源集。如果无法回答问题，请明确表示不知道。请勿尝试虚构答案\
        ，将“来源”部分留空。\n``````````````\n文件摘录列表:\n{feed_content}\n问题：\n{question}\n最终答案："
    return message
#########################################
# / change promp here!!
#########################################