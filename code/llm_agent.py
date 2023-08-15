import numpy as np
from POE import load_chat_id_map, clear_context, send_message, get_latest_message, set_auth
import variables
import embedding_saving



#########################################
# change promp here!!
#########################################
def myprompt(question,feed_content):
    message=f"从现在开始你是一个机器人客服，根据三重反引号分隔的文本中的内容，用中文回答三重中括号分隔的文本中的问题\n```{feed_content}```\n[[[{question}]]]"
    return message

#########################################
# / change promp here!!
#########################################






def generate_feedcontent(question,split_filename):
    vectordb=embedding_saving.get_vectordb() 
    splits=np.load(split_filename, allow_pickle=True)
    comp_res = vectordb.similarity_search_with_score(question,k=3)

    feed_content=""
    p_index=comp_res[0][0].metadata["p_index"]
    for i in range(max(0,p_index-2),min(len(splits),p_index+3)):
        feed_content+=splits[i].page_content
    #print(feed_content)
    return feed_content

def config_poe():
    set_auth('Quora-Formkey',variables.QUORA_FORMKEY)
    set_auth('Cookie',variables.QUORA_COOKIES)


def llm_agent_start(split_filename,bot):
    config_poe()
    chat_id = load_chat_id_map(bot)
    clear_context(chat_id)
    print("Context is now cleared")

    while True:
        question = input("Human : ")
        if question =="!quit":
            break
        if question =="!clear":
            clear_context(chat_id)
            print("Context is now cleared")
            continue
        

        feed_content=generate_feedcontent(question,split_filename)
        message=myprompt(question,feed_content)
        print(message)
        send_message(message,bot,chat_id)
        reply = get_latest_message(bot)
        print(f"{bot} : {reply}")