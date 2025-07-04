@echo off
REM SADP AI Integration 테스트 스크립트

echo ========================================
echo SADP AI Integration 시스템 테스트
echo ========================================

echo [1/4] 가상환경 활성화...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: 가상환경 없음. 시스템 Python 사용
)

echo [2/4] 단위 테스트 실행...
echo.
set PYTHONIOENCODING=utf-8
python -m pytest tests/test_core_integration.py -v
if %errorlevel% neq 0 (
    echo ERROR: 테스트 실패가 있습니다.
) else (
    echo SUCCESS: 모든 테스트 통과!
)

echo.
echo [3/4] API 서버 연결 테스트...
echo 서버가 실행 중인지 확인합니다...

REM curl이 있는지 확인
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: curl이 설치되어 있지 않습니다.
    echo PowerShell을 사용하여 테스트합니다...
    
    powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 5; Write-Host 'API 서버 응답 성공:'; $response | ConvertTo-Json } catch { Write-Host 'API 서버가 실행되지 않거나 응답하지 않습니다.' }"
) else (
    echo curl을 사용하여 API 테스트...
    curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"
)

echo.
echo [4/4] 시스템 정보 수집...
echo Python 버전:
python --version

echo.
echo 설치된 패키지:
pip list | findstr -i "fastapi uvicorn pydantic"

echo.
echo ========================================
echo 테스트 완료!
echo ========================================
echo.
echo 문제가 있다면:
echo 1. install.bat 재실행
echo 2. run.bat으로 서버 시작 후 다시 테스트
echo 3. GitHub 이슈 보고: https://github.com/seanshin0214/SADP-AI-Integration/issues
echo.

pause
