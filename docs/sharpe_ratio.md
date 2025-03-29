# 夏普比率 (Sharpe Ratio)

夏普比率是由诺贝尔经济学奖得主 William F. Sharpe 发明的，用于衡量投资组合的风险调整收益。它是金融领域最广泛使用的绩效指标之一。

## 定义

夏普比率是超额收益（投资组合收益减去无风险利率）与收益波动性（标准差）的比率。公式如下：

$$\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}$$

其中：
- $R_p$ 是投资组合的预期收益率
- $R_f$ 是无风险利率
- $\sigma_p$ 是投资组合收益的标准差

## 解释

- **正值**：正的夏普比率表示投资组合相对于无风险资产有更高的收益。数值越大，表示每单位风险获得的超额收益越高。
- **零值**：夏普比率为零表明投资组合的预期收益与无风险利率相同。
- **负值**：负的夏普比率表示投资组合表现不如无风险资产。

一般而言：
- 夏普比率 < 1：表现不佳
- 夏普比率 1-2：良好
- 夏普比率 2-3：非常好
- 夏普比率 > 3：优秀（但可能不可持续）

## 代码实现

Empyrical 库中的夏普比率计算：

```python
def sharpe_ratio(returns, risk_free=0, period='daily', annualization=None, out=None):
    """
    计算投资组合的夏普比率。

    参数:
    ----------
    returns : pd.Series 或 np.ndarray
        投资组合的非累积日收益率序列。
    risk_free : int, float
        整个期间的恒定无风险收益率。
    period : str, 可选
        定义收益数据的周期性以用于年化。
        默认值：
            'monthly': 12
            'weekly': 52
            'daily': 252
    annualization : int, 可选
        用于将收益转换为年化收益的年化因子。
    out : array-like, 可选
        用作输出缓冲区的数组。
        如果不提供，将创建一个新数组。

    返回:
    -------
    sharpe_ratio : float
        夏普比率值。
    """
    # 实现逻辑：
    # 1. 调整收益率（减去无风险利率）
    # 2. 计算平均超额收益率与其标准差的比值
    # 3. 乘以年化因子的平方根
```

## 使用示例

```python
import numpy as np
from empyrical import sharpe_ratio

# 创建一个包含日收益率的数组
daily_returns = np.array([0.001, 0.002, -0.001, 0.003, -0.002, 0.001])

# 计算夏普比率（无风险利率为0）
sharpe = sharpe_ratio(daily_returns, risk_free=0)
print(f"夏普比率: {sharpe:.4f}")

# 使用不同的无风险利率（如年化3%的日等价值）
daily_risk_free = 0.03 / 252  # 假设一年252个交易日
sharpe_with_rf = sharpe_ratio(daily_returns, risk_free=daily_risk_free)
print(f"考虑无风险利率的夏普比率: {sharpe_with_rf:.4f}")
```

## 优缺点

### 优点
- 简单直观，易于计算和理解
- 允许不同风险特性的投资组合之间的比较
- 广泛应用于金融行业

### 缺点
- 假设收益率呈正态分布，不能很好地处理偏斜和尖峰厚尾分布
- 同样惩罚上行和下行波动性
- 对极端风险事件（黑天鹅）不敏感
- 可能被操纵（例如通过选择性回测窗口）

## 改进版本

- **经过修正的夏普比率**：调整了自由度，考虑了样本量
- **索提诺比率**：只考虑下行风险
- **信息比率**：使用基准收益代替无风险利率
- **欧米茄比率**：考虑了收益分布的更多特征

## 相关指标

- [索提诺比率](./sortino_ratio.md) - 类似于夏普比率，但只考虑下行风险
- [信息比率](./information_ratio.md) - 衡量相对于基准的超额收益与跟踪误差的比率
- [特雷诺比率](./treynor_ratio.md) - 使用贝塔代替标准差作为风险度量