import streamlit as st

st.write("Hello World")
import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="GPT-5.1 & Image Demo")

st.title("GPT-5.1 / gpt-image-1-mini 데모 앱")

# 1. API Key 입력 (비밀번호 형식)
api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# API Key가 없으면 안내
if not api_key:
    st.warning("위에 OpenAI API Key를 먼저 입력하세요.")
else:
    # 2. OpenAI Client 생성
    client = OpenAI(api_key=api_key)

    st.markdown("---")
    st.header("4. GPT-5.1 텍스트 챗봇")

    # 3. 텍스트 질문 입력
    user_question = st.text_input("질문을 입력하세요")

    if st.button("텍스트 응답 받기"):
        if user_question.strip() == "":
            st.error("질문을 입력해 주세요.")
        else:
            try:
                # gpt-5.1 모델 사용
                completion = client.chat.completions.create(
                    model="gpt-5.1",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_question},
                    ],
                )
                answer = completion.choices[0].message.content
                st.subheader("모델 응답")
                st.write(answer)
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

    st.markdown("---")
    st.header("5. gpt-image-1-mini 이미지 생성")

    # 4. 이미지 프롬프트 입력
    img_prompt = st.text_input("이미지 프롬프트를 입력하세요")

    if st.button("이미지 생성하기"):
        if img_prompt.strip() == "":
            st.error("이미지 프롬프트를 입력해 주세요.")
        else:
            try:
                # gpt-image-1-mini로 이미지 생성 (b64_json 사용)
                img = client.images.generate(
                    model="gpt-image-1-mini",
                    prompt=img_prompt,
                    size="512x512",        # 필요하면 크기 변경 가능
                    n=1,
                    response_format="b64_json",
                )

                # b64_json → bytes
                image_bytes = base64.b64decode(img.data[0].b64_json)

                # 메모리 상의 이미지 보여주기
                st.image(image_bytes, caption="생성된 이미지")

            except Exception as e:
                st.error(f"이미지 생성 중 에러가 발생했습니다: {e}")

