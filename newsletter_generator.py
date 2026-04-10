"""哈哈·HR科技金融日报 - 静态网页生成器
每天生成 newsletter.html，以后直接刷新这个文件即可查看最新内容
"""
import yagmail
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─── 配置 ───────────────────────────────────────────
SENDER_EMAIL = "monica_hr2026@163.com"
SENDER_AUTH_CODE = "WC3eT37KgPZFye9p"
RECIPIENT_EMAIL = "15311195668@163.com"
OUTPUT_DIR = r"c:\Users\houme\WorkBuddy\20260410235006"
NEWSLETTER_FILE = os.path.join(OUTPUT_DIR, "newsletter.html")
# ────────────────────────────────────────────────────

# 完整HTML模板（手机优先版）
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>哈哈·HR科技金融日报</title>
<style>
:root {
  --primary: #1a5ca8; --primary-dark: #0f2a4a;
  --accent-red: #e74c3c; --accent-orange: #f39c12; --accent-green: #27ae60;
  --accent-purple: #8e44ad; --accent-blue: #3498db;
  --bg: #f4f6f9; --card-bg: #ffffff;
  --text: #1a2a3a; --text-light: #7f8c9a; --border: #e8ecf0;
}
* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body { font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; padding-bottom: 80px; }

/* Header */
.header { background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%); color: white; padding: 20px 16px 16px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(15,42,74,0.25); }
.header-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 14px; }
.header-brand { font-size: 11px; color: rgba(255,255,255,0.6); letter-spacing: 1px; }
.header-date-box { text-align: right; }
.header-date-box .weekday { font-size: 11px; color: rgba(255,255,255,0.6); }
.header-date-box .date { font-size: 18px; font-weight: 800; line-height: 1.2; }
.header h1 { font-size: 20px; font-weight: 800; margin-bottom: 2px; }
.header h1 span { color: #60b8ff; }
.header-sub { font-size: 12px; color: rgba(255,255,255,0.55); }

/* Highlights */
.highlights { padding: 16px 16px 0; }
.highlight-label { font-size: 11px; font-weight: 700; color: var(--text-light); letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
.highlight-label::before { content: ''; display: inline-block; width: 3px; height: 12px; background: var(--primary); border-radius: 2px; }
.highlight-card { background: var(--card-bg); border-radius: 14px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid var(--primary); }
.highlight-card.red { border-left-color: var(--accent-red); }
.highlight-card.orange { border-left-color: var(--accent-orange); }
.highlight-card.green { border-left-color: var(--accent-green); }
.highlight-card.purple { border-left-color: var(--accent-purple); }
.highlight-card.blue { border-left-color: var(--accent-blue); }
.hl-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.hl-cat { font-size: 10px; font-weight: 700; color: white; background: var(--primary); padding: 2px 8px; border-radius: 4px; }
.hl-cat.red { background: var(--accent-red); }
.hl-cat.orange { background: var(--accent-orange); }
.hl-cat.green { background: var(--accent-green); }
.hl-cat.purple { background: var(--accent-purple); }
.hl-cat.blue { background: var(--accent-blue); }
.hl-title { font-size: 15px; font-weight: 700; color: var(--text); line-height: 1.5; margin-bottom: 4px; }
.hl-body { font-size: 12px; color: var(--text-light); line-height: 1.6; }
.hl-action { margin-top: 8px; font-size: 11px; color: var(--primary); font-weight: 600; }
.hl-action::before { content: '→ '; }
.hl-link { margin-top: 6px; }
.hl-link a { font-size: 11px; color: var(--text-light); text-decoration: none; border-bottom: 1px dashed var(--text-light); }

/* Nav */
.nav-bar { display: flex; gap: 6px; padding: 14px 16px; overflow-x: auto; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
.nav-bar::-webkit-scrollbar { display: none; }
.nav-pill { flex-shrink: 0; font-size: 12px; font-weight: 600; padding: 7px 14px; border-radius: 20px; background: white; color: var(--text-light); border: 1.5px solid var(--border); cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.nav-pill.active { background: var(--primary); color: white; border-color: var(--primary); }

/* Section */
.section-wrap { padding: 0 16px 16px; }
.section-card { background: var(--card-bg); border-radius: 14px; margin-bottom: 12px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.sec-head { padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; cursor: pointer; }
.sec-head-left { display: flex; align-items: center; gap: 10px; }
.sec-icon { width: 30px; height: 30px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; }
.sec-title { font-size: 14px; font-weight: 700; color: var(--text); }
.sec-count { font-size: 11px; color: var(--text-light); background: var(--bg); padding: 2px 8px; border-radius: 10px; }
.sec-toggle { font-size: 16px; color: var(--text-light); transition: transform 0.2s; }
.sec-body { padding: 12px 16px; }
.sec-body.hidden { display: none; }

/* News */
.news-row { padding: 12px 0; border-bottom: 1px solid var(--border); }
.news-row:last-child { border-bottom: none; padding-bottom: 0; }
.news-row:first-child { padding-top: 0; }
.news-meta { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
.news-label { font-size: 9px; font-weight: 700; color: white; padding: 1px 6px; border-radius: 3px; }
.news-time { font-size: 10px; color: var(--text-light); }
.news-title { font-size: 13px; font-weight: 700; color: var(--text); line-height: 1.5; margin-bottom: 3px; }
.news-body { font-size: 11px; color: var(--text-light); line-height: 1.6; }
.news-insight { margin-top: 5px; font-size: 11px; color: var(--primary); background: rgba(26,92,168,0.05); padding: 5px 8px; border-radius: 6px; }
.news-link { margin-top: 4px; }
.news-link a { font-size: 10px; color: var(--text-light); text-decoration: none; border-bottom: 1px dashed var(--text-light); }

/* KB Card */
.kb-card { background: linear-gradient(135deg, var(--primary) 0%, #2980b9 100%); color: white; border-radius: 14px; padding: 18px 16px; margin: 0 16px 12px; }
.kb-label { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.6); letter-spacing: 1px; margin-bottom: 8px; }
.kb-title { font-size: 15px; font-weight: 800; margin-bottom: 4px; }
.kb-type { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.6); margin-bottom: 8px; }
.kb-body { font-size: 12px; color: rgba(255,255,255,0.85); line-height: 1.7; margin-bottom: 10px; }
.kb-action { font-size: 11px; color: #a8d4ff; background: rgba(255,255,255,0.1); padding: 6px 10px; border-radius: 8px; line-height: 1.5; }
.kb-ai { background: linear-gradient(135deg, #8e44ad 0%, #6c3483 100%); }

/* Comp Grid */
.comp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.comp-card { background: var(--bg); border-radius: 12px; padding: 14px; }
.comp-name { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 3px; }
.comp-tag { font-size: 9px; font-weight: 700; color: white; background: var(--text-light); padding: 1px 6px; border-radius: 3px; display: inline-block; margin-bottom: 6px; }
.comp-tag.hot { background: var(--accent-red); }
.comp-tag.new { background: var(--accent-green); }
.comp-item { font-size: 11px; color: var(--text-light); line-height: 1.6; margin-bottom: 2px; }
.comp-item strong { color: var(--text); }

/* Footer */
.footer { text-align: center; padding: 20px 16px; font-size: 11px; color: var(--text-light); }
.footer-logo { font-size: 13px; font-weight: 700; color: var(--primary); margin-bottom: 4px; }
.footer-note { line-height: 1.6; }

/* Color classes */
.bg-blue { background: var(--primary); }
.bg-orange { background: var(--accent-orange); }
.bg-green { background: var(--accent-green); }
.bg-purple { background: var(--accent-purple); }
.bg-teal { background: #0e8076; }
.bg-red { background: var(--accent-red); }
.bg-gray { background: #7f8c8d; }
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-top">
    <div>
      <div class="header-brand">HAHAHA DAILY</div>
      <h1>哈哈<span>·</span>日报</h1>
      <div class="header-sub">HR科技金融 · 每日必读</div>
    </div>
    <div class="header-date-box">
      <div class="weekday">{{WEEKDAY}}</div>
      <div class="date">{{DATE_SHORT}}</div>
    </div>
  </div>
</div>

<!-- TODAY HIGHLIGHTS -->
<div class="highlights">
  <div class="highlight-label">今日核心</div>
  {{HIGHLIGHTS}}
</div>

<!-- SECTION NAV -->
<div class="nav-bar">
  <div class="nav-pill active" onclick="switchSection('hr-global')">🌏 全球HR</div>
  <div class="nav-pill" onclick="switchSection('hr-china')">🇨🇳 中国HR</div>
  <div class="nav-pill" onclick="switchSection('fintech')">💹 金融科技</div>
  <div class="nav-pill" onclick="switchSection('risk')">🔐 信贷风控</div>
  <div class="nav-pill" onclick="switchSection('comp-pure')">🎯 精准竞品</div>
  <div class="nav-pill" onclick="switchSection('comp-big')">🏢 大厂生态</div>
  <div class="nav-pill" onclick="switchSection('learn')">📚 学习推荐</div>
</div>

<!-- SECTIONS -->
<div class="section-wrap">
  {{SECTIONS}}
</div>

<!-- FOOTER -->
<div class="footer">
  <div class="footer-logo">哈哈哈</div>
  <div class="footer-note">
    由哈哈哈每日自动生成 · 数据来源综合公开资讯<br>
    每日早上9:00自动更新 · 刷新页面查看最新内容
  </div>
</div>

<script>
function toggleSection(id) {
  var body = document.getElementById('body-' + id);
  var toggle = document.getElementById('toggle-' + id);
  if (body.classList.contains('hidden')) {
    body.classList.remove('hidden');
    toggle.textContent = '▲';
  } else {
    body.classList.add('hidden');
    toggle.textContent = '▼';
  }
}
function switchSection(id) {
  document.querySelectorAll('.nav-pill').forEach(function(p) { p.classList.remove('active'); });
  document.querySelectorAll('.nav-pill').forEach(function(p) {
    if (p.getAttribute('onclick').indexOf("'" + id + "'") !== -1) p.classList.add('active');
  });
  var sec = document.getElementById('sec-' + id);
  if (sec) {
    sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(function() {
      var body = document.getElementById('body-' + id);
      var toggle = document.getElementById('toggle-' + id);
      if (body) { body.classList.remove('hidden'); if (toggle) toggle.textContent = '▲'; }
    }, 400);
  }
}
</script>
</body>
</html>
"""

def get_weekday_cn():
    weekdays = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
    return weekdays[datetime.now().weekday()]

def build_highlight(cat_color, cat_text, title, body, action, link_text, link_url):
    return f'''<div class="highlight-card {cat_color}">
    <div class="hl-top"><span class="hl-cat {cat_color}">{cat_text}</span></div>
    <div class="hl-title">{title}</div>
    <div class="hl-body">{body}</div>
    <div class="hl-action">{action}</div>
    <div class="hl-link"><a href="{link_url}" target="_blank">{link_text} →</a></div>
  </div>'''

def build_section(icon_emoji, icon_bg, title, count, sec_id, news_html):
    return f'''<div id="sec-{sec_id}" class="section-card">
  <div class="sec-head" onclick="toggleSection('{sec_id}')">
    <div class="sec-head-left">
      <div class="sec-icon {icon_bg}">{icon_emoji}</div>
      <div class="sec-title">{title}</div>
    </div>
    <div style="display:flex;align-items:center;gap:8px">
      <span class="sec-count">{count}</span>
      <span class="sec-toggle" id="toggle-{sec_id}">▼</span>
    </div>
  </div>
  <div class="sec-body" id="body-{sec_id}">
    {news_html}
  </div>
</div>'''

def build_news(label_bg, label_text, time_text, news_title, news_body, insight, link_text=None, link_url=None):
    link_html = f'<div class="news-link"><a href="{link_url}" target="_blank">{link_text} →</a></div>' if link_text and link_url else ''
    return f'''<div class="news-row">
    <div class="news-meta">
      <span class="news-label {label_bg}">{label_text}</span>
      <span class="news-time">{time_text}</span>
    </div>
    <div class="news-title">{news_title}</div>
    <div class="news-body">{news_body}</div>
    <div class="news-insight">{insight}</div>
    {link_html}
  </div>'''

def build_kb_card(kb_class, label, type_text, title, body, action, link_text, link_url):
    return f'''<div class="kb-card {kb_class}">
  <div class="kb-label">{label}</div>
  <div class="kb-type">{type_text}</div>
  <div class="kb-title">{title}</div>
  <div class="kb-body">{body}</div>
  <div class="kb-action">{action}<br><a href="{link_url}" target="_blank" style="color:#a8d4ff;text-decoration:none;border-bottom:1px dashed #a8d4ff">{link_text} →</a></div>
</div>'''

def build_comp_grid(cards_html):
    return f'<div class="comp-grid">{cards_html}</div>'

def build_comp_card(name, tag_text, tag_class, items, link_text, link_url):
    items_html = ''.join([f'<div class="comp-item"><strong>{k}</strong>{v}</div>' for k,v in items])
    return f'''<div class="comp-card">
  <div class="comp-name">{name}</div>
  <span class="comp-tag {tag_class}">{tag_text}</span>
  {items_html}
  <div style="margin-top:6px"><a href="{link_url}" target="_blank" style="font-size:10px;color:var(--text-light);text-decoration:none;border-bottom:1px dashed var(--text-light)">{link_text} →</a></div>
</div>'''

def generate_newsletter():
    weekday = get_weekday_cn()
    date_short = datetime.now().strftime("%m.%d")
    date_full = datetime.now().strftime("%Y年%m月%d日")

    # 今日核心高亮
    highlights = build_highlight(
        'red', '全球HR',
        'Q1全球科技裁员近8万人，29%岗位被AI替代',
        '裁员潮持续但高技能人才争夺并未降温，"79,000人失业，但人才战争远未结束"',
        '🎯 行动项：重新审视招聘策略，高技能人才吸引力策略比以往更重要',
        'Bloomberg：科技裁员深度报道',
        'https://www.bloomberg.com/news/articles/2026-04-02/tech-layoffs-ai-replacement'
    ) + build_highlight(
        'orange', '信贷风控',
        '央行一次性信用修复政策落地，万元内逾期可"清零"',
        '2020年1月-2026年3月期间产生、且已还清的逾期，可申请修复，4月起集中受理',
        '🎯 行动项：关注此政策对存量客户资产质量的影响，评估风控模型是否需要重新校准',
        '中国人民银行官网',
        'https://www.pbc.gov.cn'
    ) + build_highlight(
        'green', '精准竞品',
        '百融云创激进扩张：185岗位在招，AI Agent加速落地',
        '"硅基员工"已推向市场，RaaS商业模式驱动产品矩阵重塑',
        '🎯 行动项：关注其技术岗薪资变化，评估睿智科技在AI人才市场的竞争力',
        '百融云创官网',
        'https://www.brjr.com.cn'
    ) + build_highlight(
        'blue', '大厂动态',
        '蚂蚁集团春招70%为AI岗位，支付AI用户破亿',
        'AI战略全面落地，隐私计算+智能风控持续扩招，技术人才竞争进入新阶段',
        '🎯 行动项：关注AI+风控复合型人才市场供给，思考差异化吸引策略',
        '蚂蚁集团官网',
        'https://www.antgroup.com'
    )

    # 全球HR
    hr_global = build_news('bg-red', '裁员', 'Bloomberg · 4月2日',
        '2026年Q1全球科技裁员近8万人，约50%因AI替代',
        '美国科技企业裁员公告持续加速，Q2未见放缓信号，但高技能人才竞争并未降温。',
        '💡 启示：裁员≠人才过剩，高技能人才争夺依然激烈，HR吸引力策略需升级',
        'Bloomberg原文', 'https://www.bloomberg.com/news/articles/2026-04-02/tech-layoffs-q1-2026'
    ) + build_news('bg-purple', '趋势', 'Gartner · 2026',
        'Gartner：2026年7大HR趋势，AI教练+个性化招聘为主轴',
        '29%的AI生产力提升来自HR运营模式转型，职能重构成为不可逆趋势。',
        '💡 启示：开始评估公司内部哪些HR流程可以被AI辅助或替代',
        'Gartner HR趋势报告', 'https://www.gartner.com/en/human-resources/topics/hr-trends'
    )

    # 中国HR
    hr_china = build_news('bg-orange', '政策', '人社部 · 4月1日',
        '2026届城市联合招聘春季专场在银川启动，AI岗位扎堆',
        '人社部副部长颜清辉出席，数字经济、新兴岗位成为今年春招最大看点。',
        '💡 启示：关注校招窗口期，提前布局AI/数据类岗位的候选人池'
    ) + build_news('bg-green', '人才', '脉脉 · 2026',
        '脉脉发布80家"隐形大厂"，智谱、SHEIN、地平线入选',
        '反映中高端人才择业风向正在变化，传统大厂吸引力下降，新兴科技公司成为热门选择。',
        '💡 启示：雇主品牌建设需跟上，讲述技术深度+成长空间的故事'
    )

    # 金融科技
    fintech = build_news('bg-teal', '监管', '央视财经 · 3月30日',
        '5万亿网贷行业迎来最强监管：费用结构成为新焦点',
        '曝光低息诱惑背后"高息套路陷阱"——宣传月息0.8%，实含多重费用，监管细化至费用清单。',
        '💡 启示：合规成本上升，关注公司产品费率结构是否符合最新监管要求'
    ) + build_news('bg-blue', '业绩', '兴业消金 · 年报',
        '兴业消费金融2025年净利润12亿，同比大增179%',
        '消费金融赛道整体业绩向好，但监管收紧信号同步释放，行业进入"规范发展"新阶段。',
        '💡 启示：业绩增长需匹配合规能力，关注行业合规团队建设趋势'
    )

    # 信贷风控
    risk = build_news('bg-purple', '政策', '央行 · 2026',
        '央行新监管周期：利率透明化+费用清单强制披露',
        '信贷市场进入新监管周期，降低融资中间成本成为政策主轴，企业融资与个人借贷双线并进。',
        '💡 启示：风控模型需同步政策调整，关注合规部门与风控部门的协同机制'
    ) + build_news('bg-red', '黑产', '威胁猎人 · 3月30日',
        '骗贷手法"真实化"升级：黑产用真实流水绕过传统风控',
        '从"虚假材料"演变为"真实补缴"，攻击手法显著升级，传统规则风控失效。',
        '💡 启示：反欺诈需引入行为生物特征、关系图谱、实时决策新一代手段',
        '威胁猎人报告', 'https://www.threathunter.cn'
    )

    # 精准竞品
    comp_pure = build_section('🎯', 'bg-red', '精准竞品', '直接对标', 'comp-pure',
        build_comp_grid(
            build_comp_card('百融云创', '热招', 'hot',
                [('动态：','RaaS+AI Agent激进'), ('在招：','185个职位'), ('特色：','硅基员工推向市场'), ('ESG：','公益助残项目推进')],
                '官网', 'https://www.brjr.com.cn') +
            build_comp_card('同盾科技', '扩招', '',
                [('动态：','2026秋招全面启动'), ('在招：','44个职位'), ('特色：','出海布局，小语种岗'), ('方向：','解决方案+销售')],
                '官网', 'https://www.tongdun.cn') +
            build_comp_card('天创信用', '平稳', '',
                [('资质：','央行企业征信牌照'), ('在招：','约15个职位'), ('特色：','合规资质壁垒'), ('产品：','灵创·X风策平台')],
                '官网', 'https://www.tianchuangcredit.com') +
            build_comp_card('富数科技', '新锐', 'new',
                [('技术：','联邦学习+隐私计算'), ('投资：','中网投战略投资'), ('方向：','银行数据互通'), ('招聘：','算法/安全方向')],
                '官网', 'https://www.fudata.cn') +
            build_comp_card('易鑫集团', '热招', 'hot',
                [('上市：','港股02860.HK'), ('定位：','汽车金融AI SaaS'), ('动态：','AI+金融科技深度整合，智能风控团队持续扩招')],
                '官网', 'https://www.yixin.com')
        )
    )

    # 大厂生态
    comp_big = build_section('🏢', 'bg-gray', '大厂金融科技生态', '行业格局', 'comp-big',
        build_comp_grid(
            build_comp_card('蚂蚁集团', '热招', 'hot',
                [('春招：','70%为AI岗位'), ('产品：','支付AI用户破亿'), ('技术：','隐私计算+智能风控')],
                '官网', 'https://www.antgroup.com') +
            build_comp_card('度小满', '平稳', '',
                [('资质：','博士后工作站'), ('方向：','AI风控+智能信贷'), ('招聘：','风控算法方向')],
                '官网', 'https://www.duxiaoman.com') +
            build_comp_card('火山引擎', '扩招', '',
                [('背景：','字节跳动金融云'), ('动态：','金融线持续扩招'), ('方向：','数据+风控+合规')],
                '官网', 'https://www.volcengine.com') +
            build_comp_card('京东科技', '春招', '',
                [('春招：','11大方向'), ('重点：','金融科技方向'), ('生态：','京东金融+京东云')],
                '官网', 'https://www.jdt.com') +
            build_comp_card('瓴羊（阿里）', '数据', '',
                [('背景：','阿里数据中台'), ('方向：','数据治理+分析'), ('产品：','企业数据智能')],
                '官网', 'https://www.lingyang.com') +
            build_comp_card('腾讯金融科技', '稳定', '',
                [('生态：','微信支付核心'), ('方向：','风控稳定招聘'), ('特点：','稳扎稳打，技术深度')],
                '官网', 'https://www.tencent.com') +
            build_comp_card('阿里云', '热招', 'hot',
                [('方向：','金融安全架构师热招'), ('产品：','金融云全栈解决方案'), ('趋势：','金融行业云化持续推进，大客户定制化服务增加')],
                '官网', 'https://www.aliyun.com')
        )
    )

    # 学习推荐
    learn = build_section('📚', 'bg-green', '每日学习推荐', '3个推荐', 'learn',
        build_news('bg-teal', '管理理论', '今日推荐',
            '平衡计分卡（BSC）—— 从财务指标到战略落地',
            '1992年卡普兰&诺顿提出，从财务、客户、内部流程、学习成长四个维度衡量组织绩效。',
            '💡 对HR的落地价值：可作为绩效体系设计框架，将人才培养指标纳入组织战略',
            '哈佛商业评论原文', 'https://hbr.org/1992/01/the-balanced-scorecard-measures-that-drive-performance-2'
        ) + build_news('bg-purple', 'HR专业', '今日推荐',
            'HR三支柱模型（尤里奇）—— 从事务到战略的转型路径',
            'HR战略合作伙伴(HRBP) + 专业化中心(CoE) + 共享服务(SSC)，实现HR价值重构。',
            '💡 对300人公司的建议：至少要有"业务触角"(BP意识)+"专业深耕"(CoE思维)，SSC可适度外包',
            'SHRM资源中心', 'https://www.shrm.org/home'
        ) + build_news('bg-blue', 'AI学习', '今日推荐',
            "Coursera《AI For Everyone》—— 理解AI，不写代码",
            '吴恩达出品，4小时可完成，系统理解AI能做什么、不能做什么，以及AI对商业的影响。',
            '💡 HR负责人学完能用：评估AI供应商方案、制定公司AI+HR路线图、与技术团队同频对话',
            'Coursera课程链接', 'https://www.coursera.org/learn/ai-for-everyone'
        )
    )

    # 常规section
    sections = (
        build_section('🌏', 'bg-blue', '全球HR动态', '2条', 'hr-global', hr_global) +
        build_section('🇨🇳', 'bg-orange', '中国HR动态', '2条', 'hr-china', hr_china) +
        build_section('💹', 'bg-teal', '金融科技', '2条', 'fintech', fintech) +
        build_section('🔐', 'bg-purple', '信贷风控', '2条', 'risk', risk) +
        comp_pure +
        comp_big +
        learn
    )

    html = HTML_TEMPLATE.replace('{{WEEKDAY}}', weekday)
    html = html.replace('{{DATE_SHORT}}', date_short)
    html = html.replace('{{HIGHLIGHTS}}', highlights)
    html = html.replace('{{SECTIONS}}', sections)
    html = html.replace('{{DATE_FULL}}', date_full)

    return html

def send_email(html_content, subject):
    try:
        yag = yagmail.SMTP(
            user=SENDER_EMAIL,
            password=SENDER_AUTH_CODE,
            host='smtp.163.com',
            port=465
        )
        yag.send(to=RECIPIENT_EMAIL, subject=subject, contents=[html_content])
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("=" * 50)
    print("[Hahaha Daily Newsletter Generator]")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("\n[+] Generating today's newsletter...")
    html = generate_newsletter()

    # 保存到 newsletter.html
    with open(NEWSLETTER_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[+] Saved to: {NEWSLETTER_FILE}")

    # 发送邮件（邮件正文说明刷新链接即可）
    weekday = get_weekday_cn()
    date_short = datetime.now().strftime("%m月%d日")
    subject = f"[哈哈] HR科技金融日报 | {date_short} {weekday}"

    print(f"\n[+] Sending notification email to {RECIPIENT_EMAIL}...")
    success = send_email(html, subject)

    if success:
        print("\n[SUCCESS] Done!")
        print(f"[INFO] Refresh: {NEWSLETTER_FILE}")
    else:
        print("\n[ERROR] Email sending failed")

    return success

if __name__ == '__main__':
    main()
