# test_111/cli.py
import argparse
import sys
# ▼▼▼ MODIFICATION / ADDITION: Importing main for initialization and core for API ▼▼▼
from test_111.core import CoreAPI
from test_111.adapter import AdapterFactory, AdapterType # 需要AdapterFactory来设置adapter
from test_111.funs import RealDataReaderImpl, RealDataAnalyzerImpl, RealReportGeneratorImpl # 真实实现
from test_111.mock import MockDataReaderImpl, MockDataAnalyzerImpl, MockReportGeneratorImpl # 模拟实现

# ▼▼▼ MODIFICATION / ADDITION: Centralized initialization for CLI context ▼▼▼
def initialize_app_for_cli(env: str):
    print(f"\n--- CLI Initializing in '{env}' mode ---")
    
    # 决定使用哪个实现子线 (mock.py 还是 funs.py)
    if env == "dev":
        reader_impl = MockDataReaderImpl()
        analyzer_impl = MockDataAnalyzerImpl()
        report_gen_impl = MockReportGeneratorImpl()
    else: # env == "prod"
        reader_impl = RealDataReaderImpl()
        analyzer_impl = RealDataAnalyzerImpl()
        report_gen_impl = RealReportGeneratorImpl()
        
    # 通过AdapterFactory包装成接口类型
    # 注意：这里我们手动将Impl包装成AdapterFactory的返回类型，因为AdapterFactory的new方法返回的是接口
    # 在main.py中AdapterFactory的new方法会直接创建Mock/RealAdapter，此处为了演示将funs/mock作为单独的文件注入，需要稍微调整工厂逻辑
    
    # 假设AdapterFactory的new_*方法可以接收Impl实例，并将其包装为对应的接口
    # 或者，我们调整AdapterFactory，让它根据env直接返回funs/mock中的Impl
    
    # 【重要调整】：为了直接使用funs.py和mock.py作为插拔点，我们需要调整AdapterFactory
    #              使其不再直接实例化Mock/RealDataReader等，而是实例化mock.py或funs.py中的Impl类
    #              然后这些Impl类自身就是接口的实现者（或者被adapter.py中的Adapter包装）

    # 简化的处理方式：直接在工厂中选择funs/mock的Impl作为真正的接口实现
    data_reader_adapter = reader_impl # 假设这些Impl类本身就是IDataReader等接口的实现
    data_analyzer_adapter = analyzer_impl
    report_generator_adapter = report_gen_impl

    domain_service = CoreAPI.CoreDomainService(
        data_reader=data_reader_adapter,
        data_analyzer=data_analyzer_adapter,
        report_generator=report_generator_adapter
    )
    CoreAPI(domain_service=domain_service)
    print("--- CLI Initialization Complete ---\n")


def run_cli():
    parser = argparse.ArgumentParser(description="CSV Analysis CLI Tool.")
    parser.add_argument("command", choices=["analyze"], help="Command to execute.")
    parser.add_argument("--env", default="dev", choices=["dev", "prod"], help="Environment (dev for mock, prod for real).")
    parser.add_argument("--source", default="dummy_data.csv", help="CSV data source (file path or dummy content).")
    parser.add_argument("--column", default="value", help="Column name to analyze.")

    args = parser.parse_args()

    # 初始化应用
    initialize_app_for_cli(args.env)
    
    # 获取CoreAPI实例
    core_api = CoreAPI.get_instance()

    try:
        if args.command == "analyze":
            report = core_api.analyze_csv_and_generate_report(args.source, args.column)
            print("\n--- Final Report ---")
            print(report)
            print("--------------------")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # 为了演示，这里的if __name__ == '__main__'直接运行CLI
    run_cli()