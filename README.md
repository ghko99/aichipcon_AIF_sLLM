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
- **개인화된 임대주택 청약 공고문 추천**
- **공고문에 대한 질의응답(Q&A) 챗봇 서비스**

## 🧑‍💻 아키텍처
![ㅇㄹㅇ](https://github.com/user-attachments/assets/27b99a12-a6bf-4e4d-b5fa-ff9d33e29e15)

## 데이터 구축

## AI 모델 배포 환경
- RBLN-CA12 NPU
- RBLN-vLLM 서버 환경

## LH API 기반 공고문 검색 및 추천 시스템
![image](https://github.com/user-attachments/assets/c9f5488d-87b3-4788-aae9-b222fe8f1b1a)
![image](https://github.com/user-attachments/assets/11a22015-0da8-4d6e-ae0e-0f94f3b1b02b)
![image](https://github.com/user-attachments/assets/c873caa6-9ded-4185-9085-5aa6d661bad0)

## RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템
![image](https://github.com/user-attachments/assets/b2c556aa-6c5e-4e90-9d2a-ca85b6d8c5e0)
![image](https://github.com/user-attachments/assets/7d576ea4-3d20-4717-93b9-0cb0ee52f91e)
![image](https://github.com/user-attachments/assets/b8647bea-4bc5-468b-8558-d80ac733c7cf)

## 📈 성능 평가 (챗봇 답변 정확도 테스트)
- Auto-Evaluate (Allganize) 성능 측정: **182/300** (LangChain + GPT-4 Turbo 기준 183/300)
- 모델 최적화(QLoRA, Unsloth 활용) 수행
- 성능개선을 위한 하한선 및 가중치 탐색 최적화

## 🚀 모델 서빙 최적화
- KV Cache 적용
- Continuous Batching으로 초당 토큰 처리 속도 향상 (143 TPS 달성)
- Docker를 통한 Triton Inference Server 배포
- gRPC 기반 Streaming 서비스 구축
