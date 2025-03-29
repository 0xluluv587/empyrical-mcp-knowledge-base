#!/bin/bash

# Empyrical MCP服务安装脚本

echo "正在安装Empyrical MCP服务..."

# 确保pip已安装
if ! command -v pip &> /dev/null
then
    echo "错误: 未找到pip命令。请先安装Python和pip。"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip install -r requirements.txt

# 检查Empyrical库是否正确安装
python -c "import empyrical; print('Empyrical版本:', empyrical.__version__)" || {
    echo "错误: Empyrical库安装失败。请检查安装日志。"
    exit 1
}

# 检查FastAPI是否正确安装
python -c "import fastapi; print('FastAPI版本:', fastapi.__version__)" || {
    echo "错误: FastAPI库安装失败。请检查安装日志。"
    exit 1
}

# 检查Uvicorn是否正确安装
python -c "import uvicorn; print('Uvicorn版本:', uvicorn.__version__)" || {
    echo "错误: Uvicorn库安装失败。请检查安装日志。"
    exit 1
}

echo "依赖安装完成。"

# 提示如何在Cursor中配置MCP服务
echo ""
echo "===== Cursor MCP服务配置指南 ====="
echo "要将Empyrical MCP配置为Cursor IDE中的服务，请运行以下命令:"
echo ""
echo "npx @cursor/cursor-installer add-to-cursor-config --name \"Empyrical MCP\" --command \"python\" --args \"$(pwd)/empyrical_mcp_server.py\""
echo ""

# 提示如何启动服务
echo "===== 启动MCP服务 ====="
echo "运行以下命令启动MCP服务:"
echo ""
echo "uvicorn empyrical_mcp_server:app --host 0.0.0.0 --port 8000"
echo ""

echo "Empyrical MCP服务安装完成!"