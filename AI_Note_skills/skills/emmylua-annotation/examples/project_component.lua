---------------------------------------------------------------
-- 项目格式：Component 部分类 完整示例
-- 展示 class.Component + (partial) 的使用模式
---------------------------------------------------------------
local class = require("Common.Class")


---------------------------------------------------------------
-- 1. 基础 Component 声明
-- 要点：
--   - 使用 ---@class (partial) HostClass 扩展宿主类
--   - Component 本身是独立文件
--   - 不能继承其他 Component
---------------------------------------------------------------

---@class (partial) Battle
---@field public achievementData table<integer, boolean> 成就数据
---@field private achievementChecked boolean 是否已检查成就
local BattleAchievementComp = class.Component("BattleAchievementComp")
class.AddComponent(Battle, BattleAchievementComp)

-- Component 方法 —— 需要 diagnostic 抑制 duplicate-set-field
---@diagnostic disable-next-line: duplicate-set-field
function BattleAchievementComp:ctor()
    BattleAchievementComp.super.ctor(self)
    self.achievementData = {}
    self.achievementChecked = false
end

--- 检查成就是否达成
---@param achieveId integer 成就ID
---@return boolean 是否已达成
function BattleAchievementComp:CheckAchievement(achieveId)
    return self.achievementData[achieveId] == true
end


---------------------------------------------------------------
-- 2. 多 Component 扩展同一个类
-- 每个 Component 文件都使用 (partial) 声明
---------------------------------------------------------------

-- 文件: BattleBuffComp.lua
---@class (partial) Battle
---@field public buffList table<integer, BuffInstance[]> 按实体分组的buff列表
---@field public buffIdCounter integer buff实例ID计数器
local BattleBuffComp = class.Component("BattleBuffComp")
class.AddComponent(Battle, BattleBuffComp)

---@diagnostic disable-next-line: duplicate-set-field
function BattleBuffComp:ctor()
    BattleBuffComp.super.ctor(self)
    self.buffList = {}
    self.buffIdCounter = 0
end

--- 添加buff到指定实体
---@param entityId integer 目标实体ID
---@param buffId integer buff配置ID
---@param caster Entity 施加者
---@param duration integer 持续回合数
---@return BuffInstance? 创建的buff实例
function BattleBuffComp:AddBuff(entityId, buffId, caster, duration)
end

--- 移除指定buff
---@param entityId integer 目标实体ID
---@param buffInstanceId integer buff实例ID
---@return boolean 是否成功移除
function BattleBuffComp:RemoveBuff(entityId, buffInstanceId)
end


-- 文件: BattleDebugComp.lua
---@class (partial) Battle
---@field public debugLogs string[] 调试日志
---@field private debugEnabled boolean 是否开启调试
local BattleDebugComp = class.Component("BattleDebugComp")
class.AddComponent(Battle, BattleDebugComp)


---------------------------------------------------------------
-- 3. UI Component 示例
-- Control 类通过 UIEvent Component 扩展事件功能
---------------------------------------------------------------

---@class (partial) Control
---@field public onClick fun(self: Control, go: UnityEngine.GameObject)?
---@field public onPress fun(self: Control, go: UnityEngine.GameObject, isPress: boolean)?
---@field public onDrag fun(self: Control, go: UnityEngine.GameObject, delta: UnityEngine.Vector2)?
local UIEvent = class.Component("UIEvent")

--- 绑定UI事件（由框架调用）
function UIEvent:BindUIEvents()
end

--- 解绑UI事件（由框架调用）
function UIEvent:UnBindUIEvents()
end


---------------------------------------------------------------
-- 4. AddComponents 批量添加
-- Battle.lua 中的实际模式
---------------------------------------------------------------

-- local Battle = class.Class("Battle", EventCenter, false)
-- class.AddComponents(Battle, {
--     BattleMapComp,
--     BattleTriggerComp,
--     BattleTurnComp,
--     BattleBuffComp,
--     BattleFightComp,
--     BattleReportComp,
--     BattleLogicComp,
--     BattleLoadComp,
--     BattleAIGroupComp,
--     BattleRegretComp,
--     BattleAchievementComp,
--     BattleDebugComp,
-- })
