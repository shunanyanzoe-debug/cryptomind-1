import pandas as pd, numpy as np, os, joblib, ast
from pathlib import Path
from collections import Counter
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error
from typing import Literal, Tuple
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
############改变小数
import matplotlib.ticker as mtick

import matplotlib
matplotlib.use('Agg')



# 用于滚动预测（rolling window forecasting）的函数，目标是：
# 每周重新训练模型；输出下周收益的预测值（ret_lead1）；并将预测结果和模型保存下来。
def rolling_weekly_prediction(df: pd.DataFrame, save_dir: Path, roll_window: int = 52):
# 模型组合：
# 使用了两种模型：ElasticNet：线性模型带有 L1 和 L2 正则项，适合高维特征；
#              ExtraTreesRegressor：一种随机森林变种，适合非线性关系。
# 每个模型配备了超参数网格，用于后续 GridSearchCV。
    model_configs = {
        "enet": {
            "estimator": ElasticNet(max_iter=10000, random_state=42),
            "param_grid": {
                "model__alpha": [0.01, 0.1, 1.0, 10.0],
                "model__l1_ratio": [0.1, 0.5, 0.9]
            }
        },
        "extra": {
            "estimator": ExtraTreesRegressor(random_state=42),
            "param_grid": {
                "model__n_estimators": [100, 200],
                "model__max_depth": [5, 10],
                "model__max_features": ["sqrt", "log2"]
            }
        }
    }

# ✅ 自动构造三类特征集："all"：所有非排除列（全部特征）
#                     "market"：技术面因子，如动量、波动率、成交量冲击
#                     "sentiment"：仅含情绪类特征，如 compound, extremely_negative 等

    def get_feature_sets(df: pd.DataFrame):
        exclude_cols = ["date", "symbol", "return", "ret_lead1", "open", "high", "low", "close"]
        market_features = [col for col in df.columns if any(k in col for k in ["momentum", "volatility", "usd_volume", "base_volume", "return_sign", "long_candle", "strev"])]
        sentiment_features = [col for col in df.columns if any(k in col for k in ["compound", "extremely"])]
        all_features = [col for col in df.columns if col not in exclude_cols]
        return {
            "all": all_features,
            "market": market_features,
            "sentiment": sentiment_features
        }

    # ✅ 修复点①：不要一开始就 dropna（否则会误删很多币的最后一周）
