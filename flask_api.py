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
import json



# 可选：用于接入 OpenAI Chat API（仅当你需要）
# import openai
# openai.api_key = "你的 API Key"

app = Flask(__name__)
CORS(app)

# @app.route("/api/generate-weights", methods=["GET"])
# def generate_weights():
#     try:
#         # 运行预测
#         main()
#
#         # 读取结果
#         pred_path = Path("stage3-4_result/data/pred_enet_sentiment.csv")
#         df = pd.read_csv(pred_path)
#         latest_date = df["date"].max()
#         latest = df[df["date"] == latest_date].sort_values("y_pred", ascending=False)
#
#         # ✅ 从前端 URL 获取 top_n 参数（默认为10）
#         top_n = int(request.args.get("top_n", 10))
#         latest = latest.head(top_n)
#
#         output = latest[["symbol", "y_pred"]].rename(columns={"y_pred": "predicted_return"})
#         return jsonify(output.to_dict(orient="records"))
#
#     except Exception as e:
#         return jsonify({"error": str(e)})
#
#
# @app.route("/api/ask", methods=["POST"])
# def ask_ai():
#     try:
#         data = request.get_json()
#         question = data.get("question", "")
#
#         if not question:
#             return jsonify({"answer": "❌ No question received."})
#
#         # ❗如果你接入 OpenAI API，取消注释以下内容👇
#         # response = openai.ChatCompletion.create(
#         #     model="gpt-4",
#         #     messages=[
#         #         {"role": "system", "content": "You are a helpful financial assistant."},
#         #         {"role": "user", "content": question}
#         #     ]
#         # )
#         # answer = response["choices"][0]["message"]["content"]
#
#         # 临时 mock 模式返回固定答案
#         answer = "💡 This is a simulated answer. Please connect to a real AI service."
#
#         return jsonify({"answer": answer})
#
#     except Exception as e:
#         return jsonify({"answer": f"❌ Failed to fetch AI answer: {str(e)}"})
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

@app.route('/')
def index():
    return "CryptoMind Flask API is running!"


@app.route("/api/generate-weights", methods=["GET"])
def generate_weights():
    try:
        # ✅ 获取前端参数 top_n（默认10）
        top_n = int(request.args.get("top_n", 10))

        # ✅ 运行主预测函数
        #main()

        # ✅ 尝试读取最新预测结果
        pred_path = Path("stage3-4_result/data/pred_enet_sentiment.csv")
        df = pd.read_csv(pred_path)
        latest_date = df["date"].max()
        latest = df[df["date"] == latest_date].sort_values("y_pred", ascending=False)

        latest = latest.head(top_n)
        output = latest[["symbol", "y_pred"]].rename(columns={"y_pred": "predicted_return"})
        return jsonify(output.to_dict(orient="records"))

    except Exception as e:
        # ✅ 如果失败，则读取备用的权重文件 weights.json
        try:
            with open("weights.json", "r") as f:
                weights = json.load(f)
            return jsonify(weights)
        except Exception as backup_error:
            return jsonify({"error": f"Main failed: {str(e)}; Backup failed: {str(backup_error)}"})



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


# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

