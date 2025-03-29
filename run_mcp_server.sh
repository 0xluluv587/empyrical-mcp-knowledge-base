#!/bin/bash

# 构建Docker镜像
docker build -t empyrical-mcp-server .

# 停止已存在的容器
docker stop empyrical-mcp-server 2>/dev/null || true
docker rm empyrical-mcp-server 2>/dev/null || true

# 运行新容器
docker run -d --name empyrical-mcp-server -p 8001:8001 empyrical-mcp-server

# 配置Cursor MCP
mkdir -p ~/.cursor/mcp/

cat > ~/.cursor/mcp/empyrical_mcp_server.json << 'EOF'
{
  "description": "Empyrical金融指标MCP服务",
  "jsonrpc": {
    "url": "http://localhost:8001",
    "methods": {
      "mcp_empyrical_annual_return": {
        "name": "annual_return",
        "description": "计算投资组合的年化收益率",
        "parameters": {
          "properties": {
            "returns": {
              "description": "收益率数据序列",
              "type": "array"
            },
            "period": {
              "description": "数据周期，如daily、monthly、yearly",
              "type": "string"
            },
            "annualization": {
              "description": "年化系数",
              "type": "number"
            }
          },
          "required": ["returns"]
        }
      },
      "mcp_empyrical_sharpe_ratio": {
        "name": "sharpe_ratio",
        "description": "计算投资组合的夏普比率",
        "parameters": {
          "properties": {
            "returns": {
              "description": "收益率数据序列",
              "type": "array"
            },
            "risk_free": {
              "description": "无风险收益率",
              "type": "number"
            },
            "period": {
              "description": "数据周期，如daily、monthly、yearly",
              "type": "string"
            },
            "annualization": {
              "description": "年化系数",
              "type": "number"
            }
          },
          "required": ["returns"]
        }
      },
      "mcp_empyrical_max_drawdown": {
        "name": "max_drawdown",
        "description": "计算投资组合的最大回撤",
        "parameters": {
          "properties": {
            "returns": {
              "description": "收益率数据序列",
              "type": "array"
            }
          },
          "required": ["returns"]
        }
      }
    }
  }
}
EOF

echo "==========================================="
echo "Empyrical MCP服务已启动，运行在 http://localhost:8001"
echo "Cursor MCP配置已更新，请重启Cursor以使更改生效"
echo "===========================================" 