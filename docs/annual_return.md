# 年化收益率 (Annual Return)

年化收益率是评估投资绩效的基础指标，用于标准化不同时期的投资回报，使它们可以在同一基础上进行比较。它表示投资如果保持相同的增长率，一年内可能获得的回报率。

## 定义

年化收益率将不同时间段的收益率转换为等效的年度收益率。计算方法为：

$$\text{Annual Return} = \left(1 + \text{总收益率}\right)^{\frac{365}{\text{时间段(天)}}} - 1$$

对于日度、周度或月度收益率数据，Empyrical使用相应的年化因子进行转换：
- 日度：252个交易日/年
- 周度：52周/年
- 月度：12个月/年

## 代码实现

Empyrical库中的年化收益率计算：

```python
def annual_return(returns, period='daily', annualization=None):
    """
    计算策略的年化收益率。

    参数
    ----------
    returns : pd.Series 或 np.ndarray
        策略的非累积周期性收益率。
    period : str, 可选
        - 'monthly', 'weekly', 'daily'之一，用于年化。
        - 默认是'daily'。
    annualization : int, 可选
        用于年化收益率的常数。
        如果period被指定，这个值将被忽略。

    返回
    -------
    annual_return : float
        年化收益率。
    """
    # 实现逻辑：
    # 1. 确定年化因子
    # 2. 计算累积收益
    # 3. 根据公式计算年化收益率
```

## 使用示例

```python
import numpy as np
import pandas as pd
from empyrical import annual_return

# 示例1：使用numpy数组
daily_returns = np.array([0.001, 0.002, -0.001, 0.003, 0.002])
annual_ret = annual_return(daily_returns, period='daily')
print(f"日度数据的年化收益率: {annual_ret:.4f}")

# 示例2：使用pandas Series，带有时间索引
dates = pd.date_range('2023-01-01', periods=100, freq='B')
returns = pd.Series(np.random.normal(0.001, 0.02, 100), index=dates)
annual_ret = annual_return(returns)
print(f"100天的年化收益率: {annual_ret:.4f}")

# 示例3：月度数据
monthly_returns = np.array([0.02, 0.01, -0.015, 0.025, 0.03, -0.01])
annual_ret = annual_return(monthly_returns, period='monthly')
print(f"月度数据的年化收益率: {annual_ret:.4f}")
```

## 累积收益与年化收益的关系

Empyrical库同时支持计算累积收益率和年化收益率：

```python
from empyrical import cum_returns, annual_return
import matplotlib.pyplot as plt

# 创建一年的日度收益率数据
dates = pd.date_range('2023-01-01', '2023-12-31', freq='B')  # 工作日
returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)

# 计算累积收益
cumulative_returns = cum_returns(returns, starting_value=1.0)

# 计算年化收益率
ann_ret = annual_return(returns)

# 可视化
plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns)
plt.title(f'累积收益曲线 (年化收益率: {ann_ret:.2%})')
plt.xlabel('日期')
plt.ylabel('价值')
plt.grid(True)
plt.show()
```

## 滚动年化收益率

Empyrical还支持计算滚动窗口的年化收益率：

```python
from empyrical import roll_annual_return

# 计算60天滚动窗口的年化收益率
dates = pd.date_range('2023-01-01', periods=252, freq='B')
returns = pd.Series(np.random.normal(0.0005, 0.01, 252), index=dates)

rolling_annual_returns = roll_annual_return(returns, window=60)
plt.figure(figsize=(12, 6))
plt.plot(rolling_annual_returns)
plt.title('60天滚动年化收益率')
plt.xlabel('日期')
plt.ylabel('年化收益率')
plt.grid(True)
plt.show()
```

## 实际应用

年化收益率广泛应用于：

1. **业绩比较**：在标准化基础上比较不同投资策略
2. **投资目标设定**：设定年度收益目标
3. **投资者沟通**：报告基金或投资组合表现
4. **回测分析**：评估交易策略的长期表现

## 注意事项

- 年化收益率不能反映收益的波动性或风险
- 短期高回报不一定能持续，年化计算可能会高估长期表现
- 应结合风险指标（如最大回撤、波动率）一同考虑
- 不同年化因子（如252、365、260等）可能产生略有不同的结果

## 相关指标

- **总收益率 (Total Return)**：整个投资期间的总收益
- **复合年增长率 (CAGR)**：另一种表达年化收益的方式
- **风险调整收益率**：如夏普比率，将收益与风险结合考虑
- **阿尔法 (Alpha)**：衡量相对于基准的超额收益

## 延伸阅读

- [夏普比率](./sharpe_ratio.md) - 风险调整后的收益衡量指标
- [最大回撤](./max_drawdown.md) - 评估下行风险的指标
- [阿尔法](./alpha.md) - 衡量相对于基准的超额收益