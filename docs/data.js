/**
 * FateryBench leaderboard data.
 * This file is auto-generated from results/ directory.
 * To update: python scripts/build_docs_data.py
 */

const BENCHMARK_DATA = {
  version: "1.0",
  lastUpdated: "2025-03-19",
  totalQuestions: 272,

  dataset: {
    sources: {
      "HKJFMA 2020 (11th)": 35,
      "HKJFMA 2022 (13th)": 50,
      "HKJFMA 2023 (14th)": 50,
      "HKJFMA 2024 (15th)": 60,
      "HKJFMA 2025 (16th)": 37,
      "Celebrity Cases": 40,
    },
    categories: {
      "婚姻 Marriage": 65,
      "事业 Career": 48,
      "家庭 Family": 35,
      "健康 Health": 29,
      "性格 Personality": 24,
      "学业 Education": 19,
      "运势 Fate": 18,
      "财运 Wealth": 16,
      "子女 Children": 10,
      "外貌 Appearance": 4,
      "官非 Legal": 2,
      "灾劫 Disaster": 2,
    },
  },

  // Placeholder results — will be replaced with actual benchmark data
  // Fatery = Gemini 3 Flash + Fatery-Enhanced prompt
  // Format: model → mode → accuracy
  results: [
    {
      model: "Fatery (Gemini 3 Flash + Prompt)",
      modelId: "gemini-3-flash",
      provider: "Fatery.me",
      isFateryDefault: true,
      scores: {
        vanilla: { accuracy: 0.0, correct: 0, total: 272 },
        cot: { accuracy: 0.0, correct: 0, total: 272 },
        astro: { accuracy: 0.0, correct: 0, total: 272 },
        fatery: { accuracy: 0.0, correct: 0, total: 272 },
      },
    },
    {
      model: "Gemini 3 Flash",
      modelId: "gemini-3-flash",
      provider: "Google",
      isFateryDefault: false,
      scores: {
        vanilla: { accuracy: 0.0, correct: 0, total: 272 },
        cot: { accuracy: 0.0, correct: 0, total: 272 },
        astro: { accuracy: 0.0, correct: 0, total: 272 },
        fatery: { accuracy: 0.0, correct: 0, total: 272 },
      },
    },
    {
      model: "Gemini 3 Pro",
      modelId: "gemini-3-pro",
      provider: "Google",
      isFateryDefault: false,
      scores: {
        vanilla: { accuracy: 0.0, correct: 0, total: 272 },
        cot: { accuracy: 0.0, correct: 0, total: 272 },
        astro: { accuracy: 0.0, correct: 0, total: 272 },
        fatery: { accuracy: 0.0, correct: 0, total: 272 },
      },
    },
    {
      model: "GPT-5.3",
      modelId: "gpt-5.3",
      provider: "OpenAI",
      isFateryDefault: false,
      scores: {
        vanilla: { accuracy: 0.0, correct: 0, total: 272 },
        cot: { accuracy: 0.0, correct: 0, total: 272 },
        astro: { accuracy: 0.0, correct: 0, total: 272 },
        fatery: { accuracy: 0.0, correct: 0, total: 272 },
      },
    },
    {
      model: "DeepSeek Thinking",
      modelId: "deepseek-reasoner",
      provider: "DeepSeek",
      isFateryDefault: false,
      scores: {
        vanilla: { accuracy: 0.0, correct: 0, total: 272 },
        cot: { accuracy: 0.0, correct: 0, total: 272 },
        astro: { accuracy: 0.0, correct: 0, total: 272 },
        fatery: { accuracy: 0.0, correct: 0, total: 272 },
      },
    },
  ],

  sampleQuestions: [
    {
      id: "fb_0001",
      source: "HKJFMA 2022",
      birth: "男命：1974年4月28日下午4:40分 出生地点：usa",
      question: "此命1996年发生何事？",
      options: ["A. 患上严重抑郁症", "B. 回港认识现任妻子", "C. 交通意外，撞车，人平安", "D. 得到一笔意外之财"],
      answer: "A",
      category: "健康",
    },
    {
      id: "fb_c001",
      source: "Celebrity (黄仁勋)",
      birth: "男命：1963年2月17日 出生地点：台湾台南",
      question: "此人30岁左右（1993年前后）最可能发生什么事？",
      options: ["A. 创办科技公司，成为CEO", "B. 移民美国，在大学任教", "C. 家族企业破产，负债累累", "D. 从政，当选地方议员"],
      answer: "A",
      category: "事业",
    },
  ],
};
