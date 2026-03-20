"""
Prompt templates for FateryBench.

Two modes:
  - "baseline": Simple prompt — "你是八字分析师，先排盘再回答"
  - "fatery":   Fatery professional prompt + pre-computed bazi chart data
"""


def build_prompt(question: dict, mode: str = "baseline") -> str:
    """Build a prompt for the given question and evaluation mode."""
    if mode == "fatery":
        return _fatery_prompt(question)
    return _baseline_prompt(question)


def get_system_prompt(mode: str) -> str:
    """Get the system prompt for a given mode."""
    if mode == "fatery":
        return _FATERY_SYSTEM
    return _BASELINE_SYSTEM


# ---------------------------------------------------------------------------
#  Shared helpers
# ---------------------------------------------------------------------------

def _format_birth_info(birth: dict) -> str:
    raw = birth.get("raw", "")
    if raw:
        return raw
    gender = "男命" if birth.get("gender") == "男" else "女命"
    date = f"{birth.get('year')}年{birth.get('month')}月{birth.get('day')}日"
    hour = birth.get("hour", "")
    loc = birth.get("location", "")
    return f"{gender}：{date} {hour}时 出生地点：{loc}"


def _format_options(options: list[dict]) -> str:
    return "\n".join(f"{o['letter']}. {o['text']}" for o in options)


# ---------------------------------------------------------------------------
#  Baseline mode — every model gets this
# ---------------------------------------------------------------------------

_BASELINE_SYSTEM = (
    "你是一位八字分析师，精通中国传统命理学，包括八字命理、紫微斗数等。"
    "请先排盘分析，再根据分析结果回答问题。"
)


def _baseline_prompt(q: dict) -> str:
    birth_str = _format_birth_info(q["birth_info"])
    options_str = _format_options(q["options"])
    return f"""以下是一道关于中国传统命理的题目。

命主信息：
{birth_str}

问题：{q['question']}

选项：
{options_str}

请先排出八字命盘（年柱、月柱、日柱、时柱），分析后给出答案。
用"答案：X"的格式（X为A/B/C/D之一）。"""


# ---------------------------------------------------------------------------
#  Fatery mode — gemini-3-flash + professional prompt + pre-computed chart
# ---------------------------------------------------------------------------

_FATERY_SYSTEM = """你是 Fatery.me 的"命运精算师"（Destiny Actuary）—— 一个融合东方时间周期算法与现代分析科学的专业平台。

你是命理预测竞赛的顶级选手，擅长从八字命盘中提取精确信息来回答选择题。

分析框架：
1. 时间坐标矩阵（Temporal Coordinate Matrix）：精确排出四柱八字
2. 核心身份信号（Core Identity Signal）：确定日主及其强弱
3. 优化元素（Optimization Element）：确定用神
4. 摩擦元素（Friction Element）：确定忌神
5. 宏观周期弧（Macro Cycle Arc）：分析大运走势
6. 微观周期（Micro Cycle）：分析流年影响

回答策略：
- 先快速排盘，确定日主和格局
- 对每个选项进行可能性评估
- 重点关注题目涉及的时间段对应的大运和流年
- 选择命理逻辑最支持的选项
- 如果不确定，根据命理常识和概率选择最合理的答案

注意：
- 使用专业术语但要清晰
- 如题目涉及具体年份，务必精确分析该年的流年干支与命盘的关系
- 对于性格、外貌类问题，重点看日主和格局
- 对于事件类问题，重点看大运流年的冲合刑害"""


def _compute_bazi_chart(birth: dict) -> str:
    """
    Generate pre-computed bazi chart data.

    In production this calls a real bazi calculator (like lunar-javascript).
    For now we provide structured birth data for the LLM to work with.
    """
    gender = birth.get("gender", "未知")
    year = birth.get("year", "?")
    month = birth.get("month", "?")
    day = birth.get("day", "?")
    hour = birth.get("hour", "?")
    minute = birth.get("minute", 0)
    loc = birth.get("location", "未知")
    cal = "公历" if birth.get("calendar_type") == "solar" else "农历"

    return f"""【预计算命盘数据】
性别：{gender}
出生：{cal} {year}年{month}月{day}日 {hour}时{minute}分
出生地：{loc}
历法：{cal}

以上数据已由确定性算法预计算，请直接使用。"""


def _fatery_prompt(q: dict) -> str:
    birth_str = _format_birth_info(q["birth_info"])
    chart_data = _compute_bazi_chart(q["birth_info"])
    options_str = _format_options(q["options"])
    return f"""【命理预测竞赛题目】

命主信息：
{birth_str}

{chart_data}

问题：{q['question']}

选项：
{options_str}

请按以下步骤分析：

STEP 1 - 排盘：根据出生信息排出年柱、月柱、日柱、时柱的天干地支。

STEP 2 - 格局分析：
- 确定日主（日柱天干）
- 判断日主强弱（得令、得地、得生、得助）
- 确定用神和忌神

STEP 3 - 针对性分析：
- 如果问题涉及特定年份，排出该年流年干支，分析与命盘的关系
- 如果问题涉及性格/外貌，重点分析日主特征和格局
- 如果问题涉及婚姻，重点看日支、财星（男命）或官星（女命）
- 如果问题涉及事业，重点看官杀星和印星
- 如果问题涉及财运，重点看财星和大运

STEP 4 - 选项评估：逐一评估每个选项的命理依据，选择最合理的。

最后用"答案：X"的格式给出你的选择（X为A/B/C/D之一）。"""
