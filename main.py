import time
import streamlit as st
import logging
from modules.GetAnswer import GetAnswer
from modules.message_alert import message_alert

logging.basicConfig(level=logging.INFO)

st.markdown(f"""
                    <div style='text-align: center;font-weight: bold; font-size: 24px;'>
                        <img src='https://portalt4h.s3-sa-east-1.amazonaws.com/wp-content/uploads/2022/07/Interface_Cerebro_Computador_AI_Hanyang.jpg' 
                        style='height: 250px;'/>  
                    </div>
                """, unsafe_allow_html=True)
st.markdown(f"""
                    <div style='text-align: center;font-weight: bold; font-size: 24px;'>
                        <h1>📝 Assistente do Curso de ADS</h1>  
                        <h6>🚀 Este é um chatbot que utiliza Inteligência Artificial Generativa para responder perguntas sobre o 
                            Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas. Sinta-se à vontade para perguntar, 
                            porém lembre-se de que ele pode apresentar inconsistências nas respostas, por isso é importante avaliar 
                            cada uma delas. Uma dica é tentar ser bem específico na pergunta, pois quanto mais detalhes fornecer, 
                            melhor e mais precisa será a resposta. Utilize '?' sempre que fizer uma pergunta.
                        </h6>
                    </div>
                """, unsafe_allow_html=True)
st.session_state.alert = False


def main():
    message_placeholder = st.empty()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Pergunte algo sobre o Curso de ADS:")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Processando a resposta..."):
            thread = GetAnswer.create_thread(st.secrets['MESSAGE_FILE_ID'], question)

            if not thread:
                message_placeholder.error("Erro ao criar thread.")
                st.stop()

            try:
                response = GetAnswer.get_answer_with_assistant(thread.id, st.secrets['ASSISTANT_ID'])

                if not response:
                    message_placeholder.error("Erro ao gerar resposta.")
                    st.stop()
                else:
                    message_placeholder.success("Resposta gerada com sucesso!")
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    with st.chat_message("assistant"):
                        st.markdown(response)
            except AttributeError as e:
                logging.error(f"Erro ao acessar thread.id: {e}")
                message_placeholder.error("Erro ao processar a thread.")
                st.stop()


    if st.session_state.alert:
        message_alert()


if __name__ == "__main__":
    main()
