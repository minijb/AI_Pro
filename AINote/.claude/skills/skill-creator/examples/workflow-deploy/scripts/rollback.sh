#!/bin/bash
# 示例回滚脚本

set -e

echo "执行回滚..."

# 找到最新的备份
LATEST_BACKUP=$(ls -td ./backup/*/ | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "错误：没有可用的备份"
    exit 1
fi

echo "从 $LATEST_BACKUP 恢复..."
rm -rf ./dist
cp -r "$LATEST_BACKUP" ./dist

# 重启服务
pm2 restart app

echo "回滚完成！"
