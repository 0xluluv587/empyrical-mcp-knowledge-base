# Empyrical MCP知识库

该项目是一个全面的量化金融指标知识库，提供了量化金融指标的定义、计算方法、代码实现和实际应用介绍，同时包含了将这些指标作为MCP服务提供的实现。

## 项目组成

本项目分为两个主要部分：

1. **金融指标知识库**：详细的金融指标文档，包含定义、计算方法、代码实现和应用场景。
2. **Empyrical MCP服务**：基于[Empyrical库](https://github.com/quantopian/empyrical)的MCP服务实现，允许通过API调用进行金融指标计算。

## 金融指标文档

### 收益类指标
- [年化收益率 (Annual Return)](docs/annual_return.md)

### 风险类指标
- [最大回撤 (Maximum Drawdown)](docs/max_drawdown.md)
- [波动率 (Volatility)](docs/volatility.md)
- [下行风险 (Downside Risk)](docs/downside_risk.md)
- [跟踪误差 (Tracking Error)](docs/tracking_error.md)
- [风险价值 (Value at Risk, VaR)](docs/value_at_risk.md)

### 风险调整收益类指标
- [夏普比率 (Sharpe Ratio)](docs/sharpe_ratio.md)
- [索提诺比率 (Sortino Ratio)](docs/sortino_ratio.md)
- [卡玛比率 (Calmar Ratio)](docs/calmar_ratio.md)
- [信息比率 (Information Ratio)](docs/information_ratio.md)
- [阿尔法与贝塔 (Alpha & Beta)](docs/alpha_beta.md)

### 指标适用场景表

| 指标名称 | 策略评估 | 风险管理 | 资产配置 | 基准比较 | 适合长期 | 适合短期 |
|---------|---------|---------|---------|---------|---------|---------|
| 年化收益率 | ✓ | | ✓ | ✓ | ✓ | |
| 最大回撤 | ✓ | ✓ | ✓ | | ✓ | |
| 波动率 | ✓ | ✓ | ✓ | | ✓ | ✓ |
| 下行风险 | ✓ | ✓ | ✓ | | ✓ | |
| 跟踪误差 | | | ✓ | ✓ | ✓ | |
| 风险价值 | | ✓ | ✓ | | | ✓ |
| 夏普比率 | ✓ | | ✓ | ✓ | ✓ | |
| 索提诺比率 | ✓ | | ✓ | ✓ | ✓ | |
| 卡玛比率 | ✓ | | ✓ | | ✓ | |
| 信息比率 | ✓ | | ✓ | ✓ | ✓ | |
| 阿尔法 | ✓ | | ✓ | ✓ | ✓ | |
| 贝塔 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Empyrical MCP服务

本项目提供了基于Empyrical库的MCP服务实现，使AI能够直接调用金融指标计算功能。

### 服务特点

- 基于FastAPI实现的高性能MCP服务
- 支持所有Empyrical库的主要金融指标计算
- 提供RESTful API接口
- 易于集成到AI助手和应用程序中

### 快速开始

完整的MCP服务代码和文档位于[mcp_server](mcp_server/)目录下。

#### 安装

```bash
# 克隆仓库
git clone https://github.com/0xluluv587/empyrical-mcp-knowledge-base.git
cd empyrical-mcp-knowledge-base/mcp_server

# 安装依赖
pip install -r requirements.txt

# 或使用安装脚本
chmod +x install.sh
./install.sh
```

#### 启动服务

```bash
uvicorn empyrical_mcp_server:app --host 0.0.0.0 --port 8000
```

#### 在Cursor中配置MCP服务

```bash
npx @cursor/cursor-installer add-to-cursor-config --name "Empyrical MCP" --command "python" --args "$(pwd)/empyrical_mcp_server.py"
```

#### 测试服务

```bash
# 运行测试脚本
python test_mcp_service.py
```

### 详细文档

更多关于MCP服务的详细信息，包括API参考、使用示例和测试方法，请参阅[MCP服务文档](mcp_server/README.md)。

## 示例数据

项目提供了数据生成工具，用于生成测试和演示用的金融数据：

```bash
cd mcp_server
python example_data_generator.py
```

## 许可证

该项目采用MIT许可证。详细信息请参阅[LICENSE](LICENSE)文件。