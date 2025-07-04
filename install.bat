@echo off
REM SADP AI Integration 설치 스크립트
REM Windows 배치 파일

echo ========================================
echo SADP AI Integration 시스템 설치
echo ========================================

echo [1/5] Python 버전 확인...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python이 설치되어 있지 않습니다.
    echo Python 3.11 이상을 설치해주세요: https://python.org
    pause
    exit /b 1
)

echo [2/5] 가상환경 생성...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: 가상환경 생성 실패
    pause
    exit /b 1
)

echo [3/5] 가상환경 활성화...
call venv\Scripts\activate.bat

echo [4/5] 의존성 설치...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: 의존성 설치 실패
    pause
    exit /b 1
)

echo [5/5] 환경 설정 확인...
if not exist .env (
    echo 기본 환경 설정 파일이 준비되었습니다.
) else (
    echo 환경 설정 파일이 이미 존재합니다.
)

echo.
echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo 다음 단계:
echo 1. run.bat 실행하여 서버 시작
echo 2. 브라우저에서 http://127.0.0.1:8000/docs 접속
echo 3. API 테스트 및 사용
echo.
echo GERI/JSIC 교육 혁신을 위한 SADP 시스템을 즐겨보세요!
echo.

pause
