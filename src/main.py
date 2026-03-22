import json
import os
import time
import logging
from datetime import datetime
import feedparser
import google.generativeai as genai

# ==========================================
# 1. 设置生产级日志记录
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. 核心功能函数
# ==========================================
def load_config(config_path="src/config.json"):
    """加载项目配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        raise

def fetch_rss_news(industry_name, rss_url, max_items=5):
    """获取并解析指定行业的 RSS 新闻"""
    logger.info(f"正在抓取【{industry_name}】的最新动态...")
    try:
        feed = feedparser.parse(rss_url)
        entries = feed.entries[:max_items]
        
        if not entries:
            logger.warning(f"【{industry_name}】未抓取到任何新闻。")
            return []
            
        news_items = []
        for entry in entries:
            title = entry.get('title', '无标题')
            link = entry.get('link', '#')
            news_items.append({"title": title, "link": link})
        return news_items
    except Exception as e:
        logger.error(f"抓取【{industry_name}】RSS源失败: {e}")
        return []

def analyze_with_ai(industry_name, news_items, model_name):
    """调用大模型生成跨界洞察 (带重试与防封禁策略)"""
    if not news_items:
        return "> 今日暂无高价值资讯更新，AI 休假中。\n"

    # 格式化新闻列表供 AI 阅读
    formatted_news = "\n".join([f"- {item['title']} ({item['link']})" for item in news_items])
    
    # 核心 Prompt：要求 AI 提供增量价值和降维打击视角
    prompt = f"""
    你是一位具备顶尖跨界思维的商业分析师和技术预言家。你的任务是帮助被困在"信息茧房"中的读者看懂陌生行业的底层剧变。
    
    以下是【{industry_name}】行业过去24小时的核心新闻动态：
    {formatted_news}
    
    请严格按照以下 Markdown 格式输出你的深度分析报告（语言必须极其犀利、通俗且直击商业本质）：
    
    ### 📌 行业核心脉络
    (用一句话总结这些新闻反映出的该行业今天的核心主线、痛点或技术突破)
    
    ### 🧠 跨界降维打击点 (打破信息差)
    - **底层逻辑剧变**：这些事件背后，该行业的资源配置、技术栈或商业模式发生了怎样的根本改变？
    - **他山之石**：身处互联网、金融、服务业等其他行业的从业者，可以从中直接"抄作业"或警惕什么？
    - **个体生态位**：对于普通人在择业方向、技能储备或副业探索上，这预示着什么新的生态位（红利）或绞肉机（风险）？
    """

    try:
        model = genai.GenerativeModel(model_name)
        
        # 增加重试机制，防止 GitHub Actions 运行时因为偶尔的网络抖动而失败
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as api_e:
                logger.warning(f"AI API 调用异常 (尝试 {attempt + 1}/{max_retries}): {api_e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # 退避重试
                else:
                    raise api_e
                    
    except Exception as e:
        logger.error(f"AI 分析【{industry_name}】失败: {e}")
        return f"> AI 洞察生成失败，请检查 API 状态。\n\n**今日原始新闻：**\n{formatted_news}"

# ==========================================
# 3. 主调度程序
# ==========================================
def main():
    logger.info("启动 360 行 AI 跨界洞察引擎...")
    
    # 1. 环境变量校验 (GitHub Actions 注入)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("未找到 GEMINI_API_KEY 环境变量，请确保已正确配置。")
        return
    genai.configure(api_key=api_key)

    # 2. 加载配置
    config = load_config()
    model_name = config.get("model_name", "gemini-2.5-flash")
    output_dir = config.get("output_dir", "360_Industry_Insights")
    max_news = config.get("max_news_per_industry", 5)
    industries = config.get("industries", [])

    # 3. 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"已创建输出目录: {output_dir}")

    # 4. 初始化报告内容
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_title = f"# 🚀 360行 AI 每日跨界洞察 ({today_str})"
    report_intro = "> **项目愿景**：打破信息茧房，每天带你窥探这个世界正在发生的不同折叠。利用 AI 的跨领域联想能力，寻找行业间的降维打击机会。\n\n---\n\n"
    report_content = f"{report_title}\n\n{report_intro}"

    # 5. 遍历抓取与分析
    for industry in industries:
        ind_name = industry.get("name")
        rss_url = industry.get("rss_url")
        
        if not ind_name or not rss_url:
            continue

        # 抓取 -> 分析 -> 拼接
        news_items = fetch_rss_news(ind_name, rss_url, max_items=max_news)
        insight = analyze_with_ai(ind_name, news_items, model_name)
        report_content += f"## 🌍 【{ind_name}】\n\n{insight}\n\n---\n\n"
        
        # 遵守 API 速率限制，温柔地请求
        time.sleep(3)

    # 6. 写入最终报告文件
    file_path = os.path.join(output_dir, f"Insight_Report_{today_str}.md")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        logger.info(f"🎉 成功！今日洞察报告已生成并保存至: {file_path}")
    except Exception as e:
        logger.error(f"写入报告文件失败: {e}")

if __name__ == "__main__":
    main()