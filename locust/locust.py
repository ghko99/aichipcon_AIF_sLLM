# 실행1 (백엔드 켜기) : guest@aif:~/main/backend$ uvicorn app:app --host 0.0.0.0 --port 5000 --reload
# 실행2 (locust 실행) : guest@aif:~/main/locust$ locust -f locust.py
# 실행3 (웹 UI 접속) : http://localhost:8089/

from locust import HttpUser, task, between
import json

class ChatbotApiTest(HttpUser):
    wait_time = between(1, 2)  # 요청 사이의 대기 시간 (초)
    host = "http://localhost:5000"  # Flask API 서버 주소

    @task
    def ask_question(self):
        # 주택청약에 대한 질문
        data = {
            "message": "주택청약에 대해서 설명해줘"
        }

        # 주택청약에 대한 요청을 /ex 엔드포인트에 보냄
        response = self.client.post("/ex", json=data, stream=True)

        # 응답 처리
        if response.status_code == 200:
            print("응답 받음:", response.text)
        else:
            print("요청 실패:", response.status_code)

    @task
    def survey(self):
        # 설문 데이터 예시
        survey_data = {
            "birthDate": "1997-10-14",
            "enrolledUniversity": False,
            "jobSeeking": True,
            "familyMembersCount": 4,
            "married": True,
            "marriageDate": "2019-11-01",
            "dualIncome": False,
            "hasChildren": True,
            "childrenCount": 2,
            "youngestChildBirthDate": "2023-10-09",
            "singleParent": False,
            "monthlyIncome": 1500000,
            "householdMonthlyIncome": 4000000,
            "ownHouse": False,
            "assets": 340000000,
            "ownCar": True,
            "carPrice": 30000000,
            "hasSubscriptionAccount": True,
            "subscriptionStartDate": "2020-10-09",
            "subscriptionPaymentCount": 30,
            "subscriptionPaymentAmount": 10000000,
            "region": "강원특별자치도",
            "status": "공고중",
            "startDate": "2023.11.08",
            "endDate": "2024.11.08"
        }

        # 설문 데이터를 /survey 엔드포인트에 보냄
        response = self.client.post("/survey", json=survey_data)

        # 설문 응답 처리
        if response.status_code == 200:
            print("설문 응답 성공:", response.text)
        else:
            print("설문 응답 실패:", response.status_code)
