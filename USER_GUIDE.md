# SADP AI Integration 사용자 가이드

## 🚀 빠른 시작

### 1. 설치
```bash
# 리포지토리 클론
git clone https://github.com/seanshin0214/SADP-AI-Integration.git
cd SADP-AI-Integration

# Windows에서 설치
install.bat

# 또는 수동 설치
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 실행
```bash
# Windows에서 실행
run.bat

# 또는 수동 실행
python src\api\api_server.py
```

### 3. 접속
- **API 문서**: http://127.0.0.1:8000/docs
- **대체 문서**: http://127.0.0.1:8000/redoc
- **기본 페이지**: http://127.0.0.1:8000/

## 📋 주요 기능

### AI 에이전트 관리
- **Claude AI**: 전략 수립, 문서화, 프로젝트 관리
- **Cursor AI**: 코드 개발, 최적화, 테스트
- **Figma AI**: UI/UX 디자인, 프로토타입

### 협업 모드
1. **Sequential**: 순차적 협업 (Claude → Figma → Cursor)
2. **Parallel**: 병렬 협업 (동시 실행)
3. **Interactive**: 상호작용 협업 (여러 라운드)
4. **Autonomous**: 자율 협업 (AI가 계획 수립)

## 🔧 API 사용법

### 1. 시스템 상태 확인
```bash
GET /health
```

### 2. AI 에이전트 목록 조회
```bash
GET /agents
```

### 3. 협업 세션 시작
```bash
POST /collaborate
Content-Type: application/json

{
  "title": "GERI 교육 플랫폼 개발",
  "description": "AI 기반 교육 혁신 플랫폼 구축",
  "mode": "sequential",
  "participants": ["claude", "figma_ai", "cursor_ai"],
  "requirements": {
    "skills": ["전략", "디자인", "개발"],
    "quality_standard": 90
  },
  "priority": "high"
}
```

### 4. 협업 상태 조회
```bash
GET /collaborate/{collaboration_id}
```

### 5. 성과 지표 확인
```bash
GET /metrics
```

## 🎓 교육적 활용

### 학생 실습 예제
1. **AI 협업 체험**:
   ```bash
   # 간단한 웹사이트 개발 협업
   POST /collaborate
   {
     "title": "학생 포트폴리오 웹사이트",
     "mode": "sequential",
     "participants": ["claude", "figma_ai", "cursor_ai"]
   }
   ```

2. **프로젝트 관리 학습**:
   ```bash
   # 프로젝트 진행 상황 모니터링
   GET /metrics
   GET /collaborate
   ```

3. **API 개발 실습**:
   ```bash
   # 개별 AI 에이전트에게 작업 할당
   POST /agents/claude/task
   {
     "title": "마케팅 전략 수립",
     "description": "신제품 출시 전략 문서화",
     "priority": "medium"
   }
   ```

### 연구 활용
- **AI 협업 효과성 분석**: `/metrics` 엔드포인트 데이터 활용
- **충돌 해결 패턴 연구**: `/conflicts` 엔드포인트 데이터 분석
- **다중 AI 시스템 성능 측정**: 실시간 모니터링 데이터

## ⚙️ 설정

### 환경 변수 (.env 파일)
```bash
# 서버 설정
HOST=127.0.0.1
PORT=8000
DEBUG=true

# AI API 키 (선택사항)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# GERI 설정
ORGANIZATION_NAME=GERI
PROJECT_NAME=SADP AI Integration
ADMIN_EMAIL=sshin@geri.kr
```

### 고급 설정
- **데이터베이스**: SQLite (기본) 또는 PostgreSQL
- **캐싱**: Redis (선택사항)
- **로깅**: 파일 또는 콘솔
- **보안**: API 키, 토큰 설정

## 🛠️ 문제 해결

### 자주 발생하는 문제
1. **서버 시작 실패**:
   ```bash
   # 포트 충돌 확인
   netstat -ano | findstr :8000
   
   # 다른 포트 사용
   set PORT=8001
   python src\api\api_server.py
   ```

2. **인코딩 오류**:
   ```bash
   # UTF-8 인코딩 설정
   set PYTHONIOENCODING=utf-8
   ```

3. **의존성 오류**:
   ```bash
   # 의존성 재설치
   pip install --upgrade -r requirements.txt
   ```

### 로그 확인
- **API 로그**: 콘솔 출력 확인
- **시스템 로그**: `sadp.log` 파일 확인
- **에러 로그**: 브라우저 개발자 도구 확인

## 📞 지원

### GERI 지원팀
- **이메일**: sshin@geri.kr
- **GitHub**: https://github.com/seanshin0214/SADP-AI-Integration
- **이슈 보고**: [GitHub Issues](https://github.com/seanshin0214/SADP-AI-Integration/issues)

### 커뮤니티
- **교육 기관 협력**: GERI 파트너십 프로그램
- **연구 협력**: JSIC 국제대학 연구 네트워크
- **오픈소스 기여**: MIT 라이선스 하에 자유롭게 활용

## 📚 추가 학습 자료

### 기술 문서
- **FastAPI**: https://fastapi.tiangolo.com/
- **AI 협업 이론**: GERI 연구 논문
- **다중 에이전트 시스템**: 관련 학술 자료

### 교육 과정
- **GERI AI 교육 프로그램**: AI 협업 전문가 과정
- **JSIC 국제대학**: AI 융합 학과 커리큘럼
- **온라인 튜토리얼**: SADP 활용 실습 과정

---

**© 2025 GERI (Global Education Research Institute)**  
**Created by: Sean K.S. Shin**  
**License: MIT**
