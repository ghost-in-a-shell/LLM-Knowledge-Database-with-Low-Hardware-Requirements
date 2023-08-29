import numpy as np
#from poe_api_wrapper import PoeApi
import variables
import embedding_saving
from utils import error_handler,get_list_from_str
import poe_llm
import tools_lib
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.schema.messages import SystemMessage
import prompt







def generate_feedcontent(comp_res_element,splits):
    feed_content=""
    metadata=comp_res_element[0].metadata
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

def generate_combined_feedcontent(comp_res,splits):
    content=""
    for comp_res_element in comp_res:
        feed_content,sourcefile,page=generate_feedcontent(comp_res_element,splits)
        content+=sourcefile+"-page"+str(page)+":\n"
        content+=feed_content+"\n\n"
    return content

def split_question(client,chat_id,bot,question):
    feed=splitquestionprompt(question)
    reply=client.send_message(bot, feed, chatId=chat_id)
    return get_list_from_str(reply)


class llm_agent:
    llm=None
    vectordb=None
    splits=None
    bot=""
    def __init__(self,split_filename,bot) -> None:
        self.llm=poe_llm.PoeClient()
        #client.chat_break(bot, chatId=chat_id)
        print("Context is now cleared")
    
        self.vectordb=embedding_saving.get_vectordb() 
        self.splits=np.load(split_filename, allow_pickle=True)
        self.bot=bot
    def run(self):
        while True:
            bot=self.bot
            question = input("Human : ")
            reply=self.run_single(question)
            print(f"Human : {question}\n{bot} : {reply}\t")

    def run_single(self,question):
        if question =="!quit":
            error_handler("user end",97987)
        if question =="!clear":
            reply=self.llm(question)
            return reply


        
    #         #tools = load_tools(["llm-math","wikipedia"], llm=llm)
    #         tools=[tools_lib.FreeFallHeight()]

    #         system_message = SystemMessage(
    #             content="""Assistant is a large language model trained by OpenAI.

    # Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    # Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    # Unfortunately, Assistant is terrible at maths and phisics. When provided with math or phisics questions, no matter how simple, assistant always refers to it's trusty tools and absolutely does NOT try to answer math or phisics questions by itself

    # Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist."""
    #         )

    #         #创建代理
    #         agent= initialize_agent(
    #             tools, 
    #             llm, 
    #             agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #             handle_parsing_errors=True,
    #             verbose = True,
    #             max_iterations=3,
    #             system_message=system_message,
    #             early_stopping_method='generate'
    #            )


        #agent(question)
        #print(split_question(client,chat_id,bot,question))
        #flag_reply=False
        comp_res = self.vectordb.similarity_search_with_score(question,k=variables.NEAREST_K)
        feed_content=generate_combined_feedcontent(comp_res,self.splits)
        message=prompt.allinoneprompt(question,feed_content)
        reply=self.llm(message)
        return reply
            # for i in range(variables.NEAREST_K):
                
            #     feed_content,sourcefile,pageno=generate_feedcontent(comp_res,splits,i)
            #     message=rejectprompt(question,feed_content)
            #     if variables.DEBUG:
            #         print(message)
            #     #print (message,chat_id)
            #     #reply=client.send_message(bot, message, chatId=chat_id)
            #     reply=llm(message)
            #     if variables.DEBUG:
            #         print("\n\n\n"+reply+"\n\n\n")
            #     if reply=="否":
            #         continue
            #     elif reply=="是":
            #         message=askprompt(question,feed_content)
            #         #reply=client.send_message(bot, message, chatId=chat_id)
            #         reply=llm(message)
            #         if pageno!='--':
            #             print(f"{bot} : {reply}\n\t出处：{sourcefile}\t第{pageno}页附近")
            #         else:
            #             print(f"{bot} : {reply}\n\t出处：{sourcefile}\t")
            #         flag_reply=True
            #         break
            #     else:
            #         error_handler("JUDGE REPLY ERROR: "+reply,888)

                #---------------------------------v015 above---------------------------------------#

            

            # if not flag_reply:
            #     print(f"{bot} :抱歉，我无法回答")