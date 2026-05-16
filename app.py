import os
import re
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "没有收到内容"}), 400
    if not GROQ_API_KEY:
        return jsonify({"error": "服务器未配置API Key"}), 500

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a meeting assistant. Always respond with valid JSON only. No markdown, no explanation, no code blocks."
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            },
            timeout=30,
        )
        result = response.json()

        if "error" in result:
            return jsonify({"error": result["error"].get("message", "API错误")}), 500

        text = result["choices"][0]["message"]["content"]

        # 后端直接解析JSON，返回结构化数据
        try:
            parsed = json.loads(text)
            return jsonify({"data": parsed})
        except json.JSONDecodeError:
            # 尝试提取JSON块
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
                return jsonify({"data": parsed})
            return jsonify({"error": f"JSON解析失败: {text[:200]}"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时，请重试"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
