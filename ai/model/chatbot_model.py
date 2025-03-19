# ai/model/chatbot_model.py
from ai.model import prompt_template, retrieve_dict, chain
import time

def process_chat(user_input: str, fileid="51580934"):
    try:
        retriever = retrieve_dict[fileid]
        retrieve_result = retriever.get_retriever_results(user_input)
        prompt_with_template = prompt_template.format(question=user_input, input=retrieve_result)

        # 스트리밍 방식으로 모델 호출
        for token in chain.stream({"question": user_input, "input": retrieve_result}):
            yield token  # 토큰 단위로 반환
    except Exception as e:
        yield f"오류가 발생했습니다: {str(e)}"


