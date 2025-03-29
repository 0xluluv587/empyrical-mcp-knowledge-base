#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
示例数据生成工具
用于生成测试Empyrical MCP服务的样本数据
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def generate_random_returns(days=365, mean=0.0005, volatility=0.01, seed=None):
    """
    生成符合正态分布的随机收益率序列
    
    参数:
        days (int): 天数
        mean (float): 平均每日收益率
        volatility (float): 每日波动率
        seed (int): 随机数种子
    
    返回:
        pandas.Series: 日期和收益率
    """
    if seed is not None:
        np.random.seed(seed)
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # 生成日期范围，仅包含工作日
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # 生成符合正态分布的随机收益率
    returns = np.random.normal(mean, volatility, len(date_range))
    
    # 创建包含日期和收益率的Series
    return pd.Series(returns, index=date_range)

def generate_trending_returns(days=365, trend=0.0001, volatility=0.01, seed=None):
    """
    生成带趋势的随机收益率序列
    
    参数:
        days (int): 天数
        trend (float): 每日趋势，正值为上升趋势，负值为下降趋势
        volatility (float): 每日波动率
        seed (int): 随机数种子
    
    返回:
        pandas.Series: 日期和收益率
    """
    if seed is not None:
        np.random.seed(seed)
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # 生成日期范围，仅包含工作日
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # 生成基础随机收益率
    base_returns = np.random.normal(0, volatility, len(date_range))
    
    # 添加趋势
    trends = np.linspace(0, trend * len(date_range), len(date_range))
    returns = base_returns + trends
    
    # 创建包含日期和收益率的Series
    return pd.Series(returns, index=date_range)

def generate_drawdown_scenario(days=365, pre_drawdown_mean=0.001, drawdown_days=30, 
                              drawdown_mean=-0.005, post_drawdown_mean=0.0015, 
                              volatility=0.01, seed=None):
    """
    生成包含明显回撤期的收益率序列
    
    参数:
        days (int): 总天数
        pre_drawdown_mean (float): 回撤前的平均每日收益率
        drawdown_days (int): 回撤持续的天数
        drawdown_mean (float): 回撤期间的平均每日收益率
        post_drawdown_mean (float): 回撤后的平均每日收益率
        volatility (float): 每日波动率
        seed (int): 随机数种子
    
    返回:
        pandas.Series: 日期和收益率
    """
    if seed is not None:
        np.random.seed(seed)
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # 生成日期范围，仅包含工作日
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # 计算各阶段的天数
    pre_drawdown_days = (days - drawdown_days) // 3
    post_drawdown_days = days - pre_drawdown_days - drawdown_days
    
    # 生成各阶段的收益率
    pre_returns = np.random.normal(pre_drawdown_mean, volatility, pre_drawdown_days)
    drawdown_returns = np.random.normal(drawdown_mean, volatility * 1.5, drawdown_days)
    post_returns = np.random.normal(post_drawdown_mean, volatility, post_drawdown_days)
    
    # 合并收益率
    returns = np.concatenate([pre_returns, drawdown_returns, post_returns])
    
    # 如果生成的天数不足，补足
    if len(returns) < len(date_range):
        extra = np.random.normal(post_drawdown_mean, volatility, len(date_range) - len(returns))
        returns = np.concatenate([returns, extra])
    
    # 如果生成的天数过多，截断
    if len(returns) > len(date_range):
        returns = returns[:len(date_range)]
    
    # 创建包含日期和收益率的Series
    return pd.Series(returns, index=date_range)

def plot_cumulative_returns(returns, title="累积收益率"):
    """
    绘制累积收益率图表
    
    参数:
        returns (pandas.Series): 收益率序列
        title (str): 图表标题
    """
    # 计算累积收益率
    cumulative_returns = (1 + returns).cumprod() - 1
    
    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns.index, cumulative_returns.values)
    plt.title(title)
    plt.xlabel("日期")
    plt.ylabel("累积收益率")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_to_csv(returns, filename="sample_returns.csv"):
    """
    将收益率数据保存为CSV文件
    
    参数:
        returns (pandas.Series): 收益率序列
        filename (str): 输出文件名
    """
    returns.to_csv(filename)
    print(f"数据已保存至 {filename}")

def generate_and_save_examples():
    """生成并保存多种示例数据"""
    # 生成普通随机收益率
    random_returns = generate_random_returns(days=252, mean=0.0005, volatility=0.01, seed=42)
    save_to_csv(random_returns, "random_returns.csv")
    
    # 生成上升趋势收益率
    uptrend_returns = generate_trending_returns(days=252, trend=0.0001, volatility=0.01, seed=42)
    save_to_csv(uptrend_returns, "uptrend_returns.csv")
    
    # 生成下降趋势收益率
    downtrend_returns = generate_trending_returns(days=252, trend=-0.0001, volatility=0.01, seed=42)
    save_to_csv(downtrend_returns, "downtrend_returns.csv")
    
    # 生成带有明显回撤的收益率
    drawdown_returns = generate_drawdown_scenario(days=252, seed=42)
    save_to_csv(drawdown_returns, "drawdown_returns.csv")
    
    # 生成低波动率收益率
    low_vol_returns = generate_random_returns(days=252, mean=0.0003, volatility=0.005, seed=42)
    save_to_csv(low_vol_returns, "low_volatility_returns.csv")
    
    # 生成高波动率收益率
    high_vol_returns = generate_random_returns(days=252, mean=0.001, volatility=0.02, seed=42)
    save_to_csv(high_vol_returns, "high_volatility_returns.csv")
    
    print("所有示例数据已生成")

if __name__ == "__main__":
    # 生成并保存示例数据
    generate_and_save_examples()
    
    # 作为示例，绘制并显示带有回撤的情景
    drawdown_returns = generate_drawdown_scenario(days=252, seed=42)
    plot_cumulative_returns(drawdown_returns, "带回撤期的累积收益率示例")