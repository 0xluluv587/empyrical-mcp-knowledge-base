#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Empyrical MCP服务测试脚本
用于测试Empyrical MCP服务的各项功能
"""

import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# MCP服务地址
MCP_SERVICE_URL = "http://localhost:8000"

def test_annual_return():
    """测试年化收益率计算函数"""
    print("测试年化收益率计算...")
    
    # 生成测试数据 - 每天增长0.1%的收益率
    returns = [0.001] * 100
    
    # 构建请求数据
    data = {
        "returns": returns,
        "period": "daily",
        "annualization": 252
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/annual_return", json=data)
    result = response.json()
    
    # 验证结果
    expected = (1 + 0.001) ** 252 - 1
    print(f"计算结果: {result['annual_return']:.6f}")
    print(f"预期结果: {expected:.6f}")
    print(f"测试{'通过' if abs(result['annual_return'] - expected) < 0.0001 else '失败'}")
    print()

def test_max_drawdown():
    """测试最大回撤计算函数"""
    print("测试最大回撤计算...")
    
    # 生成测试数据 - 上升趋势中有一次大跌
    returns = [0.01] * 20 + [-0.15] + [0.01] * 20
    
    # 构建请求数据
    data = {
        "returns": returns
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/max_drawdown", json=data)
    result = response.json()
    
    # 验证结果
    # 计算预期最大回撤
    cumulative = []
    for r in returns:
        if not cumulative:
            cumulative.append(1 + r)
        else:
            cumulative.append(cumulative[-1] * (1 + r))
    
    # 计算最大回撤
    running_max = 0
    max_drawdown = 0
    for i, cum_return in enumerate(cumulative):
        if cum_return > running_max:
            running_max = cum_return
        drawdown = (running_max - cum_return) / running_max
        max_drawdown = max(max_drawdown, drawdown)
    
    print(f"计算结果: {result['max_drawdown']:.6f}")
    print(f"预期结果: {max_drawdown:.6f}")
    print(f"测试{'通过' if abs(result['max_drawdown'] - max_drawdown) < 0.0001 else '失败'}")
    print()

def test_sharpe_ratio():
    """测试夏普比率计算函数"""
    print("测试夏普比率计算...")
    
    # 生成测试数据 - 稳定增长的收益率
    returns = [0.002] * 50
    
    # 构建请求数据
    data = {
        "returns": returns,
        "risk_free": 0.0,
        "period": "daily",
        "annualization": 252
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/sharpe_ratio", json=data)
    result = response.json()
    
    # 打印结果
    print(f"夏普比率: {result['sharpe_ratio']:.6f}")
    print(f"测试{'通过' if result['sharpe_ratio'] > 0 else '失败'}")
    print()
    
def test_sortino_ratio():
    """测试索提诺比率计算函数"""
    print("测试索提诺比率计算...")
    
    # 生成测试数据 - 有正有负的收益率
    returns = [0.02] * 25 + [-0.01] * 10 + [0.015] * 15
    
    # 构建请求数据
    data = {
        "returns": returns,
        "required_return": 0.0,
        "period": "daily",
        "annualization": 252
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/sortino_ratio", json=data)
    result = response.json()
    
    # 打印结果
    print(f"索提诺比率: {result['sortino_ratio']:.6f}")
    print(f"测试{'通过' if result['sortino_ratio'] > 0 else '失败'}")
    print()

def test_alpha():
    """测试阿尔法系数计算函数"""
    print("测试阿尔法系数计算...")
    
    # 生成测试数据 - 策略收益率高于基准收益率
    returns = [0.002] * 50
    benchmark_returns = [0.001] * 50
    
    # 构建请求数据
    data = {
        "returns": returns,
        "factor_returns": benchmark_returns,
        "risk_free": 0.0,
        "period": "daily",
        "annualization": 252
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/alpha", json=data)
    result = response.json()
    
    # 打印结果
    print(f"阿尔法系数: {result['alpha']:.6f}")
    print(f"测试{'通过' if result['alpha'] > 0 else '失败'}")
    print()

def test_beta():
    """测试贝塔系数计算函数"""
    print("测试贝塔系数计算...")
    
    # 生成测试数据 - 策略收益率与基准收益率相关
    benchmark_returns = [0.001] * 50
    returns = [r * 1.2 for r in benchmark_returns]  # 贝塔应该接近1.2
    
    # 构建请求数据
    data = {
        "returns": returns,
        "factor_returns": benchmark_returns
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/beta", json=data)
    result = response.json()
    
    # 打印结果
    print(f"贝塔系数: {result['beta']:.6f}")
    print(f"预期结果: 约1.2")
    print(f"测试{'通过' if abs(result['beta'] - 1.2) < 0.1 else '失败'}")
    print()

def test_calmar_ratio():
    """测试卡玛比率计算函数"""
    print("测试卡玛比率计算...")
    
    # 生成测试数据 - 上升趋势中有一次大跌
    returns = [0.01] * 20 + [-0.15] + [0.01] * 20
    
    # 构建请求数据
    data = {
        "returns": returns,
        "period": "daily",
        "annualization": 252
    }
    
    # 发送请求
    response = requests.post(f"{MCP_SERVICE_URL}/calmar_ratio", json=data)
    result = response.json()
    
    # 打印结果
    print(f"卡玛比率: {result['calmar_ratio']:.6f}")
    print(f"测试{'通过' if result['calmar_ratio'] > 0 else '失败'}")
    print()

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("开始测试Empyrical MCP服务...")
    print("=" * 50)
    print()
    
    try:
        # 测试服务是否在线
        response = requests.get(f"{MCP_SERVICE_URL}/")
        if response.status_code == 200:
            print("MCP服务连接成功!")
            print(f"服务信息: {response.json()}")
            print()
        else:
            print(f"错误: 无法连接到MCP服务。状态码: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到MCP服务。请确保服务已启动并在监听端口8000。")
        print("运行命令: uvicorn empyrical_mcp_server:app --host 0.0.0.0 --port 8000")
        return
    
    # 运行各项功能测试
    test_annual_return()
    test_max_drawdown()
    test_sharpe_ratio()
    test_sortino_ratio()
    test_alpha()
    test_beta()
    test_calmar_ratio()
    
    print("=" * 50)
    print("所有测试完成!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()