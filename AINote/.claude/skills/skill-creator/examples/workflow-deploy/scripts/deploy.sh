#!/bin/bash
# 示例部署脚本

set -e

echo "开始部署..."

# 检查环境
if [ ! -f "./build/app.js" ]; then
    echo "错误：构建产物不存在，请先运行 npm run build"
    exit 1
fi

# 备份
echo "备份当前版本..."
cp -r ./dist ./backup/$(date +%Y%m%d_%H%M%S)

# 部署
echo "部署新版本..."
cp ./build/app.js ./dist/app.js

# 重启服务
echo "重启服务..."
pm2 restart app

echo "部署完成！"
