#    uvicorn app:app --host 0.0.0.0 --port 5000 --reload
import sys
import os
import asyncio
import logging
import json

from fastapi import FastAPI, Request, Response, status, HTTPException ,Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 현재 파일의 절대 경로를 얻은 후, 상위 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.search.search_3 import search
from backend.chatbot.chatbot import retrieve_and_generate, async_init  # async_init 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 모든 출처에 대해 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시 비동기 초기화 함수 실행
    """
    await async_init()
    logger.info("Application startup complete.")

@app.post("/ex")
async def ex(
    request: Request,
    file_id: str = Query(..., description="ID of the file to process (e.g., '59421911')")
    ):
    try:
        # 클라이언트로부터 메시지 데이터를 가져옴
        data = await request.json()
        user_input = data.get('message', '')
        logger.info(f"POST /ex 요청 받음: {file_id,user_input}")  # 로그 추가

        # 메시지가 없는 경우 400 에러 반환
        if not user_input:
            logger.warning("No message provided in request")
            raise HTTPException(status_code=400, detail="No message provided")

        async def async_generate_stream():
            try:
                if file_id == None:
                    file_id_pkl = "51580934.pkl"
                file_id_pkl = f"{file_id}.pkl"
                async for output in retrieve_and_generate(file_id_pkl, user_input):
                    logger.info(f"POST /ex 응답 받음: |{output}|")  # 로그 추가
                    # yield f"data: {output}\n\n"
                    yield f"data: {json.dumps(output, ensure_ascii=False)}\n\n"

            except Exception as e:
                logger.error(f"Error during async generation: {e}")
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(
            async_generate_stream(),
            media_type='text/event-stream'
        )

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/survey")
async def survey(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received data: {data}")

        logger.info("Search start")
        result = search(data)
        logger.info(f"Search result: {result}")

        return JSONResponse(content={'status': 'success', 'message': 'Survey data received.', 'result': result})

    except Exception as e:
        logger.error(f"Error in search function: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process data.")

@app.get("/dashboard")
async def get_announcements():
    try:
        # 현재 파일의 위치를 기준으로 JSON 파일 경로 생성
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_FILE_PATH = os.path.join(BASE_DIR, 'search', 'announcements.json')
        # JSON 파일 읽기
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Announcements data: {data}")
                return JSONResponse(content=data)
        else:
            logger.error("JSON 파일이 존재하지 않습니다.")
            raise HTTPException(status_code=404, detail="JSON 파일이 존재하지 않습니다.")

    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"JSON 파일을 읽는 중 오류 발생: {str(e)}")

# 필요에 따라 추가적인 설정이나 라우트를 정의할 수 있습니다.

# 애플리케이션 실행 부분은 별도의 파일에서 실행하거나, 아래와 같이 uvicorn을 통해 실행할 수 있습니다.
# 이 부분은 실제 운영 환경이나 개발 환경에 따라 조정됩니다.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        reload=True  # 개발 환경에서 코드 변경 시 자동으로 서버를 재시작하도록 합니다.
        )