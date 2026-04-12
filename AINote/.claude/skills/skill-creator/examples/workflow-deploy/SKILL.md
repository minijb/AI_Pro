---
name: example-deploy
description: >
  示例：部署应用到生产环境。当用户想要部署应用、运行部署脚本、发布新版本时使用。
  触发场景："/deploy"、"部署到生产"、"发布新版本"、"run deploy"
disable-model-invocation: true
context: fork
---

# 应用部署流程

按照以下步骤部署应用到生产环境。

## 步骤 1：前置检查

在部署前执行以下检查：

- [ ] 所有测试通过
- [ ] 构建产物存在
- [ ] 生产环境配置正确
- [ ] 备份当前版本

## 步骤 2：执行部署

运行部署脚本：

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/deploy.sh
```

部署脚本会：
1. 停止当前服务
2. 备份数据库
3. 部署新版本
4. 重启服务

## 步骤 3：健康检查

部署完成后，运行健康检查：

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/health-check.sh
```

检查项：
- [ ] 服务响应正常
- [ ] 数据库连接正常
- [ ] 日志无错误

## 步骤 4：回滚（如失败）

如果部署失败，执行回滚：

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/rollback.sh
```

回滚会恢复到最后一次成功的版本。

## 注意事项

1. **不要在高峰期部署** — 选择低流量时段
2. **保持通信** — 重要部署通知团队
3. **监控日志** — 部署后持续监控 30 分钟
