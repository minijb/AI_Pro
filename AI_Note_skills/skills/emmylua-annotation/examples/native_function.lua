---------------------------------------------------------------
-- EmmyLua 原生格式：函数注解 完整示例
-- 包含 @param, @return, @overload, @generic 的详细用法
---------------------------------------------------------------


---------------------------------------------------------------
-- @param 完整用法
---------------------------------------------------------------

-- 基础参数
---@param name string 用户名
---@param age number 年龄
local function createUser(name, age) end

-- 可选参数 —— 用 ? 标记
---@param name string 用户名（必填）
---@param nickname? string 昵称（可选）
---@param avatar? string 头像URL（可选）
local function register(name, nickname, avatar) end

-- 可变参数
---@param format string 格式字符串
---@param ... any 格式参数
local function printf(format, ...) end

-- 函数类型参数
---@param callback fun(result: any, error: string?): nil
local function processDataAsync(data, callback) end

-- 表字面量参数（描述复杂结构）
---@param options {method: string, url: string, headers?: table<string, string>, body?: string}
local function httpRequest(options) end

-- 联合类型参数
---@param value string | number | boolean
local function serialize(value) end


---------------------------------------------------------------
-- @return 完整用法
---------------------------------------------------------------

-- 单返回值
---@return boolean 是否成功
local function validate(input) end

-- 命名返回值
---@return boolean success 操作是否成功
---@return string message 结果信息
local function process(data) end

-- 多返回值
---@return number x X坐标
---@return number y Y坐标
---@return number z Z坐标
local function getPosition() end

-- 可空返回值
---@return User|nil 用户对象，未找到返回nil
---@return string? 错误信息
local function findUser(id) end

-- 关联返回值缩窄（@return_overload）
---@return boolean
---@return string|nil
---@return_overload true, nil
---@return_overload false, string
local function tryParse(input) end


---------------------------------------------------------------
-- @overload 完整用法
---------------------------------------------------------------

-- 基础重载
---@param x number
---@param y number
---@return number
---@overload fun(x: string, y: string): string
local function add(x, y) end

-- 多重载签名
---@param name string
---@return User
---@overload fun(name: string, age: number): User
---@overload fun(name: string, age: number, email: string): User
local function createUser2(name, age, email) end

-- 不同参数数量的重载
---@overload fun(): string                     -- 无参，返回默认值
---@overload fun(key: string): string           -- 单参，按 key 取值
---@overload fun(key: string, default: string): string  -- 双参，带默认值
local function getConfig(key, default) end


---------------------------------------------------------------
-- @generic 完整用法
---------------------------------------------------------------

-- 基础泛型函数
---@generic T
---@param value T
---@return T
local function identity(value) return value end

-- 多泛型参数
---@generic K, V
---@param map table<K, V>
---@return K[]
local function getKeys(map) end

-- 带约束的泛型
---@generic T : table
---@param obj T
---@return T
local function deepClone(obj) end

-- 泛型与数组
---@generic T
---@param items T[]
---@param predicate fun(item: T): boolean
---@return T[]
local function filter(items, predicate) end

-- 泛型与回调
---@generic T, R
---@param items T[]
---@param transform fun(item: T, index: integer): R
---@return R[]
local function map(items, transform) end

-- 反引号语法 —— 字符串字面量映射到类型
---@generic T
---@param className `T`
---@return T
local function createInstance(className) end

-- 泛型类
---@class Stack<T>
---@field private items T[]
local Stack = {}

---@generic T
---@param self Stack<T>
---@param item T
function Stack:push(item) end

---@generic T
---@param self Stack<T>
---@return T?
function Stack:pop() end


---------------------------------------------------------------
-- 组合使用示例
---------------------------------------------------------------

-- 完整函数签名：泛型 + 多参数 + 多返回值
---@generic T
---@param list T[] 输入列表
---@param comparator fun(a: T, b: T): boolean 比较函数
---@param ascending? boolean 是否升序（默认true）
---@return T[] sorted 排序后的列表
---@return integer count 元素数量
local function sortList(list, comparator, ascending) end
