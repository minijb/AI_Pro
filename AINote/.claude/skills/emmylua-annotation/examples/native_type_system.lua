---------------------------------------------------------------
-- EmmyLua 原生格式：类型系统注解 完整示例
-- 包含 @class, @field, @type, @enum, @alias 的详细用法
---------------------------------------------------------------


---------------------------------------------------------------
-- @class 基础用法
---------------------------------------------------------------

-- 基础类定义
---@class Animal
---@field name string
---@field age number
local Animal = {}

-- 单继承
---@class Dog : Animal
---@field breed string
local Dog = {}

-- 多重继承
---@class Duck : Animal, Flyable, Swimmable
local Duck = {}

-- 精确类 —— 禁止动态添加未声明的字段
---@class (exact) Point
---@field x number
---@field y number
local Point = {}

-- 部分类 —— 在别处扩展已有类的字段
---@class (partial) Animal
---@field weight number
---@field color string

-- 泛型类
---@class Container<T>
---@field private items T[]
---@field private count number
local Container = {}


---------------------------------------------------------------
-- @field 完整用法
---------------------------------------------------------------

-- 访问控制
---@class UserProfile
---@field public id number                  用户ID
---@field public name string                用户名
---@field private password string           密码（私有）
---@field protected email string            邮箱（受保护）
---@field package internal boolean          包内可见

-- 可选字段 —— 用 ? 标记
---@class HttpRequest
---@field url string                        请求地址（必填）
---@field method string                     请求方法（必填）
---@field headers? table<string, string>    请求头（可选）
---@field body? string                      请求体（可选）
---@field timeout? number                   超时时间（可选）

-- 联合类型字段
---@class APIResponse
---@field data table | nil
---@field error string | nil

-- 函数类型字段
---@class EventEmitter
---@field emit fun(self: EventEmitter, event: string, ...: any)
---@field on fun(self: EventEmitter, event: string, callback: fun(...: any))

-- 数组字段
---@class Company
---@field employees Employee[]
---@field branches Address[]

-- 表字面量类型字段
---@class Pagination
---@field meta {page: number, total: number, perPage: number}

-- 索引签名（任意键）
---@class Dictionary
---@field [string] any                      任意字符串键

-- 整数索引签名
---@class NumberArray
---@field [integer] number


---------------------------------------------------------------
-- @type 完整用法
---------------------------------------------------------------

-- 基础类型
---@type string
local name = "hello"

---@type number
local count = 42

---@type boolean
local flag = true

-- 联合类型
---@type string | number
local mixedValue = "hello"

-- 可选类型（等价于 Type | nil）
---@type string?
local maybeName = nil

-- 交叉类型
---@type Serializable & Printable
local obj = {}

-- 数组
---@type string[]
local names = {"张三", "李四", "王五"}

-- 字典
---@type table<string, number>
local scores = {["数学"] = 95, ["语文"] = 88}

-- 嵌套泛型
---@type table<string, table<integer, boolean>>
local nested = {}

-- 元组
---@type [string, number, boolean]
local tuple = {"张三", 25, true}

-- 表字面量
---@type {name: string, age: number, tags: string[]}
local person = {name = "张三", age = 25, tags = {"dev"}}

-- 函数类型
---@type fun(x: number, y: number): number
local add = function(x, y) return x + y end

-- 异步函数类型
---@type async fun(url: string): string
local fetch = nil

-- 字符串字面量联合
---@type 'left' | 'center' | 'right'
local alignment = 'left'


---------------------------------------------------------------
-- @enum 完整用法
---------------------------------------------------------------

-- 数值型值枚举
---@enum HTTPStatus
local HTTPStatus = {
    OK = 200,
    NOT_FOUND = 404,
    INTERNAL_ERROR = 500,
}

-- 字符串型值枚举
---@enum LogLevel
local LogLevel = {
    DEBUG = "debug",
    INFO = "info",
    WARN = "warn",
    ERROR = "error",
}

-- 键枚举 —— 用键名作为枚举值
---@enum (key) Permission
local Permission = {
    READ = true,
    WRITE = true,
    DELETE = true,
}

-- 枚举用于函数参数
---@param status HTTPStatus
---@return string
local function getStatusMessage(status)
    if status == HTTPStatus.OK then return "成功" end
    if status == HTTPStatus.NOT_FOUND then return "未找到" end
    return "未知"
end

-- 枚举用于类型声明
---@type table<HTTPStatus, string>
local statusMessages = {
    [HTTPStatus.OK] = "成功",
    [HTTPStatus.NOT_FOUND] = "未找到",
}


---------------------------------------------------------------
-- @alias 完整用法
---------------------------------------------------------------

-- 简单别名
---@alias ID number
---@alias StringOrNumber string | number

-- 复杂别名
---@alias EventCallback fun(event: string, data: any): boolean?

-- 枚举式别名（字符串字面量联合）
---@alias HTTPMethod
---| 'GET'    # HTTP GET 请求
---| 'POST'   # HTTP POST 请求
---| 'PUT'    # HTTP PUT 请求
---| 'DELETE' # HTTP DELETE 请求

-- 泛型别名
---@alias Result<T, E> {success: boolean, data: T, error: E}
---@alias AsyncCallback<T> fun(error: string?, result: T?): nil
---@alias Predicate<T> fun(item: T): boolean

-- 别名用于函数签名
---@param method HTTPMethod
---@param url string
---@param callback AsyncCallback<table>
local function request(method, url, callback) end
