# ai/model/chatbot_model.py
from ai.model import prompt_template, retriever, chain
import time

# 전역 변수
is_initialized = False  # 초기화 여부를 추적

def init():
    """
    Initializes dependencies and configurations for the chatbot model.
    """
    global retriever, prompt_template, chain, is_initialized
    if not is_initialized:  # 이미 초기화되었는지 확인
        print("Initializing dependencies...")
        retriever = retriever.initialize()
        prompt_template = prompt_template.load_template("chat_prompt")
        chain = chain.create_chain("default_chain")
        is_initialized = True  # 초기화 완료 표시
        print("Initialization complete.")

def process_chat(user_input: str) -> str:
    global is_initialized
    if not is_initialized:
        init()  # 처음 실행 시 초기화

    print(f"chatbot_model output: {user_input}")
    
    try:
        prev = time.time()
        retrieve_result = retriever.get_retriever_results(user_input)
        print("retrieve time elapsed:", time.time() - prev)
        prompt_with_template = prompt_template.format(question=user_input, input=retrieve_result)
        prev = time.time()
        response = chain.invoke({"question": user_input, "input": retrieve_result})
        print("response time elapsed:", time.time() - prev)
    except Exception as e:
        print(f"Error occurred: {e}")
        response = "메시지를 입력해주세요."

    return response[len(prompt_with_template):].strip()

