# 最大回撤 (Maximum Drawdown)

最大回撤是衡量投资风险的一个重要指标，它表示投资组合从峰值到谷值的最大损失百分比。这个指标特别关注下行风险，是投资者评估策略潜在风险的关键指标。

## 定义

最大回撤是投资组合在特定时间段内从峰值到后续最低点的最大百分比下跌。用数学方式表示为：

$$\text{MDD} = \min_{t \in (0,T)} \left( \frac{V_t - \max_{0 \leq \tau \leq t} V_\tau}{\max_{0 \leq \tau \leq t} V_\tau} \right)$$

其中：
- $V_t$ 是时间 t 的投资组合价值
- $T$ 是考察期间的总时间长度

简单来说，最大回撤回答了一个问题："如果我在最糟糕的时机买入并在最差的时机卖出，我会损失多少？"

## 解释

- 最大回撤以百分比表示，范围通常在 0 到 -1 之间，即 0% 到 -100%
- 数值越小（越接近 -1 或 -100%），表示风险越大
- 较低的最大回撤表示策略可能更稳定
- 最大回撤不考虑回撤持续的时间长度（恢复期）

## 代码实现

Empyrical 库中的最大回撤计算：

```python
def max_drawdown(returns, out=None):
    """
    确定策略的最大回撤。

    参数
    ----------
    returns : pd.Series 或 np.ndarray
        策略的非累积日收益率。
    out : array-like, 可选
        用作输出缓冲区的数组。
        如果不提供，将创建一个新数组。

    返回
    -------
    max_drawdown : float
        最大回撤值。
    """
    # 实现逻辑：
    # 1. 计算累积收益
    # 2. 计算累积最大收益
    # 3. 计算回撤 = (当前累积收益 - 累积最大收益) / 累积最大收益
    # 4. 返回最小回撤值（即最大损失）
```

## 使用示例

```python
import numpy as np
from empyrical import max_drawdown, cum_returns
import matplotlib.pyplot as plt

# 创建收益率序列
returns = np.array([0.01, 0.02, 0.03, -0.05, -0.1, 0.01, 0.02, 0.04, -0.03, 0.01])

# 计算最大回撤
mdd = max_drawdown(returns)
print(f"最大回撤: {mdd:.4f}")  # 以小数形式输出，如 -0.1456

# 可视化
cumulative_returns = cum_returns(returns, starting_value=1)

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns)
plt.title(f'累积收益曲线 (最大回撤: {mdd:.2%})')
plt.xlabel('时间')
plt.ylabel('价值')
plt.grid(True)
plt.show()
```

## 滚动最大回撤

Empyrical 还提供了计算滚动窗口最大回撤的功能：

```python
from empyrical import roll_max_drawdown

# 计算3期滚动窗口最大回撤
returns = np.array([0.01, 0.02, 0.03, -0.04, -0.05, 0.02])
rolling_mdd = roll_max_drawdown(returns, window=3)
print(rolling_mdd)
```

## 实际应用

最大回撤常用于：

1. **风险管理**：设定止损阈值
2. **策略评估**：比较不同投资策略的风险特性
3. **投资者沟通**：向客户解释潜在的下行风险
4. **基金评级**：评估基金管理者控制风险的能力

## 最大回撤的缺点

- 仅关注单一最差时期，忽略其他回撤
- 不考虑回撤持续的时间长度
- 过去的最大回撤不一定能预测未来
- 不考虑回撤发生的频率

## 相关指标

- **卡尔玛比率 (Calmar Ratio)**：年化收益率除以最大回撤
- **MAR比率**：类似于卡尔玛比率，但通常使用3年或5年的最大回撤
- **平均回撤 (Average Drawdown)**：所有回撤的平均值
- **回撤持续时间 (Drawdown Duration)**：从峰值到恢复到峰值的时间长度

## 延伸阅读

- [卡尔玛比率](./calmar_ratio.md) - 将年化收益与最大回撤结合的指标
- [贝塔值](./beta.md) - 另一种衡量投资风险的指标
- [下行风险](./downside_risk.md) - 只考虑负收益的风险度量