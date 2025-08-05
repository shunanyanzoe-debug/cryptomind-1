# import React, { useState } from "react";
# import "./styles.css";
#
# const App = () => {
#   const [activeCategory, setActiveCategory] = useState(
#     "Cumulative Return Comparison"
#   );
#   const [activeTab, setActiveTab] = useState("All");
#   const [userQuestion, setUserQuestion] = useState("");
#   const [aiAnswer, setAiAnswer] = useState("");
#   const [weights, setWeights] = useState([]);
#   const [loading, setLoading] = useState(false);
#   const [error, setError] = useState("");
#
#   const [topN, setTopN] = useState(10); // 默认展示前10个
#
#   const images = {
#     "Cumulative Return Comparison": {
#       All: "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/cum_return_comparison_all_nnpmce.png",
#       Market:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/cum_return_comparison_market_jcptak.png",
#       Sentiment:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/cum_return_comparison_sentiment_tkkmmk.png",
#     },
#     "Mean Return Bar Chart": {
#       All: "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/mean_return_bar_all_sgl1oh.png",
#       Market:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/mean_return_bar_market_iqlzrq.png",
#       Sentiment:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/mean_return_bar_sentiment_p1bwzz.png",
#     },
#     "Sharpe Ratio": {
#       All: "https://res.cloudinary.com/didecgs0o/image/upload/v1754331829/sharpe_bar_all_iyxpty.png",
#       Market:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331830/sharpe_bar_market_jye7rb.png",
#       Sentiment:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331830/sharpe_bar_sentiment_cjkybj.png",
#     },
#     Volatility: {
#       All: "https://res.cloudinary.com/didecgs0o/image/upload/v1754331830/volatility_bar_all_ahqcyx.png",
#       Market:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331830/volatility_bar_market_olrjjv.png",
#       Sentiment:
#         "https://res.cloudinary.com/didecgs0o/image/upload/v1754331841/volatility_bar_sentiment_wwqaez.png",
#     },
#   };
#
#   const descriptions = {
#     "Cumulative Return Comparison":
#       "This chart compares cumulative returns across strategies.",
#     "Mean Return Bar Chart":
#       "This chart shows the average weekly return per strategy.",
#     "Sharpe Ratio":
#       "This chart compares risk-adjusted return using the Sharpe ratio.",
#     Volatility: "This chart presents weekly volatility per strategy.",
#   };
#
#   const financeContent = [
#     {
#       title: "What is Volatility?",
#       content:
#         "Volatility measures the degree of variation in asset prices over time. Higher volatility means higher risk.",
#     },
#     {
#       title: "What is Sharpe Ratio?",
#       content:
#         "Sharpe Ratio evaluates the risk-adjusted return of an investment. A higher ratio indicates better return per unit of risk.",
#     },
#     {
#       title: "What is a Long-Short Strategy?",
#       content:
#         "This strategy involves taking long positions in undervalued assets and short positions in overvalued ones.",
#     },
#     {
#       title: "What is a Portfolio?",
#       content:
#         "A portfolio is a group of financial assets held by an investor. Diversifying a portfolio helps manage risk.",
#     },
#
#     {
#       title: "What is Cryptocurrency?",
#       content:
#         "Cryptocurrency is a digital asset built on blockchain technology that uses cryptography for secure transactions. Examples include Bitcoin (BTC), Ethereum (ETH), and Solana (SOL).",
#     },
#     {
#       title: "What is a Portfolio?",
#       content:
#         "A portfolio is a group of financial assets held by an investor. Diversifying a portfolio helps manage risk.",
#     },
#     {
#       title: "What is a Systematic Strategy?",
#       content:
#         "A systematic strategy is a rule-based investment approach that relies on data, models, and automation rather than human judgment.",
#     },
#     {
#       title: "What is Momentum Factor?",
#       content:
#         "Momentum is the tendency of assets that have performed well in the past to continue performing well in the future. It is often used as a ranking signal in portfolio construction.",
#     },
#     {
#       title: "What is Volatility?",
#       content:
#         "Volatility measures how much the price of an asset fluctuates. Higher volatility means higher potential risk and return.",
#     },
#     {
#       title: "What is Sharpe Ratio?",
#       content:
#         "Sharpe Ratio is a measure of risk-adjusted return. It is calculated as excess return divided by volatility. A higher Sharpe Ratio indicates better risk-adjusted performance.",
#     },
#     {
#       title: "What is Sentiment Analysis?",
#       content:
#         "Sentiment analysis uses natural language processing to determine the emotional tone behind news articles or social media posts. In crypto, sentiment scores can help predict short-term price moves.",
#     },
#     {
#       title: "What is Risk Parity?",
#       content:
#         "Risk Parity is a portfolio allocation strategy where each asset contributes equally to the overall risk, aiming for better diversification and stability.",
#     },
#     {
#       title: "How is Machine Learning Used in Crypto Investing?",
#       content:
#         "Machine learning models like ElasticNet and Random Forest are used to predict asset returns and rank cryptocurrencies based on factors like momentum, volatility, and sentiment.",
#     },
#     {
#       title: "What Makes Crypto Markets Unique?",
#       content:
#         "Crypto markets operate 24/7, are highly volatile, and are influenced heavily by retail sentiment and global news—making them ideal for systematic strategies.",
#     },
#   ];
#
#   const handleAIQuery = async () => {
#     if (!userQuestion) return;
#     setAiAnswer("⏳ Thinking...");
#     try {
#       const response = await fetch("http://127.0.0.1:5000/api/ask", {
#         method: "POST",
#         headers: { "Content-Type": "application/json" },
#         body: JSON.stringify({ question: userQuestion }),
#       });
#       const data = await response.json();
#       setAiAnswer(data.answer);
#     } catch (err) {
#       setAiAnswer("❌ Failed to fetch AI answer: " + err.message);
#     }
#   };
#
#   const fetchWeights = async () => {
#     setLoading(true);
#     setError("");
#     try {
#       const response = await fetch(
#         `http://127.0.0.1:5000/api/generate-weights?top_n=${topN}`
#       );
#
#       if (!response.ok) {
#         throw new Error("Failed to fetch weights");
#       }
#       const data = await response.json();
#       setWeights(data); // Flask returns a list of weights
#     } catch (err) {
#       setError("Error fetching weights: " + err.message);
#     } finally {
#       setLoading(false);
#     }
#   };
#
#   return (
#     <div className="app">
#       <div className="sidebar">
#         <h2>CryptoMind </h2>
#         {Object.keys(images).map((category) => (
#           <button key={category} onClick={() => setActiveCategory(category)}>
#             {category}
#           </button>
#         ))}
#         <button onClick={() => setActiveCategory("Strategy Intro")}>
#           Strategy Intro
#         </button>
#
#         <label className="dropdown-label-tech">
#           Show Top N assets:
#           <select
#             className="dropdown-select"
#             value={topN}
#             onChange={(e) => setTopN(Number(e.target.value))}
#           >
#             {[5, 10, 15, 20].map((n) => (
#               <option key={n} value={n}>
#                 {n}
#               </option>
#             ))}
#           </select>
#         </label>
#
#         <button onClick={() => setActiveCategory("Finance Knowledge")}>
#           Finance Knowledge
#         </button>
#         <button onClick={() => setActiveCategory("Ask AI")}>AI Q&A</button>
#         <button onClick={fetchWeights}>Generate Portfolio Weights</button>
#       </div>
#
#       <div className="main">
#         <div className="risk-warning">
#           📢 <strong>Disclaimer:</strong> The strategies and backtesting results
#           shown on this platform are for educational and informational purposes
#           only. Investing involves risk. Please make decisions carefully and at
#           your own discretion.
#         </div>
#         <div className="tabs">
#           {["All", "Market", "Sentiment"].map((tab) => (
#             <button
#               key={tab}
#               onClick={() => setActiveTab(tab)}
#               className={activeTab === tab ? "active" : ""}
#             >
#               {tab}
#             </button>
#           ))}
#         </div>
#
#         {activeCategory === "Ask AI" ? (
#           <div className="ai-box">
#             <h3>🤖 Ask the Crypto AI</h3>
#             <input
#               type="text"
#               value={userQuestion}
#               onChange={(e) => setUserQuestion(e.target.value)}
#               placeholder="Ask a question like 'Which strategy is best?'"
#             />
#             <button onClick={handleAIQuery}>Ask</button>
#             <p className="ai-answer">{aiAnswer}</p>
#           </div>
#         ) : activeCategory === "Strategy Intro" ? (
#           <div className="strategy-explanation">
#             <h3>Strategy Explanation</h3>
#             <ul>
#               <li>
#                 <strong>enet</strong>: Elastic Net regression model combining L1
#                 & L2 penalties.
#               </li>
#               <li>
#                 <strong>extra</strong>: Extra Trees, a non-linear ensemble
#                 method.
#               </li>
#               <li>
#                 <strong>enet_EW</strong>: Elastic Net with equal-weight
#                 long-only allocation.
#               </li>
#             </ul>
#           </div>
#         ) : activeCategory === "Finance Knowledge" ? (
#           <div className="finance-knowledge">
#             <h3>📘 Financial Knowledge</h3>
#             <ul>
#               {financeContent.map((item, index) => (
#                 <li key={index}>
#                   <strong>{item.title}</strong>
#                   <p>{item.content}</p>
#                 </li>
#               ))}
#             </ul>
#           </div>
#         ) : (
#           <div className="chart">
#             <img
#               src={images[activeCategory][activeTab]}
#               alt={`${activeCategory} - ${activeTab}`}
#             />
#             <p>{descriptions[activeCategory]}</p>
#             <strong className="strategy-label">Best Strategy:</strong>
#             <span className="strategy-name"> extra</span>
#           </div>
#         )}
#
#         {loading && <p>Loading weights...</p>}
#         {error && <p style={{ color: "red" }}>{error}</p>}
#
#         {Array.isArray(weights) && weights.length > 0 && (
#           <div className="weights">
#             <h3>Latest Portfolio Weights</h3>
#             <ul>
#               {weights.map((item, index) => (
#                 <li key={index}>
#                   {item.symbol}: {item.predicted_return.toFixed(4)}
#                 </li>
#               ))}
#             </ul>
#           </div>
#         )}
#       </div>
#     </div>
#   );
# };
#
# export default App;
