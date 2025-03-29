# 阿尔法和贝塔 (Alpha & Beta)

阿尔法(α)和贝塔(β)是资产定价和投资组合分析中的两个关键指标，源自于资本资产定价模型(CAPM)，用于衡量投资组合相对于市场或特定基准的表现。

## 基本定义

在CAPM模型中，投资组合的预期收益可以表示为：

$$E(R_p) = R_f + \beta \times (E(R_m) - R_f) + \alpha$$

其中：
- $E(R_p)$ 是投资组合的预期收益率
- $R_f$ 是无风险利率
- $E(R_m)$ 是市场预期收益率
- $\beta$ 是贝塔系数，衡量相对于市场的波动性
- $\alpha$ 是阿尔法，衡量投资组合的超额收益

## 贝塔 (Beta)

### 定义

贝塔衡量资产相对于市场的系统性风险，计算公式为：

$$\beta = \frac{\text{Cov}(R_p, R_m)}{\text{Var}(R_m)}$$

其中：
- $\text{Cov}(R_p, R_m)$ 是投资组合收益率与市场收益率的协方差
- $\text{Var}(R_m)$ 是市场收益率的方差

### 解释

- $\beta = 1$：投资组合与市场波动性完全一致
- $\beta > 1$：投资组合波动性大于市场（更具攻击性）
- $\beta < 1$：投资组合波动性小于市场（更具防御性）
- $\beta = 0$：投资组合与市场无相关性
- $\beta < 0$：投资组合与市场呈负相关性（罕见）

## 阿尔法 (Alpha)

### 定义

阿尔法代表投资组合相对于根据其贝塔系数预期应获得的收益率的超额收益，计算公式为：

$$\alpha = R_p - [R_f + \beta \times (R_m - R_f)]$$

其中：
- $R_p$ 是投资组合的实际收益率
- $R_f$ 是无风险利率
- $R_m$ 是市场收益率
- $\beta$ 是投资组合的贝塔系数

### 解释

- $\alpha > 0$：投资组合表现优于其风险水平所预期的回报（积极）
- $\alpha = 0$：投资组合表现与其风险水平恰好相符
- $\alpha < 0$：投资组合表现不如其风险水平所预期的回报（消极）

## Empyrical库中的实现

### 贝塔计算

```python
def beta(returns, factor_returns, risk_free=0.0, period='daily',
         annualization=None, out=None):
    """
    计算投资组合的贝塔系数。

    参数
    ----------
    returns : pd.Series 或 np.ndarray
        策略的非累积周期性收益率。
    factor_returns : pd.Series 或 np.ndarray
        因子（通常是市场）的非累积周期性收益率。
    risk_free : float, 可选
        无风险利率。默认值为0。
    period : str, 可选
        - 'monthly', 'weekly', 'daily'之一，用于年化。
        - 默认是'daily'。
    annualization : int, 可选
        用于年化收益率的常数。
        如果period被指定，这个值将被忽略。
    out : array-like, 可选
        用作输出缓冲区的数组。
        如果不提供，将创建一个新数组。

    返回
    -------
    beta : float
        贝塔系数。
    """
    # 实现逻辑：
    # 1. 计算超额收益
    # 2. 计算收益与因子收益的协方差
    # 3. 计算因子收益的方差
    # 4. 返回协方差与方差的比值
```

### 阿尔法计算

```python
def alpha(returns, factor_returns, risk_free=0.0, period='daily',
          annualization=None, out=None):
    """
    计算投资组合的阿尔法。

    参数
    ----------
    returns : pd.Series 或 np.ndarray
        策略的非累积周期性收益率。
    factor_returns : pd.Series 或 np.ndarray
        因子（通常是市场）的非累积周期性收益率。
    risk_free : float, 可选
        无风险利率。默认值为0。
    period : str, 可选
        - 'monthly', 'weekly', 'daily'之一，用于年化。
        - 默认是'daily'。
    annualization : int, 可选
        用于年化收益率的常数。
        如果period被指定，这个值将被忽略。
    out : array-like, 可选
        用作输出缓冲区的数组。
        如果不提供，将创建一个新数组。

    返回
    -------
    alpha : float
        阿尔法值。
    """
    # 实现逻辑：
    # 1. 计算贝塔系数
    # 2. 计算平均超额收益率
    # 3. 计算平均因子超额收益率
    # 4. 计算并返回阿尔法
```

