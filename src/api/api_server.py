"""
SADP API Server
Smart AI Development Platform REST API 엔드포인트

Author: Sean K.S. Shin (GERI)
Created: 2025-07-04
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import uvicorn

# SADP 모듈 import
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.sadp_core import SADPCore, CollaborationRequest, CollaborationMode, Priority

# FastAPI 앱 초기화
app = FastAPI(
    title="SADP AI Integration API",
    description="Smart AI Development Platform - Multi-Agent Collaboration System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SADP Core 인스턴스
sadp_core = SADPCore()

# Pydantic 모델 정의
class CollaborationRequestModel(BaseModel):
    title: str
    description: str
    mode: str  # sequential, parallel, interactive, autonomous
    participants: List[str]
    requirements: Dict[str, Any] = {}
    deadline: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high, critical

class TaskModel(BaseModel):
    title: str
    description: str
    agent: str
    priority: str = "medium"
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}

class AgentStatusResponse(BaseModel):
    agent: str
    status: str
    capabilities: List[str]
    active_tasks: int
    last_activity: str

class CollaborationResponse(BaseModel):
    id: str
    status: str
    participants: Dict[str, Any]
    results: Dict[str, Any]
    duration: Optional[float]
    created_at: str

# API 엔드포인트
@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "SADP AI Integration API",
        "version": "1.0.0",
        "status": "active",
        "documentation": "/docs",
        "core_system": "ready"
    }

@app.get("/health")
async def health_check():
    """시스템 상태 확인"""
    try:
        status = sadp_core.get_system_status()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System unhealthy: {str(e)}")

@app.get("/agents", response_model=List[AgentStatusResponse])
async def get_agents():
    """등록된 AI 에이전트 목록 조회"""
    try:
        agents_info = []
        for agent_name, agent in sadp_core.agents.items():
            agent_info = AgentStatusResponse(
                agent=agent_name,
                status="ready",
                capabilities=agent.capabilities,
                active_tasks=len(getattr(agent, 'active_tasks', [])),
                last_activity=datetime.now().isoformat()
            )
            agents_info.append(agent_info)
        
        return agents_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agents: {str(e)}")

@app.get("/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """특정 AI 에이전트 상세 정보"""
    if agent_name not in sadp_core.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        agent = sadp_core.agents[agent_name]
        
        if hasattr(agent, 'get_status_report'):
            report = agent.get_status_report()
        elif hasattr(agent, 'get_performance_report'):
            report = agent.get_performance_report()
        elif hasattr(agent, 'get_design_report'):
            report = agent.get_design_report()
        else:
            report = {
                "agent": agent_name,
                "capabilities": agent.capabilities,
                "status": "ready"
            }
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent details: {str(e)}")

@app.post("/collaborate", response_model=CollaborationResponse)
async def start_collaboration(request: CollaborationRequestModel, background_tasks: BackgroundTasks):
    """새로운 협업 세션 시작"""
    try:
        # 요청 변환
        collaboration_request = CollaborationRequest(
            id=f"api_collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=request.title,
            description=request.description,
            mode=CollaborationMode(request.mode),
            participants=request.participants,
            requirements=request.requirements,
            deadline=request.deadline,
            priority=Priority[request.priority.upper()],
            created_at=datetime.now()
        )
        
        # 백그라운드에서 협업 실행
        background_tasks.add_task(execute_collaboration_background, collaboration_request)
        
        # 즉시 응답 반환 (비동기 처리)
        return CollaborationResponse(
            id=collaboration_request.id,
            status="initiated",
            participants={},
            results={},
            duration=None,
            created_at=collaboration_request.created_at.isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start collaboration: {str(e)}")

async def execute_collaboration_background(request: CollaborationRequest):
    """백그라운드에서 협업 실행"""
    try:
        result = await sadp_core.initiate_collaboration(request)
        print(f"협업 완료: {request.id}")
    except Exception as e:
        print(f"협업 실행 오류: {e}")

@app.get("/collaborate/{collaboration_id}")
async def get_collaboration_status(collaboration_id: str):
    """협업 상태 조회"""
    if collaboration_id not in sadp_core.active_collaborations:
        raise HTTPException(status_code=404, detail=f"Collaboration {collaboration_id} not found")
    
    collaboration = sadp_core.active_collaborations[collaboration_id]
    return CollaborationResponse(
        id=collaboration["id"],
        status=collaboration["status"],
        participants=collaboration["participants"],
        results=collaboration.get("results", {}),
        duration=collaboration.get("duration"),
        created_at=collaboration["started_at"].isoformat()
    )

@app.get("/collaborate")
async def list_collaborations():
    """모든 협업 세션 목록"""
    collaborations = []
    for collab_id, collab_data in sadp_core.active_collaborations.items():
        collaborations.append({
            "id": collab_id,
            "title": collab_data["request"]["title"],
            "status": collab_data["status"],
            "participants": list(collab_data["participants"].keys()),
            "created_at": collab_data["started_at"].isoformat()
        })
    
    return {
        "total": len(collaborations),
        "collaborations": collaborations
    }

@app.post("/agents/{agent_name}/task")
async def assign_task_to_agent(agent_name: str, task: TaskModel):
    """특정 에이전트에게 작업 할당"""
    if agent_name not in sadp_core.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        from core.sadp_core import AITask, TaskStatus
        
        ai_task = AITask(
            id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=task.title,
            description=task.description,
            agent=agent_name,
            status=TaskStatus.PENDING,
            priority=Priority[task.priority.upper()],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            dependencies=task.dependencies,
            metadata=task.metadata
        )
        
        # Claude AI만 task 수신 메서드가 있음
        if agent_name == "claude":
            result = await sadp_core.claude.receive_task(ai_task)
            return {
                "task_id": ai_task.id,
                "agent": agent_name,
                "status": "assigned",
                "result": result
            }
        else:
            return {
                "task_id": ai_task.id,
                "agent": agent_name,
                "status": "queued",
                "message": f"Task queued for {agent_name}"
            }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid task: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign task: {str(e)}")

@app.get("/metrics")
async def get_performance_metrics():
    """시스템 성과 지표 조회"""
    try:
        status = sadp_core.get_system_status()
        return {
            "timestamp": datetime.now().isoformat(),
            "performance_metrics": status["performance_metrics"],
            "conflict_resolution": status["conflict_resolution"],
            "agent_utilization": status["performance_metrics"]["agent_utilization"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@app.get("/conflicts")
async def get_conflict_history():
    """충돌 해결 기록 조회"""
    try:
        conflicts = []
        for resolution in sadp_core.conflict_history:
            conflicts.append({
                "conflict_id": resolution.conflict_id,
                "type": resolution.conflict_type.value,
                "affected_agents": resolution.affected_agents,
                "strategy": resolution.resolution_strategy,
                "success": resolution.success,
                "resolved_at": resolution.resolved_at.isoformat()
            })
        
        return {
            "total_conflicts": len(conflicts),
            "resolution_rate": sadp_core.calculate_resolution_rate(),
            "conflicts": conflicts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get conflicts: {str(e)}")

@app.post("/system/reset")
async def reset_system():
    """시스템 리셋 (개발용)"""
    try:
        global sadp_core
        sadp_core = SADPCore()
        return {
            "status": "reset_completed",
            "timestamp": datetime.now().isoformat(),
            "message": "SADP Core system has been reset"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset system: {str(e)}")

# 개발 서버 실행
if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
