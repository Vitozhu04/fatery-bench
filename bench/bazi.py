"""BaZi (四柱八字) calculator using lunar-python.

Mirrors the deterministic calculation in fatery's bazi-calculator.ts,
which uses lunar-javascript under the hood.
"""

from dataclasses import dataclass

from lunar_python import Solar


STEM_ELEMENT = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

STEM_YINYANG = {
    "甲": "阳木", "乙": "阴木",
    "丙": "阳火", "丁": "阴火",
    "戊": "阳土", "己": "阴土",
    "庚": "阳金", "辛": "阴金",
    "壬": "阳水", "癸": "阴水",
}

BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}


@dataclass(frozen=True)
class Pillar:
    stem: str       # 天干
    branch: str     # 地支

    @property
    def full(self) -> str:
        return f"{self.stem}{self.branch}"

    @property
    def stem_element(self) -> str:
        return STEM_ELEMENT.get(self.stem, "?")

    @property
    def branch_element(self) -> str:
        return BRANCH_ELEMENT.get(self.branch, "?")


@dataclass(frozen=True)
class DaYunCycle:
    gan_zhi: str
    start_age: int
    end_age: int


@dataclass(frozen=True)
class BaZiChart:
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str         # 日主天干
    day_master_element: str  # 日主五行
    da_yun: tuple[DaYunCycle, ...]

    @property
    def four_pillars(self) -> str:
        return f"{self.year.full} {self.month.full} {self.day.full} {self.hour.full}"


def _parse_pillar(gz: str) -> Pillar:
    """Parse a 2-char 干支 string into a Pillar."""
    return Pillar(stem=gz[0], branch=gz[1])


def calculate_bazi(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    gender: str = "男",
    calendar_type: str = "solar",
) -> BaZiChart:
    """Calculate BaZi four pillars from birth info.

    Args:
        year/month/day/hour/minute: Birth date/time.
        gender: "男" or "女".
        calendar_type: "solar" (公历) or "lunar" (农历).

    Returns:
        BaZiChart with four pillars, day master, and Da Yun cycles.
    """
    if calendar_type == "solar":
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
    else:
        from lunar_python import Lunar
        lunar = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
        solar = lunar.getSolar()

    lunar = solar.getLunar()
    eight = lunar.getEightChar()

    year_p = _parse_pillar(eight.getYear())
    month_p = _parse_pillar(eight.getMonth())
    day_p = _parse_pillar(eight.getDay())
    hour_p = _parse_pillar(eight.getTime())

    day_master = day_p.stem
    day_master_element = STEM_ELEMENT.get(day_master, "?")

    # Da Yun (大运)
    gender_int = 1 if gender == "男" else 0
    yun = eight.getYun(gender_int, 1)
    cycles = []
    for dy in yun.getDaYun():
        gz = dy.getGanZhi()
        if gz:  # skip the pre-luck period
            cycles.append(DaYunCycle(
                gan_zhi=gz,
                start_age=dy.getStartAge(),
                end_age=dy.getEndAge(),
            ))

    return BaZiChart(
        year=year_p,
        month=month_p,
        day=day_p,
        hour=hour_p,
        day_master=day_master,
        day_master_element=day_master_element,
        da_yun=tuple(cycles),
    )


def format_chart(chart: BaZiChart, gender: str = "男") -> str:
    """Format a BaZiChart into a prompt-ready string."""
    lines = [
        "【预计算命盘数据 — 确定性算法排盘，请直接使用】",
        "",
        f"性别：{gender}",
        f"四柱：{chart.four_pillars}",
        f"  年柱：{chart.year.full}（{STEM_YINYANG[chart.year.stem]}·{BRANCH_ELEMENT[chart.year.branch]}）",
        f"  月柱：{chart.month.full}（{STEM_YINYANG[chart.month.stem]}·{BRANCH_ELEMENT[chart.month.branch]}）",
        f"  日柱：{chart.day.full}（{STEM_YINYANG[chart.day.stem]}·{BRANCH_ELEMENT[chart.day.branch]}）",
        f"  时柱：{chart.hour.full}（{STEM_YINYANG[chart.hour.stem]}·{BRANCH_ELEMENT[chart.hour.branch]}）",
        f"日主：{chart.day_master}（{STEM_YINYANG[chart.day_master]}）",
        "",
        "大运：",
    ]
    for c in chart.da_yun:
        lines.append(f"  {c.start_age}-{c.end_age}岁：{c.gan_zhi}")

    return "\n".join(lines)
