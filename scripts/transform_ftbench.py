#!/usr/bin/env python3
"""
Transform ftbench data.json and raw 2025.txt into FateryBench unified schema.

Usage:
    python scripts/transform_ftbench.py
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def assign_year_to_case(case_id: str, question_number: int) -> int:
    """
    Assign competition year based on case_id and question ranges from ftbench.
    ftbench data.json covers 2022 (13th), 2023 (14th), 2024 (15th) competitions.
    Based on ftbench README: 160 questions across these 3 years.
    """
    # ftbench cases are numbered sequentially across years
    # 2022: cases 1-10 (~Q1-50), 2023: cases 11-20 (~Q51-100), 2024: cases 21-32 (~Q101-160)
    case_num = int(case_id.replace("case_", ""))
    if case_num <= 10:
        return 2022
    elif case_num <= 20:
        return 2023
    else:
        return 2024


def transform_ftbench_question(q: dict, year: int) -> dict:
    """Transform a single ftbench question to FateryBench schema."""
    birth = q["birth_info"]
    return {
        "id": q["id"].replace("ftb_", "fb_"),
        "source": f"hkjfma_{year}",
        "case_id": q["case_id"],
        "birth_info": {
            "raw": birth.get("raw", ""),
            "gender": birth.get("gender", ""),
            "year": birth.get("year"),
            "month": birth.get("month"),
            "day": birth.get("day"),
            "hour": birth.get("hour"),
            "minute": birth.get("minute", 0),
            "location": birth.get("location", birth.get("country", "")),
            "calendar_type": birth.get("calendar_type", "solar"),
        },
        "question": q["question"],
        "options": q["options"],
        "answer": q["answer"],
        "category": q.get("category", ""),
        "difficulty": "medium",
        "year": year,
    }


def parse_2025_raw(raw_text: str) -> list[dict]:
    """Parse 2025.txt raw competition text into structured questions."""
    lines = raw_text.strip().split("\n")
    questions = []
    current_birth_info = None
    current_case_id = None
    case_counter = 0
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect birth info lines (starts with 坤造/乾造/男命/女命 or contains 西曆/西历)
        if re.match(r"^(坤造|乾造|男命|女命)", line) or (
            "西曆" in line or "西历" in line
        ):
            case_counter += 1
            current_case_id = f"case_2025_{case_counter}"
            current_birth_info = _parse_birth_line(line, lines, i)
            i += 1
            # Skip additional birth info lines
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("Q"):
                extra = lines[i].strip()
                if "西曆" in extra or "西历" in extra or "出生" in extra:
                    current_birth_info = _merge_birth_info(current_birth_info, extra)
                i += 1
            continue

        # Detect question lines (Q1, Q2, etc.)
        q_match = re.match(r"^Q(\d+)\s+(.+)", line)
        if q_match and current_birth_info:
            q_num = int(q_match.group(1))
            question_text = q_match.group(2).strip()
            i += 1

            # Parse options
            options = []
            while i < len(lines):
                opt_line = lines[i].strip()
                opt_match = re.match(r"^([A-D])[.．、\s]+(.+)", opt_line)
                if opt_match:
                    letter = opt_match.group(1)
                    text = opt_match.group(2).strip()
                    is_answer = "正确答案" in text or "正確答案" in text
                    # Remove answer markers
                    text = re.sub(r"\s*[（(]正[确確]答案[)）]\s*", "", text).strip()
                    options.append({
                        "letter": letter,
                        "text": text,
                        "_is_answer": is_answer,
                    })
                    i += 1
                elif opt_line == "" or re.match(r"^(坤造|乾造|男命|女命|Q\d+)", opt_line):
                    break
                else:
                    i += 1

            # Extract answer
            answer = ""
            for opt in options:
                if opt.pop("_is_answer", False):
                    answer = opt["letter"]

            if options:
                fb_id = f"fb_{160 + q_num:04d}"
                questions.append({
                    "id": fb_id,
                    "source": "hkjfma_2025",
                    "case_id": current_case_id,
                    "birth_info": {**current_birth_info},
                    "question": question_text,
                    "options": options,
                    "answer": answer,
                    "category": _guess_category(question_text),
                    "difficulty": "medium",
                    "year": 2025,
                })
            continue

        i += 1

    return questions


def _parse_birth_line(line: str, lines: list, idx: int) -> dict:
    """Parse a birth info header line."""
    info = {"raw": line}

    # Gender
    if "坤造" in line or "女命" in line:
        info["gender"] = "女"
    elif "乾造" in line or "男命" in line:
        info["gender"] = "男"

    # Location
    loc_match = re.search(r"([\u4e00-\u9fff]+)出生", line)
    if loc_match:
        info["location"] = loc_match.group(1)

    # Date: 西曆:YYYY年MM月DD日 + time
    date_match = re.search(r"西[曆历][：:]?\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", line)
    if date_match:
        info["year"] = int(date_match.group(1))
        info["month"] = int(date_match.group(2))
        info["day"] = int(date_match.group(3))
        info["calendar_type"] = "solar"

    # Alternative date format: 西历YYYY-MM-DD
    alt_date = re.search(r"西[曆历]\s*(\d{4})-(\d{2})-(\d{2})", line)
    if alt_date and "year" not in info:
        info["year"] = int(alt_date.group(1))
        info["month"] = int(alt_date.group(2))
        info["day"] = int(alt_date.group(3))
        info["calendar_type"] = "solar"

    # Time: 時辰 or specific time
    time_match = re.search(r"(子|丑|寅|卯|辰|巳|午|未|申|酉|戌|亥)[时時]", line)
    if time_match:
        branch_to_hour = {
            "子": 0, "丑": 2, "寅": 4, "卯": 6, "辰": 8, "巳": 10,
            "午": 12, "未": 14, "申": 16, "酉": 18, "戌": 20, "亥": 22,
        }
        info["hour"] = branch_to_hour.get(time_match.group(1), 12)
        info["minute"] = 0

    # Specific time: 上午/下午 + N时/N-N时
    spec_time = re.search(r"(上午|下午)(\d{1,2})[-~]?(\d{1,2})?[时時]", line)
    if spec_time:
        h = int(spec_time.group(2))
        if spec_time.group(1) == "下午" and h < 12:
            h += 12
        info["hour"] = h
        info["minute"] = 0

    return info


def _merge_birth_info(info: dict, extra_line: str) -> dict:
    """Merge additional birth info from subsequent lines."""
    result = {**info}
    result["raw"] = info.get("raw", "") + " " + extra_line

    date_match = re.search(r"西[曆历][：:]?\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", extra_line)
    if date_match:
        result["year"] = int(date_match.group(1))
        result["month"] = int(date_match.group(2))
        result["day"] = int(date_match.group(3))
        result["calendar_type"] = "solar"

    alt_date = re.search(r"西[曆历]\s*(\d{4})-(\d{2})-(\d{2})", extra_line)
    if alt_date and "year" not in result:
        result["year"] = int(alt_date.group(1))
        result["month"] = int(alt_date.group(2))
        result["day"] = int(alt_date.group(3))
        result["calendar_type"] = "solar"

    loc_match = re.search(r"([\u4e00-\u9fff]+)出生", extra_line)
    if loc_match:
        result["location"] = loc_match.group(1)

    time_match = re.search(r"(子|丑|寅|卯|辰|巳|午|未|申|酉|戌|亥)[时時]", extra_line)
    if time_match:
        branch_to_hour = {
            "子": 0, "丑": 2, "寅": 4, "卯": 6, "辰": 8, "巳": 10,
            "午": 12, "未": 14, "申": 16, "酉": 18, "戌": 20, "亥": 22,
        }
        result["hour"] = branch_to_hour.get(time_match.group(1), 12)
        result["minute"] = 0

    return result


def _guess_category(question: str) -> str:
    """Guess question category from question text."""
    category_keywords = {
        "婚姻": ["婚", "配偶", "夫", "妻", "伴侶", "感情", "桃花", "戀"],
        "事业": ["事業", "事业", "職業", "职业", "工作", "生意", "公司", "創業"],
        "健康": ["健康", "病", "手術", "手术", "傷", "伤", "身體", "身体"],
        "财运": ["財", "财", "錢", "钱", "收入", "投資", "投资"],
        "家庭": ["家", "父", "母", "兄", "弟", "姐", "妹", "親", "亲"],
        "性格": ["性格", "性情", "樣貌", "样貌", "外貌", "特質", "特质"],
        "学业": ["學", "学", "讀書", "读书", "畢業", "毕业", "學歷", "学历"],
        "子女": ["子女", "兒", "女兒", "兒子"],
        "运势": ["運", "运", "年發生", "年发生", "何事"],
    }
    for cat, keywords in category_keywords.items():
        for kw in keywords:
            if kw in question:
                return cat
    return "运势"  # default for "何年发生何事" type questions


def main():
    # 1. Transform ftbench data.json (160 questions from 2022-2024)
    ftbench_path = Path("/tmp/ftbench_data.json")
    if not ftbench_path.exists():
        print("Error: Download ftbench data first. Run:")
        print('  curl -sL "https://raw.githubusercontent.com/DestinyLinker/ftbench/main/data/data.json" -o /tmp/ftbench_data.json')
        sys.exit(1)

    with open(ftbench_path) as f:
        ftbench_data = json.load(f)

    transformed = []
    for q in ftbench_data["questions"]:
        year = assign_year_to_case(q["case_id"], q["question_number"])
        transformed.append(transform_ftbench_question(q, year))

    # Save by year
    for year in [2022, 2023, 2024]:
        year_qs = [q for q in transformed if q["year"] == year]
        out_path = PROJECT_ROOT / "data" / "hkjfma" / f"{year}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"questions": year_qs, "source": f"hkjfma_{year}", "count": len(year_qs)}, f, ensure_ascii=False, indent=2)
        print(f"  {year}: {len(year_qs)} questions -> {out_path}")

    # 2. Parse 2025 raw text
    raw_2025_path = Path("/tmp/ftbench_2025.txt")
    if raw_2025_path.exists():
        with open(raw_2025_path, encoding="utf-8") as f:
            raw_text = f.read()
        questions_2025 = parse_2025_raw(raw_text)
        out_path = PROJECT_ROOT / "data" / "hkjfma" / "2025.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"questions": questions_2025, "source": "hkjfma_2025", "count": len(questions_2025)}, f, ensure_ascii=False, indent=2)
        print(f"  2025: {len(questions_2025)} questions -> {out_path}")
        transformed.extend(questions_2025)
    else:
        print("  Warning: 2025 raw data not found, skipping")

    # 3. Build combined.json
    combined_path = PROJECT_ROOT / "data" / "combined.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump({
            "questions": transformed,
            "total": len(transformed),
            "sources": {
                "hkjfma_2022": len([q for q in transformed if q["source"] == "hkjfma_2022"]),
                "hkjfma_2023": len([q for q in transformed if q["source"] == "hkjfma_2023"]),
                "hkjfma_2024": len([q for q in transformed if q["source"] == "hkjfma_2024"]),
                "hkjfma_2025": len([q for q in transformed if q["source"] == "hkjfma_2025"]),
                "celebrity": len([q for q in transformed if q["source"] == "celebrity"]),
            },
            "categories": _count_categories(transformed),
        }, f, ensure_ascii=False, indent=2)
    print(f"\nCombined: {len(transformed)} questions -> {combined_path}")


def _count_categories(questions: list) -> dict:
    counts = {}
    for q in questions:
        cat = q.get("category", "unknown")
        counts[cat] = counts.get(cat, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


if __name__ == "__main__":
    main()
