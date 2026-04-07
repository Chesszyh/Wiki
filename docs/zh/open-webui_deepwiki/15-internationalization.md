# 国际化 (Internationalization)

相关源文件

- [src/lib/i18n/locales/bg-BG/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/bg-BG/translation.json)
- [src/lib/i18n/locales/ca-ES/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/ca-ES/translation.json)
- [src/lib/i18n/locales/de-DE/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/de-DE/translation.json)
- [src/lib/i18n/locales/en-GB/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/en-GB/translation.json)
- [src/lib/i18n/locales/en-US/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/en-US/translation.json)
- [src/lib/i18n/locales/es-ES/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/es-ES/translation.json)
- [src/lib/i18n/locales/fa-IR/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/fa-IR/translation.json)
- [src/lib/i18n/locales/fr-CA/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/fr-CA/translation.json)
- [src/lib/i18n/locales/fr-FR/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/fr-FR/translation.json)
- [src/lib/i18n/locales/it-IT/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/it-IT/translation.json)
- [src/lib/i18n/locales/ja-JP/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/ja-JP/translation.json)
- [src/lib/i18n/locales/ko-KR/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/ko-KR/translation.json)
- [src/lib/i18n/locales/nl-NL/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/nl-NL/translation.json)
- [src/lib/i18n/locales/pt-BR/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/pt-BR/translation.json)
- [src/lib/i18n/locales/pt-PT/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/pt-PT/translation.json)
- [src/lib/i18n/locales/ru-RU/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/ru-RU/translation.json)
- [src/lib/i18n/locales/uk-UA/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/uk-UA/translation.json)
- [src/lib/i18n/locales/vi-VN/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/vi-VN/translation.json)
- [src/lib/i18n/locales/zh-CN/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/zh-CN/translation.json)
- [src/lib/i18n/locales/zh-TW/translation.json](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/i18n/locales/zh-TW/translation.json)

本文档描述了 Open WebUI 中的国际化 (i18n) 系统，该系统为整个应用程序提供多语言支持。该系统目前支持 17 种语言环境，拥有超过 1,500 个翻译键，并包含一个用于动态内容插值的占位符变量系统。

有关用户界面设置和主题管理的信息，请参阅 [用户偏好和界面设置](/open-webui/open-webui/10.2-oauth-integration)。

---

## 目的和范围

i18n 系统通过以下方式使 Open WebUI 能够以多种语言呈现其界面：

-   维护 17 个受支持语言环境的翻译文件
-   提供基于键的翻译查询机制
-   支持动态占位符变量，用于运行时值插入
-   实现无需刷新页面即可在运行时切换语言环境
-   管理每个语言环境的日期/时间格式模式

---

## 翻译系统架构

i18n 系统使用扁平的 JSON 键值结构，其中英语短语键映射到本地化字符串。每个语言环境文件包含约 1,500-2,800 个翻译条目，作为一个单级 JSON 对象。

### 翻译文件组织

