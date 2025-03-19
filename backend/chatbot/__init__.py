
# import numpy as np
# from rank_bm25 import BM25Okapi
# from konlpy.tag import Okt
# import pickle
# from FlagEmbedding import BGEM3FlagModel
# import tritonclient.grpc.aio as grpcclient
# from tqdm.asyncio import tqdm  # 비동기 tqdm 사용
# import json
# import os
# import asyncio
# # 모델 및 토크나이저 초기화 (동기적으로 초기화 가능)
# emb_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
# korean_tokenizer = Okt()

# # 트리톤 클라이언트 초기화는 비동기로 수행해야 함
# triton_client = None  # 나중에 초기화

# # Retriever Class
# class AnnouncementRetriever:
#     def __init__(self, elements, emb_model, korean_tokenizer):
#         """ RAG 리트리버 초기화 """
#         self.elements = elements
#         self.emb_model = emb_model
#         self.korean_tokenizer = korean_tokenizer

#         # BM25 설정
#         self.chunks_with_title = [e['title'] + '\n' + e['markdown'] for e in self.elements]
#         self.tokenized_chunks = [self.korean_tokenizer.morphs(chunk) for chunk in self.chunks_with_title]
#         self.bm25 = BM25Okapi(self.tokenized_chunks)

#         # 제목 및 문서 임베딩 설정
#         self.title_embeddings = np.array([e['title_emb'] for e in elements], dtype=np.float16)
#         self.doc_embeddings = np.array([e['doc_emb'] for e in elements], dtype=np.float16)

#         # 가중치 설정
#         self.bm25_weights = 0.1
#         self.title_similarity_weights = 0.2
#         self.doc_similarity_weights = 0.7
#         self.lower_bound = 0.77

#     def get_bm25_scores(self, query):
#         tokenized_query = self.korean_tokenizer.morphs(query)
#         bm_scores = self.bm25.get_scores(tokenized_query)
#         return bm_scores

#     def get_similarity(self, query):
#         query_embedding = self.emb_model.encode([query])['dense_vecs']
#         title_sim = query_embedding @ self.title_embeddings.T
#         doc_sim = query_embedding @ self.doc_embeddings.T
#         return (title_sim, doc_sim)

#     def min_max_normalize(self, scores):
#         if scores.max() == scores.min():
#             return np.array([0] * len(scores), dtype=np.float16)
#         return (scores - scores.min()) / (scores.max() - scores.min())

#     def get_rag_scores(self, query):
#         bm25_scores = self.get_bm25_scores(query)
#         sims = self.get_similarity(query)
#         norm_bm25 = self.min_max_normalize(bm25_scores)
#         norm_title = self.min_max_normalize(sims[0][0])
#         norm_doc = self.min_max_normalize(sims[1][0])
#         rag_scores = self.bm25_weights * norm_bm25 + \
#                      self.title_similarity_weights * norm_title + \
#                      self.doc_similarity_weights * norm_doc
#         return rag_scores

#     def get_retriever_results(self, query):
#         rag_scores = self.get_rag_scores(query)
#         arg_max_idx = rag_scores.argsort()[::-1]
#         total_token_len = 0
#         idx_with_order = []
#         for idx in arg_max_idx:
#             if rag_scores[idx] < self.lower_bound:
#                 break
#             token_len = self.elements[idx]['token_len']
#             order = self.elements[idx]['id']
#             if total_token_len + token_len > 3000:
#                 break
#             idx_with_order.append([order, idx])
#             total_token_len += token_len
#         idx_with_order.sort()
#         cur_title = ''
#         total_md_txt = ''
#         for idx in idx_with_order:
#             title = self.elements[idx[1]]['title']
#             md_txt = self.elements[idx[1]]['markdown']
#             if title != cur_title:
#                 total_md_txt = total_md_txt + '\n' + title + '\n'
#                 cur_title = title
#             total_md_txt = total_md_txt + md_txt + '\n'
#         return total_md_txt

