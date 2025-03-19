#!/bin/bash

# 첫 번째 터미널 프롬프트에서 명령어 실행
gnome-terminal -- bash -c "cd main/frontend && npm run dev; exec bash"

# 두 번째 터미널 프롬프트에서 명령어 실행
gnome-terminal -- bash -c "cd main/backend && uvicorn app:app --host 0.0.0.0 --port 5000 --reload; exec bash"

# 세 번째 터미널 프롬프트에서 명령어 실행
gnome-terminal -- bash -c "cd main && sudo docker ps && sudo docker exec -it 5919bd36a0bc /bin/bash -c 'tritonserver --model-repository /opt/tritonserver/python_backend/examples/rbln'; exec bash"

# 각 프롬프트가 독립적인 터미널 창에서 실행됩니다.
