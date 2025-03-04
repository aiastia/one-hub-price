import json
import os

# ====================== 用户配置区域 ======================
# 1. 固定参数（除 channel_type 外的其他参数）
FIXED_PARAMS = {
    "type": "tokens",
    "input": 1,
    "output": 1
}

# 2. 定义 channel_type 到输出文件名后缀的映射
CHANNEL_TYPE_MAPPING = {
    1: "OpenAI",
    11: "GooglePaLM",
    14: "Anthropic",
    15: "Baidu",
    16: "Zhipu",
    17: "Qwen",
    18: "Spark",
    19: "360",
    23: "Tencent",
    25: "GoogleGemini",
    26: "Baichuan",
    27: "MiniMax",
    28: "Deepseek",
    29: "Moonshot",
    30: "Mistral",
    31: "Groq",
    33: "Yi",
    34: "Midjourney",
    35: "CloudflareAI",
    36: "Cohere",
    37: "StabilityAI",
    38: "Coze",
    39: "Ollama",
    40: "Hunyuan",
    41: "Suno",
    43: "Meta",
    44: "Ideogram",
    45: "Siliconflow",
    46: "Flux",
    47: "Jina",
    48: "Rerank",
    51: "RecraftAI",
    53: "Kling",
    1120: "Grok_xAI",
    1121: "Stepfun",
    1122: "Volcengine",
    1123: "Spark",
    1124: "Azure",
    1125: "GIthub",
    1126: "together"
}

# 3. 模型列表文件路径
MODELS_FILE = "models.txt"

# 4. 输出文件夹
OUTPUT_DIR = "json_files"
# ========================================================

def read_all_models(file_path):
    """
    读取模型列表文件，返回字典，键为channel_type，值为模型列表
    """
    result = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(None, 1)
                if len(parts) != 2:
                    continue
                try:
                    ch = int(parts[0])
                except ValueError:
                    continue
                models_str = parts[1]
                model_list = [model.strip() for model in models_str.split(",") if model.strip()]
                result[ch] = model_list
        return result
    except FileNotFoundError:
        print(f"错误：模型列表文件 {file_path} 未找到！")
        return {}
    except Exception as e:
        print(f"读取模型列表文件失败：{e}")
        return {}

def generate_json_for_channel(channel_type, model_list):
    """
    生成或更新JSON文件，保留旧条目并添加新模型
    """
    # 准备新数据条目
    params = FIXED_PARAMS.copy()
    params["channel_type"] = channel_type
    new_data = [{"model": model, **params} for model in model_list]
    
    # 确定输出路径
    output_filename = f"{CHANNEL_TYPE_MAPPING.get(channel_type, channel_type)}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    existing_data = []
    # 读取现有文件（如果存在）
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                # 确保数据是列表格式
                if not isinstance(existing_data, list):
                    print(f"警告：{output_path} 格式不正确，将覆盖。")
                    existing_data = []
        except json.JSONDecodeError:
            print(f"警告：{output_path} 包含无效JSON，将覆盖。")
        except Exception as e:
            print(f"读取 {output_path} 失败：{e}，将覆盖。")
    
    # 提取现有模型的名称
    existing_models = {item.get("model") for item in existing_data}
    # 筛选需要添加的新模型
    new_entries_to_add = [entry for entry in new_data if entry["model"] not in existing_models]
    
    # 合并数据
    merged_data = existing_data + new_entries_to_add
    
    # 写入文件
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        print(f"成功更新文件：{output_path}")
    except Exception as e:
        print(f"保存文件失败：{e}")

def generate_all_json():
    models_dict = read_all_models(MODELS_FILE)
    if not models_dict:
        return
    
    # 创建输出目录（如果不存在）
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 为每个channel_type生成文件
    for ch, model_list in models_dict.items():
        generate_json_for_channel(ch, model_list)

if __name__ == "__main__":
    generate_all_json()
