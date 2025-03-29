# 下行风险 (Downside Risk)

## 定义

下行风险是一种风险度量方法，只考虑资产或投资组合收益率低于某一特定目标或最低可接受收益率(MAR)时的波动性。与传统的风险度量（如标准差）不同，下行风险只关注投资者真正担忧的部分——潜在的损失风险。

下行风险的核心理念源于行为金融学的观察：投资者对损失的厌恶程度远高于对等额收益的偏好（损失厌恶心理）。

## 计算方法

下行风险的一般计算公式为：

```
下行风险 = √[Σ min(0, Ri - MAR)² / n]
```

其中：
- Ri：第i期的收益率
- MAR：最低可接受收益率或目标收益率
- n：样本数量
- min(0, Ri - MAR)表示仅当收益率低于MAR时，才计入风险

## 常见的下行风险指标

### 1. 下行偏差 (Downside Deviation)
最常用的下行风险指标，衡量收益率低于MAR时的平均偏离程度。

### 2. 半方差 (Semi-Variance)
特殊情况下的下行偏差，当MAR设为平均收益率时的下行风险。

### 3. 下行潜力 (Downside Potential)
收益率低于MAR时的平均偏离，不进行平方处理。

## 代码实现

使用Python计算下行风险的示例：

```python
import numpy as np
import pandas as pd

def downside_risk(returns, mar=0, period='daily', annualization=252):
    """
    计算下行风险
    
    参数:
    returns: 收益率序列
    mar: 最低可接受收益率，默认为0
    period: 收益率周期，可选daily、weekly、monthly等
    annualization: 年化因子
    
    返回:
    年化下行风险
    """
    # 只选取低于最低可接受收益率的部分
    downside_returns = np.minimum(returns - mar, 0)
    
    # 计算平方和再开方
    downside_risk = np.sqrt(np.mean(downside_returns**2))
    
    # 转换为年化下行风险
    if period == 'daily':
        annualized_downside_risk = downside_risk * np.sqrt(annualization)
    elif period == 'weekly':
        annualized_downside_risk = downside_risk * np.sqrt(52)
    elif period == 'monthly':
        annualized_downside_risk = downside_risk * np.sqrt(12)
    else:
        annualized_downside_risk = downside_risk
    
    return annualized_downside_risk

# 示例使用
returns = np.array([0.01, -0.02, 0.03, 0.01, -0.01, -0.03, 0.02, 0.01, -0.02, 0.01])
mar = 0  # 最低可接受收益率设为0

# 计算下行风险
result = downside_risk(returns, mar, 'daily', 252)
print(f"年化下行风险: {result:.4f}")
```

## 实际应用

下行风险在投资决策中的应用：

1. **投资组合构建**：构建偏重下行风险而非总体波动性的投资组合
2. **风险调整后收益评估**：作为索提诺比率等风险调整后收益指标的分母
3. **不同资产类别的比较**：特别适用于收益分布不对称的资产（如对冲基金、期权策略）
4. **金融产品设计**：设计符合投资者真实风险偏好的产品

## 最低可接受收益率(MAR)的选择

MAR的选择对下行风险计算有重大影响，常见的选择包括：

1. **零收益率**：最保守的选择，任何负收益都被视为风险
2. **无风险利率**：如短期国债收益率
3. **通胀率**：保持实际购买力的最低要求
4. **绝对目标收益**：基于投资者特定收益目标
5. **相对基准**：如市场指数收益率

## 优势与局限性

### 优势
1. 更符合投资者实际风险感知（损失厌恶）
2. 适用于收益分布不对称的投资策略
3. 提供了更精确的下行风险度量
4. 便于设定特定风险目标

### 局限性
1. 计算相对复杂
2. MAR的选择具有主观性
3. 可能需要更长的历史数据才能得到稳健估计
4. 不像标准差那样被广泛使用和理解

## 相关指标

- **索提诺比率**：使用下行风险替代标准差的风险调整后收益指标
- **欧米茄比率**：考虑上行潜力与下行风险的综合指标
- **最大回撤**：另一种关注下行风险的度量，衡量从峰值到谷值的最大损失

下行风险为投资者提供了更符合实际风险感知的风险度量方法，特别适用于评估不遵循正态分布的投资策略的风险。