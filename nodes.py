import json
import re

class ProductPromptGeneratorSimple:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "qwen_output_1": ("STRING", {"multiline": True, "forceInput": True}),
                "qwen_output_2": ("STRING", {"multiline": True, "forceInput": True}),
                "qwen_output_3": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate"
    CATEGORY = "Custom"

    def generate(self, qwen_output_1, qwen_output_2, qwen_output_3):
        def parse_json(text):
            if not isinstance(text, str):
                return {}
            try:
                # Remove markdown code blocks if present
                text = re.sub(r'```json\s*', '', text)
                text = re.sub(r'```', '', text)
                
                # Find the first { and last }
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = text[start:end]
                    return json.loads(json_str)
                return {}
            except Exception as e:
                print(f"Error parsing JSON: {e}, text: {text}")
                return {}

        data1 = parse_json(qwen_output_1)
        data2 = parse_json(qwen_output_2)
        data3 = parse_json(qwen_output_3)

        # Extract fields
        product_type = data1.get('商品类型', '商品')
        is_handheld_str = str(data1.get('是否支持手持', '否')).strip()
        background = data1.get('推荐背景', '背景')
        
        interaction = data2.get('交互方式', '')
        
        is_wearable_str = str(data3.get('是否支持佩戴', '否')).strip()

        # Determine logic flags
        is_wearable = '是' in is_wearable_str
        is_handheld = '是' in is_handheld_str

        # Determine Verb
        verb = "使用"
        if is_wearable:
            verb = "佩戴"
        elif is_handheld:
            verb = "手持"
        
        # If interaction implies specific verb, we might want to use it? 
        # But for now, stick to the safe logic.
        
        # Construct Prompt
        # "请让图中模特{verb}图中{product_type}，背景为{background}，要求保持图中{product_type}与模特相对比例、大小、位置不变，画面聚焦模特与商品，人脸细节必须完整，{product_type}正确{interaction}。"
        
        # Ensure interaction is not empty for the final sentence
        final_interaction = interaction if interaction else f"{verb}"

        prompt = f"请让图中模特{verb}图中{product_type}，背景为{background}，要求保持图中{product_type}与模特相对比例、大小、位置不变，画面聚焦模特与商品，人脸细节必须完整，{product_type}正确{final_interaction}。"

        return (prompt,)
