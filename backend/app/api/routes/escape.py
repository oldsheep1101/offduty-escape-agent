"""下班逃离助手API路由"""

from fastapi import APIRouter, HTTPException
from ...models.schemas import (
    EscapeRequest,
    EscapePlanResponse,
    ErrorResponse
)
from ...agents.escape_planner_agent import get_escape_planner_agent

router = APIRouter(prefix="/escape", tags=["下班逃离助手"])


@router.post(
    "/plan",
    response_model=EscapePlanResponse,
    summary="生成下班逃离计划",
    description="根据起点、终点和下班时间，规划看电影和晚餐的逃离路线"
)
async def plan_escape(request: EscapeRequest):
    """
    生成下班逃离计划

    Args:
        request: 逃离请求参数

    Returns:
        逃离计划响应
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 收到下班逃离规划请求:")
        print(f"   起点: {request.origin}")
        print(f"   终点: {request.destination}")
        print(f"   下班时间: {request.off_work_time}")
        print(f"   城市: {request.city}")
        print(f"{'='*60}\n")

        # 获取Agent实例
        print("🔄 获取逃离规划智能体...")
        agent = get_escape_planner_agent()

        # 生成逃离计划
        print("🚀 开始生成逃离计划...")
        escape_plan = agent.plan_escape(request)

        print("✅ 逃离计划生成成功，准备返回响应\n")

        return EscapePlanResponse(
            success=True,
            message="逃离计划生成成功",
            data=escape_plan
        )

    except Exception as e:
        print(f"❌ 生成逃离计划失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"生成逃离计划失败: {str(e)}"
        )


@router.get(
    "/health",
    summary="健康检查",
    description="检查下班逃离助手服务是否正常"
)
async def health_check():
    """健康检查"""
    try:
        agent = get_escape_planner_agent()

        return {
            "status": "healthy",
            "service": "escape-planner",
            "agent_name": "下班逃离助手"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"服务不可用: {str(e)}"
        )
