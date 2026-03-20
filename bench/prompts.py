"""
Prompt templates for FateryBench.

Two modes:
  - "baseline": Simple prompt — "你是八字分析师，先排盘再回答"
  - "fatery":   Fatery professional prompt + pre-computed bazi chart data

Supports both single-question and batch (per-case) prompts.
"""

from bench.bazi import calculate_bazi, format_chart


def build_prompt(question: dict, mode: str = "baseline") -> str:
    """Build a prompt for a single question."""
    if mode == "fatery":
        return _fatery_prompt(question)
    return _baseline_prompt(question)


def build_batch_prompt(questions: list[dict], mode: str = "baseline") -> str:
    """Build a prompt for multiple questions sharing the same birth chart."""
    if mode == "fatery":
        return _fatery_batch_prompt(questions)
    return _baseline_batch_prompt(questions)


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


def _format_questions_block(questions: list[dict]) -> str:
    """Format multiple questions as a numbered block."""
    parts = []
    for i, q in enumerate(questions, 1):
        options_str = _format_options(q["options"])
        parts.append(f"Q{i}. {q['question']}\n{options_str}")
    return "\n\n".join(parts)


def _format_answer_instruction(count: int) -> str:
    """Instruction for answering multiple questions."""
    lines = "\n".join(f"Q{i}答案：X" for i in range(1, count + 1))
    return f"""分析完成后，必须在回答末尾给出所有答案，严格按以下格式（X为A/B/C/D之一）：

{lines}"""


# ---------------------------------------------------------------------------
#  Baseline mode
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


def _baseline_batch_prompt(questions: list[dict]) -> str:
    birth_str = _format_birth_info(questions[0]["birth_info"])
    questions_block = _format_questions_block(questions)
    answer_inst = _format_answer_instruction(len(questions))
    return f"""以下是关于同一命主的{len(questions)}道命理题目。

命主信息：
{birth_str}

请先排出八字命盘（年柱、月柱、日柱、时柱），然后逐题分析回答。

{questions_block}

{answer_inst}"""


# ---------------------------------------------------------------------------
#  Fatery mode
# ---------------------------------------------------------------------------

_FATERY_SYSTEM = """你是 Fatery.me 的"命运精算师"——一个融合东方时间周期算法与西方高管教练方法论的精英级分析平台。
你的人格融合了荣格原型深度心理学的洞察力、顶级咨询公司合伙人的精准度，以及东方时间坐标分析（四柱体系）大师的功底。

调性要求：
- 写作风格：像一位资深命理师面对面聊天——温和但有洞察力，专业但不冰冷。
- 善用过渡语：用"从你的命盘来看"、"有趣的是"、"值得留意的是"、"换个角度看"等自然过渡。
- 语言：简体中文，第二人称（"你"），分析用现在时，预测用将来时。

你同时是命理预测竞赛的顶级选手。你的任务是根据预计算的命盘数据，精准回答选择题。

时间坐标矩阵——分析协议：

四柱八字和大运已由确定性算法预计算并提供在用户提示中。
你必须直接使用这些精确的柱值。不要重新排盘计算。
你的工作是分析提供的命盘，而非计算它们。

STEP 1 — 命盘分析：
- 日主（日柱天干）是核心身份信号
- 统计所有八个字的五行分布（4天干 + 4地支，含藏干）
- 判断命局强弱：旺（五行得助多）、中和、弱（五行得助少）
- 确定用神（优化元素）——平衡命局的五行
- 确定忌神（摩擦元素）——失衡命局的五行

STEP 2 — 宏观周期弧（大运）：
- 大运已预计算并提供在用户提示中
- 你必须使用这些精确的周期值（干支、年龄范围、年份），不要自行计算
- 判断当前大运及其五行对命局的影响

STEP 3 — 针对性分析：
- 如果问题涉及特定年份，排出该年流年干支，分析与命盘的关系（冲、合、刑、害）
- 如果问题涉及性格/外貌，重点分析日主特征、格局和五行配置
- 如果问题涉及婚姻，重点看日支、财星（男命）或官星（女命）、桃花
- 如果问题涉及事业，重点看官杀星、印星和食伤
- 如果问题涉及财运，重点看财星、大运流年与财星的关系
- 如果问题涉及健康，五行对应脏腑：木→肝胆、火→心脏小肠、土→脾胃、金→肺大肠、水→肾膀胱
- 如果问题涉及学业，重点看印星和食伤

STEP 4 — 选项评估：
- 逐一评估每个选项的命理依据
- 三合（san he）、六合（liu he）→ 有利
- 冲（chong）、刑（xing）、害（hai）→ 不利
- 选择命理逻辑最支持的选项
- 如果不确定，根据命理常识和概率选择最合理的答案"""


def _compute_bazi_chart(birth: dict) -> str:
    """Compute real BaZi chart using lunar-python (same engine as fatery)."""
    gender = birth.get("gender", "男")
    year = birth.get("year")
    month = birth.get("month")
    day = birth.get("day")
    hour = birth.get("hour", 12)
    minute = birth.get("minute", 0)
    calendar_type = birth.get("calendar_type", "solar")

    if not all([year, month, day]):
        return f"【命主信息】\n{birth.get('raw', '信息不完整')}"

    try:
        chart = calculate_bazi(
            year=year, month=month, day=day,
            hour=hour, minute=minute,
            gender=gender, calendar_type=calendar_type,
        )
        return format_chart(chart, gender=gender)
    except Exception:
        # Fallback to raw info if calculation fails
        return f"【命主信息】\n{birth.get('raw', f'{year}年{month}月{day}日 {hour}时')}"


def _fatery_prompt(q: dict) -> str:
    birth_str = _format_birth_info(q["birth_info"])
    chart_data = _compute_bazi_chart(q["birth_info"])
    options_str = _format_options(q["options"])
    return f"""命主出生档案：
{birth_str}

{chart_data}

指令：
1. 使用上面预计算的时间坐标矩阵（四柱八字）——不要重新排盘。
2. 使用上面预计算的宏观周期弧（大运）——不要重新计算，精确匹配干支和年龄范围。
3. 分析命盘：核心身份信号（日主）、强弱、用神、忌神。
4. 根据分析结果回答以下选择题。

问题：{q['question']}

选项：
{options_str}

请先完成命盘分析，然后用"答案：X"的格式给出你的选择（X为A/B/C/D之一）。"""


def _fatery_batch_prompt(questions: list[dict]) -> str:
    birth_str = _format_birth_info(questions[0]["birth_info"])
    chart_data = _compute_bazi_chart(questions[0]["birth_info"])
    questions_block = _format_questions_block(questions)
    answer_inst = _format_answer_instruction(len(questions))
    return f"""命主出生档案：
{birth_str}

{chart_data}

指令：
1. 使用上面预计算的时间坐标矩阵（四柱八字）——不要重新排盘。
2. 使用上面预计算的宏观周期弧（大运）——不要重新计算，精确匹配干支和年龄范围。
3. 分析命盘：核心身份信号（日主）、强弱、用神、忌神。
4. 根据分析结果逐题回答以下{len(questions)}道选择题。

{questions_block}

请对每题进行针对性分析后给出答案。
{answer_inst}"""
