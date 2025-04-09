# ✨ LH 임대주택청약 고객 맞춤형 추천 및 챗봇서비스 ✨

## 🎯 프로젝트 개요

본 프로젝트는 **제1회 AI 반도체 기술 인재선발 대회**에 출품된 작품으로, LH 임대주택 청약 고객을 위한 맞춤형 추천 및 질의응답 챗봇 시스템입니다. 금융데이터와 LH 공고문 데이터를 활용하여 개인화된 추천과 빠른 정보 검색을 제공합니다.

## 👥 팀원
| 이름 | 역할 |
|-------|-------|
| 박진감 | 프로젝트 기획 및 총괄, 웹 풀스택 |
| 신광훈 | 데이터 전처리, 데이터 증강, PM |
| 권태형 | 데이터 구축, AI 모델 서빙 |
| 고강희 | AI 모델 튜닝 및 RAG 구현 |


## ⚙️ 주요 기능
### **개인화된 임대주택 청약 공고문 추천**
![KAIT-ezgif com-speed](https://github.com/user-attachments/assets/27372b38-74ec-4042-a98c-53051044deb1)
### **공고문에 대한 질의응답(Q&A) 챗봇 서비스**
![KAIT-ezgif com-speed (1)](https://github.com/user-attachments/assets/3a0ab255-c3f0-4482-9d58-5f18ce7bff88)


## 🧑‍💻 아키텍처
![ㅇㄹㅇ](https://github.com/user-attachments/assets/27b99a12-a6bf-4e4d-b5fa-ff9d33e29e15)
- **최소 서비스 사양**: 초당 처리 요청 수(TPS)는 20 이상 유지되도록 설계됨
- **RBLN 리소스 활용**: RBLN의 NPU 서버 및 sLLM [(EEVE-Korean-Instruct-10.8B-v1.0)](https://huggingface.co/yanolja/EEVE-Korean-Instruct-10.8B-v1.0) 모델 활용으로 서비스 효율성 극대화

### 🌐 기술 스택 선정
<div align="center">
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=Next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/gRPC-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Triton%20Server-19C3EF?style=for-the-badge&logo=nvidia&logoColor=white" />
  <br />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white" />
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=NumPy&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=Matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Transformers-FFD21F?style=for-the-badge&logo=huggingface&logoColor=white" />
</div>

#### 📌 프론트엔드
- **Next.js**: SEO에 유리한 SSR(Server Side Rendering)과 빠른 페이지 로딩 속도, React 기반으로 높은 유지 보수성 보장

#### 🔧 백엔드
- **FastAPI**: 고성능, 비동기 처리가 가능하며, RAG 기반 공고문 분석 및 챗봇 서비스 구현에 최적화
- **gRPC 기반 비동기 통신**: 토큰 단위로 효율적인 실시간 데이터 전송을 지원하여 서비스 응답 속도 향상

#### 🚀 AI 서버
- **RBLN-CA12** NPU
- **Triton Server**: RBLN-vllm 모델을 기반으로 GPU 연산 효율화 및 Continuous-batching, KV Cache 등의 최적화 기술 적용
## 🔍 LH API 기반 공고문 검색 및 추천 시스템
![image](https://github.com/user-attachments/assets/c9f5488d-87b3-4788-aae9-b222fe8f1b1a)
![image](https://github.com/user-attachments/assets/11a22015-0da8-4d6e-ae0e-0f94f3b1b02b)
![image](https://github.com/user-attachments/assets/c873caa6-9ded-4185-9085-5aa6d661bad0)
>프론트엔드에서 고객이 설문을 통해 입력한 개인 및 가구 정보를 기반으로, LH의 임대주택 유형별 소득과 자산 기준을 우선 적용하여 적합한 임대 유형을 필터링한 뒤, 다시 고객이 원하는 지역, 공고 상태, 기간 등 세부 조건을 추가로 필터링하여 최종적으로 고객에게 가장 적합한 맞춤형 공공임대주택 공고 리스트를 추천합니다. 또한 공고 데이터가 많고 파일 형태가 다양하여 정확히 공고명을 포함한 공고문만을 빠르게 추출 및 저장하기 위해 병렬 처리를 적용하였습니다.
## 💬 RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템
![image](https://github.com/user-attachments/assets/b2c556aa-6c5e-4e90-9d2a-ca85b6d8c5e0)
![image](https://github.com/user-attachments/assets/7d576ea4-3d20-4717-93b9-0cb0ee52f91e)
![image](https://github.com/user-attachments/assets/b8647bea-4bc5-468b-8558-d80ac733c7cf)
>시스템은 비정형 PDF 형태의 공고문을 효율적으로 처리하기 위해 먼저 Upstage Document Parse API를 활용하여 문서를 문장, 단락, 제목과 같은 Element 단위로 정확하게 나누고, 각 Element에 Title을 태그하여 Chunk 단위로 저장합니다. 저장된 Chunk들은 한국어에 특화된 BAAI/bge-m3 임베딩 모델로 변환되어 Vector DB에 저장되며, LH API를 활용해 새로 등록되는 공고문을 자동으로 전처리합니다. 사용자의 질의가 발생하면, 질의문을 동일한 임베딩 모델로 변환하고, Semantic search와 BM25 기반의 Lexical search를 결합한 하이브리드 검색을 통해 최적의 Chunk들을 선별하여, 원본 공고문의 순서에 맞게 재정렬 후 최종 Context를 구성합니다. 마지막으로 구성된 Context와 사용자의 질의를 결합한 Prompt를 한국어 지시문에 최적화된 EEVE-Korean-Instruct 모델(sLLM)에 입력하여 사용자에게 자연스럽고 정확한 답변을 제공합니다.
## 🗃️ 데이터 구축
![image](https://github.com/user-attachments/assets/e1ec0aed-e879-4d7b-9324-f942cba20a02)
![image](https://github.com/user-attachments/assets/5baf1def-09b0-4dcf-846e-1d7979431be7)
![image](https://github.com/user-attachments/assets/c00b403c-74cf-4c74-b3ea-99dbe832346b)
>데이터 구축 단계는 원시 데이터 수집, 1차 검수, 데이터 정제, 2차 검수, 데이터 증강, 최종 검수의 총 6단계로 구성됩니다. 먼저 주택 청약 도메인 특화 질의응답 모델 학습을 위해 일반적인 주택 청약 관련 질문(QA)과 공고문 기반의 상세 질문-컨텍스트-답변(QCA) 데이터 두 가지를 수집했습니다. 일반 QA 데이터는 국토교통부의 FAQ 및 자체 수집한 데이터를 포함했으며, QCA 데이터는 실제 공고문을 Markdown으로 변환하고 GPT-4로 질문과 답변을 자동 생성해 확보했습니다. 원시 데이터 약 2200만 어절을 확보한 후 저작권, 중복, 유해성 및 개인정보 검수를 통해 약 2000만 어절로 정제했습니다. 이후 GPT 및 DeepL을 활용한 역번역으로 4배 증강한 뒤, 순서 변경·삭제·치환·TF-IDF 기반 등의 규칙 기반 증강으로 추가 4배, 총 16배 규모의 약 3억 어절의 고품질 데이터를 구축했습니다. 최종 품질 검수 단계에서는 네이버 맞춤법 검사기(py-hanspell)를 활용한 맞춤법·띄어쓰기 검사와, cosine_similarity 라이브러리를 통한 코사인 유사도 검사를 실시하여 문법적 정확성과 데이터 중복 문제를 철저히 관리하였습니다.
## ⚙️ RAG 성능 고도화
### Passage Filtering & Retrieval Score Weight Optimization
![image](https://github.com/user-attachments/assets/b8128424-10b2-4897-89dc-0abd93aff55d)
>Retrieval 단계에서 정확성을 높이기 위해 Passage filtering과 Retrieval Score Weight 최적화를 진행했습니다. Passage filtering 단계에서는 검색 결과에 대한 하한선(Lower bound)을 설정하고, QCA 데이터셋을 활용하여 Retrieval score를 0부터 0.01 단위로 증가시키며 실험한 결과, Retrieval Score가 0.77일 때 가장 좋은 성능을 보였습니다. 또한, BM25 score의 비중이 지나치게 높아 주요 정보가 검색되지 않는 문제를 해결하기 위해, BM25, Title similarity, Element similarity의 가중치를 조정했습니다. 세 요소의 가중치를 각각 0.1 단위로 조정하여 최적화를 진행한 결과, BM25 : Title similarity : Element similarity가 0.1 : 0.2 : 0.7의 비율일 때 Retrieval 성능이 가장 우수한 것으로 확인되었습니다.

### Fine-tuning
![image](https://github.com/user-attachments/assets/3fb5e69c-2e64-43f3-bf8d-01c62c4f06d9)
>답변 생성 성능을 향상시키기 위해, 구축된 약 3억 어절 규모의 주택 청약 특화 QCA 및 QA 데이터셋을 활용하여, A100 GPU 환경에서 1 epoch 동안 모델 Fine-tuning을 수행하였습니다. 이를 통해 모델이 주택 청약 도메인에 최적화된 자연스러운 답변을 생성할 수 있도록 성능을 고도화하였습니다.

### RAG 성능 고도화 이후 RAGAS 성능 평가
![image](https://github.com/user-attachments/assets/6081eec5-9600-4294-a56d-fa0906272d18)

## 🚀 모델 서빙 최적화
![image](https://github.com/user-attachments/assets/3307291b-c708-496e-b8a8-eee21c6286da)
>답변 생성 성능 향상을 위해, 리벨리온 ATOM NPU를 탑재한 Triton Inference 서버를 활용하여 EEVE 모델을 서빙하였고, vLLM을 통해 Continuous Batching과 비동기 실시간 스트리밍 기능을 적용했습니다. 이를 통해 고객의 요청 데이터를 실시간으로 처리하고 즉시 응답함으로써 빠르고 정확한 챗봇 응답을 제공할 수 있었습니다. 또한 병렬 처리를 위해 최대 batch size를 8로 설정하고 8개의 입력 프롬프트에 대해 테스트한 결과, 초당 143개의 토큰이 생성되는 우수한 성능을 확인하였습니다. 이를 통해 ATOM NPU 기반의 Triton 서버 및 vLLM 환경에서 다수의 요청도 원활히 처리하는 고성능 시스템을 구축했습니다.

## 📈 성능 평가 (챗봇 답변 정확도 테스트)
![image](https://github.com/user-attachments/assets/eafae086-b4be-402c-9727-3f49438b40ec)
- [Auto-Evaluate (Allganize)](https://colab.research.google.com/drive/1c9hH429iAqw4xkgKoQq1SC9f_4p_nwcc?usp=sharing) 성능 측정: **182/300** (LangChain + GPT-4 Turbo 기준 183/300)
>Open Source sLLM 모델을 자체 튜닝해 LangChain + GPT-4 Turbo 프레임 워크 시스템의 RAG와 거의 동일한 수준의 성능을 기록했습니다.
## 📈 성능 평가 (챗봇 서버 처리량 테스트 - Locust)
![image](https://github.com/user-attachments/assets/c778eada-1748-490c-a3d4-d0d7432e293f)
## 📈 성능 평가 (챗봇 서버 속도 테스트 - Locust)
![image](https://github.com/user-attachments/assets/ac79c53a-71d8-40f6-a8aa-503932e2051b)

## 🔗 Links
[AI 반도체 기술인재 선발대회](https://www.aichipcon.or.kr/main)

