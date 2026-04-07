# 开发 (Development)

相关源文件

-   [CHANGELOG.md](https://github.com/openclaw/openclaw/blob/8873e13f/CHANGELOG.md)
-   [README.md](https://github.com/openclaw/openclaw/blob/8873e13f/README.md)
-   [apps/android/app/build.gradle.kts](https://github.com/openclaw/openclaw/blob/8873e13f/apps/android/app/build.gradle.kts)
-   [apps/ios/Sources/Info.plist](https://github.com/openclaw/openclaw/blob/8873e13f/apps/ios/Sources/Info.plist)
-   [apps/ios/Tests/Info.plist](https://github.com/openclaw/openclaw/blob/8873e13f/apps/ios/Tests/Info.plist)
-   [apps/ios/project.yml](https://github.com/openclaw/openclaw/blob/8873e13f/apps/ios/project.yml)
-   [apps/macos/Sources/OpenClaw/Resources/Info.plist](https://github.com/openclaw/openclaw/blob/8873e13f/apps/macos/Sources/OpenClaw/Resources/Info.plist)
-   [assets/avatar-placeholder.svg](https://github.com/openclaw/openclaw/blob/8873e13f/assets/avatar-placeholder.svg)
-   [docs/cli/index.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/cli/index.md)
-   [docs/gateway/configuration.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/gateway/configuration.md)
-   [docs/gateway/index.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/gateway/index.md)
-   [docs/gateway/troubleshooting.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/gateway/troubleshooting.md)
-   [docs/index.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/index.md)
-   [docs/platforms/mac/release.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/platforms/mac/release.md)
-   [docs/start/getting-started.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/start/getting-started.md)
-   [docs/start/wizard.md](https://github.com/openclaw/openclaw/blob/8873e13f/docs/start/wizard.md)
-   [extensions/bluebubbles/src/send-helpers.ts](https://github.com/openclaw/openclaw/blob/8873e13f/extensions/bluebubbles/src/send-helpers.ts)
-   [package.json](https://github.com/openclaw/openclaw/blob/8873e13f/package.json)
-   [pnpm-lock.yaml](https://github.com/openclaw/openclaw/blob/8873e13f/pnpm-lock.yaml)
-   [scripts/clawtributors-map.json](https://github.com/openclaw/openclaw/blob/8873e13f/scripts/clawtributors-map.json)
-   [scripts/update-clawtributors.ts](https://github.com/openclaw/openclaw/blob/8873e13f/scripts/update-clawtributors.ts)
-   [scripts/update-clawtributors.types.ts](https://github.com/openclaw/openclaw/blob/8873e13f/scripts/update-clawtributors.types.ts)
-   [src/agents/subagent-registry-cleanup.test.ts](https://github.com/openclaw/openclaw/blob/8873e13f/src/agents/subagent-registry-cleanup.test.ts)
-   [src/cli/program.ts](https://github.com/openclaw/openclaw/blob/8873e13f/src/cli/program.ts)
-   [src/config/config.ts](https://github.com/openclaw/openclaw/blob/8873e13f/src/config/config.ts)
-   [src/config/types.ts](https://github.com/openclaw/openclaw/blob/8873e13f/src/config/types.ts)
-   [src/config/zod-schema.ts](https://github.com/openclaw/openclaw/blob/8873e13f/src/config/zod-schema.ts)
-   [ui/package.json](https://github.com/openclaw/openclaw/blob/8873e13f/ui/package.json)

本页记录了 OpenClaw 的开发、构建和发布流程。OpenClaw 是一个多语言单体仓库 (monorepo)，包含 Node.js 网关、基于 Lit 的 Web UI、iOS/macOS Swift 应用、Android Kotlin 应用以及 Python 技能。

有关特定的流程细节，请参见：

-   **CI/CD 管道**：GitHub Actions 自动化、分片测试和缓存策略。见 [8.1](/openclaw/openclaw/8.1-cicd-pipeline)。
-   **发布流程**：版本控制策略、变更日志管理和平台分发。见 [8.2](/openclaw/openclaw/8.2-release-process)。
-   **插件开发**：使用插件 SDK 扩展 OpenClaw。见 [8.3](/openclaw/openclaw/8.3-plugins)。

---

## 技术栈与工具链 (Tech Stack & Tooling)

| 组件 | 语言 / 框架 | 构建工具 |
| --- | --- | --- |
| **网关 (Gateway)** | TypeScript (Node.js) | pnpm, esbuild, vitest |
| **控制 UI (Control UI)** | TypeScript (Lit) | Vite, pnpm |
| **iOS / macOS** | Swift (SwiftUI) | XcodeGen, SwiftPM |
| **Android** | Kotlin (Compose) | Gradle |
| **技能 (Skills)** | Python | poetry (可选), pytest |

**核心依赖**：

-   **智能体 SDK**：`@mariozechner/pi-agent-core`
-   **配置验证**：`zod`
-   **CLI 框架**：`commander`
-   **数据库**：SQLite (通过 `better-sqlite3` 或内置驱动)

**来源**：[package.json1-443](https://github.com/openclaw/openclaw/blob/8873e13f/package.json#L1-L443) [README.md92-120](https://github.com/openclaw/openclaw/blob/8873e13f/README.md#L92-L120)

---

## 本地开发入门 (Local Development)

### 1. 环境准备

确保已安装 **Node.js 22+** 和 **pnpm**。

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
```
### 2. 构建与运行

```bash
# 构建网关和 UI
pnpm build
pnpm ui:build

# 启动开发模式网关（自动重载）
pnpm gateway:watch
```
### 3. 测试

```bash
pnpm test          # 运行所有单元测试
pnpm test:e2e      # 运行端到端测试
pnpm check         # 运行类型检查和 Lint
```
**来源**：[package.json217-230](https://github.com/openclaw/openclaw/blob/8873e13f/package.json#L217-L230) [README.md92-120](https://github.com/openclaw/openclaw/blob/8873e13f/README.md#L92-L120)

---

## 贡献指南 (Contribution Guidelines)

我们欢迎代码贡献、文档改进和 Bug 报告。

1.  **Fork 仓库**并创建功能分支。
2.  **遵循代码风格**：使用 `pnpm format` 自动格式化。
3.  **编写测试**：为新功能或 Bug 修复添加 Vitest 测试。
4.  **更新变更日志**：在 `CHANGELOG.md` 的 `## Unreleased` 部分添加描述。
5.  **提交 PR**：确保 CI 通过。

**贡献者致谢**：`scripts/update-clawtributors.ts` 脚本用于自动维护 README.md 中的贡献者列表。

**来源**：[scripts/update-clawtributors.ts1-227](https://github.com/openclaw/openclaw/blob/8873e13f/scripts/update-clawtributors.ts#L1-L227) [CHANGELOG.md1-166](https://github.com/openclaw/openclaw/blob/8873e13f/CHANGELOG.md#L1-L166)