# # 요소 로드 함수 (동적으로 fileid를 받아 로드)
# def get_elements(fileid):
#     base_path = './backend/chatbot/preprocessed_data'
#     file_path = os.path.join(base_path, fileid)  # 경로 생성
#     print(f"Trying to load file: {file_path}")  # 디버깅용 출력
#     with open(file_path, 'rb') as f:
#         elements = pickle.load(f)
#     return elements

# # Prompt 생성 함수
# def construct_prompt(question, retrieve_result):
#     prompt_template = """
# A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
# NOTE:
# - DO NOT use the Context to generate a response unless the user explicitly refers to it or asks about its content.
# - If the user's input is unclear, incomplete, or nonsensical, respond politely by asking for clarification. Example: "질문이 명확하지 않습니다. 다시 한번 설명 부탁드립니다."
# - If the user's input does not relate to the Context, answer only based on general knowledge.
# - DO NOT generate answers unrelated to the user's question or intent.
# - DO NOT include or create irrelevant content like tables, symbols, or lengthy explanations unless explicitly asked.
# - ALWAYS ANSWER IN KOREAN.
# Context: {input}
# Human: {question}
# Assistant:
# """
#     return prompt_template.format(question=question, input=retrieve_result)

# # Generation 요청 생성 함수
# def create_generation_request(prompt, request_id):
#     input_tensor = grpcclient.InferInput("text_input", [1], "BYTES")
#     prompt_data = np.array([prompt.encode("utf-8")])
#     input_tensor.set_data_from_numpy(prompt_data)

#     stream_setting = grpcclient.InferInput("stream", [1], "BOOL")
#     stream_setting.set_data_from_numpy(np.array([True]))

#     # 샘플링 파라미터 추가
#     sampling_parameters = {
#         "max_tokens": 256,
#         "temperature": 0.1,
#         "top_p": 0.95,
#         "repetition_penalty": 1.2,
#     }
#     sampling_parameters_input = grpcclient.InferInput("sampling_parameters", [1], "BYTES")
#     sampling_parameters_data = np.array([json.dumps(sampling_parameters).encode("utf-8")], dtype=object)
#     sampling_parameters_input.set_data_from_numpy(sampling_parameters_data)

#     inputs = [input_tensor, stream_setting, sampling_parameters_input]

#     output = grpcclient.InferRequestedOutput("text_output")
#     outputs = [output]

#     return {
#         "model_name": "vllm_model",
#         "inputs": inputs,
#         "outputs": outputs,
#         "request_id": request_id
#     }

# # 비동기 초기화 함수
# async def async_init():
#     global triton_client, retriever_dict

#     url = "localhost:8001"  # Triton inference server URL
#     print("Initializing Triton client...")
#     triton_client = grpcclient.InferenceServerClient(url=url, verbose=False)
#     await triton_client.is_server_ready()

#     # 모든 retriever load (비동기적으로 파일 로드)
#     files = os.listdir('./backend/chatbot/preprocessed_data')
#     retrievers = []
#     for file in tqdm(files):
#         # 파일 로드는 동기적으로 수행 (pickle은 동기적)
#         elements = await asyncio.to_thread(get_elements, file)
#         retriever = AnnouncementRetriever(elements=elements, emb_model=emb_model, korean_tokenizer=korean_tokenizer)
#         retrievers.append((retriever, file))

#     # file id와 retriever 객체들 mapping
#     retriever_dict = {retrieve[1]: retrieve[0] for retrieve in retrievers}
#     print("Initialization complete.")

# # 모듈이 임포트될 때 자동으로 초기화하려면, 아래와 같이 asyncio를 사용하여 이벤트 루프에서 초기화를 수행할 수 있습니다.
# # 단, 이는 애플리케이션의 메인 이벤트 루프와 충돌할 수 있으므로 주의가 필요합니다.
# # 보통은 메인 애플리케이션에서 async_init을 호출하는 것이 좋습니다.

# # 예시로, 모듈 임포트 시 초기화 수행 (권장하지 않음)
# # asyncio.get_event_loop().run_until_complete(async_init())

# # 대신, 애플리케이션의 메인 코드에서 async_init을 호출하세요.
