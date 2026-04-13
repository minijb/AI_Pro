#!/bin/bash
# 示例健康检查脚本

set -e

echo "运行健康检查..."

# 检查服务响应
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✓ 服务响应正常"
else
    echo "✗ 服务无响应"
    exit 1
fi

# 检查数据库连接
if curl -f http://localhost:3000/api/db-check > /dev/null 2>&1; then
    echo "✓ 数据库连接正常"
else
    echo "✗ 数据库连接失败"
    exit 1
fi

echo "所有检查通过！"
