#!/usr/bin/env python3
"""
Empyrical MCP Server

这个MCP服务为AI提供了访问Empyrical库金融指标计算功能的能力。
"""

import json
import numpy as np
import pandas as pd
from typing import List, Dict, Union, Optional, Any
from dataclasses import dataclass
import empyrical

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Empyrical MCP Server")

# 定义MCP方法请求模型
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[Union[str, int]] = None


# 定义MCP方法响应模型
class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[str, int]] = None


@app.post("/")
async def handle_request(request: Request):
    """处理所有MCP请求的主入口点"""
    try:
        data = await request.json()
        mcp_request = MCPRequest(**data)
        
        # 调度到相应的处理函数
        method_name = mcp_request.method
        handler = method_handlers.get(method_name)
        
        if not handler:
            return MCPResponse(
                jsonrpc="2.0",
                error={"code": -32601, "message": f"Method {method_name} not found"},
                id=mcp_request.id
            ).dict()
        
        # 调用相应的处理函数
        result = handler(mcp_request.params)
        
        # 返回结果
        return MCPResponse(
            jsonrpc="2.0",
            result=result,
            id=mcp_request.id
        ).dict()
    
    except Exception as e:
        # 处理异常
        return MCPResponse(
            jsonrpc="2.0",
            error={"code": -32603, "message": f"Internal error: {str(e)}"},
            id=data.get("id") if "id" in data else None
        ).dict()


# 工具函数：转换输入数据为numpy数组
def convert_to_numpy(returns_data: List[float]) -> np.ndarray:
    """将输入的浮点数列表转换为numpy数组"""
    return np.array(returns_data)


# ===== MCP方法处理函数 =====

def handle_annual_return(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算年化收益率"""
    returns = convert_to_numpy(params.get("returns", []))
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    result = empyrical.annual_return(
        returns=returns,
        period=period,
        annualization=annualization
    )
    
    return {
        "annual_return": float(result)
    }


def handle_max_drawdown(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算最大回撤"""
    returns = convert_to_numpy(params.get("returns", []))
    
    result = empyrical.max_drawdown(returns=returns)
    
    return {
        "max_drawdown": float(result)
    }


def handle_sharpe_ratio(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算夏普比率"""
    returns = convert_to_numpy(params.get("returns", []))
    risk_free = params.get("risk_free", 0.0)
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    result = empyrical.sharpe_ratio(
        returns=returns,
        risk_free=risk_free,
        period=period,
        annualization=annualization
    )
    
    return {
        "sharpe_ratio": float(result)
    }


def handle_sortino_ratio(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算索提诺比率"""
    returns = convert_to_numpy(params.get("returns", []))
    required_return = params.get("required_return", 0.0)
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    result = empyrical.sortino_ratio(
        returns=returns,
        required_return=required_return,
        period=period,
        annualization=annualization
    )
    
    return {
        "sortino_ratio": float(result)
    }


def handle_calmar_ratio(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算卡玛比率"""
    returns = convert_to_numpy(params.get("returns", []))
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    result = empyrical.calmar_ratio(
        returns=returns,
        period=period,
        annualization=annualization
    )
    
    return {
        "calmar_ratio": float(result)
    }


def handle_alpha_beta(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算阿尔法和贝塔系数"""
    returns = convert_to_numpy(params.get("returns", []))
    factor_returns = convert_to_numpy(params.get("factor_returns", []))
    risk_free = params.get("risk_free", 0.0)
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    alpha, beta = empyrical.alpha_beta(
        returns=returns,
        factor_returns=factor_returns,
        risk_free=risk_free,
        period=period,
        annualization=annualization
    )
    
    return {
        "alpha": float(alpha),
        "beta": float(beta)
    }


def handle_annual_volatility(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算年化波动率"""
    returns = convert_to_numpy(params.get("returns", []))
    period = params.get("period", "daily")
    alpha = params.get("alpha", 2.0)
    annualization = params.get("annualization", None)
    
    result = empyrical.annual_volatility(
        returns=returns,
        period=period,
        alpha=alpha,
        annualization=annualization
    )
    
    return {
        "annual_volatility": float(result)
    }


def handle_information_ratio(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算信息比率"""
    returns = convert_to_numpy(params.get("returns", []))
    factor_returns = convert_to_numpy(params.get("factor_returns", []))
    period = params.get("period", "daily")
    
    result = empyrical.information_ratio(
        returns=returns,
        factor_returns=factor_returns,
        period=period
    )
    
    return {
        "information_ratio": float(result)
    }


def handle_downside_risk(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算下行风险"""
    returns = convert_to_numpy(params.get("returns", []))
    required_return = params.get("required_return", 0.0)
    period = params.get("period", "daily")
    annualization = params.get("annualization", None)
    
    result = empyrical.downside_risk(
        returns=returns,
        required_return=required_return,
        period=period,
        annualization=annualization
    )
    
    return {
        "downside_risk": float(result)
    }


def handle_tracking_error(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算跟踪误差"""
    returns = convert_to_numpy(params.get("returns", []))
    factor_returns = convert_to_numpy(params.get("factor_returns", []))
    period = params.get("period", "daily")
    
    result = empyrical.tracking_error(
        returns=returns,
        factor_returns=factor_returns,
        period=period
    )
    
    return {
        "tracking_error": float(result)
    }


def handle_value_at_risk(params: Dict[str, Any]) -> Dict[str, Any]:
    """计算风险价值"""
    returns = convert_to_numpy(params.get("returns", []))
    cutoff = params.get("cutoff", 0.05)
    
    result = empyrical.value_at_risk(returns=returns, cutoff=cutoff)
    
    return {
        "value_at_risk": float(result)
    }


def handle_get_available_metrics(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取所有可用的指标函数列表"""
    metrics = list(method_handlers.keys())
    metrics.remove("get_available_metrics")  # 排除这个元函数
    
    return {
        "available_metrics": metrics
    }


# 方法处理函数映射
method_handlers = {
    "annual_return": handle_annual_return,
    "max_drawdown": handle_max_drawdown,
    "sharpe_ratio": handle_sharpe_ratio,
    "sortino_ratio": handle_sortino_ratio,
    "calmar_ratio": handle_calmar_ratio,
    "alpha_beta": handle_alpha_beta,
    "annual_volatility": handle_annual_volatility,
    "information_ratio": handle_information_ratio,
    "downside_risk": handle_downside_risk,
    "tracking_error": handle_tracking_error,
    "value_at_risk": handle_value_at_risk,
    "get_available_metrics": handle_get_available_metrics
}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)