import streamlit as st
import hydralit_components as hc
import numpy as np
import llm_agent
import variables
import utils
import time
css='''
<style>
    @keyframes animated-border {
    0% {
            box-shadow: 0 0 0 0 rgba(0,0,255,0.4);
        }
    100% {
            box-shadow: 0 0 0 20px rgba(0,0,255,0);
        }
    }
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-z5fcl4.ea3mdgi4 > div:nth-child(1) > div > div:nth-child(6) > div{
        overflow:scroll;
        height:450px;
        position: fixed;

        animation: animated-border 1.5s infinite;
        font-family: Arial;
        font-size: 18px;
        line-height: 30px;
        font-weight: bold;
        color: blue;
        border: 2px solid;
        border-radius: 5px;
        padding: 0px;
        flex:none;
    }
</style>
'''
css_input='''
<style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-z5fcl4.ea3mdgi4 > div:nth-child(1) > div > div.css-ocqkz7.e1f1d6gn3{
        position: fixed;
        bottom:65px;
        width: 100%;
    }
</style>
'''





st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

def generate_response(llma,question):
    return llma.run_single(question)

#def on_input_change():


with st.spinner('正在初始化。。。'):
    if 'llma' not in st.session_state:
        split_filename=utils.get_npy(variables.FILEARRAY_PATH)
        llma=llm_agent.llm_agent(split_filename,variables.POE_BOT)
        st.session_state['llma'] = llma

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["你好呀👋，我是一个智能的知识库问答机器人🤖，有什么问题尽管问我吧！😎"]
    if 'past' not in st.session_state:
        st.session_state['past'] = []





# specify the primary menu definition
menu_data = [
    {'id':'tab1','icon':"💬",'label':"对话"},
    {'id':'tab2','icon':"📖",'label':"知识"},
]

over_theme = {'txc_inactive': '#FFFFFF'}
#override=st.selectbox('Menu override',[0,1])
chosen_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)







# chosen_id = stx.tab_bar(data=[
#     stx.TabBarItemData(id="tab1", title="💬 对话", description="与智能问答知识库机器人交流"),
#     stx.TabBarItemData(id="tab2", title="📖 知识", description="管理知识库文件")],default="tab1")

if chosen_id=="tab1":
    col1, col2 = st.columns([5, 1])
    user_input=col1.text_input("User Input:", key="u_input")

    st.markdown(css, unsafe_allow_html=True)

    

    if user_input:
        st.session_state['past'].append(user_input)
        # print(message_log)
        

    if st.session_state['generated']:
        last_response_loaded=True
        with st.container():
            st.markdown(css_input, unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.write(f'''**AI:** {st.session_state["generated"][0]}''')
            for i in range(len(st.session_state['past'])):
                with st.chat_message("user"):
                    st.write(f'''**You:** {st.session_state['past'][i]}''')
                last_response_loaded=i+1<len(st.session_state["generated"])
                if last_response_loaded:
                    with st.chat_message("assistant"):                    
                        st.write(f'''**AI:** {st.session_state["generated"][i+1]}''')
            if user_input:
                with st.spinner('等待回复中。。。'):
                    question=user_input
                    output=generate_response(st.session_state.llma,question)
            
                #store the output
                st.session_state['generated'].append(output)
            if not last_response_loaded:
                with st.chat_message("assistant"):
                        st.write(f'''**AI:** {st.session_state["generated"][-1]}''')
else:
    st.markdown("开发中。。")