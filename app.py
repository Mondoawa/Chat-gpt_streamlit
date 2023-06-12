import openai
import streamlit as st
import os

from message_log import message_log

# 打开credentials.txt文件
with open("./credentials.txt", "r") as f:
    # 从文件中读取行
    lines = f.readlines()

# 循环遍历所有行并找到包含API密钥的行
for line in lines:
    if "CHATGPT_API_KEY" in line:
        # 从行中提取API密钥并去除空格和换行符
        api_key = line.replace("CHATGPT_API_KEY=", "").strip()

openai.api_key = api_key

def generate_response(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,  # The conversation history up to this point, as a list of dictionaries
        temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


st.set_page_config(page_title="Xi_chat_gpt")

st.markdown("# 当前使用模型为gpt-3.5-turbo")
# 增加一个按钮，点击后清空对话记录，重新开始对话
if st.button('重制对话'):
    st.balloons()
    st.session_state['generated'] = []
    st.session_state['past'] = []
    message_log.clear()
    st.experimental_rerun()
st.markdown("### 请在下方输入对话内容")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.text_area("You:", key='input')

if user_input:
    # print(message_log)
    message_log.append({"role": "user", "content": user_input})
    output = generate_response(message_log)
    message_log.append({"role": "assistant", "content": output})
    # store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.markdown(f'''**You:** {st.session_state['past'][i]}''')
        # message(st.session_state["generated"][i], key=str(i))
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')
        # 添加分隔符，跟输入框的长度一致
        st.markdown(f'''---''')
