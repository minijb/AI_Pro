---------------------------------------------------------------
-- 项目格式：Enum 和 Data-Only Class 完整示例
-- 展示项目中枚举定义和纯数据类型声明的模式
---------------------------------------------------------------


---------------------------------------------------------------
-- 1. 全局 Enum 表内的枚举
-- 格式：---@enum Enum.EnumName
-- 枚举名使用 UPPER_SNAKE_CASE
---------------------------------------------------------------

local Enum = {
    ---@enum Enum.COLOR
    COLOR = {
        ORANGE = "#FF8600",
        WHITE = "#FFFFFF",
        BLUE = "#58C4FF",
        DEFAULT = "#c2c2c2",
    },

    ---@enum Enum.ITEMSTATE
    ITEMSTATE = {
        NORMAL = 0,
        LOCKED = 1,
        SELECTED = 2,
        CLAIM = 3,
        COMPLETED = 4,
    },

    ---@enum Enum.EquipSize
    EQUIPSIZE = {
        SMALL = 1,
        BIG = 2,
    },

    ---@enum Enum.BattleState
    BATTLE_STATE = {
        NONE = 0,
        INIT = 1,
        RUNNING = 2,
        PAUSE = 3,
        END = 4,
    },
}


---------------------------------------------------------------
-- 2. 独立文件中的枚举
-- 格式：---@enum EnumName
---------------------------------------------------------------

---@enum ReleaseType
local ReleaseType = {
    Default = 0,
    CE = 1,
}

-- 枚举值用于 table 键类型
---@type table<ReleaseType, string>
local ReleaseName = {
    [ReleaseType.Default] = "trunk",
    [ReleaseType.CE] = "ce",
}


---------------------------------------------------------------
-- 3. 带文档注释的枚举（每个值有说明）
---------------------------------------------------------------

---@enum NoticeType
local NoticeType = {
    --- 登录公告
    NtypeLogin = 0,
    --- 游戏内公告
    NtypeGame = 1,
    --- 系统维护
    NtypeMaintenance = 2,
    --- 活动公告
    NtypeActivity = 3,
}

---@enum NoticeMode
local NoticeMode = {
    --- 弹窗模式
    ModePopup = 0,
    --- 滚动模式
    ModeScroll = 1,
    --- 红点模式
    ModeRedDot = 2,
}


---------------------------------------------------------------
-- 4. 带 @deprecated 的枚举值
---------------------------------------------------------------

---@enum Enum.bt_STATES_NAME
local BTN_STATES = {
    bt_gold_L1 = "bt_gold_L1",
    bt_gold_L2 = "bt_gold_L2",
    ---@deprecated 暂时没用
    bt_old_style = "bt_old_style",
}


---------------------------------------------------------------
-- 5. 键枚举 (key enum)
---------------------------------------------------------------

---@enum (key) NpcGroupShapeEnum
local NpcGroupShapeEnum = {
    Circle = 1,
    Line = 2,
    Grid = 3,
}


---------------------------------------------------------------
-- 6. Data-Only Class（纯数据类型声明）
-- 用于描述网络协议、配置数据结构
-- 不关联实际变量，纯做类型文档
---------------------------------------------------------------

-- 战斗信息数据结构
---@class BattleInfo
---@field public levelId integer 关卡ID
---@field public battleType integer 战斗类型
---@field public mapId integer 地图ID
---@field public teams table<integer, TeamInfo> 阵营信息
---@field public victoryCondition integer 胜利条件
---@field public failCondition integer 失败条件

---@class TeamInfo
---@field public teamId integer 阵营ID
---@field public heroes HeroSlotInfo[] 武将列表
---@field public formation integer 阵型ID

---@class HeroSlotInfo
---@field public slot integer 槽位
---@field public heroId integer 武将ID
---@field public level integer 等级
---@field public star integer 星级
---@field public equipList EquipInfo[] 装备列表
---@field public skillList SkillSlotInfo[] 技能列表

---@class EquipInfo
---@field public equipId integer 装备ID
---@field public refineLevel integer 精炼等级
---@field public attrs table<integer, number> 属性加成

---@class SkillSlotInfo
---@field public slot integer 技能槽位
---@field public skillId integer 技能ID
---@field public level integer 技能等级


-- 竞技场战斗数据
---@class ArenaBattleInfo
---@field public arenaId integer 竞技场ID
---@field public opponentId integer 对手ID
---@field public isRobot boolean 是否为机器人

---@class ArenaBattleRuleInfo
---@field public victoryCondition integer 胜利条件
---@field public failCondition integer 失败条件
---@field public turnLimit integer 回合上限


---------------------------------------------------------------
-- 7. 网络消息数据结构
---------------------------------------------------------------

---@class NoticeResponse
---@field public code integer 状态码
---@field public noticeList NoticeObjData[] 公告列表

---@class NoticeObjData
---@field public noticeId integer 公告ID
---@field public title string 标题
---@field public content string 内容
---@field public noticeType NoticeType 公告类型
---@field public startTime integer 开始时间戳
---@field public endTime integer 结束时间戳
---@field public priority integer 优先级
