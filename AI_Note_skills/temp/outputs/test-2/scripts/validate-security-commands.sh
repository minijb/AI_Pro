#!/bin/bash
# 验证安全扫描 agent 只能运行安全相关的命令
# 此脚本作为 PreToolUse hook 拦截非白名单命令

# 从 stdin 读取 JSON 输入
INPUT=$(cat)

# 使用 jq 提取命令内容
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# 定义允许的命令前缀白名单
# 安全审计工具
ALLOWED_PATTERNS=(
  # npm/yarn 审计
  "npm audit"
  "yarn audit"
  "pnpm audit"
  # Python 安全扫描
  "pip-audit"
  "pip list"
  "safety check"
  "bandit"
  # Go 安全扫描
  "govulncheck"
  # Rust 安全扫描
  "cargo audit"
  # 通用安全扫描工具
  "trivy"
  "grype"
  "syft"
  "snyk test"
  "snyk code"
  # 密钥扫描
  "gitleaks"
  "trufflehog"
  "detect-secrets"
  # 查看文件内容（只读）
  "cat "
  "head "
  "tail "
  "less "
  "wc "
  # 版本/帮助信息
  "npm --version"
  "npm -v"
  "node --version"
  "node -v"
  "python --version"
  "python3 --version"
  "pip --version"
  "go version"
  "rustc --version"
  "cargo --version"
  # 依赖信息查看
  "npm list"
  "npm ls"
  "npm outdated"
  "pip show"
  "pip freeze"
  "go list"
  "cargo tree"
  # 文件查找（只读）
  "find "
  "ls "
  "ls"
  # git 只读命令
  "git log"
  "git show"
  "git diff"
  "git status"
  "git ls-files"
)

# 检查命令是否匹配白名单
COMMAND_TRIMMED=$(echo "$COMMAND" | sed 's/^[[:space:]]*//')

for pattern in "${ALLOWED_PATTERNS[@]}"; do
  if echo "$COMMAND_TRIMMED" | grep -q "^${pattern}"; then
    exit 0
  fi
done

# 拦截危险操作的额外检查：即使命令前缀匹配，也拦截包含写入/修改意图的命令
if echo "$COMMAND" | grep -iE '(rm |rm$|mv |chmod |chown |install|uninstall|>\s|>>|sudo |mkfs|dd |format|wget |curl .* -o|curl .* --output)' > /dev/null; then
  echo "已拦截：安全扫描 agent 不允许执行修改操作。检测到潜在的写入/修改命令。" >&2
  exit 2
fi

# 命令不在白名单中，拦截
echo "已拦截：命令不在安全扫描允许的白名单中。" >&2
echo "允许的操作包括：安全审计工具（npm audit、pip-audit、trivy 等）、只读文件查看、依赖信息查看、git 只读命令。" >&2
exit 2
