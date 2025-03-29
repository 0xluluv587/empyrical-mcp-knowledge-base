# Empyrical MCP 服务

这个MCP（Model Client Protocol）服务封装了[Empyrical库](https://github.com/quantopian/empyrical)的功能，使AI模型能够轻松调用各种金融风险和收益指标计算功能。

## 功能特点

- 提供对Empyrical库主要金融指标的访问
- 支持常用指标如夏普比率、最大回撤、年化收益率等计算
- 符合MCP协议标准，可与AI模型无缝集成
- 提供简单清晰的API接口

## 安装与设置

### 前置条件

- Python 3.8或更高版本
- pip包管理器
- 稳定的网络连接（用于安装依赖）

### 详细安装步骤

1. **获取代码**

```bash
# 克隆整个知识库
git clone https://github.com/0xluluv587/empyrical-mcp-knowledge-base.git
cd empyrical-mcp-knowledge-base
```

2. **安装依赖**

```bash
# 安装所有必要的依赖
python3 -m pip install -r mcp_server/requirements.txt
```

或使用项目提供的安装脚本（需要先赋予执行权限）：

```bash
chmod +x mcp_server/install.sh
./mcp_server/install.sh
```

### 启动服务

**重要**：服务必须在正确的目录下启动，否则会出现模块导入错误。

```bash
# 在项目根目录下启动服务（开发模式，带自动重载）
cd empyrical-mcp-knowledge-base  # 确保在项目根目录
python3 -m uvicorn mcp_server.empyrical_mcp_server:app --reload
```

生产环境启动方式：

```bash
python3 -m uvicorn mcp_server.empyrical_mcp_server:app --host 0.0.0.0 --port 8000
```

#### 启动常见问题

如果遇到 `ModuleNotFoundError: No module named 'mcp_server'` 错误，这通常是因为命令运行的位置不正确。请确保：

1. 你在项目根目录（empyrical-mcp-knowledge-base）下运行命令，而不是在mcp_server子目录内
2. 使用模块导入方式启动服务（`python3 -m uvicorn`）
3. 模块路径正确（`mcp_server.empyrical_mcp_server:app`）

## 在Cursor中配置

### 方法一：直接编辑mcp.json配置文件（推荐）

最新版本的Claude需要通过直接编辑mcp.json文件来配置MCP服务：

1. 找到Cursor的配置目录：
   - macOS: `~/Library/Application Support/Cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\mcp.json`
   - Linux: `~/.config/Cursor/mcp.json`

2. 如果mcp.json文件不存在，创建该文件

3. 编辑mcp.json文件，添加以下内容：

```json
{
  "servers": [
    {
      "name": "Empyrical MCP",
      "command": "python3",
      "args": [
        "-m",
        "uvicorn",
        "mcp_server.empyrical_mcp_server:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "cwd": "/完整路径/empyrical-mcp-knowledge-base"
    }
  ]
}
```

4. 将上面的`"/完整路径/empyrical-mcp-knowledge-base"`替换为你实际的项目路径
   - macOS/Linux示例: `"/Users/username/Coding/empyrical-mcp-knowledge-base"`
   - Windows示例: `"C:\\Users\\username\\Coding\\empyrical-mcp-knowledge-base"`

5. 保存文件后重启Cursor IDE

### 方法二：手动通过GUI配置（如果支持）

1. 打开Cursor IDE
2. 点击"设置"（或按下Ctrl+,）
3. 搜索"MCP"或导航至"MCP服务"设置部分
4. 点击"添加MCP服务"按钮
5. 填写以下信息：
   - 名称：Empyrical MCP
   - 命令：python3
   - 参数：-m uvicorn mcp_server.empyrical_mcp_server:app --host 0.0.0.0 --port 8000
   - 工作目录：选择empyrical-mcp-knowledge-base目录的完整路径

### 方法三：命令行配置（如果Cursor安装工具可用）

```bash
# 确保在项目根目录
cd empyrical-mcp-knowledge-base

# 使用Cursor安装工具添加MCP服务
npx @cursor/cursor-installer add-to-cursor-config --name "Empyrical MCP" --command "python3" --args "-m uvicorn mcp_server.empyrical_mcp_server:app --host 0.0.0.0 --port 8000" --path "$(pwd)"
```

## 验证服务

使用以下命令验证服务是否正常运行：

```bash
# 健康检查
curl http://127.0.0.1:8000/

# 应返回: {"status":"ok","service":"Empyrical MCP Server","version":"1.0.0"}
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

### 1. 获取可用指标列表

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0", 
  "method": "get_available_metrics", 
  "params": {}, 
  "id": 1
}' http://127.0.0.1:8000/
```

### 2. 计算夏普比率

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
}' http://127.0.0.1:8000/
```

### 3. A计算最大回撤

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0", 
  "method": "max_drawdown", 
  "params": {
    "returns": [0.01, 0.02, 0.03, -0.4, -0.06, -0.02, 0.1, 0.05]
  }, 
  "id": 2
}' http://127.0.0.1:8000/
```

## 参数说明

- `returns`: 收益率数据列表，如[0.01, -0.02, 0.03, 0.01]
- `factor_returns`: 基准收益率数据列表，如[0.005, -0.01, 0.02, 0.005]
- `period`: 收益率周期，可选值为'daily', 'weekly', 'monthly', 'quarterly', 'yearly'
- `annualization`: 年化因子，如果不指定则根据period自动确定
- `risk_free`: 无风险利率，默认为0
- `required_return`: 最低要求收益率，默认为0
- `cutoff`: 风险价值(VaR)的置信水平，默认为0.05

## 常见问题排查

1. **服务无法启动**：
   - 检查Python版本是否为3.8或更高
   - 确认所有依赖是否正确安装
   - 查看日志中的具体错误信息

2. **连接被拒绝**：
   - 确保服务已成功启动
   - 检查使用的IP和端口是否正确
   - 确认防火墙设置不会阻止连接

3. **计算结果异常**：
   - 检查输入数据格式是否正确
   - 确认参数值在合理范围内
   - 参考Empyrical库文档验证计算方法

## 在AI模型中使用

配置完成后，AI模型可以通过MCP协议无缝调用所有金融指标计算函数。服务遵循标准JSON-RPC 2.0协议，支持AI模型高效地进行复杂金融分析。

## 与知识库集成

本MCP服务与[Empyrical指标知识库](https://github.com/0xluluv587/empyrical-mcp-knowledge-base)完全集成，您可以在知识库文档中找到各项指标的详细解释和使用示例。