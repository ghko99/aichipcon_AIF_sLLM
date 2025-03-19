# ✨ AI 기반 개인화 임대주택 청약 챗봇 서비스 ✨

## 🎯 프로젝트 개요

본 프로젝트는 **제1회 AI 반도체 기술 인재선발 대회**에 출품된 작품으로, LH 임대주택 청약 고객을 위한 맞춤형 추천 및 질의응답 챗봇 시스템입니다. 금융데이터와 LH 공고문 데이터를 활용하여 개인화된 추천과 빠른 정보 검색을 제공합니다.

## 👥 팀원
| 이름 | 역할 |
|-------|-------|
| 박진감 | AI 모델 튜닝 및 RAG 구현 |
| 신광훈 | 데이터 전처리, 데이터 구축 |
| 권태형 | 데이터 증강, AI 모델 서빙 |
| 고강희 | PM, 프로젝트 매니지먼트 |


## ⚙️ 주요 기능
- **개인화된 임대주택 청약 추천**
- **RAG 기반의 공고문 검색 및 추천**
- **공고문에 대한 질의응답(Q&A) 챗봇 서비스**


## 🧑‍💻 아키텍처
- AI 모델 학습 및 배포
  - RBLN-CA12 NPU
  - RBLN-vLLM 서버 환경

- **RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템**
  - LH API를 이용한 공고 데이터 자동 수집
  - BAAI/bge-m3을 활용한 데이터 Embedding 및 Title Tagging, Chunking
  - Retrieval 성능 최적화를 위한 Chunk 단위 Embedding
  - yanolja/EEVE-Korean-Instruct-10.8aB-v1.0 활용

## 🔍 검색 엔진
- 고객 정보 기반 임대 주택 유형 필터링
- 고객 요구 기반 특정 공고 필터링

## 📈 성능 평가
- Auto-Evaluate (Allganize) 성능 측정: **182/300** (LangChain + GPT-4 Turbo 기준 183/300)
- 모델 최적화(QLoRA, Unsloth 활용) 수행
- 성능개선을 위한 하한선 및 가중치 탐색 최적화

## 🚀 모델 서빙 최적화
- KV Cache 적용
- Continuous Batching으로 초당 토큰 처리 속도 향상 (143 TPS 달성)
- Docker를 통한 Triton Inference Server 배포
- gRPC 기반 Streaming 서비스 구축

## 🛠 기술 스택
<div align="center">
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

## 🛠 도구 및 환경
<div align="center">
  <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=VisualStudioCode&logoColor=white" />
  <img src="https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=Anaconda&logoColor=white" />
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white" />
</div>

## 📫 Contact
<div align="center">
  <a href="https://velog.io/@khko99/posts" target="_blank">
    <img src="https://img.shields.io/badge/Velog-20C997?style=for-the-badge&logo=Velog&logoColor=white" />
  </a>
  <a href="https://huggingface.co/khko99" target="_blank">
    <img src="https://img.shields.io/badge/Hugging%20Face-FFD21F?style=for-the-badge&logo=huggingface&logoColor=white" />
  </a>
  <a href="mailto:khko99@inha.edu">
    <img src="https://img.shields.io/badge/Mail-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
</div>

<br />

<div align="center">
  <strong>🚀Thank you for visiting! 😄</strong><br />
  <sub>Feel free to explore my repositories and leave feedback!</sub>
</div>