#     构造“未来一周的收益率”（作为 y 标签）
# ⚠️ 注意：这里的 shift(-1) 假设数据按周排好序（已groupby）
    df = df.copy()
    df["ret_lead1"] = df.groupby("symbol")["return"].shift(-1)
    # ❌ 原来的做法（我们删除了这句）：
    # df = df.dropna(subset=["ret_lead1"])
    weeks = sorted(df["date"].unique())
    feature_sets = get_feature_sets(df)

    for tag, feature_set in feature_sets.items():
        for model_key, config in model_configs.items():

            # ==== 全样本调参 ====
            # ✅ 只在调参用的数据中 dropna
            # 使用全样本（非滚动）调参：
            # 建立 Pipeline: 标准化 + 模型
            # 使用 GridSearchCV：3折交叉验证寻找最佳参数
            # SimpleImputer: 用均值填补缺失值，避免模型报错
            # 得到： best_estimator: 拟合后的最佳模型
            #       best_param_dict: 最优参数组合
            # 非常合理：先全样本选出模型结构，后续滚动窗口中复用。
            df_train_all = df.dropna(subset=["ret_lead1"])
            X_full = df_train_all[feature_set].copy()
            y_full = df_train_all["ret_lead1"].copy()
            imputer = SimpleImputer(strategy="mean")
            X_full_imputed = imputer.fit_transform(X_full)
            y_full_clean = y_full.fillna(0)

            pipe = Pipeline([
                ("scale", StandardScaler()),
                ("model", config["estimator"])
            ])
            grid = GridSearchCV(pipe, config["param_grid"], scoring="neg_mean_squared_error", cv=3, n_jobs=-1)
            grid.fit(X_full_imputed, y_full_clean)

            best_estimator = grid.best_estimator_
            best_param_dict = grid.best_params_

            model_save_dir = Path("models") / f"{model_key}_{tag}"
            model_save_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(best_estimator, model_save_dir / "final_model.pkl")
            with open(model_save_dir / "best_params.txt", "w") as f:
                f.write(str(best_param_dict))

            all_results, all_y_true, all_y_pred = [], [], []

            for i in range(roll_window, len(weeks) - 1):
                train_weeks = weeks[i - roll_window:i]
                test_week = weeks[i]

                # ✅ 修复点②：训练集 dropna（不能有空label），但测试集不 dropna（即使 y_true 是 NaN 也要保留）
                df_train = df[df["date"].isin(train_weeks)].dropna(subset=["ret_lead1"])
                df_test = df[df["date"] == test_week]

                X_test = df_test[feature_set].copy()
                y_test = df_test["ret_lead1"].copy()
                X_test_imputed = imputer.transform(X_test)
                y_pred = best_estimator.predict(X_test_imputed)

                result = df_test[["date", "symbol"]].copy()
                result["y_pred"] = y_pred
                result["y_true"] = y_test.values
                result["model_tag"] = f"{model_key}_{tag}"
                result["rank"] = result.groupby("date")["y_pred"].rank(ascending=False, method="first")
                all_results.append(result)

                all_y_true.extend(y_test.dropna().values)
                all_y_pred.extend([p for t, p in zip(y_test, y_pred) if not pd.isna(t)])

            r2 = r2_score(all_y_true, all_y_pred)
            mse = mean_squared_error(all_y_true, all_y_pred)
            print(f"R²: {r2:.4f} | MSE: {mse:.6f}")

            final_df = pd.concat(all_results, ignore_index=True)
            out_path = save_dir / f"pred_{model_key}_{tag}.csv"
            final_df.to_csv(out_path, index=False)
            print(f"save to: {out_path}")
#########################################
#上面这个函数：
#“基于滚动窗口训练和预测的方式，用机器学习模型预测下周加密货币收益，并输出预测值用于后续构建排序策略与投资组合。”

