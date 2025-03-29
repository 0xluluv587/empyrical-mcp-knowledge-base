# 索提诺比率 (Sortino Ratio)

索提诺比率是夏普比率的改进版，它只考虑下行风险（负收益的波动性），而不是总波动性。这使得索提诺比率在分析不对称回报分布的投资策略时特别有用。

## 定义

索提诺比率计算公式为：

$$\text{Sortino Ratio} = \frac{R_p - R_f}{\sigma_d}$$

其中：
- $R_p$ 是投资组合的预期收益率
- $R_f$ 是无风险利率
- $\sigma_d$ 是下行偏差（只考虑负收益的标准偏差）

下行偏差计算方式：

$$\sigma_d = \sqrt{\frac{1}{N}\sum_{i=1}^{N} \min(r_i - T, 0)^2}$$

其中：
- $r_i$ 是第 i 期的收益率
- $T$ 是目标收益率（通常为无风险利率或零）
- $N$ 是观察期数

## 解释

- 索提诺比率越高，表示每单位下行风险的收益越高
- 相比夏普比率，索提诺比率不会"惩罚"正向波动
- 一般认为索提诺比率大于2是优秀的，0.5-1之间是一般的

## 代码实现

Empyrical 库中的索提诺比率计算：

```python
def sortino_ratio(returns, required_return=0, period='daily',
                  annualization=None, _downside_risk=None):
    """
    计算索提诺比率。

    参数
    ----------
    returns : pd.Series 或 np.ndarray
        策略的非累积周期性收益率。
    required_return : float, 可选
        最小可接受收益率。
    period : str, 可选
        - 'monthly', 'weekly', 'daily'之一，用于年化。
        - 默认是'daily'。
    annualization : int, 可选
        用于年化收益率的常数。
        如果period被指定，这个值将被忽略。
    _downside_risk : float, 可选
        已预先计算的下行风险。
        如果提供，将直接使用而不重新计算。

    返回
    -------
    sortino_ratio : float
        策略的索提诺比率。
    """
    # 实现逻辑：
    # 1. 计算平均超额收益
    # 2. 计算下行风险（或使用提供的下行风险）
    # 3. 计算并返回索提诺比率
```

## 使用示例

```python
import numpy as np
import pandas as pd
from empyrical import sortino_ratio, sharpe_ratio
import matplotlib.pyplot as plt

# 创建一个收益率序列
np.random.seed(42)
returns = np.random.normal(0.001, 0.02, 252)  # 252个交易日，平均每日收益0.1%

# 计算索提诺比率和夏普比率进行比较
sortino = sortino_ratio(returns, required_return=0)
sharpe = sharpe_ratio(returns, risk_free=0)

print(f"索提诺比率: {sortino:.4f}")
print(f"夏普比率: {sharpe:.4f}")

# 创建一个有偏分布的收益率序列（正偏态）来展示两者的区别
skewed_returns = np.concatenate([
    np.random.normal(0.002, 0.01, 200),  # 大部分是小的正收益
    np.random.normal(-0.01, 0.02, 52)    # 少部分是较大的负收益
])

sortino_skewed = sortino_ratio(skewed_returns)
sharpe_skewed = sharpe_ratio(skewed_returns)

print(f"偏态分布的索提诺比率: {sortino_skewed:.4f}")
print(f"偏态分布的夏普比率: {sharpe_skewed:.4f}")

# 可视化两种分布下的比率差异
labels = ['正态分布', '偏态分布']
sortino_values = [sortino, sortino_skewed]
sharpe_values = [sharpe, sharpe_skewed]

plt.figure(figsize=(10, 6))
x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, sortino_values, width, label='索提诺比率')
plt.bar(x + width/2, sharpe_values, width, label='夏普比率')

plt.xlabel('收益分布类型')
plt.ylabel('比率值')
plt.title('索提诺比率与夏普比率比较')
plt.xticks(x, labels)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 滚动索提诺比率

与夏普比率类似，Empyrical 也支持计算滚动窗口的索提诺比率：

```python
from empyrical import roll_sortino_ratio

# 使用60天窗口的滚动索提诺比率
dates = pd.date_range('2023-01-01', periods=252, freq='B')
returns = pd.Series(np.random.normal(0.0005, 0.01, 252), index=dates)

rolling_sortino = roll_sortino_ratio(returns, window=60)

plt.figure(figsize=(12, 6))
plt.plot(rolling_sortino)
plt.title('60天滚动索提诺比率')
plt.xlabel('日期')
plt.ylabel('索提诺比率')
plt.grid(True)
plt.show()
```

## 实际应用

索提诺比率常用于：

1. **对冲基金评估**：评估具有非正态回报分布的策略
2. **不对称策略**：评估期权策略、投机交易等不对称回报的策略
3. **风险调整后的绩效比较**：比较两个投资组合的风险调整后收益率
4. **风险管理**：设定风险预算和止损标准

## 索提诺比率 vs 夏普比率

| 特点 | 索提诺比率 | 夏普比率 |
|------|------------|----------|
| 风险衡量 | 仅考虑下行风险 | 考虑总波动率 |
| 适用情景 | 非对称回报分布 | 正态分布回报 |
| 对正向波动 | 不惩罚 | 同等对待正负波动 |
| 计算复杂度 | 较高 | 较低 |
| 理论基础 | 后现代投资组合理论 | 现代投资组合理论 |

## 索提诺比率的局限性

- 仅考虑波动性，不考虑其他风险类型
- 依赖历史数据，可能不能很好地预测未来
- 对异常值敏感
- 相比夏普比率，市场认可度较低

## 相关指标

- [夏普比率](./sharpe_ratio.md) - 考虑总波动率的风险调整收益指标
- [卡尔玛比率](./calmar_ratio.md) - 使用最大回撤作为风险度量
- [信息比率](./information_ratio.md) - 衡量相对于基准的超额收益与跟踪误差比值
- [下行风险](./downside_risk.md) - 索提诺比率使用的风险衡量指标