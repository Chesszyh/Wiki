# 构建系统和开发

相关源文件

- [.npmrc](https://github.com/microsoft/vscode/blob/1be3088d/.npmrc)\n

本文档描述了 VS Code 的构建系统架构、依赖管理策略和开发工作流程。

有关整体应用程序架构的信息，请参阅[概述](/microsoft/vscode/1-overview)。

---

## 构建系统架构

VS Code 使用多阶段构建系统来编译 TypeScript 源代码、管理本机依赖项并生成特定于平台的分发包。

### 包结构

__代码块_0__\n

### 依赖管理

VS Code 使用混合方法，针对不同的上下文使用多个 `package.json` 文件：

|

根 `package.json` 通过 `.npmrc` 定义 npm 配置：

__代码块_1__\n

来源：[package.json74-122](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L74-L122)[.npmrc1-7](https://github.com/microsoft/vscode/blob/1be3088d/.npmrc#L1-L7) 

---

## 构建脚本和编译管道

### 核心构建脚本

根 `package.json` 定义主要构建脚本：

__代码块_2__\n

- **`compile`**：通过 Gulp 进行主要 TypeScript 编译\n

来源：[package.json12-72](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L12-L72)

### TypeScript 编译流程

__代码块_3__\n

__代码块_4__\n

---

## 本机模块和跨平台构建

### 本机模块管理

VS Code 包含几个必须针对每个平台和架构进行编译的本机 Node.js 插件。

**使用的本机模块：**

|

`.moduleignore` 文件定义清理规则以减少包大小：

__代码块_5__\n

来源： [build/.moduleignore1-191](https://github.com/microsoft/vscode/blob/1be3088d/build/.moduleignore#L1-L191) [package.json74-91](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L74-L91)

### 特定于平台的构建配置

__代码块_6__\n

__代码块_7__\n

### Linux 系统根配置

对于 Linux 版本，系统使用基于 Debian 的 sysroots 来确保二进制兼容性：

__代码块_8__\n

来源：[build/linux/setup-env.sh1-100](https://github.com/microsoft/vscode/blob/1be3088d/build/linux/setup-env.sh#L1-L100) 

---

## Azure DevOps 构建管道

### 管道架构

__代码块_9__\n

1. **编译**：TypeScript编译、卫生检查、遥测提取\n

来源：[build/azure-pipelines/product-build.yml1-520](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/product-build.yml#L1-L520)

### 编译阶段详细信息

__代码块_10__\n

- **Node.js 设置**：使用 `.nvmrc` (22.21.1) 中的版本\n

来源： [build/azure-pipelines/product-compile.yml1-172](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/product-compile.yml#L1-L172) [.nvmrc1](https://github.com/microsoft/vscode/blob/1be3088d/.nvmrc#L1-L1)

### 平台构建阶段

每个平台阶段都会下载编译工件并执行特定于平台的构建：

**Windows 构建 (product-build-win32.yml):**

- 编译 x64/ARM64 的本机模块\n

**Linux 构建 (product-build-linux.yml):**

- 使用 sysroot 进行编译以实现兼容性\n

**macOS 构建 (product-build-darwin.yml):**

- 针对 x64/ARM64 编译\n

来源：[build/azure-pipelines/win32/product-build-win32.yml1-96](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/win32/product-build-win32.yml#L1-L96) 

---

## 出版和发行

### 工件发布流程

__代码块_11__\n

1. **Artifact Collection**：从平台构建阶段下载所有工件\n

来源：[build/azure-pipelines/product-publish.yml1-100](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/product-publish.yml#L1-L100) 

### ESRP 代码签名

VS Code 使用 Microsoft 的企业签名发布管道 (ESRP) 进行代码签名：

__代码块_12__\n

1. 向 ESRP 服务提交工件\n

来源：[build/azure-pipelines/common/publish.ts44-73](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/common/publish.ts#L44-L73)

### CDN 和分发

分发使用 Azure Blob 存储和 `@azure/storage-blob` SDK：

__代码块_13__\n

- **存储帐户**：`vscodeweb`\n

来源：[build/azure-pipelines/common/publish.ts1-1000](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/common/publish.ts#L1-L1000) 

---

## 代码质量和开发工具

### ESLint 配置

VS Code 使用全面的 ESLint 设置以及 `.eslint-plugin-local/` 中定义的自定义规则：

__代码块_14__\n

- **`code-layering`**：强制实施架构层边界

- `common`：核心逻辑（无依赖性）\n    

- **`code-must-use-super-dispose`**：确保子类中正确的处置链

- **`code-declare-service-brand`**：强制执行服务身份模式

- **`code-no-unexternalized-strings`**：验证所有面向用户的字符串是否已本地化

来源：[eslint.config.js1-400](https://github.com/microsoft/vscode/blob/1be3088d/eslint.config.js#L1-L400)

### 构建验证脚本

`package.json` 包括验证脚本：

|

这些检查在编译管道中运行以捕获架构违规：

__代码块_15__\n

---

## 开发工作流程

### 本地开发设置

__代码块_16__\n

__代码块_17__\n

### 烟雾测试

集成冒烟测试验证端到端功能：

__代码块_18__\n

__代码块_19__\n

### 性能分析

__代码块_20__\n

- 启动时间指标\n

来源：[package.json71](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L71-L71)

---

## 模块清理和优化

### 构建时模块修剪

构建系统使用 `.moduleignore` 通过从依赖项中删除不必要的文件来减小包大小：

__代码块_21__\n

__代码块_22__\n

__代码块_23__\n

### Tree Shaking 和捆绑

生产构建使用 esbuild 和 webpack 进行代码优化：

__代码块_24__\n

- **esbuild 0.27.2**：快速 JavaScript/TypeScript 捆绑器\n

来源：[package.json63-65](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L63-L65)[build/package.json51-71](https://github.com/microsoft/vscode/blob/1be3088d/build/package.json#L51-L71)

---

## CI/CD 集成

### 持续集成阶段

管道根据构建类型运行不同的测试套件：

__代码块_25__\n

__代码块_26__\n

### 预定构建

该管道包括用于常规构建的预定触发器：

__代码块_27__\n

来源：[build/azure-pipelines/product-build.yml3-13](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/product-build.yml#L3-L13)

---

＃＃ 概括

VS Code 构建系统是一个复杂的多级管道，它：

1. **管理依赖关系**：使用 npm 工作区以及针对桌面、远程服务器、Web 和扩展的单独包配置\n

关键构建文件及其作用：

- **package.json**：包含构建脚本和依赖项的根工作区\n

来源：[package.json1-242](https://github.com/microsoft/vscode/blob/1be3088d/package.json#L1-L242)[build/azure-pipelines/product-build.yml1-520](https://github.com/microsoft/vscode/blob/1be3088d/build/azure-pipelines/product-build.yml#L1-L520) 