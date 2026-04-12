---
name: emmylua-annotation
description: >
  EmmyLua 类型注解编写规范。当编写或修改 Lua 代码、添加类型注解、定义类/函数/字段类型、
  使用 @class/@param/@return/@field/@type/@enum/@generic 等 EmmyLua 注解时，使用此 skill。
  覆盖场景：新建 Lua 模块、给已有代码补充类型注解、审查注解正确性、Component 部分类声明、
  枚举定义、泛型函数签名、诊断抑制等。即使用户没有明确提到"EmmyLua"，只要涉及 Lua 类型标注，
  都应使用此 skill。
paths: "**/*.lua"
---

# EmmyLua 注解编写规范

本 skill 分为两部分：**原生格式**（EmmyLua 标准语法）和 **项目格式**（本项目的特定约定）。

> **Token 节约提示**：每个部分都提供了简要说明和最小示例。详细的完整示例存放在本 skill 目录下的 `examples/` 子目录中。
> **仅在需要使用对应注解格式时**，才通过 Read 工具加载对应的 example 文件（路径相对于本 SKILL.md 所在目录）。
> 不要一次性加载所有 example 文件。

---

## 第一部分：原生 EmmyLua 格式

所有注解以 `---@` 开头（三个短横线 + @）。

### 1.1 类型系统注解

#### @class — 类定义

```lua
---@class ClassName [: ParentClass[, Interface...]]
---@class (exact) ClassName      -- 精确类，禁止动态添加字段
---@class (partial) ClassName    -- 部分类，在别处扩展已有类
---@class Container<T>           -- 泛型类
```

#### @field — 字段定义

```lua
---@field [public|private|protected|package] fieldName[?] Type [描述]
---@field [keyType] ValueType    -- 索引签名
```

#### @type — 变量类型声明

```lua
---@type Type
---@type Type1 | Type2           -- 联合类型
---@type Type?                   -- 等价于 Type | nil
```

#### @enum — 枚举

```lua
---@enum EnumName                -- 值枚举
---@enum (key) EnumName          -- 键枚举
```

#### @alias — 类型别名

```lua
---@alias AliasName Type
---@alias AliasName              -- 枚举式别名
---| 'value1' # 描述
---| 'value2' # 描述
```

> 需要以上注解的详细用法和完整示例时，Read `examples/native_type_system.lua`

### 1.2 函数注解

#### @param — 参数

```lua
---@param name Type [描述]
---@param name? Type             -- 可选参数
---@param ... Type               -- 可变参数
```

#### @return — 返回值

```lua
---@return Type [name] [描述]
---@return Type1, Type2          -- 多返回值
---@return_overload true, T      -- 关联返回值缩窄
---@return_overload false, E
```

#### @overload — 函数重载

```lua
---@overload fun(x: number): number
---@overload fun(x: string): string
```

#### @generic — 泛型

```lua
---@generic T [: Constraint]
---@param value T
---@return T
```

> 需要以上注解的详细用法和完整示例时，Read `examples/native_function.lua`

### 1.3 修饰与辅助注解

| 注解 | 语法 | 用途 |
|------|------|------|
| `@async` | `---@async` | 标记异步函数（协程） |
| `@nodiscard` | `---@nodiscard` | 不可忽略返回值 |
| `@deprecated` | `---@deprecated [描述]` | 标记弃用 |
| `@cast` | `---@cast var [+\|-]Type` | 类型转换/收窄 |
| `@diagnostic` | `---@diagnostic action:name` | 诊断控制 |
| `@see` | `---@see Symbol` | 引用相关符号 |
| `@operator` | `---@operator op[(ParamType)]: ReturnType` | 操作符重载 |
| `@module` | `---@module 'name'` | 模块声明 |
| `@version` | `---@version 5.1,5.2,...` | Lua 版本要求 |
| `@source` | `---@source path` | 源代码引用 |

> 需要以上注解的详细用法和完整示例时，Read `examples/native_modifiers.lua`

### 1.4 类型表达式速查

| 类型 | 写法 |
|------|------|
| 基础类型 | `string`, `number`, `boolean`, `integer`, `nil`, `any`, `table`, `function`, `thread`, `userdata` |
| 数组 | `Type[]` |
| 字典 | `table<K, V>` |
| 联合 | `Type1 \| Type2` |
| 可选 | `Type?` |
| 交叉 | `Type1 & Type2` |
| 元组 | `[Type1, Type2, Type3]` |
| 表字面量 | `{field1: Type1, field2: Type2}` |
| 函数 | `fun(param: Type): ReturnType` |
| 异步函数 | `async fun(param: Type): ReturnType` |
| 字符串字面量 | `'value1' \| 'value2'` |

