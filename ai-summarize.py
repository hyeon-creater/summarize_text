#필요한 모듈 사용
import streamlit as st
from openai import OpenAI

## ai 응답 요청 기능 함수 - 긴글 요약 ####
def askGpt(prompt, apikey):
    client= OpenAI(api_key=apikey) #사용자가 입력한 openai api key 사용

    #AI 답변 지침을 정의하기(프롬프트 엔지니어링)
    instruction='''
    ** role **
    너는 한국어로 글을 요약하는 전문가야.

    **task**
    - 전달된 글을 한국어로 요약해라.
    - 핵심 개념(Concepts)과 주장(Arguments)을 중심으로 텍스트를 요약해라.
    - 개념과 주제별로 3줄이내로 요약해라.
    - bullet 점을 이용해라.
    '''

    #표준 api 방식
    # response= client.chat.completions.create(
    #     model='gpt-4o-mini',
    #     messages=[
    #         {'role':'system','content':'instruction'},
    #         {'role':'user', 'content':prompt}
    #     ]
    # )

    #최신 responses api 이용
    response= client.responses.create(
        model='gpt-4o-mini',
        instructions=instruction, #시스템 지침
        input=prompt,
    )
    return response.output_text
#-------------------------------------------------------

#그냥 코드를 바로 쓰면.. 이 문서를 다른 곳에서 import하면 바로 실행됨
def main():
    st.set_page_config(page_title='AI 요약 프로그램')
    #매번 api_key를 입력받으면 짜증내니까.. st.session_state에 저장
    if "OPENAI_API" not in st.session_state:
        st.session_state['OPENAI_API']= ' '

    #사이드 바
    with st.sidebar:
        openai_apikey= st.text_input(label='OPENAI API 키', placeholder='openai api' 플랫폼에서 발급한 API를 입력하세요.)
        #사용자가 입력한 키를 session_state에 저장
        if openai_apikey:
            st.session_state['OPENAI API']= openai_apikey

        st.markdown('------')#구분선

    #메인공간
    st.header('AI 글 요약 프로그램')
    st.markdown('---')

    #여러줄 입력할 수 있는 입력상자
    text= st.text_area('요약할 글을 입력하세요.')
    #[요약]버튼을 클릭하여 AI를 이용하여 요약한 결과를 출력
    if st.button('요약'):
        with st.spinner('AI가 응답 중입니다...잠시만 기다려 주세요..'):
            #ai llm모델에게 글을 전달하고..streamlit의 info 상자에 결과 보여주기
            response=askGpt(prompt=text, apikey=openai_apikey)
            st.info(response)

#현재 파일을 직접 실행했을때만 main()기능이 동작하도록..
if __name__ == '_main_':
    main()