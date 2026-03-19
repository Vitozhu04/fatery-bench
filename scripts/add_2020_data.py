#!/usr/bin/env python3
"""
Add HKJFMA 2020 (11th) competition questions to the dataset.
Source: https://www.etongwen.com/blogsdetail/103

35 questions from 7 teachers, 5 questions each.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

QUESTIONS_2020 = [
    # Case 1: Female, born April 4, 1962, Si hour, Hong Kong (Teacher: 鄧碧玉)
    {
        "birth_info": {
            "raw": "女命：1962年4月4日巳時 出生地点：香港",
            "gender": "女", "year": 1962, "month": 4, "day": 4,
            "hour": 10, "minute": 0, "location": "香港", "calendar_type": "solar",
        },
        "questions": [
            {"q": "命主在那一年離婚?", "opts": [("A", "2005"), ("B", "2007"), ("C", "2012"), ("D", "2017")], "answer": "", "cat": "婚姻"},
            {"q": "命主在那一年創業?", "opts": [("A", "2001"), ("B", "2006"), ("C", "2008"), ("D", "2016")], "answer": "", "cat": "事业"},
            {"q": "1992年，命主曾經發生什麼事?", "opts": [("A", "命主結婚，同一年生小朋友"), ("B", "升職加薪掌大權，事業一帆風順"), ("C", "父親因突發心臟病過世"), ("D", "上半身神經線受損，導致短暫癱瘓")], "answer": "", "cat": "运势"},
            {"q": "1974年，命主媽媽曾經發生什麼事?", "opts": [("A", "經被火水燒傷身體"), ("B", "曾經被劫匪搶奪物品"), ("C", "婚姻失敗而導致離婚"), ("D", "患有肺病")], "answer": "", "cat": "家庭"},
            {"q": "命主在何年曾經發生交通意外?", "opts": [("A", "1971"), ("B", "1977"), ("C", "1979"), ("D", "1984")], "answer": "", "cat": "健康"},
        ],
    },
    # Case 2: Female, born March 1, 1979 at 23:50, Guangzhou (Teacher: 方亮初)
    {
        "birth_info": {
            "raw": "女命：1979年3月1日 23:50 出生地点：广州",
            "gender": "女", "year": 1979, "month": 3, "day": 1,
            "hour": 23, "minute": 50, "location": "广州", "calendar_type": "solar",
        },
        "questions": [
            {"q": "此命的性格如何?", "opts": [("A", "固執自我，節儉顧家"), ("B", "爭強好勝，揮金如土"), ("C", "溫柔和順，謙厚約束"), ("D", "孤獨不言，脾氣爆燥")], "answer": "", "cat": "性格"},
            {"q": "此命於何時期結婚?", "opts": [("A", "1998-1999"), ("B", "2001-2002"), ("C", "2004-2005"), ("D", "2007-2008")], "answer": "", "cat": "婚姻"},
            {"q": "婚後與丈夫的關係和丈夫的成就如何?", "opts": [("A", "丈夫成就非常高，常常需要應酬，夫妻關係一般"), ("B", "丈夫成就高，丈夫常常對命主打罵"), ("C", "丈夫成就普通，夫妻關係和順"), ("D", "丈夫成就低，夫妻關係不佳，常因金錢吵鬧")], "answer": "", "cat": "婚姻"},
            {"q": "此命與婆婆的關係如何?", "opts": [("A", "婆婆非常強勢，命主常常被婆婆罵"), ("B", "婆婆非常強勢，命主也是強勢，互不相讓"), ("C", "婆婆平易近人，婆媳關係如朋友"), ("D", "婆婆和善謙讓，命主強勢，婆婆忍讓")], "answer": "", "cat": "家庭"},
            {"q": "命主現在的物質錢財在那個階層?", "opts": [("A", "不必工作享受富裕生活，住獨立屋"), ("B", "專業人士中高收入，中產小康生活"), ("C", "普通打工中低收入，每月供樓之平民生活"), ("D", "打工收入低，租房還債")], "answer": "", "cat": "财运"},
        ],
    },
    # Case 3: Female, born March 15, 1985, Wu hour, Hong Kong (Teacher: 梅思賢)
    {
        "birth_info": {
            "raw": "女命：1985年3月15日午時 出生地点：香港",
            "gender": "女", "year": 1985, "month": 3, "day": 15,
            "hour": 12, "minute": 0, "location": "香港", "calendar_type": "solar",
        },
        "questions": [
            {"q": "這女命的性格如何？", "opts": [("A", "反叛性強"), ("B", "隨波逐流，被人欺"), ("C", "性情柔弱，但喜打扮"), ("D", "性格橫蠻，不妥協")], "answer": "", "cat": "性格"},
            {"q": "這女命16歲前，讀書及健康運如何？", "opts": [("A", "學業好讀名校，無病痛"), ("B", "學業不理想讀名校，身體多病"), ("C", "學業好讀普通學校，身體有缺陷"), ("D", "學業不理想讀普通學校，無病痛")], "answer": "", "cat": "学业"},
            {"q": "這女命於2013至2014年，身體發生了什麼變化？", "opts": [("A", "內分泌失調，卵巢早衰"), ("B", "血管瘤，兼有肝炎"), ("C", "膀胱炎，久治不癒"), ("D", "心律不正常，神智失常")], "answer": "", "cat": "健康"},
            {"q": "這女命於2016丙申流年，發生了什麼大事？", "opts": [("A", "心臟搭橋手術"), ("B", "發現男朋友在內地早已結婚"), ("C", "被正印當眾羞辱，被揭通姦"), ("D", "破產")], "answer": "", "cat": "运势"},
            {"q": "這女命的感情狀況？", "opts": [("A", "左右逢源，全是達官貴人"), ("B", "與大學相識的男朋友修成正果"), ("C", "與老闆有不尋常關係，但男方不肯離婚"), ("D", "無感情可言，未拍拖")], "answer": "", "cat": "婚姻"},
        ],
    },
    # Case 4: Male, born July 21, 1979, Mao hour, Hong Kong (raised in UK) (Teacher: 余法一)
    {
        "birth_info": {
            "raw": "男命：1979年7月21日卯時 出生地点：香港（英國長大）",
            "gender": "男", "year": 1979, "month": 7, "day": 21,
            "hour": 6, "minute": 0, "location": "香港", "calendar_type": "solar",
        },
        "questions": [
            {"q": "此命學歷如何?", "opts": [("A", "大學畢業"), ("B", "中學畢業"), ("C", "小學畢業"), ("D", "博士學位")], "answer": "", "cat": "学业"},
            {"q": "此命直至2020年婚姻狀況如何?", "opts": [("A", "已婚"), ("B", "未婚"), ("C", "離婚"), ("D", "重婚")], "answer": "", "cat": "婚姻"},
            {"q": "此命自小英國生活，那年回香港定居?", "opts": [("A", "2008"), ("B", "2010"), ("C", "2014"), ("D", "2016")], "answer": "", "cat": "运势"},
            {"q": "此命於那年被電話騙案騙走200多萬元?", "opts": [("A", "2012"), ("B", "2015"), ("C", "2018"), ("D", "2020")], "answer": "", "cat": "财运"},
            {"q": "此命於2017年發生何事?", "opts": [("A", "父親死亡"), ("B", "3次小型交通意外"), ("C", "創業失敗破財100多萬"), ("D", "肺結核病")], "answer": "", "cat": "运势"},
        ],
    },
    # Case 5: Female, born May 6, 1986, Wu hour, Hong Kong (Teacher: 方法振)
    {
        "birth_info": {
            "raw": "女命：1986年5月6日午時 出生地点：香港",
            "gender": "女", "year": 1986, "month": 5, "day": 6,
            "hour": 12, "minute": 0, "location": "香港", "calendar_type": "solar",
        },
        "questions": [
            {"q": "以下哪項最貼切形容命主的真實性格？", "opts": [("A", "沉默寡言，難以相處"), ("B", "和藹可親，受人歡迎"), ("C", "表面友善，實際脾氣欠佳，喜說謊話"), ("D", "陰險小氣")], "answer": "", "cat": "性格"},
            {"q": "命主的父親在哪一年去世？", "opts": [("A", "2007"), ("B", "2009"), ("C", "2012"), ("D", "2018")], "answer": "", "cat": "家庭"},
            {"q": "命主在庚寅大運的感情生活如何？", "opts": [("A", "一直單身"), ("B", "有一固定男朋友"), ("C", "追求者眾，沒有固定男朋友"), ("D", "數次戀上有婦之夫，當第三者")], "answer": "", "cat": "婚姻"},
            {"q": "命主在哪一年因犯官非被判守行為？", "opts": [("A", "2016"), ("B", "2017"), ("C", "2018"), ("D", "2019")], "answer": "", "cat": "官非"},
            {"q": "命主在哪一年誕下一名女兒？", "opts": [("A", "2015"), ("B", "2016"), ("C", "2017"), ("D", "2018")], "answer": "", "cat": "子女"},
        ],
    },
    # Case 6: Female, born June 16, 1962, Wei hour, Malaysia (Teacher: 东南易生)
    {
        "birth_info": {
            "raw": "女命：1962年6月16日未時 出生地点：马来西亚",
            "gender": "女", "year": 1962, "month": 6, "day": 16,
            "hour": 14, "minute": 0, "location": "马来西亚", "calendar_type": "solar",
        },
        "questions": [
            {"q": "此命主性格如何？", "opts": [("A", "善良温和，但有依赖性"), ("B", "急性子、心狠、好斗"), ("C", "自私、贪心、好胜"), ("D", "怕事、胆小、没主见")], "answer": "", "cat": "性格"},
            {"q": "此命主学历出生环境如何？", "opts": [("A", "大学毕业出身大富之家"), ("B", "大学毕业出身小康中产之家"), ("C", "高中毕业出身中产之家"), ("D", "初中毕业出身贫穷之家")], "answer": "", "cat": "学业"},
            {"q": "此命主在家排行第几？", "opts": [("A", "大女儿"), ("B", "二女儿"), ("C", "三女儿"), ("D", "四女儿")], "answer": "", "cat": "家庭"},
            {"q": "此命主何年结婚？", "opts": [("A", "1980"), ("B", "1981"), ("C", "1982"), ("D", "1983")], "answer": "", "cat": "婚姻"},
            {"q": "此命主工作是何行业？", "opts": [("A", "食品加工业，自创业"), ("B", "律师，自创业"), ("C", "美容，自创业"), ("D", "教育培训，打工")], "answer": "", "cat": "事业"},
        ],
    },
    # Case 7: Female, born Nov 25, 1993, Shen hour, Guigang Guangxi (Teacher: 李小康)
    {
        "birth_info": {
            "raw": "女命：1993年11月25日申時 出生地点：广西贵港",
            "gender": "女", "year": 1993, "month": 11, "day": 25,
            "hour": 16, "minute": 0, "location": "广西贵港", "calendar_type": "solar",
        },
        "questions": [
            {"q": "命主性格、长相、身高如何？", "opts": [("A", "性格冲动倔强讲义气，国字脸大婶身材，165CM"), ("B", "性格冲动脾气急对人好，水桶腰国字脸下巴尖，160CM"), ("C", "性格温柔刀子嘴豆腐心，模特身材国字脸下巴宽，163CM"), ("D", "性格冲动讲义气，模特身材尖脸，158CM")], "answer": "", "cat": "性格"},
            {"q": "命主学历如何？", "opts": [("A", "小学没毕业"), ("B", "初中毕业（高中没毕业）"), ("C", "大学毕业"), ("D", "博士学位")], "answer": "", "cat": "学业"},
            {"q": "命主何时交男友？何时结婚？", "opts": [("A", "2010年交男友，2012年结婚"), ("B", "2011年交男友，2013年结婚"), ("C", "2012年交男友，2014年结婚"), ("D", "2013年交男友，2015年结婚")], "answer": "", "cat": "婚姻"},
            {"q": "命主夫妻感情如何？", "opts": [("A", "婚姻和谐共处偶尔小矛盾（没离婚）"), ("B", "婚姻不和谐经常吵架（没离婚）"), ("C", "婚姻非常差又吵架又打架（已离婚）"), ("D", "婚姻非常差吵架不打架（已离婚）")], "answer": "", "cat": "婚姻"},
            {"q": "命主何时怀孕？生男生女？", "opts": [("A", "2014年怀孕生男孩"), ("B", "2015年怀孕生女孩"), ("C", "2016年怀孕生男孩"), ("D", "2017年怀孕生女孩")], "answer": "", "cat": "子女"},
        ],
    },
]


def main():
    all_questions = []
    global_q_num = 0

    for case_idx, case in enumerate(QUESTIONS_2020, start=1):
        case_id = f"case_2020_{case_idx}"
        for q_data in case["questions"]:
            global_q_num += 1
            all_questions.append({
                "id": f"fb_2020_{global_q_num:03d}",
                "source": "hkjfma_2020",
                "case_id": case_id,
                "birth_info": {**case["birth_info"]},
                "question": q_data["q"],
                "options": [{"letter": l, "text": t} for l, t in q_data["opts"]],
                "answer": q_data["answer"],  # empty — answers not found
                "category": q_data["cat"],
                "difficulty": "medium",
                "year": 2020,
            })

    # Save 2020 data
    out_path = PROJECT_ROOT / "data" / "hkjfma" / "2020.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "questions": all_questions,
            "source": "hkjfma_2020",
            "count": len(all_questions),
            "note": "Answers not available — questions from etongwen.com reproduction of 11th competition",
        }, f, ensure_ascii=False, indent=2)
    print(f"2020: {len(all_questions)} questions -> {out_path}")

    # Update combined.json
    combined_path = PROJECT_ROOT / "data" / "combined.json"
    with open(combined_path, encoding="utf-8") as f:
        combined = json.load(f)

    # Remove old 2020 data if any, add new
    combined["questions"] = [q for q in combined["questions"] if q.get("source") != "hkjfma_2020"]
    combined["questions"].extend(all_questions)
    combined["total"] = len(combined["questions"])
    combined["sources"]["hkjfma_2020"] = len(all_questions)

    # Recount categories
    cats = {}
    for q in combined["questions"]:
        cat = q.get("category", "unknown")
        cats[cat] = cats.get(cat, 0) + 1
    combined["categories"] = dict(sorted(cats.items(), key=lambda x: -x[1]))

    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    print(f"Combined updated: {combined['total']} total questions")


if __name__ == "__main__":
    main()
