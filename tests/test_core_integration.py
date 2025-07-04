"""
SADP Core System 통합 테스트
"""

import pytest
import asyncio
from datetime import datetime, timedelta
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.sadp_core import (
    SADPCore, CollaborationRequest, CollaborationMode, 
    Priority, ConflictType
)

class TestSADPCore:
    """SADP Core 시스템 테스트"""
    
    @pytest.fixture
    def sadp_core(self):
        """SADP Core 인스턴스 픽스처"""
        return SADPCore()
    
    @pytest.fixture
    def sample_collaboration_request(self):
        """샘플 협업 요청 픽스처"""
        return CollaborationRequest(
            id="test_collab_001",
            title="테스트 협업",
            description="SADP 시스템 테스트를 위한 협업",
            mode=CollaborationMode.SEQUENTIAL,
            participants=["claude", "cursor_ai", "figma_ai"],
            requirements={
                "skills": ["전략", "개발", "디자인"],
                "quality_standard": 90.0
            },
            deadline=datetime.now() + timedelta(hours=1),
            priority=Priority.MEDIUM,
            created_at=datetime.now()
        )
    
    def test_sadp_core_initialization(self, sadp_core):
        """SADP Core 초기화 테스트"""
        assert sadp_core is not None
        assert len(sadp_core.agents) == 3
        assert "claude" in sadp_core.agents
        assert "cursor_ai" in sadp_core.agents
        assert "figma_ai" in sadp_core.agents
    
    def test_agent_capabilities(self, sadp_core):
        """AI 에이전트 역량 테스트"""
        claude = sadp_core.agents["claude"]
        cursor = sadp_core.agents["cursor_ai"]
        figma = sadp_core.agents["figma_ai"]
        
        assert len(claude.capabilities) > 0
        assert len(cursor.capabilities) > 0
        assert len(figma.capabilities) > 0
        
        # Claude는 전략 관련 역량 포함
        assert any("전략" in cap for cap in claude.capabilities)
        
        # Cursor는 코딩 관련 역량 포함
        assert any("코드" in cap for cap in cursor.capabilities)
        
        # Figma는 디자인 관련 역량 포함
        assert any("디자인" in cap for cap in figma.capabilities)
    
    @pytest.mark.asyncio
    async def test_prepare_agent(self, sadp_core, sample_collaboration_request):
        """에이전트 준비 테스트"""
        result = await sadp_core.prepare_agent("claude", sample_collaboration_request)
        
        assert result["ready"] is True
        assert "role" in result
        assert "capabilities_matched" in result
        assert isinstance(result["capabilities_matched"], float)
        assert 0 <= result["capabilities_matched"] <= 1
    
    def test_match_capabilities(self, sadp_core):
        """역량 매칭 테스트"""
        agent_capabilities = ["전략 수립", "문서화", "분석"]
        requirements = {"skills": ["전략", "문서"]}
        
        match_score = sadp_core.match_capabilities(agent_capabilities, requirements)
        
        assert isinstance(match_score, float)
        assert 0 <= match_score <= 1
        assert match_score > 0  # 일부 매칭되어야 함
    
    def test_execution_order(self, sadp_core):
        """실행 순서 결정 테스트"""
        participants = {
            "claude": {"ready": True},
            "cursor_ai": {"ready": True},
            "figma_ai": {"ready": True}
        }
        
        order = sadp_core.determine_execution_order(participants)
        
        assert len(order) == 3
        assert "claude" in order
        assert "cursor_ai" in order
        assert "figma_ai" in order
        
        # Claude가 첫 번째여야 함 (전략 수립)
        assert order[0] == "claude"
    
    @pytest.mark.asyncio
    async def test_execute_agent_task(self, sadp_core):
        """에이전트 작업 실행 테스트"""
        context = {"session_info": {"id": "test_session"}}
        
        # Claude 작업 테스트
        result = await sadp_core.execute_agent_task("claude", context)
        
        assert result["agent"] == "claude"
        assert result["status"] == "success"
        assert "completed_at" in result
    
    def test_detect_conflicts(self, sadp_core):
        """충돌 감지 테스트"""
        agent_result = {
            "agent": "claude",
            "quality_score": 95.0,
            "status": "success"
        }
        
        all_results = {
            "cursor_ai": {
                "agent": "cursor_ai",
                "quality_score": 70.0,  # 큰 차이
                "status": "success"
            }
        }
        
        conflicts = sadp_core.detect_conflicts("claude", agent_result, all_results)
        
        assert isinstance(conflicts, list)
        if conflicts:  # 충돌이 감지된 경우
            conflict = conflicts[0]
            assert "type" in conflict
            assert "agents" in conflict
            assert "claude" in conflict["agents"]
    
    @pytest.mark.asyncio
    async def test_resolve_quality_conflict(self, sadp_core):
        """품질 충돌 해결 테스트"""
        conflict = {
            "id": "test_conflict_001",
            "type": ConflictType.QUALITY,
            "agents": ["claude", "cursor_ai"],
            "description": "품질 점수 차이",
            "severity": "medium"
        }
        
        resolution = await sadp_core.resolve_quality_conflict(conflict)
        
        assert resolution.conflict_id == conflict["id"]
        assert resolution.conflict_type == ConflictType.QUALITY
        assert resolution.success is True
        assert len(resolution.resolution_actions) > 0
    
    def test_performance_metrics_initialization(self, sadp_core):
        """성과 지표 초기화 테스트"""
        metrics = sadp_core.performance_metrics
        
        assert "total_collaborations" in metrics
        assert "successful_collaborations" in metrics
        assert "conflicts_resolved" in metrics
        assert "average_completion_time" in metrics
        assert "agent_utilization" in metrics
        
        # 초기값 확인
        assert metrics["total_collaborations"] == 0
        assert metrics["successful_collaborations"] == 0
        assert metrics["conflicts_resolved"] == 0
        assert metrics["average_completion_time"] == 0.0
    
    def test_get_system_status(self, sadp_core):
        """시스템 상태 조회 테스트"""
        status = sadp_core.get_system_status()
        
        assert "core_system" in status
        assert "agents" in status
        assert "active_collaborations" in status
        assert "performance_metrics" in status
        assert "conflict_resolution" in status
        
        # 에이전트 상태 확인
        assert len(status["agents"]) == 3
        for agent_name in ["claude", "cursor_ai", "figma_ai"]:
            assert agent_name in status["agents"]
            assert "status" in status["agents"][agent_name]
            assert "capabilities" in status["agents"][agent_name]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