**目录结构：src/lib/i18n/locales/**

```mermaid
flowchart TD
    i18nRoot["src/lib/i18n/locales/"]
    enUS["en-US/translation.json~76KB, ~1500 keys 基础语言环境（空值）"]
    zhCN["zh-CN/translation.json~271KB, ~2800 keys 99% 完成度"]
    zhTW["zh-TW/translation.json~170KB, ~2800 keys 98% 完成度"]
    deDE["de-DE/translation.json~124KB, ~2800 keys 95% 完成度"]
    esES["es-ES/translation.json~99KB, ~2700 keys"]
    frFR["fr-FR/translation.json~78KB, ~2500 keys"]
    jaJP["ja-JP/translation.json~49KB, ~2400 keys"]
    koKR["ko-KR/translation.json~95KB, ~2600 keys"]
    ruRU["ru-RU/translation.json~86KB, ~2500 keys"]
    others["it-IT, nl-NL, uk-UA, ca-ES, fr-CA, fa-IR, bg-BG"]
    flatJSON["扁平 JSON 结构：{  'Account': '账号',  'Add User': '添加用户',  '{{user}}'s Chats': '{{user}} 的对话记录'}"]

    i18nRoot --> enUS
    i18nRoot --> zhCN
    i18nRoot --> zhTW
    i18nRoot --> deDE
    i18nRoot --> esES
    i18nRoot --> frFR
    i18nRoot --> jaJP
    i18nRoot --> koKR
    i18nRoot --> ruRU
    i18nRoot --> others
    zhCN --> flatJSON
```
**JSON 文件格式**

所有翻译文件均遵循此结构：

-   具有字符串键（英语短语）的根对象
-   字符串值（本地化翻译）
-   无嵌套；所有键均在根级别
-   键是易于阅读的英语短语
-   占位符变量使用 `{{VARIABLE}}` 语法
-   特殊字符根据 JSON 规范进行转义

---

## 语言环境文件和键结构

每个翻译文件都是一个扁平的 JSON 对象，其中英语键映射到本地化字符串。这些键按功能领域组织，但存储在单级结构中，以便进行高效查询。

### 键命名规范

翻译键是完整的英语短语，既作为查询键，也作为回退显示文本：

| 模式类型 | 示例键 | 语言环境示例 (zh-CN) | 备注 |
| --- | --- | --- | --- |
| 简单动作 | `"Add"` | `"添加"` | 单个动词 |
| 描述性标签 | `"Add a model ID"` | `"添加模型 ID"` | 完整句子 |
| 上下文相关 | `"Admin Panel"` | `"管理员面板"` | 功能标签 |
| 权限 | `"Allow Chat Delete"` | `"允许删除对话记录"` | 布尔权限 |
| 确认 | `"Are you sure?"` | `"您确认吗？"` | 对话框提示 |
| 模板 | `"{{user}}'s Chats"` | `"{{user}} 的对话记录"` | 带有占位符 |
| 复数形式 | `"{{COUNT}} Sources"` | `"{{COUNT}} 个引用来源"` | 基于计数的字符串 |
| 日期格式 | `"[Today at] h:mm A"` | `"[今天] h:mm A"` | Moment.js 模式 |

**键构建规则**

-   键必须在所有功能领域中唯一
-   键区分大小写
-   键应为完整的英语短语，而非缩写
-   带有占位符的键必须包含 `{{VARIABLE}}` 语法
-   日期/时间键在方括号 `[]` 中使用 moment.js 格式标记

### 按功能领域的翻译键分类

**跨功能领域的键分布**

```mermaid
flowchart TD
    TranslationKeys["translation.json 每个语言环境约 2800 个键"]
    AuthKeys["身份验证与访问 ~150 个键"]
    ChatKeys["对话界面 ~400 个键"]
    ModelKeys["模型管理 ~200 个键"]
    SettingsKeys["设置与配置 ~350 个键"]
    FileKeys["文件与文档 ~180 个键"]
    ToolKeys["工具与函数 ~220 个键"]
    UIKeys["UI 组件 ~300 个键"]
    ValidationKeys["错误与验证 ~250 个键"]
    OtherKeys["其他功能 ~750 个键"]
    AuthEx["'Account' 'Admin Panel' 'Access Control' 'Allow Chat Delete'"]
    ChatEx["'Chat Controls' 'Chat Bubble UI' 'Message Input' 'Continue Response'"]
    ModelEx["'Add Model' 'Arena Models' 'Default Model' 'Model ID'"]
    SettEx["'Admin Settings' 'Advanced Parameters' 'API Base URL' 'Enable API Keys'"]
    FileEx["'Add Files' 'File Upload' 'Document Intelligence' 'Attach Knowledge'"]
    ToolEx["'Available Tools' 'Tool Servers' 'Function Calling' 'Code Execution'"]

    TranslationKeys --> AuthKeys
    TranslationKeys --> ChatKeys
    TranslationKeys --> ModelKeys
    TranslationKeys --> SettingsKeys
    TranslationKeys --> FileKeys
    TranslationKeys --> ToolKeys
    TranslationKeys --> UIKeys
    TranslationKeys --> ValidationKeys
    TranslationKeys --> OtherKeys
    AuthKeys --> AuthEx
    ChatKeys --> ChatEx
    ModelKeys --> ModelEx
    SettingsKeys --> SettEx
    FileKeys --> FileEx
    ToolKeys --> ToolEx
```
**键模式分析**

| 功能领域 | 键数量 | 常用前缀 | 示例键 |
| --- | --- | --- | --- |
| 权限 | ~120 | `"Allow "` | `"Allow Chat Delete"`, `"Allow File Upload"` |
| 设置 | ~180 | `"Enable "`, `"Default "` | `"Enable API Keys"`, `"Default Model"` |
| 动作 | ~200 | `"Add "`, `"Delete "`, `"Edit "` | `"Add User"`, `"Delete Chat"` |
| 状态消息 | ~150 | `"successfully"`, `"failed"` | `"Connection successful"`, `"Failed to save"` |
| 确认 | ~80 | `"Are you sure"` | `"Are you sure you want to delete"` |
| 占位符 | ~250 | `"{{COUNT}}"`, `"{{user}}"` | `"{{COUNT}} Sources"`, `"{{user}}'s Chats"` |

---

## 占位符变量系统

i18n 系统支持使用双大括号语法的运行时变量插值：`{{VARIABLE}}`。变量区分大小写，并在渲染时由前端 i18n 库替换。

### 占位符变量类型与用法

| 变量名称 | 类型 | 示例键 | zh-CN 翻译 | 使用上下文 |
| --- | --- | --- | --- | --- |
| `{{COUNT}}` | 整数 | `"{{COUNT}} Available Tools"` | `"{{COUNT}} 个可用工具"` | 项目计数、复数处理 |
| `{{user}}` | 字符串 | `"{{user}}'s Chats"` | `"{{user}} 的对话记录"` | 用户显示名称 |
| `{{NAME}}` | 字符串 | `"Are you sure you want to delete \"{{NAME}}\""` | `"您确认要删除 \"{{NAME}}\" 吗？"` | 确认对话框中的实体名称 |
| `{{model}}` | 字符串 | `"{{model}} download has been canceled"` | `"已取消模型 {{model}} 的下载"` | 模型标识符 |
| `{{COMMAND}}` | 字符串 | `"Activate this command by typing \"/{{COMMAND}}\""` | `"在对话框中输入 \"/{{COMMAND}}\" 激活此命令"` | 命令字符串 |
| `{{LATEST_VERSION}}` | 字符串 | `"A new version (v{{LATEST_VERSION}}) is now available."` | `"新版本（v{{LATEST_VERSION}}）现已发布"` | 版本号 |
| `{{webUIName}}` | 字符串 | `"{{webUIName}} Backend Required"` | `"{{webUIName}} 需要后端服务"` | 应用程序品牌 |
| `{{provider}}` | 字符串 | `"Continue with {{provider}}"` | `"使用 {{provider}} 继续"` | OAuth 提供商名称 |
| `{{LOCALIZED_DATE}}` | 字符串 | `"{{LOCALIZED_DATE}} at {{LOCALIZED_TIME}}"` | `"{{LOCALIZED_DATE}} {{LOCALIZED_TIME}}"` | 预格式化的日期 |
| `{{LOCALIZED_TIME}}` | 字符串 | `"{{LOCALIZED_DATE}} at {{LOCALIZED_TIME}}"` | `"{{LOCALIZED_DATE}} {{LOCALIZED_TIME}}"` | 预格式化的时间 |
| `{{NAMES}}` | 字符串 | `"{{NAMES}} reacted with {{REACTION}}"` | `"{{NAMES}} 给了 {{REACTION}}"` | 多个名称（逗号分隔） |
| `{{REACTION}}` | 字符串 | `"{{NAMES}} reacted with {{REACTION}}"` | `"{{NAMES}} 给了 {{REACTION}}"` | 表情符号或反应名称 |

**变量插值规则**

-   变量在渲染前被替换
-   未定义的变量在输出中保持为 `{{VARIABLE}}`
-   变量可以在同一个键中多次出现
-   变量名使用 大写下划线 (UPPER_CASE) 或 驼峰命名法 (camelCase) 规范
-   `{{}}` 定界符内不允许有空格

### 日期和时间格式模式

日期和时间键使用 moment.js 格式标记，并结合方括号 `[]` 中的字面量文本。这些模式根据语言环境进行本地化，以确保符合文化习惯的日期/时间显示。

**Moment.js 格式标记参考**

| 标记 | 描述 | 示例输出 |
| --- | --- | --- |
| `h:mm A` | 12 小时制带 AM/PM | `3:45 PM` |
| `H:mm` | 24 小时制 | `15:45` |
| `dddd` | 完整星期名称 | `Monday`, `星期一` |
| `DD/MM/YYYY` | 日/月/年 | `25/12/2024` |
| `[text]` | 字面量文本（不格式化） | `at` (保持不变) |

**日期/时间翻译示例**

| 键 (en-US) | zh-CN 翻译 | ko-KR 翻译 | 用途 |
| --- | --- | --- | --- |
| `"[Today at] h:mm A"` | `"[今天] h:mm A"` | `"[오늘] A h:mm"` | 今天的消息 |
| `"[Yesterday at] h:mm A"` | `"[昨天] h:mm A"` | `"[어제] A h:mm"` | 昨天的消息 |
| `"[Last] dddd [at] h:mm A"` | `"[上次] dddd [于] h:mm A"` | `"[지난] dddd A h:mm"` | 较旧的消息 |
| `"DD/MM/YYYY"` | `"DD/MM/YYYY"` | `"DD/MM/YYYY"` | 日期输入格式 |
| `"{{LOCALIZED_DATE}} at {{LOCALIZED_TIME}}"` | `"{{LOCALIZED_DATE}} {{LOCALIZED_TIME}}"` | `"{{LOCALIZED_DATE}} {{LOCALIZED_TIME}}"` | 组合的日期/时间 |

**语言环境特定的适配**

-   中文语言环境移除了 "at" 连接符：`"[今天] h:mm A"`（无 "at"）
-   韩语语言环境重新排序了时间位置：`"[오늘] A h:mm"`（AM/PM 在时间前）
-   RTL 语言环境 (fa-IR) 保持 RTL 文本流
-   某些语言环境保留英语时间格式 (`h:mm A`)，同时本地化星期名称

---

## 翻译覆盖率与完整性

### 受支持的语言环境

系统目前支持 17 个语言环境，翻译完成度各不相同：

| 语言环境代码 | 语言 | 翻译完成度 | 备注 |
| --- | --- | --- | --- |
| `en-US` | 英语 (美国) | 100% (基准) | 带有空值的基准语言环境 |
| `zh-CN` | 中文 (简体) | ~99% | 最完整的翻译 |
| `zh-TW` | 中文 (繁体) | ~98% | 高覆盖率 |
| `de-DE` | 德语 | ~95% | 良好的覆盖率 |
| `es-ES` | 西班牙语 | ~94% | 良好的覆盖率 |
| `ko-KR` | 韩语 | ~92% | 大部分条目已翻译 |
| `fr-FR` | 法语 | ~90% | 许多条目已翻译 |
| `ru-RU` | 俄语 | ~88% | 许多条目已翻译 |
| `ja-JP` | 日语 | ~85% | 良好的覆盖率 |
| `ca-ES` | 加泰罗尼亚语 | ~85% | 良好的覆盖率 |
| `uk-UA` | 乌克兰语 | ~80% | 许多缺失条目 |
| `it-IT` | 意大利语 | ~75% | 部分覆盖 |
| `nl-NL` | 荷兰语 | ~70% | 部分覆盖 |
| `fr-CA` | 法语 (加拿大) | ~65% | 部分覆盖 |
| `fa-IR` | 波斯语 | ~62% | 部分覆盖 |
| `bg-BG` | 保加利亚语 | ~58% | 部分覆盖 |

### 空值处理

英语语言环境 (`en-US`) 主要包含空字符串值，作为回退机制使用。当没有可用的本地化字符串时，系统将显示翻译键本身：

```json
{
  "Account": "",
  "Add User": "",
  "Admin Panel": ""
}
```
当所选语言环境缺少翻译时，系统将回退到显示英语键字符串。

---

## 按功能的翻译键模式

### 身份验证与账号管理

```mermaid
flowchart TD
    AuthKeys["身份验证键"]
    Account["账号管理"]
    Permissions["访问控制"]
    OAuth["OAuth 集成"]
    AccountKeys["'Account' 'Account Activation Pending' 'Already have an account?' 'Create Account'"]
    PermKeys["'Access Control' 'Admin Panel' 'Admin Settings' 'Accessible to all users'"]
    OAuthKeys["'Continue with {{provider}}' 'Authenticate' 'Authentication'"]

    AuthKeys --> Account
    AuthKeys --> Permissions
    AuthKeys --> OAuth
    Account --> AccountKeys
    Permissions --> PermKeys
    OAuth --> OAuthKeys
```
**身份验证翻译键**

### 对话界面

对话相关的翻译涵盖了消息操作、控件和显示选项：

| 类别 | 示例键 |
| --- | --- |
| 操作 | `"Add Memory"`, `"Delete Message"`, `"Edit Last Message"` |
| 控件 | `"Chat Controls"`, `"Chat Bubble UI"`, `"Chat direction"` |
| 权限 | `"Allow Chat Delete"`, `"Allow Chat Edit"`, `"Allow Chat Export"` |
| 状态 | `"Active"`, `"Away"`, `"Chat moved successfully"` |
| 显示 | `"Display chat title in tab"`, `"Chat Background Image"` |

### 模型管理

```json
{
  "Add Model": "添加模型",
  "Add Arena Model": "添加竞技场模型",
  "Arena Models": "启用竞技场匿名评价模型",
  "Base Model (From)": "基础模型(来自)",
  "Current Model": "当前模型",
  "Default Model": "默认模型",
  "Model ID": "模型 ID",
  "{{model}} download has been canceled": "已取消模型 {{model}} 的下载"
}
```

### 设置与配置

设置翻译包括界面自定义、主题选项和高级参数：

| 设置类别 | 翻译键 |
| --- | --- |
| 通用 | `"General"`, `"Settings"`, `"Admin Settings"` |
| 界面 | `"Display"`, `"Chat Bubble UI"`, `"Theme System"` |
| 高级 | `"Advanced Parameters"`, `"Advanced Params"`, `"Additional Parameters"` |
| 权限 | `"Default permissions"`, `"Features Permissions"`, `"Chat Permissions"` |

---

## 特殊翻译模式

### 复数支持

系统支持带有 `{{COUNT}}` 占位符的基于计数的翻译：

```json
{
  "{{COUNT}} Available Tools": "{{COUNT}} 个可用工具",
  "{{COUNT}} characters": "{{COUNT}} 个字符",
  "{{COUNT}} Replies": "{{COUNT}} 条回复",
  "{{COUNT}} Sources": "{{COUNT}} 个引用来源",
  "{{COUNT}} words": "{{COUNT}} 个字",
  "and {{COUNT}} more": "还有 {{COUNT}} 个",
  "1 Source": "1 个引用来源"
}
```
注意：系统为单数形式（例如 `"1 Source"`）和复数形式（例如 `"{{COUNT}} Sources"`）使用单独的键，而不是单一的复数规则。

### RTL 语言支持

系统包含对右至左 (RTL) 语言的支持，如波斯语 (Farsi)：

```json
{
  "Account": "حساب",
  "Add User": "افزودن کاربر",
  "Admin Panel": "پنل مدیریت"
}
```
语言环境代码 `fa-IR` 标识波斯语翻译，允许前端应用适当的 RTL 文本方向。

### 翻译中的格式与标记

某些翻译包含内联格式提示：

```json
{
  "Executing **{{NAME}}**...": "正在执行 **{{NAME}}**...",
  "e.g. `sh webui.sh --api`": "（例如：`sh webui.sh --api`）",
  "(e.g. `sh webui.sh --api --api-auth username_password`)": "（例如：`sh webui.sh --api --api-auth username_password`）"
}
```
系统在翻译中保留 markdown 格式（`**加粗**`, `` `代码` ``），从而允许在不同语言环境中保持一致的文本样式。

---

## 前端集成架构

i18n 系统通过基于响应式 store 的架构与 SvelteKit 前端集成。语言环境更改会触发所有使用翻译字符串的组件自动重新渲染。

### I18n 系统流程

**翻译查询与应用**

```mermaid
flowchart TD
    UserAction["用户选择语言环境 例如：'zh-CN'"]
    LoadFile["获取 JSON 文件：/locales/zh-CN/translation.json"]
    ParseJSON["解析 JSON 约 2800 个键值对"]
    StoreUpdate["更新内存缓存中的 i18n store"]
    ComponentReactive["Svelte 组件订阅 store"]
    ReRender["使用新翻译进行响应式重新渲染"]
    Component["组件代码：$t('Add User')"]
    Lookup["在 store 中查询：translations['Add User']"]
    Found["是否找到键？"]
    ReturnTranslation["返回：'添加用户'"]
    ReturnKey["回退：'Add User'"]
    Interpolate["如果存在，插值 {{variables}}"]
    Display["在 UI 中显示"]

    UserAction --> LoadFile
    LoadFile --> ParseJSON
    ParseJSON --> StoreUpdate
    StoreUpdate --> ComponentReactive
    ComponentReactive --> ReRender
    Component --> Lookup
    Lookup --> Found
    Found --> ReturnTranslation
    Found --> ReturnKey
    ReturnTranslation --> Interpolate
    ReturnKey --> Interpolate
    Interpolate --> Display
```
**基于 Store 的响应式**

-   I18n 库维护一个响应式 Svelte store
-   Store 包含：`{ locale: string, translations: Record<string, string> }`
-   组件使用 `$t()` 函数或 `$_()` 简写进行订阅
-   Store 更新会触发所有已订阅组件的 Svelte 响应式
-   不需要手动调用组件更新

### 翻译函数使用模式

**在 Svelte 组件中**

```javascript
// 基本翻译查询
$t('Add User')  // 返回："添加用户"（如果选择了 zh-CN）

// 带有占位符插值
$t('{{user}}\'s Chats', { user: 'Alice' })  // 返回："Alice 的对话记录"

// 带有计数占位符
$t('{{COUNT}} Sources', { COUNT: 5 })  // 返回："5 个引用来源"

// 多个占位符
$t('Are you sure you want to delete "{{NAME}}"?', { NAME: 'My Model' })
```
**Store 持久化**

用户语言环境偏好存储在：

1.  浏览器 localStorage（键名：`locale` 或 `language`）
2.  用户偏好 API（持久化到数据库）
3.  在应用程序初始化时恢复
4.  在首次渲染前应用，以确保一致的 UX

---

## 翻译文件维护

### 添加新的翻译键

添加新的 UI 功能时，开发人员必须：

1.  在所有语言环境文件中添加英语键
2.  提供英语翻译（如果不使用键作为显示文本）
3.  向社区贡献者请求其他语言环境的翻译
4.  使用描述性的完整英语短语作为键，以确保清晰度

### 缺失翻译处理

```mermaid
flowchart TD
    TranslationRequest["翻译查询"]
    CheckLocale["检查所选语言环境 例如：zh-CN"]
    KeyExists["键是否存在？"]
    ReturnTranslation["返回本地化字符串 '添加用户'"]
    FallbackEnglish["回退到英语键 'Add User'"]
    DisplayKey["显示英语键作为回退"]

    TranslationRequest --> CheckLocale
    CheckLocale --> KeyExists
    KeyExists --> ReturnTranslation
    KeyExists --> FallbackEnglish
    FallbackEnglish --> DisplayKey
```
**翻译回退机制**

当所选语言环境缺少翻译键时，系统将显示英语键字符串本身作为回退，从而确保即使翻译不完整，UI 也能保持正常工作。

---

## 常见翻译模式

### 确认对话框

```json
{
  "Are you sure?": "您确认吗？",
  "Are you sure you want to delete \"{{NAME}}\"?": "您确认要删除 \"{{NAME}}\" 吗？",
  "Are you sure you want to delete this message?": "您确认要删除此消息吗？",
  "Are you sure you want to delete this channel?": "您确认要删除此频道吗？",
  "Confirm": "确认",
  "Confirm your action": "确认要继续吗？",
  "Cancel": "取消"
}
```
### 成功与错误消息

```json
{
  "Connection successful": "连接成功",
  "Connection failed": "连接失败",
  "Channel deleted successfully": "删除频道成功",
  "Channel updated successfully": "更新频道成功",
  "Failed to delete note": "删除笔记失败",
  "Failed to save conversation": "保存对话失败",
  "Error": "错误"
}
```
### 功能开关

```json
{
  "Allow Call": "允许语音通话",
  "Allow Chat Controls": "允许使用对话高级设置",
  "Allow Chat Delete": "允许删除对话记录",
  "Allow File Upload": "允许上传文件",
  "Enable API Keys": "启用接口密钥",
  "Enable Code Execution": "启用代码执行"
}
```

---

## 技术实现说明

### JSON 文件格式

每个翻译文件都遵循严格的 JSON 格式：

-   键始终为英语字符串
-   值为本地化翻译
-   特殊字符已正确转义
-   占位符变量使用 `{{variable}}` 语法
-   空字符串表示未翻译的键

### 文件大小与性能

| 指标 | 值 |
| --- | --- |
| 平均文件大小 | 每个语言环境约 150-250 KB |
| 总翻译键数量 | 约 1,500 个键 |
| 最大的翻译文件 | zh-CN (约 270 KB) |
| 最小的翻译文件 | en-US (约 75 KB) |

翻译文件在用户选择语言环境时按需加载，从而最大限度地减小初始包体积。
