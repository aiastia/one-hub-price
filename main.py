import json
import os
from collections import defaultdict

# ========== Step 1: 处理目录下 JSON 文件，拆分重复和唯一数据 ==========
def process_files():
    INPUT_DIR = "./json_files"       # JSON文件所在目录
    OUTPUT_DUPLICATED = "duplicated.json"     # 包含重复model的文件（排序后）
    OUTPUT_UNIQUE = "unique.json"         # 包含唯一model的文件
    SORT_KEY = "model"               # 排序依据字段（如 "model", "input" 等）
    SORT_REVERSE = False             # 是否降序排序（True=从Z到A，False=从A到Z）

    all_data = []
    model_counter = defaultdict(int)

    # 读取所有 JSON 文件并统计 model 出现次数
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(INPUT_DIR, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.extend(data)
                    for item in data:
                        model = item.get("model")
                        if model:
                            model_counter[model] += 1
            except Exception as e:
                print(f"读取文件 {filename} 失败: {e}")
                continue

    duplicated = []
    unique = []
    for item in all_data:
        model = item.get("model")
        if model and model_counter.get(model, 0) > 1:
            duplicated.append(item)
        else:
            unique.append(item)

    # 对重复数据进行排序
    if SORT_KEY:
        duplicated = sorted(duplicated, key=lambda x: x.get(SORT_KEY, ""), reverse=SORT_REVERSE)

    try:
        with open(OUTPUT_DUPLICATED, "w", encoding="utf-8") as f:
            json.dump(duplicated, f, indent=2, ensure_ascii=False)
        with open(OUTPUT_UNIQUE, "w", encoding="utf-8") as f:
            json.dump(unique, f, indent=2, ensure_ascii=False)
        print(f"Step 1: 合并完成！重复数据保存到 {OUTPUT_DUPLICATED} ({len(duplicated)}条)，唯一数据保存到 {OUTPUT_UNIQUE}")
    except Exception as e:
        print(f"Step 1: 保存失败: {e}")

# ========== Step 2: 处理重复数据，生成 deduplicated.json ==========
def process_duplicates():
    INPUT_FILE = "duplicated.json"  # 输入文件路径
    OUTPUT_FILE = "deduplicated.json"  # 输出文件路径
    NEW_CHANNEL_TYPE = 2000  # 修改后的 channel_type 值

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        model_to_entry = {}
        # 按 model 分组，筛选每个 model 中 input + output 最大的条目
        for item in data:
            model = item.get("model")
            if not model:
                continue
            total = item.get("input", 0) + item.get("output", 0)
            if model not in model_to_entry or total > model_to_entry[model]["total"]:
                model_to_entry[model] = {"item": item, "total": total}

        result = []
        for entry in model_to_entry.values():
            item = entry["item"]
            item["channel_type"] = NEW_CHANNEL_TYPE  # 修改 channel_type
            result.append(item)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Step 2: 处理完成！结果已保存到 {OUTPUT_FILE}")
    except Exception as e:
        print(f"Step 2: 处理失败: {e}")

# ========== Step 3: 合并 unique.json 与 deduplicated.json ==========
def merge_unique_and_deduplicated():
    unique_file = "unique.json"
    dedup_file = "deduplicated.json"
    output_file = "merged.json"

    try:
        with open(unique_file, "r", encoding="utf-8") as f:
            a = json.load(f)
        with open(dedup_file, "r", encoding="utf-8") as f:
            b = json.load(f)

        models_in_a = {item["model"] for item in a if "model" in item}
        # 保留 a 的全部内容，添加 b 中 model 不重复的条目
        for item in b:
            if "model" in item and item["model"] not in models_in_a:
                a.append(item)
                models_in_a.add(item["model"])

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2, ensure_ascii=False)
        print(f"Step 3: 合并完成，结果已保存到 {output_file}")
    except Exception as e:
        print(f"Step 3: 合并失败: {e}")

# ========== Step 4: 合并 prices.json 与 merged.json ==========
def merge_prices_and_merged():
    prices_file = "prices.json"
    merged_file = "merged.json"
    output_file = "new.json"

    try:
        with open(prices_file, "r", encoding="utf-8") as f:
            a = json.load(f)
        with open(merged_file, "r", encoding="utf-8") as f:
            b = json.load(f)

        models_in_a = {item["model"] for item in a if "model" in item}
        # 保留 prices.json 的全部内容，添加 merged.json 中 model 不重复的条目
        for item in b:
            if "model" in item and item["model"] not in models_in_a:
                a.append(item)
                models_in_a.add(item["model"])

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2, ensure_ascii=False)
        print(f"Step 4: 合并完成，结果已保存到 {output_file}")
    except Exception as e:
        print(f"Step 4: 合并失败: {e}")

if __name__ == "__main__":
    print("开始执行合并流程...")
    process_files()
    process_duplicates()
    merge_unique_and_deduplicated()
    merge_prices_and_merged()
    print("所有步骤执行完成。")
