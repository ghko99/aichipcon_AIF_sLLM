#guest@aif:~/main$ python3 -m backend.app
#비동기
#hypercorn backend.app:app --bind 0.0.0.0:5000

import sys
import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import asyncio
import numpy as np
import tritonclient.grpc.aio as grpcclient
import logging

# 현재 파일의 절대 경로를 얻은 후, 상위 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.search.search_2 import search
JSON_FILE_PATH = os.path.join(os.getcwd(), 'backend', 'search', 'announcements.json')

from backend.chatbot.chatbot import retrieve_and_generate, async_init  # async_init 추가
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
#로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/ex', methods=['POST', 'OPTIONS'])
def ex():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')  # 모든 도메인 허용
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        logger.info("OPTIONS request handled")
        return response, 200

    if request.method == 'POST':
        try:
            # 클라이언트로부터 메시지 데이터를 가져옴
            user_input = request.json.get('message', '')
            logger.info(f"POST request received: {user_input}")  # 메시지 로그 출력

            # 메시지가 없는 경우 400 에러 반환
            if not user_input:
                logger.warning("No message provided in request")
                return jsonify({"error": "No message provided"}), 400

            # 비동기 스트리밍 데이터를 동기적으로 실행하여 제너레이터 생성
            async def async_generate_stream():
                try:
                    async for output in retrieve_and_generate("51580934.pkl", user_input):
                        yield f"data: {output}\n\n"  # SSE 포맷으로 데이터 전송
                except Exception as e:
                    logger.error(f"Error during async generation: {e}")
                    yield f"data: [ERROR] {str(e)}\n\n"  # 오류 메시지도 SSE로 전송

            # 동기적 제너레이터로 변환
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            stream = loop.run_until_complete(asyncio.gather(async_generate_stream()))

            # 실제로는 아래와 같이 동기적으로 데이터를 가져와 제너레이터를 생성해야 합니다.
            # 하지만 이는 복잡하고 비효율적일 수 있습니다.

            # 아래는 간단한 예제로, 실제 비동기 스트리밍을 동기적으로 처리하는 것은 권장되지 않습니다.
            # 보다 안정적인 방법은 비동기 프레임워크로 전환하는 것입니다.
            # 따라서, 이 방법보다는 방법 2를 권장합니다.

            return Response(
                stream_with_context(stream),
                content_type='text/event-stream'
            )

        except Exception as e:
            # 오류 발생 시 500 응답 반환
            logger.error(f"Error occurred: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
async def initialize_app():
    """
    애플리케이션 초기화 함수.
    비동기 초기화를 수행한 후 Flask 앱을 실행합니다.
    """
    await async_init()  # 비동기 초기화 함수 호출
    # Flask 앱을 실행합니다. 호스트와 포트는 필요에 따라 조정하세요.
    app.run(host='0.0.0.0', port=5000,debug=True, use_reloader=False)


@app.route('/survey', methods=['GET', 'POST', 'OPTIONS'])
def survey():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    
    if request.method == 'POST':
        data = request.json
        app.logger.info("Received data: %s", data)
        try:
            app.logger.info("Search start")
            app.logger.info("\n\n\n")
            result = search(data)
            app.logger.info("Search result: %s", result)
            return jsonify({'status': 'success', 'message': 'Survey data received.', 'result': result}), 200
        except Exception as e:
            app.logger.error("Error in search function: %s", str(e))
            return jsonify({'status': 'error', 'message': 'Failed to process data.'}), 500
    
    return jsonify({'status': 'GET method reached'}), 200

@app.route('/dashboard', methods=['GET', 'POST', 'OPTIONS'])
def get_announcements():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    elif request.method == 'GET':
        try:
            # JSON 파일 읽기
            if os.path.exists(JSON_FILE_PATH):
                with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    app.logger.info("Announcements data: %s", data)
                    return jsonify(data), 200  # JSON 데이터 반환
            else:
                return jsonify({'error': 'JSON 파일이 존재하지 않습니다.'}), 404
        except Exception as e:
            app.logger.error("Error reading JSON file: %s", str(e))
            return jsonify({'error': f'JSON 파일을 읽는 중 오류 발생: {str(e)}'}), 500

    elif request.method == 'POST':
        # POST 요청 처리 필요 시 추가
        return jsonify({'status': 'POST method not implemented'}), 501

    else:
        return jsonify({'error': 'Invalid request method'}), 405


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000,debug=True, use_reloader=False)
    asyncio.run(initialize_app())




