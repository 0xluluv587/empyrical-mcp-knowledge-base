#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 检查是否安装了Docker
let useDocker = true;
try {
  execSync('docker --version', { stdio: 'ignore' });
  console.log('✅ 检测到Docker，将使用Docker运行服务');
} catch (e) {
  useDocker = false;
  console.log('⚠️ 未检测到Docker，将使用本地Python运行服务');
}

// MCP配置目录
const mcpDir = path.join(os.homedir(), '.cursor', 'mcp');
if (!fs.existsSync(mcpDir)) {
  fs.mkdirSync(mcpDir, { recursive: true });
  console.log(`✅ 创建MCP配置目录: ${mcpDir}`);
}

// MCP配置文件
const mcpConfigPath = path.join(mcpDir, 'empyrical_mcp_server.json');
const mcpConfig = {
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
};

fs.writeFileSync(mcpConfigPath, JSON.stringify(mcpConfig, null, 2));
console.log(`✅ 已更新MCP配置: ${mcpConfigPath}`);

// 运行服务
if (useDocker) {
  // 停止已存在的容器
  try {
    execSync('docker stop empyrical-mcp-server', { stdio: 'ignore' });
    execSync('docker rm empyrical-mcp-server', { stdio: 'ignore' });
  } catch (e) {
    // 忽略错误
  }

  // 构建并运行Docker容器
  console.log('🔨 构建Docker镜像...');
  execSync('docker build -t empyrical-mcp-server .', { stdio: 'inherit' });
  
  console.log('🚀 启动Docker容器...');
  execSync('docker run -d --name empyrical-mcp-server -p 8001:8001 empyrical-mcp-server', { stdio: 'inherit' });
} else {
  // 检查所需Python包
  try {
    const requiredPackages = ['fastapi', 'uvicorn', 'pandas', 'numpy', 'empyrical'];
    for (const pkg of requiredPackages) {
      try {
        execSync(`pip show ${pkg}`, { stdio: 'ignore' });
      } catch (e) {
        console.log(`📦 安装缺失的包: ${pkg}`);
        execSync(`pip install ${pkg}`, { stdio: 'inherit' });
      }
    }
  } catch (e) {
    console.error('❌ 安装Python包失败:', e);
    process.exit(1);
  }

  // 启动服务
  console.log('🚀 启动本地Python MCP服务...');
  const pythonProcess = spawn('python', [
    '-m', 'uvicorn', 
    'mcp_server.empyrical_mcp_server:app', 
    '--host', '0.0.0.0', 
    '--port', '8001'
  ], { stdio: 'inherit' });

  // 处理进程退出
  pythonProcess.on('close', (code) => {
    console.log(`🛑 MCP服务已停止，退出码: ${code}`);
  });
}

console.log('\n===========================================');
console.log('✨ Empyrical MCP服务已启动，运行在 http://localhost:8001');
console.log('✨ Cursor MCP配置已更新，请重启Cursor使更改生效');
console.log('==========================================='); 