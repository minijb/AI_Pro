---------------------------------------------------------------
-- EmmyLua 原生格式：修饰与辅助注解 完整示例
-- 包含 @async, @nodiscard, @deprecated, @cast, @diagnostic,
--      @see, @operator, @module 的详细用法
---------------------------------------------------------------


---------------------------------------------------------------
-- @async 异步函数标记
---------------------------------------------------------------

---@async
---@param url string 请求地址
---@return string 响应内容
local function fetchData(url) end

---@async
---@param path string 文件路径
---@param encoding? string 编码（默认utf-8）
---@return string content 文件内容
local function readFileAsync(path, encoding) end


---------------------------------------------------------------
-- @nodiscard 不可忽略返回值
---------------------------------------------------------------

---@nodiscard
---@return boolean 操作是否成功
local function criticalOperation() end

-- 正确用法
local success = criticalOperation()   -- OK

-- 错误用法（会产生警告）
-- criticalOperation()                -- Warning: return value discarded

---@nodiscard
---@param data table
---@return boolean success
---@return string? error
local function validateData(data) end


---------------------------------------------------------------
-- @deprecated 弃用标记
---------------------------------------------------------------

-- 弃用函数
---@deprecated 请使用 newCalculate 代替
---@param a number
---@param b number
---@return number
local function oldCalculate(a, b) end

-- 弃用类
---@deprecated 从v2.0起弃用，请使用 ModernUser
---@class OldUser
---@field id number
---@field name string

-- 弃用字段
---@class APIConfig
---@field endpoint string
---@deprecated 使用 endpoint 代替
---@field url string

-- 带版本信息
---@deprecated Since v2.0, removed in v3.0. Use executeQuery
local function query(sql) end


---------------------------------------------------------------
-- @cast 类型转换
---------------------------------------------------------------

---@type string | number | nil
local value = getValue()

-- 收窄到指定类型
---@cast value string

-- 添加类型到联合
---@cast value +boolean

-- 移除类型
---@cast value -nil

-- 同时移除多个类型
---@cast value -boolean, -nil

-- 实际使用场景：JSON解析后收窄
---@type table
local data = parseJSON(jsonStr)
---@cast data {users: {id: number, name: string}[]}


---------------------------------------------------------------
-- @diagnostic 诊断控制
---------------------------------------------------------------

-- 禁用下一行的某个诊断
---@diagnostic disable-next-line: undefined-global
local val = SOME_GLOBAL

-- 禁用当前行（行内）
local x = someFunc() ---@diagnostic disable-line: unused-local

-- 禁用整个文件后续区域
---@diagnostic disable: unused-local, unused-vararg

-- 禁用后重新启用
---@diagnostic disable: undefined-global
_G.GLOBAL_CONFIG = {}
---@diagnostic enable: undefined-global

-- 常见诊断项：
-- undefined-global       未定义的全局变量
-- unused-local           未使用的局部变量
-- unused-vararg          未使用的可变参数
-- duplicate-set-field    重复设置字段
-- inject-field           动态注入字段
-- assign-type-mismatch   赋值类型不匹配
-- return-type-mismatch   返回类型不匹配
-- param-type-mismatch    参数类型不匹配
-- missing-parameter      缺少参数
-- redundant-parameter    多余参数


---------------------------------------------------------------
-- @see 引用相关符号
---------------------------------------------------------------

---@see User
---@see createUser
local function validateUser(userData) end

-- 引用类方法
---@see Logger.info
---@see Logger.error
local function writeLog(level, message) end

-- 引用外部文档
---@see https://lua.org/manual/5.4/manual.html#6.4
local function findMatches(pattern, str) end


---------------------------------------------------------------
-- @operator 操作符重载
---------------------------------------------------------------

---@class Vector
---@field x number
---@field y number
---@operator add(Vector): Vector        加法
---@operator sub(Vector): Vector        减法
---@operator mul(number): Vector        标量乘法
---@operator unm: Vector                取负（一元）
---@operator len: number                长度（一元）
---@operator tostring: string           转字符串
local Vector = {}

-- 多种类型的操作符重载
---@class Matrix
---@operator mul(Matrix): Matrix
---@operator mul(number): Matrix
---@operator mul(Vector): Vector
local Matrix = {}


---------------------------------------------------------------
-- @module 模块声明
---------------------------------------------------------------

---@module 'socket'
local socket = require('socket')

---@module 'http.client'
local httpClient = require('http.client')
