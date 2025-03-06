import json
import os

# ====================== 用户配置区域 ======================
#该脚本会覆盖json文件，不会保留旧条目，请确保该文件夹下没有其他文件
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
    1123: "0000000000000000",
    1124: "Azure",
    1125: "GIthub",
    1126: "together"
}

# 3. 模型列表文件路径
# models.txt 文件中每一行格式如下：
# channel_type 模型1,模型2,模型3,...
# 例如：
# 1125 google/gemma-2-27b-it,deepseek-ai/DeepSeek-R1-Distill-Qwen-14B,meta-llama/Llama-3-70b-chat-hf,stabilityai/stable-diffusion-xl-base-1.0,deepseek-ai/DeepSeek-R1-Distill-Llama-70B
# 1123 google/gemma-2-27b-it,deepseek-ai/DeepSeek-R1-Distill-Qwen-14B,meta-llama/Llama-3-70b-chat-hf
MODELS_FILE = "models.txt"

# 4. 输出文件夹
OUTPUT_DIR = "json_files"
# ========================================================

def read_all_models(file_path):
    """
    读取模型列表文件，返回一个字典，
    键为 channel_type（int），值为对应的模型列表（list）
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
    根据指定 channel_type 和模型列表生成 JSON 文件，
    JSON 中每个项包含模型及固定参数（并自动附加 channel_type）。
    生成的 JSON 按 model 名称排序。
    """
    params = FIXED_PARAMS.copy()
    params["channel_type"] = channel_type

    # 生成数据，并按 model 名称排序
    data = sorted(
        [{"model": model, **params} for model in model_list], 
        key=lambda x: x["model"]
    )

    output_filename = f"{CHANNEL_TYPE_MAPPING.get(channel_type, channel_type)}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"成功生成文件（已排序）：{output_path}")
    except Exception as e:
        print(f"文件保存失败：{e}")

def generate_all_json():
    models_dict = read_all_models(MODELS_FILE)
    if not models_dict:
        return
    
    # 检查输出目录是否存在，不存在则创建
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 遍历所有 channel_type，生成对应的 JSON 文件
    for ch, model_list in models_dict.items():
        generate_json_for_channel(ch, model_list)

if __name__ == "__main__":
    generate_all_json()
