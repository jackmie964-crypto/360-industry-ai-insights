# 🚀 360行 AI 跨界洞察引擎 (Anti-Cocoon AI)

[![GitHub Actions Status](https://img.shields.io/badge/Auto_Update-Active-brightgreen?style=flat-square)](#)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](#)

## 💡 为什么做这个项目？

在全面 AI 的时代，我们本该拥有获取全人类知识的最高效工具。然而现实是：**推荐算法让我们深陷比以往更坚固的"信息茧房"**。做互联网的只看大厂裁员，做硬件的只关心芯片制程，我们对其他行业正在发生的巨变一无所知。

本项目旨在利用 **GitHub Actions 自动化 + 大语言模型（LLM）的跨界归纳能力**，建立一个"全行业破壁机"。

我们每天自动抓取那些被你忽略的冷门或硬核行业（如：特种冶金、远洋航运、合成生物、精密仪器）的最新动态，并强迫 AI 回答一个核心问题：**这些行业的变动，对其他领域的普通人有什么启发、机会或降维打击的风险？**

## 🌟 核心功能

- **🤖 全自动运行**：零服务器成本！依托 GitHub Actions，每天早上自动抓取、分析并生成 Markdown 报告，直接 Commit 到仓库中。
- **🧠 跨界 Prompt 引擎**：拒绝流水账式的新闻总结。本项目的 AI 必须输出"底层逻辑"、"他山之石"和"个体生态位"三个维度的深度洞察。
- **⚙️ 极简配置**：通过 `src/config.json` 即可无限扩展你想关注的行业 RSS 源，无需修改任何代码。

## 📂 项目结构

```text
├── .github/workflows/daily_update.yml  # GitHub Actions 自动化定时任务
├── src/
│   ├── config.json                     # 360行数据源配置中心
│   └── main.py                         # AI 抓取与分析核心引擎
├── 360_Industry_Insights/              # 每天自动生成的历史洞察报告存放处
├── requirements.txt                    # Python 环境依赖
└── README.md                           # 你正在读的文件
```