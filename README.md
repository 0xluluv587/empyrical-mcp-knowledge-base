# Empyrical 指标知识库

这个知识库包含了量化金融中常用的风险指标和绩效评估指标的详细说明。每个文档都包括指标的定义、计算方法、代码实现和实际应用场景。

## 目录

### 收益指标
- [年化收益率 (Annual Return)](docs/annual_return.md) - 投资收益率的年化表示
- [阿尔法 (Alpha)](docs/alpha_beta.md#阿尔法-alpha) - 相对于市场基准的超额收益

### 风险指标
- [贝塔 (Beta)](docs/alpha_beta.md#贝塔-beta) - 相对于市场的系统性风险
- [最大回撤 (Maximum Drawdown)](docs/max_drawdown.md) - 最大损失幅度
- [波动率 (Volatility)](docs/volatility.md) - 收益率的标准差
- [风险价值 (Value at Risk, VaR)](docs/value_at_risk.md) - 特定置信水平下的最大潜在损失

### 风险调整后收益指标
- [夏普比率 (Sharpe Ratio)](docs/sharpe_ratio.md) - 超额收益与总风险的比率
- [索提诺比率 (Sortino Ratio)](docs/sortino_ratio.md) - 超额收益与下行风险的比率
- [卡玛比率 (Calmar Ratio)](docs/calmar_ratio.md) - 年化收益与最大回撤的比率
- [信息比率 (Information Ratio)](docs/information_ratio.md) - 超额收益与跟踪误差的比率

## 使用指南

每个文档都遵循相同的结构：
1. **定义** - 指标的基本概念和意义
2. **计算方法** - 数学公式和计算步骤
3. **代码实现** - 使用Python和Empyrical库的示例代码
4. **实际应用** - 指标的实际使用场景和解释标准
5. **优势与局限性** - 指标的优点和不足之处

## 示例代码

以下是使用Empyrical库计算夏普比率的示例：

```python
import numpy as np
from empyrical import sharpe_ratio

# 假设我们有一系列每日收益率
daily_returns = np.array([0.001, -0.002, 0.003, 0.001, -0.001, 0.002, 0.001])

# 计算夏普比率（假设年化无风险利率为2%）
risk_free_rate = 0.02
annualization_factor = 252  # 交易日数量
result = sharpe_ratio(daily_returns, risk_free=risk_free_rate, 
                      period='daily', annualization=annualization_factor)

print(f"夏普比率: {result}")
```

## 贡献指南

欢迎提交pull request来完善和扩展这个知识库。添加新文档时，请确保：
1. 遵循现有的文档结构
2. 包含准确的定义和计算方法
3. 提供实用的代码示例
4. 解释实际应用场景

## 相关资源

- [Empyrical库文档](https://github.com/quantopian/empyrical)
- [量化投资学习资源](https://github.com/0xluluv587/quant-learning-resources)

## 许可证

本知识库采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。