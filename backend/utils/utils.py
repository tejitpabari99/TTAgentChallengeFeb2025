from typing import List
from backend.utils.GPT import GPT

def _ensure_keys_exist(check_dict: dict, keys: List[str], additiona_error_message: str = ""):
    for key in keys:
        if key not in check_dict:
            raise ValueError(f"{key} not found in agent data. {additiona_error_message}".strip())

def _get_prompt(gpt:GPT, gpt_prompt:str, prompt:str, default_prompt:str=None, additional_prompts:List[str] = []) -> str:
    additional_prompts_str = '\n--------\n'.join(additional_prompts) or ''
    if prompt: return additional_prompts_str + prompt
    elif gpt_prompt:
        return additional_prompts_str + gpt.run_conversation(additional_prompts_str + gpt_prompt)['response']
    else:
        return additional_prompts_str + gpt.run_conversation(additional_prompts_str + default_prompt)['response']
        
    