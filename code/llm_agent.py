import numpy as np
from poe_api_wrapper import PoeApi
import variables
import embedding_saving
from utils import error_handler



#########################################
# change promp here!!
#########################################
def askprompt(question,feed_content):
    message=f"从现在开始你是一个机器人客服，根据三重反引号分隔的文本中的内容，用中文回答三重中括号分隔的文本中的问题\n```{feed_content}```\n[[[{question}]]]"
    return message

def rejectprompt(question,feed_content):
    message=f"根据三重反引号分隔的文本中的内容，判断是否可以正确地回答三重中括号分隔的文本中的问题，不能涉及文本之外的知识，用一个字回答，只能回答是或否\n```{feed_content}```\n[[[{question}]]]"
    return message

#########################################
# / change promp here!!
#########################################






def generate_feedcontent(comp_res,splits,index):
    feed_content=""
    metadata=comp_res[index][0].metadata
    p_index=metadata["p_index"]
    sourcefile=metadata["source"].split("/")[-1]
    page=metadata["page"]
    for i in range(max(0,p_index-variables.HALF_SEARCH_RANGE),min(len(splits),p_index+variables.HALF_SEARCH_RANGE+1)):
        feed_content+=splits[i].page_content
    #print(feed_content)
    return feed_content,sourcefile,page



def llm_agent_start(split_filename,bot):
    client = PoeApi(variables.TOKEN)
    chat_id = variables.CHAT_ID
    client.chat_break(bot, chatId=chat_id)
    print("Context is now cleared")
    vectordb=embedding_saving.get_vectordb() 
    splits=np.load(split_filename, allow_pickle=True)
    while True:
        question = input("Human : ")
        if question =="!quit":
            break
        if question =="!clear":
            client.chat_break(bot, chatId=chat_id)
            print("Context is now cleared")
            continue
        
        flag_reply=False
        for i in range(variables.NEAREST_K):
            comp_res = vectordb.similarity_search_with_score(question,k=variables.NEAREST_K)
            feed_content,sourcefile,pageno=generate_feedcontent(comp_res,splits,i)
            message=rejectprompt(question,feed_content)
            if variables.DEBUG:
                print(message)
            reply=client.send_message(bot, message, chatId=chat_id)
            if variables.DEBUG:
                print("\n\n\n"+reply+"\n\n\n")
            if reply=="否":
                continue
            elif reply=="是":
                message=askprompt(question,feed_content)
                reply=client.send_message(bot, message, chatId=chat_id)
                print(f"{bot} : {reply}\n\t出处：{sourcefile}\t第{pageno}页附近")
                flag_reply=True
                break
            else:
                error_handler("JUDGE REPLY ERROR: "+reply,888)
        if not flag_reply:
            print(f"{bot} :抱歉，我无法回答")