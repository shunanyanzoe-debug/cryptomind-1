from pathlib import Path
import pandas as pd
from stage3 import (
    rolling_baseline_equal_weight,
    rolling_weekly_prediction,
    rolling_backtest_with_visuals_combined
)
#from crypto_project_pipeline import build_week_dirs  # 你自己的目录构建函数


def main():
    # 设置参数
    week_folder = "."
    results_folder = "stage3-4_result"
    top_n = 20

    # 构建目录结构
    data_dir = Path(week_folder) / results_folder / "data"
    fig_dir = Path(week_folder) / results_folder / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    # === Step 1: 加载合并后的 df_merged（包含 return 和 symbol）
    df = pd.read_csv("stage_2_merged_data.csv")

    # === Step 2: 执行 Equal-Weight Baseline 回测
    baseline_df = rolling_baseline_equal_weight(df_merged=df, top_n=top_n)
    baseline_df.to_csv(data_dir / "baseline_equal_weight.csv", index=False)

    # === Step 3: 执行滚动预测（会保存多个预测结果 CSV 文件）
    rolling_weekly_prediction(df=df, save_dir=data_dir)

    # === Step 4: 对三种特征集进行回测与可视化
    for tag in ["all", "market", "sentiment"]:
        print(f"------- Doing {tag} --------")
        pred_enet_path = data_dir / f"pred_enet_{tag}.csv"
        pred_extra_path = data_dir / f"pred_extra_{tag}.csv"

        # 加载预测结果
        pred_enet_df = pd.read_csv(pred_enet_path)
        pred_extra_df = pd.read_csv(pred_extra_path)

        # 执行融合策略回测与可视化
        rolling_backtest_with_visuals_combined(
            pred_enet_df=pred_enet_df,
            pred_extra_df=pred_extra_df,
            strategy_tag=tag,
            top_n=top_n,
            data_dir=data_dir,
            fig_dir=fig_dir
        )



# ✅ 加这一段用于修复 multiprocessing 报错
if __name__ == "__main__":
    import multiprocessing as mp
    mp.set_start_method("spawn", force=True)
    main()



