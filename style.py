# /* 全局字体与页面背景 */
# body {
#   margin: 0;
#   font-family: "Segoe UI", "Roboto Slab", Georgia, serif;
#   background-color: #0e1a2b;
#   color: #f5f5f5;
# }
#
# .App {
#   text-align: center;
# }
#
# /* 主体布局 */
# .app {
#   display: flex;
#   height: 100vh;
#   background-color: #0e1a2b;
#   color: #f5f5f5;
# }
#
# /* 侧边栏样式 */
# .sidebar {
#   width: 240px;
#   background-color: #101e33;
#   padding: 24px;
#   box-shadow: 2px 0 8px rgba(0, 0, 0, 0.4);
#   display: flex;
#   flex-direction: column;
#   align-items: stretch;
# }
#
# .sidebar h2 {
#   margin-top: 0;
#   font-size: 22px;
#   color: #f5c56b;
#   margin-bottom: 20px;
# }
#
# .sidebar button {
#   padding: 12px;
#   margin-bottom: 10px;
#   border: 1px solid #f5c56b;
#   border-radius: 6px;
#   background-color: transparent;
#   color: #f5c56b;
#   cursor: pointer;
#   font-weight: 500;
#   transition: background-color 0.2s ease, color 0.2s ease;
# }
#
# .sidebar button:hover,
# .sidebar button.active {
#   background-color: #f5c56b;
#   color: #101e33;
# }
#
# /* 主内容区域 */
# .main {
#   flex: 1;
#   padding: 30px;
#   overflow-y: auto;
# }
#
# /* 顶部切换标签 */
# .tabs {
#   margin-bottom: 24px;
# }
#
# .tabs button {
#   padding: 10px 18px;
#   margin-right: 12px;
#   background-color: #142b44;
#   color: #f5c56b;
#   border: 1px solid #f5c56b;
#   border-radius: 5px;
#   font-weight: 500;
#   cursor: pointer;
#   transition: background-color 0.2s ease, color 0.2s ease;
# }
#
# .tabs button.active,
# .tabs button:hover {
#   background-color: #f5c56b;
#   color: #101e33;
# }
#
# /* 图片展示区 */
# .image-container {
#   text-align: center;
# }
#
# .image-container img {
#   max-width: 90%;
#   border-radius: 10px;
#   border: 2px solid #f5c56b; /* 柔金色边框 */
#   box-shadow: 0 0 10px rgba(245, 197, 107, 0.3); /* 金色发光边缘 */
#   margin-bottom: 12px;
# }
#
# /* 金融基础知识区块 */
# .finance-knowledge {
#   padding: 20px;
#   background-color: #0d1b2a;
#   border-radius: 10px;
#   color: #f5c56b;
#   font-size: 16px;
#   line-height: 1.6;
#   box-shadow: 0 0 10px rgba(245, 197, 107, 0.15);
# }
#
# .finance-knowledge h3 {
#   color: #f7d27d;
#   font-size: 20px;
#   margin-bottom: 12px;
# }
#
# .finance-knowledge ul {
#   list-style-type: none;
#   padding-left: 0;
# }
#
# .finance-knowledge li {
#   margin-bottom: 16px;
# }
#
# .finance-knowledge li strong {
#   display: block;
#   font-size: 17px;
#   margin-bottom: 4px;
#   color: #f5c56b;
# }
#
# /* 风险提示框 */
# .risk-warning {
#   background-color: #fff3cd;
#   color: #856404;
#   border: 1px solid #ffeeba;
#   padding: 12px 16px;
#   margin-bottom: 24px;
#   border-radius: 6px;
#   font-size: 14px;
#   font-weight: 500;
#   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
# }
#
# select {
#   background-color: #0d1b2a;
#   color: #f5c56b;
#   border: 1px solid #f5c56b;
#   padding: 6px 12px;
#   border-radius: 5px;
#   font-size: 14px;
#   font-weight: 500;
#   outline: none;
#   appearance: none;
#   -webkit-appearance: none;
#   -moz-appearance: none;
#   cursor: pointer;
# }
#
# select:focus {
#   border-color: #f7d27d;
#   box-shadow: 0 0 4px rgba(245, 197, 107, 0.5);
# }
#
# select {
#   background-image: url('data:image/svg+xml;utf8,<svg fill="%23f5c56b" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
#   background-repeat: no-repeat;
#   background-position: right 10px center;
#   background-size: 14px;
#   padding-right: 28px;
# }
# select:hover {
#   background-color: #1f3c5c;
#   color: #fff;
# }
#
# .image-caption {
#   color: #f5c56b; /* 柔金色 */
#   font-size: 14px;
#   font-weight: 400;
#   font-style: italic;
#   margin-top: -4px;
#   line-height: 1.5;
#   text-align: center;
#   max-width: 90%;
#   margin-left: auto;
#   margin-right: auto;
# }
#
# .strategy-explanation {
#   color: #f5c56b;
#   font-size: 16px;
#   line-height: 1.6;
#   border: 1px solid #f5c56b;
#   border-radius: 8px;
#   padding: 20px;
#   background-color: #101e33;
#   box-shadow: 0 0 10px rgba(245, 197, 107, 0.15);
# }
#
# .strategy-explanation h3 {
#   color: #f7d27d;
#   margin-bottom: 12px;
# }
#
# .strategy-explanation ul {
#   list-style-type: disc;
#   padding-left: 20px;
# }
#
# .strategy-explanation li {
#   margin-bottom: 10px;
# }
#
# .strategy-explanation li strong {
#   color: #ffd87c;
# }
#
# .ai-box {
#   background-color: #e6e6e6; /* 亮灰色背景，类金属质感 */
#   color: #1a1a1a; /* 深灰字体 */
#   padding: 20px;
#   border-radius: 10px;
#   box-shadow: 0 0 10px rgba(200, 200, 200, 0.2);
#   max-width: 600px;
#   margin: 0 auto;
#   font-family: "Segoe UI", Roboto, sans-serif;
# }
#
# .ai-box h3 {
#   margin-bottom: 12px;
#   color: #2b2d42; /* 深蓝黑字体 */
# }
#
# .ai-box input[type="text"] {
#   width: 70%;
#   padding: 10px;
#   border: 1px solid #ccc;
#   border-radius: 6px;
#   background-color: rgba(255, 255, 255, 0.85);
#   color: #222;
#   margin-right: 10px;
#   box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
#   font-size: 14px;
# }
#
# .ai-box button {
#   padding: 10px 16px;
#   background-color: #2b2d42;
#   color: #f5c56b;
#   border: none;
#   border-radius: 6px;
#   font-weight: bold;
#   cursor: pointer;
#   transition: background-color 0.2s ease;
#   box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
# }
#
# .ai-box button:hover {
#   background-color: #3e4364;
# }
#
# .ai-answer {
#   margin-top: 15px;
#   font-style: italic;
#   color: #2b2d42;
# }
#
# .chart p {
#   color: #a7b6c2; /* 中性偏蓝的专业灰色，更和谐 */
#   font-size: 15px;
#   margin-top: 12px;
# }
#
# .chart strong {
#   color: #f5c56b; /* 柔和金色，用于强调策略名称 */
#   font-weight: 600;
#   display: inline-block;
#   margin-top: 6px;
# }
#
# .strategy-label {
#   color: #f5c56b; /* 金色标签 */
#   font-weight: 700;
#   font-size: 17px;
# }
#
# .strategy-name {
#   color: #f1f1f1; /* 白灰色，更柔和 */
#   font-weight: 500;
#   font-size: 16px;
# }
#
# .dropdown-label-tech {
#   color: #7fdbff; /* 冰蓝 Label */
#   font-weight: 600;
#   font-size: 15px;
#   display: block;
#   margin: 16px 0 10px 0;
# }
#
# .dropdown-select-tech {
#   background-color: #0f1b2d; /* 深灰蓝背景 */
#   color: #aeeeee; /* 字体换为更亮的冰蓝 */
#   border: 1px solid #39cccc; /* 青蓝边框 */
#   border-radius: 6px;
#   padding: 6px 12px;
#   margin-left: 8px;
#   font-size: 14px;
#   font-weight: 500;
#   outline: none;
#   appearance: none;
#   cursor: pointer;
#   transition: all 0.3s ease;
# }
#
# .dropdown-select-tech:hover {
#   border-color: #7fdbff; /* hover 更亮 */
#   background-color: #1e2a3b; /* hover 背景略亮 */
# }
#
# .dropdown-label-tech {
#   color: #f4e2c9; /* 高级蓝灰 */
#   font-size: 15px;
#   font-weight: 500;
#   margin: 16px 0 10px 0;
#   display: flex;
#   align-items: center;
# }


# https://ntcsg9.csb.app/