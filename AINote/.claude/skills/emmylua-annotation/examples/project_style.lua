---------------------------------------------------------------
-- 项目格式：标准类声明、单例、继承、函数注解风格
-- 基于 Client/Assets/Script/Lua/ 实际代码风格
---------------------------------------------------------------
local class = require("Common.Class")


---------------------------------------------------------------
-- 1. 标准类声明
-- 要点：
--   - @class 紧贴 local XX = class.Class(...) 之上
--   - 继承用冒号 :ParentClass
--   - 显式声明 super 字段
--   - @field 必须标注 public / private（不省略）
--   - 描述使用中文，空格后直接跟在类型后面
---------------------------------------------------------------

---@class BattleTeam
---@field public super Class
---@field public teamId integer 阵营ID
---@field public entities Entity[] 阵营内所有实体
---@field public isPlayerTeam boolean 是否为玩家阵营
---@field private actionQueue table 行动队列
local BattleTeam = class.Class("BattleTeam", nil, false)


---------------------------------------------------------------
-- 2. 继承类声明
---------------------------------------------------------------

local Control = require("UI.Control")

---@class Panel:Control
---@field public super Control
---@field public isPermanent boolean? 是否常驻内存
---@field public layerId integer 记录打开时的canvas
local Panel = class.Class("Panel", Control)


---------------------------------------------------------------
-- 3. 单例类声明
-- 要点：声明 GetInstance 字段
---------------------------------------------------------------

---@class PanelManager
---@field public GetInstance fun():PanelManager
---@field public panelMaps table<string, Panel> 面板映射表
---@field public panelStack Panel[] 面板栈
---@field private loadingPanels table<string, boolean> 加载中的面板
local PanelManager = class.Class("PanelManager", nil, true)


---------------------------------------------------------------
-- 4. 函数注解风格
-- 要点：
--   - 参数描述用中文
--   - 可选参数用 Type? 后缀
--   - 方法用冒号 : 定义
---------------------------------------------------------------

---@param panelName string 窗口名称
---@param delay number 延迟关闭时间（秒）
---@param uiAnimType UIAnimationType? 关闭动画类型
function PanelManager:ClosePanel(panelName, delay, uiAnimType)
end

--- 获取指定面板实例
---@param panelName string 面板名称
---@return Panel? 面板实例，未找到返回nil
function PanelManager:GetPanelByName(panelName)
end

--- 多返回值
---@return boolean isCE 是否为CE版本
---@return MainPlotInfo? cfg 主线剧情配置
function Version:isCEOpeningPlot()
end


---------------------------------------------------------------
-- 5. 泛型函数（项目中较少用）
-- 反引号语法：将字符串字面量映射到类型
---------------------------------------------------------------

---@generic T
---@param panelName `T`
---@return T?
function PanelManager:GetPanel(panelName)
end

---@generic T
---@param subName `T`
---@param assetPath string prefab路径
---@param requirePath string 子panel对应的文件路径
---@param parentTrans UnityEngine.Transform 父节点
---@param onCompletedCallback fun(subPanel:T)?
---@return T
function Panel:LoadSubPanel(subName, assetPath, requirePath, parentTrans, visible, onCompletedCallback)
end


---------------------------------------------------------------
-- 6. 内联类型标注
-- 用于局部变量、函数体内的类型提示
---------------------------------------------------------------

---@type Panel
local panel = nil

---@type table<string, PanelConfig>
local configs = {}

---@type fun():boolean
local callback = nil

-- 函数体内使用
function PanelManager:SomeMethod()
    ---@type Panel
    local curPanel = self.panelStack[#self.panelStack]

    ---@type table<integer, Entity>
    local entityMap = {}
end


---------------------------------------------------------------
-- 7. 数据类型定义（Data-Only Class）
-- 用于网络协议、配置数据等结构描述
-- 不关联实际 local 变量
---------------------------------------------------------------

---@class BattleBasicInfo
---@field public levelId integer 关卡ID
---@field public battleType integer 战斗类型
---@field public randomSeed integer 随机种子

---@class HeroInfo
---@field public heroId integer 武将ID
---@field public level integer 等级
---@field public star integer 星级
---@field public skills SkillInfo[] 技能列表

---@class SkillInfo
---@field public skillId integer 技能ID
---@field public level integer 技能等级


---------------------------------------------------------------
-- 8. 复杂字段类型（参考 Battle.lua 风格）
-- 联合类型、嵌套泛型等
---------------------------------------------------------------

---@class (partial) Battle:EventCenter
---@field public super EventCenter
---@field public debug boolean
---@field public teams OrderedMap<Enum.Team, BattleTeam>
---@field public battleInfo BattleInfo|ArenaBattleInfo 不同模式持有不同结构
---@field public dataMgr GameDataManager 所有的策划配置表
---@field public battleState Enum.BattleState
---@field public EntityOperationSign table<integer|Enum.Team, boolean> 阵营操作标志
---@field public battleRandom Random 战斗随机数
local Battle = class.Class("Battle", EventCenter, false)
