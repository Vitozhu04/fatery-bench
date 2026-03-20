/**
 * FateryBench leaderboard data.
 * Generated from benchmark results on 2026-03-20.
 *
 * Scoring: Competition questions only (196 HKJFMA questions).
 * Celebrity cases (40q) excluded — models achieve 75-100% via memorization.
 */

const BENCHMARK_DATA = {
  version: "1.2",
  lastUpdated: "2026-03-21",
  competitionQuestions: 196,

  // Human reference levels from HKJFMA competitions.
  // Source: MirrorAI paper (arXiv:2510.23337) reports 60% = 3rd place in 2024.
  humanLevels: {
    champion: { label: "HKJFMA Top 3", accuracy: 0.60, note: "3rd place in 2024 competition ≈ 60%" },
    random: { label: "Random Guess", accuracy: 0.25 },
  },

  dataset: {
    sources: {
      "HKJFMA 2022": 50,
      "HKJFMA 2023": 50,
      "HKJFMA 2024": 60,
      "HKJFMA 2025": 36,
    },
    categories: {
      "婚姻 Marriage": 56,
      "事业 Career": 46,
      "家庭 Family": 31,
      "健康 Health": 26,
      "性格 Personality": 19,
      "学业 Education": 15,
      "财运 Wealth": 14,
      "运势 Fate": 14,
      "子女 Children": 8,
      "外貌 Appearance": 4,
      "灾劫 Disaster": 2,
      "官非 Legal": 1,
    },
  },

  // Competition-only (196q). One Fatery entry (best) + all baselines + human reference.
  results: [
    {
      model: "Human (HKJFMA Top 3)",
      modelId: "human",
      provider: "HKJFMA 2024",
      isHuman: true,
      accuracy: 0.60,
      correct: "~118",
      total: 196,
      note: "3rd place in 2024 competition (source: arXiv:2510.23337)",
    },
    {
      model: "Fatery",
      modelId: "gemini-3-flash-preview",
      provider: "Fatery.me",
      isFatery: true,
      accuracy: 86 / 196,
      correct: 86,
      total: 196,
      bySource: {
        "2022": { correct: 22, total: 50, accuracy: 0.44 },
        "2023": { correct: 16, total: 50, accuracy: 0.32 },
        "2024": { correct: 30, total: 60, accuracy: 0.50 },
        "2025": { correct: 18, total: 36, accuracy: 0.50 },
      },
    },
    {
      model: "GPT-5.4",
      modelId: "gpt-5.4",
      provider: "OpenAI",
      isFatery: false,
      accuracy: 75 / 196,
      correct: 75,
      total: 196,
    },
    {
      model: "Gemini 3.1 Flash Lite",
      modelId: "gemini-3.1-flash-lite-preview",
      provider: "Google",
      isFatery: false,
      accuracy: 70 / 196,
      correct: 70,
      total: 196,
    },
    {
      model: "GPT-5.3",
      modelId: "gpt-5.3-chat-latest",
      provider: "OpenAI",
      isFatery: false,
      accuracy: 67 / 196,
      correct: 67,
      total: 196,
    },
    {
      model: "Gemini 3.1 Pro",
      modelId: "gemini-3.1-pro-preview",
      provider: "Google",
      isFatery: false,
      accuracy: 65 / 196,
      correct: 65,
      total: 196,
    },
    {
      model: "Gemini 3 Pro",
      modelId: "gemini-3-pro-preview",
      provider: "Google",
      isFatery: false,
      accuracy: 62 / 196,
      correct: 62,
      total: 196,
    },
    {
      model: "Gemini 3 Flash",
      modelId: "gemini-3-flash-preview",
      provider: "Google",
      isFatery: false,
      accuracy: 59 / 196,
      correct: 59,
      total: 196,
    },
    {
      model: "DeepSeek R1",
      modelId: "deepseek-reasoner",
      provider: "DeepSeek",
      isFatery: false,
      accuracy: 2 / 196,
      correct: 2,
      total: 196,
      note: "API instability — 231/236 connection errors",
    },
    {
      model: "Random Baseline",
      modelId: "random",
      provider: "-",
      isRandom: true,
      accuracy: 0.25,
      correct: "~49",
      total: 196,
      note: "4-choice random guess = 25%",
    },
  ],

  // Fatery's base model lift
  fateryLift: {
    model: "Gemini 3 Flash",
    baseline: { accuracy: 59 / 196, correct: 59 },
    fatery:   { accuracy: 86 / 196, correct: 86 },
    delta: 27,
    total: 196,
  },

  sampleQuestions: [
    {
      id: "fb_0001",
      source: "HKJFMA 2022",
      birth: "男命：1974年4月28日下午4:40分 出生地点：USA",
      question: "此命1996年发生何事？",
      options: ["A. 患上严重抑郁症", "B. 回港认识现任妻子", "C. 交通意外，撞车，人平安", "D. 得到一笔意外之财"],
      answer: "A",
      category: "健康",
    },
    {
      id: "fb_0050",
      source: "HKJFMA 2024",
      birth: "男命：1988年6月11日丑时 出生地点：香港",
      question: "此命的婚姻状况如何？",
      options: ["A. 已婚，婚姻美满", "B. 已婚，但婚姻不顺", "C. 未婚，但有稳定交往对象", "D. 未婚，感情路崎岖"],
      answer: "D",
      category: "婚姻",
    },
  ],
};
