@echo off
REM SADP AI Integration 실행 스크립트
REM Windows 배치 파일

echo ========================================
echo SADP AI Integration 시스템 시작
echo ========================================

echo [1/3] 가상환경 활성화...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo 가상환경 활성화 완료
) else (
    echo WARNING: 가상환경이 없습니다. install.bat를 먼저 실행하세요.
    echo 시스템 Python으로 실행을 시도합니다...
)

echo [2/3] 환경 설정 로드...
if exist .env (
    echo 환경 설정 파일 확인됨
) else (
    echo WARNING: .env 파일이 없습니다. 기본 설정으로 실행합니다.
)

echo [3/3] SADP API 서버 시작...
echo.
echo ========================================
echo 서버 시작 중...
echo ========================================
echo.
echo 접속 URL:
echo - API 문서: http://127.0.0.1:8000/docs
echo - 대체 문서: http://127.0.0.1:8000/redoc  
echo - 기본 페이지: http://127.0.0.1:8000/
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

REM UTF-8 인코딩 설정하여 실행
set PYTHONIOENCODING=utf-8
python src\api\api_server.py

echo.
echo ========================================
echo SADP 서버가 종료되었습니다.
echo ========================================
pause