## 使用示例

```python
import numpy as np
import pandas as pd
from empyrical import alpha, beta
import matplotlib.pyplot as plt

# 创建模拟数据
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=252, freq='B')
market_returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)

# 创建一个具有正阿尔法的投资组合（beta=1.2）
positive_alpha = 0.0002  # 每日额外20个基点
portfolio_returns_pos = pd.Series(
    1.2 * market_returns.values + positive_alpha + np.random.normal(0, 0.002, len(dates)),
    index=dates
)

# 创建一个具有负阿尔法的投资组合（beta=0.8）
negative_alpha = -0.0001  # 每日损失10个基点
portfolio_returns_neg = pd.Series(
    0.8 * market_returns.values + negative_alpha + np.random.normal(0, 0.002, len(dates)),
    index=dates
)

# 计算阿尔法和贝塔
beta_pos = beta(portfolio_returns_pos, market_returns)
alpha_pos = alpha(portfolio_returns_pos, market_returns, annualization=252)

beta_neg = beta(portfolio_returns_neg, market_returns)
alpha_neg = alpha(portfolio_returns_neg, market_returns, annualization=252)

print(f"积极组合 - 贝塔: {beta_pos:.4f}, 年化阿尔法: {alpha_pos:.4%}")
print(f"消极组合 - 贝塔: {beta_neg:.4f}, 年化阿尔法: {alpha_neg:.4%}")

# 可视化
plt.figure(figsize=(10, 6))

# 散点图展示收益关系
plt.scatter(market_returns, portfolio_returns_pos, alpha=0.5, label='积极组合')
plt.scatter(market_returns, portfolio_returns_neg, alpha=0.5, label='消极组合')

# 回归线
x = np.linspace(market_returns.min(), market_returns.max(), 100)
plt.plot(x, beta_pos * x + alpha_pos / 252, 'r-', linewidth=2)
plt.plot(x, beta_neg * x + alpha_neg / 252, 'b-', linewidth=2)

plt.title('贝塔和阿尔法分析')
plt.xlabel('市场收益率')
plt.ylabel('组合收益率')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 滚动阿尔法和贝塔

Empyrical还支持计算滚动窗口的阿尔法和贝塔：

```python
from empyrical import roll_alpha, roll_beta

# 使用60天窗口的滚动阿尔法和贝塔
rolling_alpha = roll_alpha(portfolio_returns_pos, market_returns, window=60)
rolling_beta = roll_beta(portfolio_returns_pos, market_returns, window=60)

# 可视化
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax1.plot(rolling_alpha)
ax1.set_title('60天滚动阿尔法')
ax1.set_ylabel('阿尔法')
ax1.grid(True)

ax2.plot(rolling_beta)
ax2.set_title('60天滚动贝塔')
ax2.set_ylabel('贝塔')
ax2.set_xlabel('日期')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## 实际应用

阿尔法和贝塔广泛应用于：

1. **基金评估**：评估基金经理是否创造了超额收益
2. **风险管理**：控制投资组合的市场敏感度
3. **风格分析**：了解投资策略的市场相关性
4. **资产配置**：构建具有目标市场敏感度的投资组合

## 注意事项和局限性

- 贝塔和阿尔法高度依赖于所选择的市场基准
- 在不同市场环境下，贝塔可能不稳定
- 短期内阿尔法和贝塔可能波动较大
- 阿尔法难以长期持续，符合有效市场假说
- 单因子CAPM模型可能过于简化，多因子模型（如Fama-French三因子模型）可能更准确

## 相关指标

- [夏普比率](./sharpe_ratio.md) - 风险调整后的收益衡量指标
- [信息比率](./information_ratio.md) - 相对于基准的风险调整后收益
- [特雷诺比率](./treynor_ratio.md) - 使用贝塔而非标准差作为风险度量的收益比率