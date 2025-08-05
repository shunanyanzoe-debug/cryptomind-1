# # flask_api.py
# from flask import Flask, jsonify
# from flask_cors import CORS
# from pathlib import Path
# import pandas as pd
#
# # ✅ 你的 stage3 策略主函数（建议是 run_stage3.py 中的 main 函数）
# from run_stage3 import main
#
# app = Flask(__name__)
# CORS(app)  # 允许前端跨域调用这个API
#
# @app.route("/api/generate-weights", methods=["GET"])
# def generate_weights():
#     try:
#         # ✅ 执行回测与预测（会输出 CSV 文件）
#         main()
#
#         # ✅ 读取最新一周的推荐投资组合（来自 enet_sentiment 策略）
#         pred_path = Path("stage3-4_result/data/pred_enet_sentiment.csv")
#         df = pd.read_csv(pred_path)
#         latest_date = df["date"].max()
#         latest = df[df["date"] == latest_date].sort_values("y_pred", ascending=False).head(10)
#
#         output = latest[["symbol", "y_pred"]].rename(columns={"y_pred": "predicted_return"})
#         return jsonify(output.to_dict(orient="records"))
#
#     except Exception as e:
#         return jsonify({"error": str(e)})
#
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)





from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
from stage3 import rolling_weekly_prediction
from run_stage3 import main


# 可选：用于接入 OpenAI Chat API（仅当你需要）
# import openai
# openai.api_key = "你的 API Key"

app = Flask(__name__)
CORS(app)

# @app.route("/api/generate-weights", methods=["GET"])
# def generate_weights():
#     try:
#         # 读取预测结果 CSV 文件
#         csv_path = Path("stage3-4_result/data/pred_enet_market.csv")
#         df = pd.read_csv(csv_path)
#
#         # 确保包含必要列
#         if not {"date", "symbol", "y_pred"}.issubset(df.columns):
#             return jsonify({"error": "Missing required columns in CSV"}), 400
#
#         # 转换日期列为 datetime 类型
#         df["date"] = pd.to_datetime(df["date"])
#
#         # 选择最新日期的数据
#         latest_date = df["date"].max()
#         latest_df = df[df["date"] == latest_date].copy()
#
#         # 过滤掉预测值过小的资产（可选）
#         latest_df = latest_df[latest_df["y_pred"] > 0]
#
#         # 选取 top 10 预测值资产
#         latest_df = latest_df.nlargest(20, "y_pred")
#
#         # 归一化权重
#         total_pred = latest_df["y_pred"].sum()
#         latest_df["weight"] = latest_df["y_pred"] / total_pred
#
#         # 构建前端需要的返回格式
#         result = [
#             {
#                 "symbol": row["symbol"],
#                 "predicted_return": round(row["weight"], 6)
#             }
#             for _, row in latest_df.iterrows()
#         ]
#
#         return jsonify(result)
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# @app.route("/api/generate-weights", methods=["GET"])
# def generate_weights():
#     try:
#         # ✅ 执行滚动预测，动态更新最新一周的预测
#         df = pd.read_csv("stage_2_merged_data.csv", parse_dates=["date"])
#         save_dir = Path("stage3-4_result/data")
#         save_dir.mkdir(parents=True, exist_ok=True)
#         rolling_weekly_prediction(df, save_dir, roll_window=52)
#
#         # ✅ 从最新的预测结果 CSV 中选出最新一周的 top 10 权重
#         pred_df = pd.read_csv(save_dir / "pred_enet_market.csv", parse_dates=["date"])
#         latest_date = pred_df["date"].max()
#         latest_week_df = pred_df[pred_df["date"] == latest_date].copy()
#
#         # ✅ 按预测值排序，提取 top 10
#         top_df = latest_week_df.sort_values("y_pred", ascending=False).head(20)
#         top_df["predicted_return"] = top_df["y_pred"]
#         result = top_df[["symbol", "predicted_return"]].to_dict(orient="records")
#
#         return jsonify(result)
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route("/api/generate-weights", methods=["GET"])
def generate_weights():
    try:
        # 运行预测
        main()

        # 读取结果
        pred_path = Path("stage3-4_result/data/pred_enet_sentiment.csv")
        df = pd.read_csv(pred_path)
        latest_date = df["date"].max()
        latest = df[df["date"] == latest_date].sort_values("y_pred", ascending=False)

        # ✅ 从前端 URL 获取 top_n 参数（默认为10）
        top_n = int(request.args.get("top_n", 10))
        latest = latest.head(top_n)

        output = latest[["symbol", "y_pred"]].rename(columns={"y_pred": "predicted_return"})
        return jsonify(output.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"answer": "❌ No question received."})

        # ❗如果你接入 OpenAI API，取消注释以下内容👇
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful financial assistant."},
        #         {"role": "user", "content": question}
        #     ]
        # )
        # answer = response["choices"][0]["message"]["content"]

        # 临时 mock 模式返回固定答案
        answer = "💡 This is a simulated answer. Please connect to a real AI service."

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"❌ Failed to fetch AI answer: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)





