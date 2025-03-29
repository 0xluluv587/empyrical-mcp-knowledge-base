# Empyrical MCP 服务

这个MCP（Model Client Protocol）服务封装了[Empyrical库](https://github.com/quantopian/empyrical)的功能，使AI模型能够轻松调用各种金融风险和收益指标计算功能。

## 功能特点

- 提供对Empyrical库主要金融指标的访问
- 支持常用指标如夏普比率、最大回撤、年化收益率等计算
- 符合MCP协议标准，可与AI模型无缝集成
- 提供简单清晰的API接口

## 安装与设置

### 依赖安装

1. 首先，确保已安装Python 3.8或更高版本
2. 安装所需依赖:

```bash
pip install -r requirements.txt
```

### 启动服务

执行以下命令启动MCP服务:

```bash
uvicorn empyrical_mcp_server:app --host 0.0.0.0 --port 8000
```

## 在Cursor中配置为MCP服务

要将此服务配置为Cursor IDE中的MCP服务，请使用Cursor的MCP安装工具:

```bash
npx @cursor/cursor-installer add-to-cursor-config --name "Empyrical MCP" --command "python" --args "mcp_server/empyrical_mcp_server.py"
```

## 可用方法

服务提供以下金融指标计算方法:

| 方法名 | 描述 | 必要参数 | 可选参数 |
|--------|------|----------|----------|
| `annual_return` | 计算年化收益率 | `returns` | `period`, `annualization` |
| `max_drawdown` | 计算最大回撤 | `returns` | - |
| `sharpe_ratio` | 计算夏普比率 | `returns` | `risk_free`, `period`, `annualization` |
| `sortino_ratio` | 计算索提诺比率 | `returns` | `required_return`, `period`, `annualization` |
| `calmar_ratio` | 计算卡玛比率 | `returns` | `period`, `annualization` |
| `alpha_beta` | 计算阿尔法和贝塔系数 | `returns`, `factor_returns` | `risk_free`, `period`, `annualization` |
| `annual_volatility` | 计算年化波动率 | `returns` | `period`, `alpha`, `annualization` |
| `information_ratio` | 计算信息比率 | `returns`, `factor_returns` | `period` |
| `downside_risk` | 计算下行风险 | `returns` | `required_return`, `period`, `annualization` |
| `tracking_error` | 计算跟踪误差 | `returns`, `factor_returns` | `period` |
| `value_at_risk` | 计算风险价值 | `returns` | `cutoff` |
| `get_available_metrics` | 获取可用指标列表 | - | - |

## 示例请求

以下是通过curl发送MCP请求的示例:

### 1. 计算夏普比率

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0", 
  "method": "sharpe_ratio", 
  "params": {
    "returns": [0.01, -0.02, 0.03, 0.01, -0.01, 0.02], 
    "risk_free": 0.0, 
    "period": "daily", 
    "annualization": 252
  }, 
  "id": 1
}' http://localhost:8000/
```

### 2. 计算最大回撤

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0", 
  "method": "max_drawdown", 
  "params": {
    "returns": [0.01, 0.02, 0.03, -0.4, -0.06, -0.02, 0.1, 0.05]
  }, 
  "id": 2
}' http://localhost:8000/
```

## 参数说明

- `returns`: 收益率数据列表，如[0.01, -0.02, 0.03, 0.01]
- `factor_returns`: 基准收益率数据列表，如[0.005, -0.01, 0.02, 0.005]
- `period`: 收益率周期，可选值为'daily', 'weekly', 'monthly', 'quarterly', 'yearly'
- `annualization`: 年化因子，如果不指定则根据period自动确定
- `risk_free`: 无风险利率，默认为0
- `required_return`: 最低要求收益率，默认为0
- `cutoff`: 风险价值(VaR)的置信水平，默认为0.05

## 错误处理

服务遵循标准JSON-RPC 2.0错误处理协议，常见错误代码包括:

- `-32700`: 解析错误
- `-32600`: 无效请求
- `-32601`: 方法不存在
- `-32602`: 无效参数
- `-32603`: 内部错误

## 与知识库集成

本MCP服务与[Empyrical指标知识库](https://github.com/0xluluv587/empyrical-mcp-knowledge-base)完全集成，您可以在知识库文档中找到各项指标的详细解释和使用示例。