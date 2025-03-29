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

### 安装指南

#### 1. 前置条件

确保系统已安装以下软件：
- Python 3.8或更高版本
- pip包管理器

#### 2. 获取代码

```bash
# 克隆仓库
git clone https://github.com/0xluluv587/empyrical-mcp-knowledge-base.git
cd empyrical-mcp-knowledge-base
```

#### 3. 安装依赖

```bash
# 安装所有必要的依赖
python3 -m pip install -r mcp_server/requirements.txt

# 或使用安装脚本（需要先赋予执行权限）
chmod +x mcp_server/install.sh
./mcp_server/install.sh
```

### 启动服务

**重要**：必须在正确目录下启动服务，否则将出现模块导入错误。

```bash
# 在项目根目录下启动服务（开发模式，自动重载）
cd empyrical-mcp-knowledge-base  # 确保在项目根目录
python3 -m uvicorn mcp_server.empyrical_mcp_server:app --reload

# 生产环境启动方式
python3 -m uvicorn mcp_server.empyrical_mcp_server:app --host 0.0.0.0 --port 8000
```

### 在Cursor中配置MCP服务

#### 方法一：编辑mcp.json配置（推荐方式）

Cursor使用`mcp.json`文件来管理MCP服务。按照以下步骤添加Empyrical服务：

1. 找到并打开Cursor配置目录下的mcp.json文件：
   - macOS: `~/.cursor/mcp.json` 或 `~/Library/Application Support/Cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\mcp.json`
   - Linux: `~/.config/Cursor/mcp.json`

2. 在`mcpServers`对象中添加Empyrical MCP服务配置：

```json
{
  "mcpServers": {
    // 其他现有服务配置...
    
    "empyrical_mcp": {
      "isActive": true,
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
      "cwd": "/YOUR_PATH/empyrical-mcp-knowledge-base"
    }
  }
}
```

3. 将`/YOUR_PATH/empyrical-mcp-knowledge-base`替换为你的实际项目路径
   - macOS/Linux示例: `/Users/username/Coding/empyrical-mcp-knowledge-base`
   - Windows示例: `C:\\Users\\username\\Coding\\empyrical-mcp-knowledge-base`

4. 保存文件并重启Cursor IDE

#### 方法二：手动配置（如果GUI支持）

1. 打开Cursor IDE
2. 点击"设置"（或按下Ctrl+,）
3. 搜索"MCP"或导航至"MCP服务"设置部分
4. 点击"添加MCP服务"按钮
5. 填写以下信息：
   - 名称：empyrical_mcp
   - 命令：python3
   - 参数：-m uvicorn mcp_server.empyrical_mcp_server:app --host 0.0.0.0 --port 8000
   - 工作目录：选择empyrical-mcp-knowledge-base目录的完整路径

### 验证服务是否正常运行

```bash
# 健康检查
curl http://127.0.0.1:8000/

# 获取可用的指标列表
curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "get_available_metrics", "params": {}, "id": 1}' http://127.0.0.1:8000/

# 测试夏普比率计算
curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "sharpe_ratio", "params": {"returns": [0.01, -0.02, 0.03, 0.01, -0.01, 0.02], "risk_free": 0.0}, "id": 1}' http://127.0.0.1:8000/
```

### 注意事项

- 确保在**项目根目录**（empyrical-mcp-knowledge-base）下启动服务，而不是在mcp_server子目录下
- 使用模块导入方式启动（`python3 -m uvicorn`），而不是直接执行脚本
- 如果遇到连接问题，检查端口是否已被占用，可尝试更改端口号

### 可用方法

服务提供多种金融指标计算方法，完整列表和参数说明请参阅[MCP服务文档](mcp_server/README.md)。

## 示例数据

项目提供了数据生成工具，用于生成测试和演示用的金融数据：

```bash
cd empyrical-mcp-knowledge-base
python3 -m mcp_server.example_data_generator
```

## 常见问题排查

1. **模块导入错误**：如果出现`ModuleNotFoundError: No module named 'mcp_server'`，请确保在项目根目录下运行命令。

2. **连接被拒绝**：如果出现`ConnectionRefusedError: [Errno 61] Connection refused`，请确保服务已成功启动，并检查IP和端口配置。

3. **依赖安装问题**：如果遇到依赖冲突，建议创建专用虚拟环境：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 或 .venv\Scripts\activate  # Windows
   pip install -r mcp_server/requirements.txt
   ```

## 许可证

该项目采用MIT许可证。详细信息请参阅[LICENSE](LICENSE)文件。