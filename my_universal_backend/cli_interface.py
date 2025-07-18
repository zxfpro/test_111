# my_universal_backend/cli_interface.py
import argparse
import json
from my_universal_backend.main import get_core_api_instance # 从main获取CoreAPI实例

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (CLI Driver Adapter) ▼▼▼
def run_cli():
    print("\n--- Starting CLI Interface ---")
    parser = argparse.ArgumentParser(description="Universal Backend CLI Interface.")
    parser.add_argument("command", choices=["process", "get_items", "trigger_action"], help="Command to execute.")
    parser.add_argument("--payload", type=str, help="JSON payload for 'process' or 'trigger_action' command.")
    parser.add_argument("--item_type", type=str, help="Item type for 'get_items' command.")

    args = parser.parse_args()
    core_api = get_core_api_instance() # 获取已初始化CoreAPI实例

    try:
        if args.command == "process":
            payload = json.loads(args.payload) if args.payload else {}
            result = core_api.process_general_request(payload)
            print("Process Command Result:")
            print(json.dumps(result, indent=2))
        elif args.command == "get_items":
            if not args.item_type:
                raise ValueError("Item type must be specified for 'get_items' command.")
            items = core_api.retrieve_all_items_of_type(args.item_type)
            print(f"Items of type '{args.item_type}':")
            print(json.dumps(items, indent=2))
        elif args.command == "trigger_action":
            payload = json.loads(args.payload) if args.payload else {}
            status = core_api.trigger_external_critical_action(payload)
            print(f"Trigger Action Status: {status}")
        
    except Exception as e:
        print(f"CLI Error: {e}")
        parser.print_help()
    print("--- CLI Command Finished ---")

if __name__ == '__main__':
    # 确保 main.py 已经初始化了 CoreAPI
    from my_universal_backend.main import initialize_application
    initialize_application(env="dev") # 或 "prod"
    run_cli()