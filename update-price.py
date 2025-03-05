import json
import os
from pathlib import Path

def update_json_files():
    # 读取prices.json
    with open('prices.json', 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    # 创建model到价格配置的映射
    price_map = {item["model"]: item for item in prices}
    
    # 遍历json_files目录下的所有json文件
    json_dir = Path('json_files')
    for json_file in json_dir.glob('*.json'):
        # 跳过prices.json本身
        if json_file.name == 'prices.json':
            continue
            
        # 读取文件内容
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"跳过无效的JSON文件: {json_file}")
                continue
        
        # 更新配置项
        updated = False
        for item in data:
            model = item.get("model")
            if model in price_map:
                # 更新字段
                price_config = price_map[model]
                for field in ["type", "input", "output"]:
                    if item.get(field) != price_config[field]:
                        item[field] = price_config[field]
                        updated = True
        
        # 如果有更新则写回文件
        if updated:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"已更新文件: {json_file}")

if __name__ == "__main__":
    update_json_files()