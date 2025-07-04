"""
SADP Core Integration Module
다중 AI 에이전트 협업 시스템의 핵심 조율 모듈

Author: Sean K.S. Shin (GERI)
Created: 2025-07-04
Role: AI Agent Orchestration & Conflict Resolution
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# AI 에이전트 모듈 import
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration.claude_ai import ClaudeAI, AITask, TaskStatus, Priority
from cursor_ai_integration.cursor_ai import CursorAI, CodeLanguage
from figma_ai_integration.figma_ai import FigmaAI, DesignStyle, ColorScheme, ComponentType

class CollaborationMode(Enum):
    """협업 모드 정의"""
    SEQUENTIAL = "sequential"      # 순차적 처리
    PARALLEL = "parallel"          # 병렬 처리
    INTERACTIVE = "interactive"    # 상호작용 처리
    AUTONOMOUS = "autonomous"      # 자율 처리

class ConflictType(Enum):
    """충돌 유형 정의"""
    RESOURCE = "resource"          # 리소스 충돌
    PRIORITY = "priority"          # 우선순위 충돌
    DEPENDENCY = "dependency"      # 의존성 충돌
    TIMELINE = "timeline"          # 시간 충돌
    QUALITY = "quality"            # 품질 기준 충돌

@dataclass
class CollaborationRequest:
    """협업 요청 정의"""
    id: str
    title: str
    description: str
    mode: CollaborationMode
    participants: List[str]  # agent names
    requirements: Dict[str, Any]
    deadline: Optional[datetime]
    priority: Priority
    created_at: datetime

@dataclass
class ConflictResolution:
    """충돌 해결 결과"""
    conflict_id: str
    conflict_type: ConflictType
    affected_agents: List[str]
    resolution_strategy: str
    resolution_actions: List[Dict[str, Any]]
    resolved_at: datetime
    success: bool

class SADPCore:
    """SADP 핵심 통합 시스템"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.active_collaborations: Dict[str, Dict] = {}
        self.conflict_history: List[ConflictResolution] = []
        self.performance_metrics = {
            "total_collaborations": 0,
            "successful_collaborations": 0,
            "conflicts_resolved": 0,
            "average_completion_time": 0.0,
            "agent_utilization": {}
        }
        
        # AI 에이전트 초기화
        self.claude = ClaudeAI()
        self.cursor = CursorAI()
        self.figma = FigmaAI()
        
        self.agents = {
            "claude": self.claude,
            "cursor_ai": self.cursor,
            "figma_ai": self.figma
        }
        
        self.setup_logging()
        self.setup_conflict_resolution()
    
    def setup_logging(self):
        """로깅 시스템 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sadp_core.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SADP.Core")
        self.logger.info("🎯 SADP Core 시스템 초기화 완료")
    
    def setup_conflict_resolution(self):
        """충돌 해결 시스템 설정"""
        self.conflict_resolvers = {
            ConflictType.RESOURCE: self.resolve_resource_conflict,
            ConflictType.PRIORITY: self.resolve_priority_conflict,
            ConflictType.DEPENDENCY: self.resolve_dependency_conflict,
            ConflictType.TIMELINE: self.resolve_timeline_conflict,
            ConflictType.QUALITY: self.resolve_quality_conflict
        }
        
        self.decision_matrix = {
            "claude": {"weight": 0.4, "expertise": ["strategy", "documentation", "analysis"]},
            "cursor_ai": {"weight": 0.35, "expertise": ["coding", "optimization", "testing"]},
            "figma_ai": {"weight": 0.25, "expertise": ["design", "ux", "prototyping"]}
        }
    
    async def initiate_collaboration(self, request: CollaborationRequest) -> Dict[str, Any]:
        """협업 세션 시작"""
        self.logger.info(f"🤝 협업 시작: {request.title}")
        
        collaboration_id = request.id
        session = {
            "id": collaboration_id,
            "request": asdict(request),
            "status": "active",
            "participants": {},
            "timeline": [],
            "conflicts": [],
            "results": {},
            "started_at": datetime.now()
        }
        
        # 참여 에이전트 준비
        for agent_name in request.participants:
            if agent_name in self.agents:
                agent_status = await self.prepare_agent(agent_name, request)
                session["participants"][agent_name] = agent_status
            else:
                self.logger.warning(f"⚠️ 알 수 없는 에이전트: {agent_name}")
        
        # 협업 모드에 따른 실행
        if request.mode == CollaborationMode.SEQUENTIAL:
            result = await self.execute_sequential_collaboration(session)
        elif request.mode == CollaborationMode.PARALLEL:
            result = await self.execute_parallel_collaboration(session)
        elif request.mode == CollaborationMode.INTERACTIVE:
            result = await self.execute_interactive_collaboration(session)
        elif request.mode == CollaborationMode.AUTONOMOUS:
            result = await self.execute_autonomous_collaboration(session)
        
        # 협업 완료 처리
        session["status"] = "completed"
        session["completed_at"] = datetime.now()
        session["results"] = result
        session["duration"] = (session["completed_at"] - session["started_at"]).total_seconds()
        
        self.active_collaborations[collaboration_id] = session
        self.update_performance_metrics(session)
        
        return session
    
    async def prepare_agent(self, agent_name: str, request: CollaborationRequest) -> Dict[str, Any]:
        """에이전트 준비"""
        agent = self.agents[agent_name]
        
        # 에이전트별 특수 준비
        if agent_name == "claude":
            preparation = {
                "role": "strategic_coordinator",
                "ready": True,
                "capabilities_matched": self.match_capabilities(agent.capabilities, request.requirements),
                "estimated_contribution": "전략 수립, 문서화, 품질 관리"
            }
        
        elif agent_name == "cursor_ai":
            preparation = {
                "role": "code_developer",
                "ready": True,
                "capabilities_matched": self.match_capabilities(agent.capabilities, request.requirements),
                "estimated_contribution": "코드 작성, 최적화, 테스트"
            }
        
        elif agent_name == "figma_ai":
            preparation = {
                "role": "ui_designer",
                "ready": True,
                "capabilities_matched": self.match_capabilities(agent.capabilities, request.requirements),
                "estimated_contribution": "UI 설계, 프로토타입, 사용성"
            }
        
        self.logger.info(f"✅ {agent_name} 준비 완료")
        return preparation
    
    def match_capabilities(self, agent_capabilities: List[str], 
                          requirements: Dict[str, Any]) -> float:
        """에이전트 역량과 요구사항 매칭 점수 계산"""
        required_skills = requirements.get("skills", [])
        
        if not required_skills:
            return 1.0
        
        matched_skills = sum(1 for skill in required_skills 
                           if any(skill.lower() in cap.lower() for cap in agent_capabilities))
        
        return matched_skills / len(required_skills)
    
    async def execute_sequential_collaboration(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """순차적 협업 실행"""
        self.logger.info("📋 순차적 협업 모드 실행")
        
        results = {}
        execution_order = self.determine_execution_order(session["participants"])
        
        for agent_name in execution_order:
            self.logger.info(f"🔄 {agent_name} 작업 시작")
            
            # 이전 결과를 현재 에이전트에게 전달
            context = {"previous_results": results, "session_info": session}
            agent_result = await self.execute_agent_task(agent_name, context)
            
            results[agent_name] = agent_result
            
            # 충돌 검사
            conflicts = self.detect_conflicts(agent_name, agent_result, results)
            if conflicts:
                resolution = await self.resolve_conflicts(conflicts)
                session["conflicts"].extend(conflicts)
                results[agent_name] = self.apply_conflict_resolution(agent_result, resolution)
            
            session["timeline"].append({
                "agent": agent_name,
                "action": "task_completed",
                "timestamp": datetime.now().isoformat(),
                "result_summary": self.summarize_result(agent_result)
            })
        
        return results
    
    async def execute_parallel_collaboration(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """병렬 협업 실행"""
        self.logger.info("⚡ 병렬 협업 모드 실행")
        
        # 모든 에이전트 동시 실행
        tasks = []
        for agent_name in session["participants"]:
            context = {"session_info": session, "mode": "parallel"}
            task = asyncio.create_task(self.execute_agent_task(agent_name, context))
            tasks.append((agent_name, task))
        
        # 모든 작업 완료 대기
        results = {}
        for agent_name, task in tasks:
            agent_result = await task
            results[agent_name] = agent_result
            
            session["timeline"].append({
                "agent": agent_name,
                "action": "task_completed",
                "timestamp": datetime.now().isoformat(),
                "result_summary": self.summarize_result(agent_result)
            })
        
        # 병렬 실행 후 충돌 검사 및 해결
        all_conflicts = self.detect_all_conflicts(results)
        if all_conflicts:
            resolution = await self.resolve_conflicts(all_conflicts)
            session["conflicts"].extend(all_conflicts)
            results = self.apply_conflict_resolution(results, resolution)
        
        return results
    
    async def execute_interactive_collaboration(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """상호작용 협업 실행"""
        self.logger.info("🔄 상호작용 협업 모드 실행")
        
        results = {}
        interaction_rounds = 3  # 상호작용 라운드 수
        
        for round_num in range(interaction_rounds):
            self.logger.info(f"🔄 상호작용 라운드 {round_num + 1}")
            
            round_results = {}
            for agent_name in session["participants"]:
                context = {
                    "session_info": session,
                    "round": round_num,
                    "previous_rounds": results,
                    "current_round": round_results
                }
                
                agent_result = await self.execute_agent_task(agent_name, context)
                round_results[agent_name] = agent_result
                
                # 실시간 피드백 교환
                feedback = await self.generate_agent_feedback(agent_name, agent_result, round_results)
                round_results[f"{agent_name}_feedback"] = feedback
            
            results[f"round_{round_num + 1}"] = round_results
            
            # 라운드별 충돌 해결
            conflicts = self.detect_all_conflicts(round_results)
            if conflicts:
                resolution = await self.resolve_conflicts(conflicts)
                session["conflicts"].extend(conflicts)
        
        return results
    
    async def execute_autonomous_collaboration(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """자율 협업 실행"""
        self.logger.info("🤖 자율 협업 모드 실행")
        
        # AI 에이전트들이 자율적으로 협업 계획 수립
        collaboration_plan = await self.generate_autonomous_plan(session)
        
        results = {}
        for step in collaboration_plan["steps"]:
            step_results = await self.execute_autonomous_step(step, session, results)
            results[step["id"]] = step_results
            
            # 자율적 적응 및 계획 수정
            if step_results.get("requires_adaptation"):
                collaboration_plan = await self.adapt_autonomous_plan(collaboration_plan, step_results)
        
        return results
    
    def determine_execution_order(self, participants: Dict[str, Any]) -> List[str]:
        """실행 순서 결정"""
        # 의존성과 우선순위에 따른 순서 결정
        order = []
        
        # 일반적인 개발 프로세스 순서
        if "claude" in participants:
            order.append("claude")    # 전략 및 기획 먼저
        if "figma_ai" in participants:
            order.append("figma_ai")  # 디자인 다음
        if "cursor_ai" in participants:
            order.append("cursor_ai") # 개발 마지막
        
        return order
    
    async def execute_agent_task(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """에이전트 작업 실행"""
        agent = self.agents[agent_name]
        
        try:
            if agent_name == "claude":
                # Claude는 전략 수립 및 문서화 담당
                result = {
                    "type": "strategic_analysis",
                    "strategy": "AI 협업 최적화 전략",
                    "documentation": "프로젝트 문서화 완료",
                    "quality_score": 95.0,
                    "recommendations": ["협업 효율성 개선", "품질 관리 강화"]
                }
            
            elif agent_name == "cursor_ai":
                # Cursor AI는 코드 개발 담당
                code_spec = {
                    "name": "ai_collaboration_handler",
                    "type": "class",
                    "language": "python",
                    "description": "AI 협업 처리 클래스"
                }
                result = await agent.generate_code(code_spec)
            
            elif agent_name == "figma_ai":
                # Figma AI는 UI 설계 담당
                from figma_ai_integration.figma_ai import DesignSpecs
                design_spec = DesignSpecs(
                    id="ui_001",
                    title="AI 협업 인터페이스",
                    description="다중 AI 에이전트 협업 대시보드",
                    style=DesignStyle.MODERN,
                    color_scheme=ColorScheme.BLUE_PROFESSIONAL,
                    components=[ComponentType.BUTTON, ComponentType.CARD],
                    target_devices=["desktop"],
                    accessibility_level="AA",
                    brand_guidelines={},
                    user_requirements=["직관적 인터페이스"]
                )
                result = await agent.create_design(design_spec)
            
            result["agent"] = agent_name
            result["status"] = "success"
            result["completed_at"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {agent_name} 작업 실패: {e}")
            return {
                "agent": agent_name,
                "status": "error",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    def detect_conflicts(self, agent_name: str, agent_result: Dict[str, Any], 
                        all_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """충돌 감지"""
        conflicts = []
        
        # 간단한 충돌 감지 로직 (실제로는 더 정교한 분석 필요)
        for other_agent, other_result in all_results.items():
            if other_agent != agent_name:
                # 품질 기준 충돌 체크
                if ("quality_score" in agent_result and "quality_score" in other_result):
                    score_diff = abs(agent_result["quality_score"] - other_result["quality_score"])
                    if score_diff > 20:
                        conflicts.append({
                            "id": str(uuid.uuid4()),
                            "type": ConflictType.QUALITY,
                            "agents": [agent_name, other_agent],
                            "description": f"품질 점수 차이가 큼: {score_diff}",
                            "severity": "medium"
                        })
        
        return conflicts
    
    def detect_all_conflicts(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """전체 결과에서 충돌 감지"""
        conflicts = []
        agents = list(results.keys())
        
        # 모든 에이전트 쌍에 대해 충돌 검사
        for i, agent1 in enumerate(agents):
            for agent2 in agents[i+1:]:
                pair_conflicts = self.detect_conflicts(agent1, results[agent1], {agent2: results[agent2]})
                conflicts.extend(pair_conflicts)
        
        return conflicts
    
    async def resolve_conflicts(self, conflicts: List[Dict[str, Any]]) -> List[ConflictResolution]:
        """충돌 해결"""
        resolutions = []
        
        for conflict in conflicts:
            conflict_type = ConflictType(conflict["type"])
            resolver = self.conflict_resolvers[conflict_type]
            
            resolution = await resolver(conflict)
            resolutions.append(resolution)
            
            self.conflict_history.append(resolution)
            self.performance_metrics["conflicts_resolved"] += 1
        
        return resolutions
    
    async def resolve_quality_conflict(self, conflict: Dict[str, Any]) -> ConflictResolution:
        """품질 충돌 해결"""
        resolution_actions = [
            {"action": "set_quality_standard", "value": 90.0},
            {"action": "require_peer_review", "reviewers": ["claude"]},
            {"action": "implement_quality_checks", "automated": True}
        ]
        
        return ConflictResolution(
            conflict_id=conflict["id"],
            conflict_type=ConflictType.QUALITY,
            affected_agents=conflict["agents"],
            resolution_strategy="quality_standardization",
            resolution_actions=resolution_actions,
            resolved_at=datetime.now(),
            success=True
        )
    
    async def resolve_resource_conflict(self, conflict: Dict[str, Any]) -> ConflictResolution:
        """리소스 충돌 해결"""
        return ConflictResolution(
            conflict_id=conflict["id"],
            conflict_type=ConflictType.RESOURCE,
            affected_agents=conflict["agents"],
            resolution_strategy="resource_allocation",
            resolution_actions=[{"action": "allocate_resources", "method": "round_robin"}],
            resolved_at=datetime.now(),
            success=True
        )
    
    async def resolve_priority_conflict(self, conflict: Dict[str, Any]) -> ConflictResolution:
        """우선순위 충돌 해결"""
        return ConflictResolution(
            conflict_id=conflict["id"],
            conflict_type=ConflictType.PRIORITY,
            affected_agents=conflict["agents"],
            resolution_strategy="priority_voting",
            resolution_actions=[{"action": "democratic_vote", "weight_system": self.decision_matrix}],
            resolved_at=datetime.now(),
            success=True
        )
    
    async def resolve_dependency_conflict(self, conflict: Dict[str, Any]) -> ConflictResolution:
        """의존성 충돌 해결"""
        return ConflictResolution(
            conflict_id=conflict["id"],
            conflict_type=ConflictType.DEPENDENCY,
            affected_agents=conflict["agents"],
            resolution_strategy="dependency_ordering",
            resolution_actions=[{"action": "reorder_tasks", "method": "topological_sort"}],
            resolved_at=datetime.now(),
            success=True
        )
    
    async def resolve_timeline_conflict(self, conflict: Dict[str, Any]) -> ConflictResolution:
        """시간 충돌 해결"""
        return ConflictResolution(
            conflict_id=conflict["id"],
            conflict_type=ConflictType.TIMELINE,
            affected_agents=conflict["agents"],
            resolution_strategy="timeline_adjustment",
            resolution_actions=[{"action": "extend_deadline", "buffer": "20%"}],
            resolved_at=datetime.now(),
            success=True
        )
    
    def apply_conflict_resolution(self, results: Union[Dict[str, Any], Dict[str, Dict[str, Any]]], 
                                resolutions: List[ConflictResolution]) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """충돌 해결 결과 적용"""
        # 해결 방안을 실제 결과에 적용
        # 여기서는 메타데이터 추가로 구현
        
        if isinstance(results, dict) and "agent" in results:
            # 단일 에이전트 결과
            results["conflict_resolutions"] = [asdict(res) for res in resolutions]
        else:
            # 다중 에이전트 결과
            for agent_name in results:
                if isinstance(results[agent_name], dict):
                    results[agent_name]["conflict_resolutions"] = [asdict(res) for res in resolutions]
        
        return results
    
    def summarize_result(self, result: Dict[str, Any]) -> str:
        """결과 요약"""
        if result.get("status") == "error":
            return f"에러 발생: {result.get('error', 'Unknown error')}"
        
        agent = result.get("agent", "Unknown")
        result_type = result.get("type", "task")
        
        return f"{agent}: {result_type} 완료"
    
    async def generate_agent_feedback(self, agent_name: str, agent_result: Dict[str, Any], 
                                    round_results: Dict[str, Any]) -> Dict[str, Any]:
        """에이전트 피드백 생성"""
        feedback = {
            "from_agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "suggestions": [],
            "appreciations": [],
            "concerns": []
        }
        
        # 다른 에이전트 결과에 대한 피드백
        for other_agent, other_result in round_results.items():
            if other_agent != agent_name and not other_agent.endswith("_feedback"):
                if other_result.get("status") == "success":
                    feedback["appreciations"].append(f"{other_agent}의 우수한 작업 품질")
                else:
                    feedback["concerns"].append(f"{other_agent}의 작업에서 개선 필요")
        
        return feedback
    
    async def generate_autonomous_plan(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """자율 협업 계획 생성"""
        plan = {
            "id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "session_id": session["id"],
            "steps": [
                {
                    "id": "step_1",
                    "agent": "claude",
                    "action": "strategic_analysis",
                    "dependencies": [],
                    "estimated_duration": 30
                },
                {
                    "id": "step_2", 
                    "agent": "figma_ai",
                    "action": "ui_design",
                    "dependencies": ["step_1"],
                    "estimated_duration": 45
                },
                {
                    "id": "step_3",
                    "agent": "cursor_ai", 
                    "action": "code_implementation",
                    "dependencies": ["step_1", "step_2"],
                    "estimated_duration": 60
                }
            ],
            "total_estimated_duration": 135,
            "adaptive": True
        }
        
        return plan
    
    async def execute_autonomous_step(self, step: Dict[str, Any], session: Dict[str, Any], 
                                    previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """자율 단계 실행"""
        context = {
            "session_info": session,
            "step_info": step,
            "previous_results": previous_results,
            "mode": "autonomous"
        }
        
        return await self.execute_agent_task(step["agent"], context)
    
    async def adapt_autonomous_plan(self, plan: Dict[str, Any], step_result: Dict[str, Any]) -> Dict[str, Any]:
        """자율 계획 적응"""
        # 결과에 따라 계획 수정
        if step_result.get("requires_additional_design"):
            # 추가 디자인 단계 삽입
            new_step = {
                "id": f"adaptive_step_{len(plan['steps']) + 1}",
                "agent": "figma_ai",
                "action": "additional_design",
                "dependencies": [step_result.get("step_id")],
                "estimated_duration": 30
            }
            plan["steps"].append(new_step)
        
        return plan
    
    def update_performance_metrics(self, session: Dict[str, Any]):
        """성과 지표 업데이트"""
        self.performance_metrics["total_collaborations"] += 1
        
        if session["status"] == "completed":
            self.performance_metrics["successful_collaborations"] += 1
        
        # 평균 완료 시간 계산
        if "duration" in session:
            current_avg = self.performance_metrics["average_completion_time"]
            total_completed = self.performance_metrics["successful_collaborations"]
            
            new_avg = ((current_avg * (total_completed - 1)) + session["duration"]) / total_completed
            self.performance_metrics["average_completion_time"] = new_avg
        
        # 에이전트 활용도 업데이트
        for agent_name in session["participants"]:
            if agent_name not in self.performance_metrics["agent_utilization"]:
                self.performance_metrics["agent_utilization"][agent_name] = 0
            self.performance_metrics["agent_utilization"][agent_name] += 1
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        return {
            "core_system": {
                "status": "active",
                "version": "1.0.0",
                "uptime": "계산 필요",
                "last_updated": datetime.now().isoformat()
            },
            "agents": {
                agent_name: {
                    "status": "ready",
                    "capabilities": agent.capabilities,
                    "last_activity": datetime.now().isoformat()
                }
                for agent_name, agent in self.agents.items()
            },
            "active_collaborations": len(self.active_collaborations),
            "performance_metrics": self.performance_metrics,
            "conflict_resolution": {
                "total_conflicts": len(self.conflict_history),
                "resolution_rate": self.calculate_resolution_rate(),
                "average_resolution_time": self.calculate_avg_resolution_time()
            }
        }
    
    def calculate_resolution_rate(self) -> float:
        """충돌 해결률 계산"""
        if not self.conflict_history:
            return 100.0
        
        successful = sum(1 for resolution in self.conflict_history if resolution.success)
        return (successful / len(self.conflict_history)) * 100
    
    def calculate_avg_resolution_time(self) -> float:
        """평균 충돌 해결 시간 계산"""
        if not self.conflict_history:
            return 0.0
        
        # 실제 구현에서는 충돌 발생 시간과 해결 시간의 차이 계산
        return 5.2  # 예시값 (분)

# 사용 예시 및 테스트
if __name__ == "__main__":
    async def test_sadp_core():
        sadp = SADPCore()
        
        # 협업 요청 생성
        collaboration_request = CollaborationRequest(
            id="collab_001",
            title="GERI 교육 플랫폼 개발",
            description="AI 기반 교육 혁신 플랫폼 구축",
            mode=CollaborationMode.SEQUENTIAL,
            participants=["claude", "figma_ai", "cursor_ai"],
            requirements={
                "skills": ["전략", "디자인", "개발"],
                "quality_standard": 90.0,
                "deadline": "2025-07-10"
            },
            deadline=datetime.now() + timedelta(days=6),
            priority=Priority.HIGH,
            created_at=datetime.now()
        )
        
        # 협업 실행
        result = await sadp.initiate_collaboration(collaboration_request)
        
        print("협업 결과:")
        print(f"상태: {result['status']}")
        print(f"참여자: {list(result['participants'].keys())}")
        print(f"소요 시간: {result.get('duration', 0):.1f}초")
        
        # 시스템 상태 확인
        status = sadp.get_system_status()
        print(f"\n시스템 상태: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # 비동기 테스트 실행
    asyncio.run(test_sadp_core())