---

## 第二部分：项目格式（本项目特定约定）

以下约定基于 `Client/Assets/Script/Lua/` 下的实际代码风格。

### 2.1 Class 声明规范

**标准类声明**（配合 `Common/Class.lua` 系统）：

```lua
local class = require("Common.Class")

---@class MyModule:SuperClass
---@field public super SuperClass
---@field public someField Type 中文描述
---@field private internalField Type
local MyModule = class.Class("MyModule", SuperClass, false)
```

要点：
- `---@class` 紧贴 `local XX = class.Class(...)` 之上
- 继承用冒号 `:ParentClass`
- 显式声明 `---@field public super ParentClass`
- **字段必须标注 `public` / `private`**（不省略访问控制）
- 描述使用中文，直接跟在类型后面（空格分隔）

### 2.2 Component 部分类

当使用 `class.Component` 或 `class.AddComponent` 扩展已有类时：

```lua
---@class (partial) HostClass
---@field public newField Type 描述
local MyComp = class.Component("MyCompName")
class.AddComponent(HostClass, MyComp)
```

### 2.3 单例类

```lua
---@class MySingleton
---@field public GetInstance fun():MySingleton
local MySingleton = class.Class("MySingleton", nil, true)
```

### 2.4 函数注解风格

```lua
---@param paramName Type 中文参数描述
---@param optionalParam Type? 可选参数描述
---@return ReturnType 中文返回值描述
function MyClass:MethodName(paramName, optionalParam)
end
```

要点：
- 可选参数用 `Type?` 后缀
- 描述使用中文

### 2.5 Enum 风格

```lua
---@enum Enum.MyEnumName
Enum.MY_ENUM = {
    VALUE_A = 1,
    VALUE_B = 2,
}
```

独立文件中的枚举：
```lua
---@enum MyEnumName
local MyEnum = {
    A = 0,
    B = 1,
}
```

### 2.6 内联类型标注

```lua
---@type Panel
local panel = nil

---@type table<string, PanelConfig>
local configs = {}

---@type fun():boolean
local callback = nil
```

### 2.7 诊断抑制

最常见的场景 — Component 方法覆盖生命周期钩子时：

```lua
---@diagnostic disable-next-line: duplicate-set-field
function MyComp:ctor()
    MyComp.super.ctor(self)
end
```

### 2.8 类型转换

在类型不确定需要收窄时使用：

```lua
---@cast battleInfo BattleBasicInfo
---@cast requestData table
```

### 2.9 数据类型定义（Data-Only Class）

用于描述网络协议数据结构、配置数据等，不关联实际变量：

```lua
---@class ResponseData
---@field public code integer 状态码
---@field public msg string 提示信息
---@field public data table 数据体
```

### 2.10 泛型函数（项目中较少用）

```lua
---@generic T
---@param panelName `T`
---@return T?
function PanelManager:GetPanel(panelName)
end
```

> 需要完整的项目格式示例时，Read `examples/project_style.lua`
> 需要 Component 部分类的详细示例时，Read `examples/project_component.lua`
> 需要 Enum 和 Data-Only Class 的详细示例时，Read `examples/project_enum_data.lua`

---

## 常见错误与注意事项

1. **`---` 不是 `--`**：注解必须用三个短横线 `---@`，不是 `--@`
2. **空值比较**：写 `obj == nil`，不写 `nil == obj`（触发 EmmyLua 警告）
3. **`?` 可选标记位置**：
   - `@field` 中：`---@field name? Type`（`?` 在字段名后）或 `---@field name Type?`（`?` 在类型后）
   - `@param` 中：`---@param name? Type` 或 `---@param name Type?`（均可）
   - 项目惯例：`@field` 多用 `Type?`（如 `boolean?`），`@param` 两种混用
4. **不要给 GameData/ 加注解** — 自动生成文件，禁止手动编辑
5. **全局变量**：使用 `GLDeclare` 声明，不要直接写入 `_G`
6. **访问控制**：`@field` 必须显式标注 `public` / `private`
7. **`.emmyrc.json` 已禁用的诊断**：`invert-if`、`unnecessary-if`、`missing-parameter`
