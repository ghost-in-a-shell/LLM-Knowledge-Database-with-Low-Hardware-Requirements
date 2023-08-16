import numpy as np
from POE import load_chat_id_map, clear_context, send_message, get_latest_message, set_auth
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
    if "page" not in metadata:
        page='--'
    else:
        page=metadata["page"]
    for i in range(max(0,p_index-variables.HALF_SEARCH_RANGE),min(len(splits),p_index+variables.HALF_SEARCH_RANGE+1)):
        feed_content+=splits[i].page_content
    #print(feed_content)
    return feed_content,sourcefile,page

def config_poe():
    set_auth('Quora-Formkey',variables.QUORA_FORMKEY)
    set_auth('Cookie',variables.QUORA_COOKIES)


def llm_agent_start(split_filename,bot):
    config_poe()
    chat_id = load_chat_id_map(bot)
    clear_context(chat_id)
    print("Context is now cleared")
    vectordb=embedding_saving.get_vectordb() 
    splits=np.load(split_filename, allow_pickle=True)
    while True:
        question = input("Human : ")
        if question =="!quit":
            break
        if question =="!clear":
            clear_context(chat_id)
            print("Context is now cleared")
            continue
        
        flag_reply=False
        for i in range(variables.NEAREST_K):
            comp_res = vectordb.similarity_search_with_score(question,k=variables.NEAREST_K)
            feed_content,sourcefile,pageno=generate_feedcontent(comp_res,splits,i)
            message=rejectprompt(question,feed_content)
            if variables.DEBUG:
                print(message)
            send_message(message,bot,chat_id)
            reply = get_latest_message(bot)
            if variables.DEBUG:
                print("\n\n\n"+reply+"\n\n\n")
            if reply=="否":
                continue
            elif reply=="是":
                message=askprompt(question,feed_content)
                send_message(message,bot,chat_id)
                reply = get_latest_message(bot)
                if pageno!='--':
                    print(f"{bot} : {reply}\n\t出处：{sourcefile}\t第{pageno}页附近")
                else:
                    print(f"{bot} : {reply}\n\t出处：{sourcefile}\t")
                flag_reply=True
                break
            else:
                error_handler("JUDGE REPLY ERROR: "+reply,888)
        if not flag_reply:
            print(f"{bot} :抱歉，我无法回答")