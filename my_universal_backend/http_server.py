# my_universal_backend/http_server.py
from flask import Flask, request, jsonify
from my_universal_backend.main import get_core_api_instance # 从main获取CoreAPI实例

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (HTTP Server Driver Adapter) ▼▼▼
app = Flask(__name__)
core_api = get_core_api_instance() # 在应用启动时获取已初始化的CoreAPI实例

@app.route('/process_request', methods=['POST'])
def process_request_endpoint():
    try:
        payload = request.json
        if not payload:
            return jsonify({"error": "Request payload is empty"}), 400

        # 调用 CoreAPI 中的一个流程
        result = core_api.process_general_request(payload)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<item_type>', methods=['GET'])
def get_items_by_type_endpoint(item_type):
    try:
        # 调用 CoreAPI 中的一个流程
        items = core_api.retrieve_all_items_of_type(item_type)
        return jsonify({"item_type": item_type, "items": items}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_http_server():
    print("\n--- Starting HTTP Server ---")
    # app.run(debug=True, port=5000) # 通常在生产环境会用Gunicorn等WSGI服务器
    print("HTTP Server ready. (Run 'flask run' or equivalent in production)")

if __name__ == '__main__':
    # 确保 main.py 已经初始化了 CoreAPI
    from my_universal_backend.main import initialize_application
    initialize_application(env="dev") # 或 "prod"
    run_http_server()
    # 手动运行 Flask App (开发模式)
    app.run(debug=True, port=5000)