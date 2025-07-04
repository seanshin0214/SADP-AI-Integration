# GitHub 업로드 스크립트
# 리포지토리 생성 후 실행할 명령어들

# GitHub에서 리포지토리 생성 후 실행:
git remote add origin https://github.com/ginnov-tech/SADP-AI-Integration.git
git branch -M main  
git push -u origin main

# 또는 SSH 사용시:
# git remote add origin git@github.com:ginnov-tech/SADP-AI-Integration.git
# git branch -M main
# git push -u origin main

# 리포지토리 URL 확인:
git remote -v

# 브랜치 확인:
git branch -a

# 상태 확인:
git status
