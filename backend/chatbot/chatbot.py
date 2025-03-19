# backend/chatbot_2/chatbot.py

import numpy as np
from rank_bm25 import BM25Okapi
from konlpy.tag import Okt
import pickle
from FlagEmbedding import BGEM3FlagModel
import tritonclient.grpc.aio as grpcclient
from tqdm.asyncio import tqdm  # 비동기 tqdm 사용
import json
import os
import asyncio
import logging

# 글로벌 변수 초기화
emb_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
korean_tokenizer = Okt()
triton_client = None
retriever_dict = {}
logger = logging.getLogger(__name__)
# Retriever Class
class AnnouncementRetriever:
    def __init__(self, elements, emb_model, korean_tokenizer):
        """ RAG 리트리버 초기화 """
        self.elements = elements
        self.emb_model = emb_model
        self.korean_tokenizer = korean_tokenizer

        # BM25 설정
        self.chunks_with_title = [e['title'] + '\n' + e['markdown'] for e in self.elements]
        self.tokenized_chunks = [self.korean_tokenizer.morphs(chunk) for chunk in self.chunks_with_title]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

        # 제목 및 문서 임베딩 설정
        self.title_embeddings = np.array([e['title_emb'] for e in elements], dtype=np.float16)
        self.doc_embeddings = np.array([e['doc_emb'] for e in elements], dtype=np.float16)

        # 가중치 설정
        self.bm25_weights = 0.1
        self.title_similarity_weights = 0.2
        self.doc_similarity_weights = 0.7
        self.lower_bound = 0.5

    def get_bm25_scores(self, query):
        tokenized_query = self.korean_tokenizer.morphs(query)
        bm_scores = self.bm25.get_scores(tokenized_query)
        return bm_scores

    def get_similarity(self, query):
        query_embedding = self.emb_model.encode([query])['dense_vecs']
        title_sim = query_embedding @ self.title_embeddings.T
        doc_sim = query_embedding @ self.doc_embeddings.T
        return (title_sim, doc_sim)

    def min_max_normalize(self, scores):
        if scores.max() == scores.min():
            return np.array([0] * len(scores), dtype=np.float16)
        return (scores - scores.min()) / (scores.max() - scores.min())

    def get_rag_scores(self, query):
        bm25_scores = self.get_bm25_scores(query)
        sims = self.get_similarity(query)
        norm_bm25 = self.min_max_normalize(bm25_scores)
        norm_title = self.min_max_normalize(sims[0][0])
        norm_doc = self.min_max_normalize(sims[1][0])
        rag_scores = self.bm25_weights * norm_bm25 + \
                     self.title_similarity_weights * norm_title + \
                     self.doc_similarity_weights * norm_doc
        return rag_scores

    def get_retriever_results(self, query):
        rag_scores = self.get_rag_scores(query)
        arg_max_idx = rag_scores.argsort()[::-1]
        total_token_len = 0
        idx_with_order = []
        for idx in arg_max_idx:
            if rag_scores[idx] < self.lower_bound:
                break
            token_len = self.elements[idx]['token_len']
            order = self.elements[idx]['id']
            if total_token_len + token_len > 3000:
                break
            idx_with_order.append([order, idx])
            total_token_len += token_len
        idx_with_order.sort()
        cur_title = ''
        total_md_txt = ''
        for idx in idx_with_order:
            title = self.elements[idx[1]]['title']
            md_txt = self.elements[idx[1]]['markdown']
            if title != cur_title:
                total_md_txt = total_md_txt + '\n' + title + '\n'
                cur_title = title
            total_md_txt = total_md_txt + md_txt + '\n'
        return total_md_txt

# 요소 로드 함수 (동적으로 fileid를 받아 로드)
def get_elements(fileid):
    base_path = './backend/chatbot/preprocessed_data'
    file_path = os.path.join(base_path, fileid)  # 경로 생성
    print(f"Trying to load file: {file_path}")  # 디버깅용 출력
    with open(file_path, 'rb') as f:
        elements = pickle.load(f)
    return elements

# Prompt 생성 함수
def construct_prompt(question, retrieve_result):
    prompt_template = """
A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
NOTE:
- DO NOT use the Context to generate a response unless the user explicitly refers to it or asks about its content.
- If the user's input is unclear, incomplete, or nonsensical, respond politely by asking for clarification. Example: "질문이 명확하지 않습니다. 다시 한번 설명 부탁드립니다."
- If the user's input does not relate to the Context, answer only based on general knowledge.
- DO NOT generate answers unrelated to the user's question or intent.
- DO NOT include or create irrelevant content like tables, symbols, or lengthy explanations unless explicitly asked.
- ALWAYS ANSWER IN KOREAN.
Context: {input}
Human: {question}
Assistant:
"""
    return prompt_template.format(question=question, input=retrieve_result)

