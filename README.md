# Empyrical MCP 知识库

这个知识库是基于 [quantopian/empyrical](https://github.com/quantopian/empyrical) 开源项目创建的 MCP (Multi-Cloud Project) 知识库，旨在提供常见金融风险和绩效指标的计算工具和知识。

## 目录

- [简介](#简介)
- [主要功能](#主要功能)
- [常用指标](#常用指标)
- [使用方法](#使用方法)
- [代码示例](#代码示例)
- [进阶应用](#进阶应用)

## 简介

Empyrical 是一个 Python 库，提供了一组用于计算金融投资风险和绩效指标的函数。它被 zipline (量化交易回测引擎) 和 pyfolio (投资组合分析工具) 等项目广泛使用。

这个库主要关注点是：
1. 计算各种金融风险指标（如最大回撤、波动率等）
2. 计算绩效指标（如夏普比率、索提诺比率等）
3. 提供基于滚动窗口的计算
4. 支持 NumPy 数组和 Pandas 系列/数据框

## 主要功能

- **收益计算**：计算累积收益、年化收益等
- **风险指标**：计算最大回撤、波动率、下行风险等
- **绩效指标**：计算夏普比率、索提诺比率、卡尔玛比率等
- **风险调整指标**：计算阿尔法、贝塔等
- **滚动计算**：支持对以上所有指标进行滚动窗口计算
- **绩效归因**：执行因子绩效归因分析

## 常用指标

本知识库详细说明了以下常用金融指标：

- [最大回撤 (Maximum Drawdown)](./docs/max_drawdown.md)
- [夏普比率 (Sharpe Ratio)](./docs/sharpe_ratio.md)
- [索提诺比率 (Sortino Ratio)](./docs/sortino_ratio.md)
- [阿尔法 (Alpha)](./docs/alpha.md)
- [贝塔 (Beta)](./docs/beta.md)
- [捕获比率 (Capture Ratios)](./docs/capture_ratios.md)
- [下行风险 (Downside Risk)](./docs/downside_risk.md)
- [年化收益 (Annual Return)](./docs/annual_return.md)
- [年化波动率 (Annual Volatility)](./docs/annual_volatility.md)
- [风险价值 (Value at Risk)](./docs/value_at_risk.md)

## 使用方法

Empyrical 库可以通过 pip 安装：

```bash
pip install empyrical
```

基本使用示例：

```python
import numpy as np
import pandas as pd
from empyrical import max_drawdown, sharpe_ratio, annual_return

# 创建日收益率数据
returns = np.array([0.01, 0.02, -0.01, 0.03, -0.02, 0.01])

# 计算最大回撤
max_dd = max_drawdown(returns)
print(f"最大回撤: {max_dd:.4f}")

# 计算夏普比率 (默认无风险利率为0)
sharpe = sharpe_ratio(returns)
print(f"夏普比率: {sharpe:.4f}")

# 计算年化收益率
annual_ret = annual_return(returns)
print(f"年化收益率: {annual_ret:.4f}")
```

## 代码示例

本知识库包含多个代码示例，演示如何使用 Empyrical 库计算各种金融指标。

- [基础指标计算](./examples/basic_metrics.md)
- [滚动窗口计算](./examples/rolling_metrics.md)
- [绩效归因分析](./examples/performance_attribution.md)
- [风险调整收益](./examples/risk_adjusted_returns.md)

## 进阶应用

- [投资组合分析](./advanced/portfolio_analysis.md)
- [因子绩效归因](./advanced/factor_attribution.md)
- [极值理论在风险评估中的应用](./advanced/extreme_value_theory.md)
- [与其他库的集成使用](./advanced/integration.md)