##########################################
#构建一个滚动的等权重基准策略（Equal-Weight Baseline Strategy）用于对比你主模型的表现。它是你整个项目中的“控制组”或“对照组”。
#你构建了一个 不依赖任何模型预测 的基准策略：每周等权投资于所有或成交量最高的币种，并计算其收益和累计收益率，以评估主动策略是否真的更优。
def rolling_baseline_equal_weight(df_merged: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    df = df_merged.copy()

    # 构造 next week return（ret_lead1）
    df["ret_lead1"] = df.groupby("symbol")["return"].shift(-1)       # ret_lead1: 下一周收益，作为未来持有收益
    df.dropna(subset=["ret_lead1"], inplace=True)                 # dropna：移除最后一周没法计算收益的数据

    all_weeks = sorted(df["date"].unique())       # 获得所有独立的周度时间戳
    results = []        # results 用于存储每周策略表现


    for i in range(len(all_weeks) - 1):
        this_week = all_weeks[i]
        next_week = all_weeks[i + 1]         # 第 i 周买入，第 i+1 周计算收益

        df_this_week = df[df["date"] == this_week]
        df_next_week = df[df["date"] == next_week][["symbol", "ret_lead1"]]            # 取出本周可投资的币种 & 下周的实际收益

        # 选取币种（等权持有）
        if top_n is not None:
            selected = df_this_week.sort_values("usd_volume", ascending=False).head(top_n)["symbol"]
        else:
            selected = df_this_week["symbol"]

        # 每个币都分配相同权重
        portfolio = pd.DataFrame({"symbol": selected})
        portfolio["weight"] = 1 / len(portfolio)

        # 与下周收益合并后计算等权组合收益（加权求和）
        merged = pd.merge(portfolio, df_next_week, on="symbol", how="left").dropna(subset=["ret_lead1"])
        merged["weighted_return"] = merged["weight"] * merged["ret_lead1"]
        ret = merged["weighted_return"].sum()

        # 记录每周表现，存储每周收益（将作为基准回测结果）
        results.append({"date": next_week, "baseline_return": ret})

    # 构建回测结果 DataFrame（计算累计收益（Compound Return）、cumprod() 是标准的累计收益计算方法）
    results_df = pd.DataFrame(results)
    results_df["cum_return"] = (1 + results_df["baseline_return"]).cumprod()

    # 计算指标
    #输出关键绩效指标（平均收益、波动率（标准差）、夏普比率（单位风险下的超额回报））
    mean_return = results_df["baseline_return"].mean()
    vol = results_df["baseline_return"].std()
    sharpe = mean_return / vol if vol != 0 else float("nan")

    print(f"\n Equal-Weight Baseline")
    print(f"Average Return: {mean_return:.4f}")
    print(f"Volatility:     {vol:.4f}")
    print(f"Sharpe Ratio:   {sharpe:.4f}")

    # 可视化累计收益
    ###########################
    results_df["date"] = pd.to_datetime(results_df["date"])
    ##########################
    plt.figure(figsize=(10, 4))
    plt.plot(results_df["date"], results_df["cum_return"], label="Equal-Weight Baseline", linewidth=2)
    plt.title(f"Cumulative Return of Equal-Weight Baseline (top_n={top_n if top_n else 'ALL'})")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    #plt.xticks(rotation=30)
    #################################
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # 每3个月显示1个
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    #################################
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.legend()
    plt.show()

    return results_df


####################################################
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Literal
import matplotlib.dates as mdates
# 你构建了一个系统化的回测框架，用于比较三种策略：并输出： 累计收益曲线、 Sharpe比率、波动率、平均收益、对应柱状图 + CSV 结果
# enet long-short（主动多空策略）
# 使用 ElasticNet 模型的预测结果 y_pred 排序币种；每周买入预测收益最高的前 N 个币（long）；同时做空预测最差的前 N 个币（short）；
# 权重相等，构成市场中性组合。在涨跌市中都寻找相对表现最好的币种，实现 alpha 捕捉 + 风险对冲。

# extra long-short（另一模型的主动多空）
# 与 enet 策略相同逻辑，只是预测模型换为 ExtraTreesRegressor；提供非线性建模对比，测试模型选择对策略表现的影响。
# 验证使用非线性模型是否在加密货币市场捕捉收益更有效。
#
# enet_EW（模型选币但不做空，只做等权重多头）
# 仍然用 ElasticNet 模型选出预测最强的前 N 个币；但不做空低预测收益的币；简单持有多头组合，平均分配资金。
# 作为中间策略：结合模型选币能力，但避免做空带来的额外风险。

def rolling_backtest_with_visuals_combined(
    pred_enet_df: pd.DataFrame,
    pred_extra_df: pd.DataFrame,
    strategy_tag: Literal["all", "market", "sentiment"],
    top_n: int,
    data_dir: Path,
    fig_dir: Path,
    pred_col: str = "y_pred"
):
# 这个函数完成的是 策略构建 + 回测 + 可视化 + 评估汇总，支持：不同模型预测结果（如 ElasticNet 和 ExtraTrees）；
# 不同特征集（如 all、market、sentiment）；可切换预测列（如 y_pred, y_pred_ema 等）

    # 获取预测时间轴；为每种策略准备列表收集周度收益。
    all_weeks = sorted(pred_enet_df["date"].unique())
    enet_results, extra_results, enet_EW_results = [], [], []

    # 每轮取出当前周 (this_week) 的预测作为选币依据，取下一周的真实收益作为回测结果。
    for i in range(len(all_weeks) - 1):
        this_week = all_weeks[i]
        next_week = all_weeks[i + 1]

        df_enet = pred_enet_df[pred_enet_df["date"] == this_week]
        df_extra = pred_extra_df[pred_extra_df["date"] == this_week]
        df_next = pred_enet_df[pred_enet_df["date"] == next_week][["symbol", "y_true"]]

        # Long-only：只传入 long_syms，平均分配正权重；Long-Short：对 long 和 short 分别赋正负权重（对冲型策略）；
        # 若只传 long，即代表方向性押注（如 enet_EW）；若传入 long + short，表示市场中性策略（如 enet、extra）
        def compute_portfolio_return(df, long_syms, short_syms=None):
            if short_syms is None:
                portfolio = pd.DataFrame({"symbol": list(long_syms)})
                portfolio["weight"] = 1 / len(portfolio)
            else:
                long_df = pd.DataFrame({"symbol": list(long_syms)})
                short_df = pd.DataFrame({"symbol": list(short_syms)})
                long_df["weight"] = 1 / len(long_df)
                short_df["weight"] = -1 / len(short_df)
                portfolio = pd.concat([long_df, short_df], ignore_index=True)

            merged = pd.merge(portfolio, df_next, on="symbol", how="left").dropna()
            merged["weighted_return"] = merged["weight"] * merged["y_true"]
            return merged["weighted_return"].sum()

        # 策略构建
        # 获取多空组合（排序 + 分组）：top_n: 选出预测最高/最低的币种；实现 基于模型预测的排序投资策略
        enet_top = df_enet.sort_values(pred_col, ascending=False).head(top_n)["symbol"]
        enet_bot = df_enet.sort_values(pred_col, ascending=True).head(top_n)["symbol"]
        extra_top = df_extra.sort_values(pred_col, ascending=False).head(top_n)["symbol"]
        extra_bot = df_extra.sort_values(pred_col, ascending=True).head(top_n)["symbol"]


        # baseline: 等权多头 enet top20
        enet_EW_ret = compute_portfolio_return(df_enet, enet_top)
        enet_EW_results.append({"date": next_week, "return": enet_EW_ret})

        # enet long-short
        enet_ret = compute_portfolio_return(df_enet, enet_top, enet_bot)
        enet_results.append({"date": next_week, "return": enet_ret})

        # extra long-short
        extra_ret = compute_portfolio_return(df_extra, extra_top, extra_bot)
        extra_results.append({"date": next_week, "return": extra_ret})

    def build_df(results, label):
        df = pd.DataFrame(results)
        df["cum_return"] = (1 + df["return"]).cumprod()
        df["strategy"] = label
        return df

    df_enet = build_df(enet_results, "enet")
    df_extra = build_df(extra_results, "extra")
    df_base = build_df(enet_EW_results, "enet_EW")

    df_all = pd.concat([df_enet, df_extra, df_base], ignore_index=True)
    df_all["date"] = pd.to_datetime(df_all["date"])
    df_all.to_csv(data_dir / f"rolling_backtest_{strategy_tag}.csv", index=False)

    # === 绘制累计收益图 ===
    plt.figure(figsize=(12, 5))
    for strategy, group in df_all.groupby("strategy"):
        plt.plot(group["date"], group["cum_return"], label=strategy, linewidth=2)
    plt.title(f"Cumulative Return Comparison: {strategy_tag}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    ######################################################################
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))

    ######################################################################
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(fig_dir / f"cum_return_comparison_{strategy_tag}.png")
    plt.close()


    # === 输出柱状图（Sharpe, Volatility, Mean Return）===
    metrics = []
    for label, df in [("enet", df_enet), ("extra", df_extra), ("enet_EW", df_base)]:
        ret = df["return"]
        metrics.append({
            "strategy": label,
            "sharpe": ret.mean() / ret.std(),
            "volatility": ret.std(),
            "mean_return": ret.mean()
        })
    metric_df = pd.DataFrame(metrics)
    metric_df.to_csv(data_dir / f"metrics_{strategy_tag}.csv", index=False)

    for col in ["sharpe", "volatility", "mean_return"]:
        plt.figure(figsize=(8, 4))
        bars = plt.bar(metric_df["strategy"], metric_df[col], color=["green", "orange", "gray"])
        plt.title(f"{col.title()} Comparison: {strategy_tag}")
        plt.ylabel(col.title())
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.3f}", ha="center", va="bottom", fontsize=10)
        plt.tight_layout()
        plt.savefig(fig_dir / f"{col}_bar_{strategy_tag}.png")
        plt.close()




