# ✨ LH 임대주택청약 고객 맞춤형 추천 및 챗봇서비스 ✨

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

- RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템
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