# Generation 요청 생성 함수
def create_generation_request(prompt, request_id):
    input_tensor = grpcclient.InferInput("text_input", [1], "BYTES")
    prompt_data = np.array([prompt.encode("utf-8")])
    input_tensor.set_data_from_numpy(prompt_data)

    stream_setting = grpcclient.InferInput("stream", [1], "BOOL")
    stream_setting.set_data_from_numpy(np.array([True]))

    # 샘플링 파라미터 추가
    sampling_parameters = {
        "max_tokens": 256,
        "temperature": 0.1,
        "top_p": 0.95,
        "repetition_penalty": 1.2,
    }
    sampling_parameters_input = grpcclient.InferInput("sampling_parameters", [1], "BYTES")
    sampling_parameters_data = np.array([json.dumps(sampling_parameters).encode("utf-8")], dtype=object)
    sampling_parameters_input.set_data_from_numpy(sampling_parameters_data)

    inputs = [input_tensor, stream_setting, sampling_parameters_input]

    output = grpcclient.InferRequestedOutput("text_output")
    outputs = [output]

    return {
        "model_name": "vllm_model",
        "inputs": inputs,
        "outputs": outputs,
        "request_id": request_id
    }

# 비동기 초기화 함수
async def async_init():
    global triton_client, retriever_dict

    url = "localhost:8001"  # Triton inference server URL
    print("Initializing Triton client...")
    triton_client = grpcclient.InferenceServerClient(url=url, verbose=False)
    await triton_client.is_server_ready()

    # 스크립트의 위치를 기준으로 절대 경로 설정
    base_path = os.path.join(os.path.dirname(__file__), '..', 'preprocessed_data')
    base_path = os.path.abspath(base_path)
    print(f"Loading preprocessed data from: {base_path}")  # 디버깅용 출력

    # 모든 retriever load (비동기적으로 파일 로드)
    try:
        files = os.listdir(base_path)
    except FileNotFoundError:
        print(f"Directory not found: {base_path}")
        raise

    retrievers = []
    for file in tqdm(files):
        # 파일 로드는 동기적으로 수행 (pickle은 동기적)
        elements = await asyncio.to_thread(get_elements, os.path.join(base_path, file))
        retriever = AnnouncementRetriever(elements=elements, emb_model=emb_model, korean_tokenizer=korean_tokenizer)
        retrievers.append((retriever, file))

    # file id와 retriever 객체들 mapping
    retriever_dict = {retrieve[1]: retrieve[0] for retrieve in retrievers}
    print("Initialization complete.")
    print("fycj")

# retrieve_and_generate 함수# retrieve_and_generate 함수
async def retrieve_and_generate(fileid, user_input):
    # Step 1: 동적으로 요소 로드 및 retriever 생성
    retriever = retriever_dict[fileid]

    # Step 2: Retrieve context using RAG retriever
    retrieve_result = retriever.get_retriever_results(user_input)
    logger.info(f"Retrieve result: {retrieve_result}")  # print 대신 logger 사용    
    # Step 3: Construct prompt for generation
    prompt = construct_prompt(user_input, retrieve_result)

    async def requests_gen():
        yield create_generation_request(prompt, "req-0")

    # 'await' 제거
    response_stream = triton_client.stream_infer(requests_gen())
    previous_output = ""
    full_output = ""
    # Step 4: Stream the response from Triton server
    async for response in response_stream:
        result, error = response
        if error:
            yield f"Error occurred! Details: {str(error)}"
        else:
            output = result.as_numpy("text_output")
            for i in output:
                decoded = i.decode("utf-8")

                # Remove prompt part if present
                if decoded.startswith(prompt):
                    decoded = decoded[len(prompt):]
                # Remove duplicate part from new output
                new_output = decoded[len(previous_output):]
                logger.debug(f"New output before spacing: '{new_output}'")

                # Update the previous output for tracking
                previous_output += new_output

                # 마크다운 줄바꿈 및 띄어쓰기 처리
                # 새로운 출력이 특정 문장으로 시작할 때 줄바꿈을 추가
                if full_output and not full_output.endswith(('\n', '<br>')):
                    # 예: 마침표, 느낌표, 물음표 등으로 끝나지 않으면 줄바꿈 추가
                    if full_output[-1] in ('.', '!', '?'):
                        new_output = '\n\n' + new_output
                    else:
                        new_output = ' ' + new_output
                else:
                    new_output = new_output

                # 강제 줄바꿈을 위해 <br> 태그 추가
                # 필요에 따라 특정 위치에 <br> 태그를 삽입할 수 있습니다.
                # 예시: 문장 끝에 <br> 추가
                if new_output.endswith(('.', '!', '?')):
                    new_output += '  \n'  # 마크다운에서 두 개의 공백과 엔터는 줄바꿈을 의미

                # full_output에 new_output 추가
                full_output += new_output
                logger.debug(f"New output after spacing: '{new_output}'")

                # 직접 청크를 반환
                yield new_output
    logger.debug(f"Final output with markdown: '{full_output}'")

    # 스트림 종료를 알리는 메시지
    yield "😃 이상 AIF LAB 이었습니다. \n 더 궁금하신점 있나요?"