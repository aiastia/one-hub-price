# 项目简介

本项目是 `https://raw.githubusercontent.com/MartialBE/one-api/prices/prices.json` 的个人延续。

## 使用说明

您可以使用以下链接获取最新的 JSON 数据：

```https://raw.githubusercontent.com/aiastia/one-hub-price/refs/heads/main/new.json```

后续可以使用 `new-model_config_generator.py` 来更新数据。

## 文件说明

- `new-model_config_generator.py`：用于生成或更新 JSON 文件，保留旧条目并添加新模型。
- `main.py`：包含多个步骤的处理脚本，用于处理和合并 JSON 文件,主要是合并输出new.json文件。
- `model_config_generator.py`：用于生成 JSON 文件，但不会保留旧条目（危险）。
- 其他 JSON 文件和配置文件：用于存储和处理模型数据。

## 更新步骤

1. 运行 `new-model_config_generator.py` 生成或更新 JSON 文件。（注意如果后续渠道有新模型需要去更新 `models.txt`文件。然后去修改json_files的价格。
2. 注意优先级是prices.json最高里面的数据会保留，然后是json_files里面合并后不重复的内容，在是重复的内容中价格最高的保留。
3. 使用 `main.py` 进行数据处理和合并。

## 注意事项
新增渠道信息如下 3
```
    1120: "Grok_xAI",
    1121: "Stepfun",
    1122: "Volcengine",
    1123: "Spark",
    1124: "Azure",
    1125: "GIthub",
    1126: "together"
```
- 请确保在运行脚本前，相关的 JSON 文件和配置文件已正确放置在项目目录中。
- 运行脚本时，请根据需要调整配置参数。
