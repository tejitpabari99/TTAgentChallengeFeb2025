from dataclasses import dataclass
from typing import Dict, Optional, Any
import json, logging

from backend.utils.PPT import PPT
from backend.utils.GPT import GPT
from backend.utils import Constants

logger = logging.getLogger(__name__)

@dataclass
class GPTPersonaAction:
    type: str
    type_intent: str
    prompt: Optional[str] = None
    result: Optional[str] = None
    ppt: Optional[PPT] = None
    mapping: Optional[Dict[str, str]] = None

    def __init__(self, type: str, type_intent: str,
                 prompt: Optional[str] = '', 
                 result: Optional[str] = None,
                 ppt: Optional[PPT] = None, gpt:GPT = None) -> None:
        self.type = type
        self.type_intent = type_intent
        self.prompt = prompt
        self.result = result
        self.ppt = ppt
        self.gpt = gpt or GPT(f"GPT Assistant {self.type}", Constants.Prompts.TINY_TROUPE_INFO)
        self._set_mapping()

    @classmethod
    def load(cls, type: str, type_intent: str, action_dict: Dict[str, Any]) -> 'GPTPersonaAction':
        logger.info(f"Loading GPTPersonaAction {type}...")
        return cls(
            type=type,
            type_intent=type_intent,
            prompt=action_dict.get(f'prompt', ''),
            result=action_dict.get('result', None),
            ppt=PPT.load(action_dict.get('ppt', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'prompt': self.prompt,
            'result': self.result
        }

    def add_prompt(self, prompt: str) -> None: self.prompt = prompt
    def remove_prompt(self) -> None: self.prompt = ''
    def reset(self): self.remove_prompt()
    def add_result(self, result: str) -> None: self.result = result
    def remove_result(self) -> None: self.result = ''
    def add_ppt(self, ppt: PPT) -> None: self.ppt = ppt
    def remove_ppt(self) -> None: self.ppt = None
    def add_gpt(self, gpt: GPT) -> None: self.gpt = gpt
    def remove_gpt(self) -> None: self.gpt = None

    def _set_mapping(self) -> None:
        self.mapping = {
            f'{self.type}_prompt': self.prompt,
            f'{self.type}_result': self.result
        }

    def update_mapping(self) -> Dict[str, str]:
        self._set_mapping()
        return self.mapping

    def run(self, updateDict: Dict[str, str], continue_chat = True) -> None:
        if not self.ppt:
            raise ValueError("No PPT provided to run the action.")
        logger.info(f"Running GPTPersonaAction {self.type}...")

        # Update prompt with the mapping values
        if self.prompt:
            self.add_prompt(self.prompt.format_map(updateDict))
        logger.debug(f"{self.type} GPT Prompt: {self.prompt}")
        updateDict.update(self.update_mapping())

        if continue_chat:
            gpt = self.gpt 
        else: 
            gpt = GPT(f"GPT Assistant {self.type}", Constants.Prompts.GPT.GPT_INFO)
        self.result = self._parse_result(gpt.continue_conversation(self.ppt.ppt_and_slide_prompt() + 
                                                self.prompt.format_map(updateDict) + 
                                                Constants.Prompts.GPT.OUTPUT_SUPPORT_PROMPT)['response'])
        logger.debug(f"{self.type} GPT Persona Result: {self.result}")

    def _parse_result(self, result: str) -> str:
        if result and '$#$' in result:
            return result.split('$#$')[1]
        return result

    def results_to_html(self) -> str:
        import markdown2
        return markdown2.markdown(self.result) if self.result else 'No results'

    def to_html(self) -> str:
        import markdown2
        html = f"""
        <div class="{self.type}-prompts">
            <details>
                <summary>Prompts</summary>
                <details>
                    <summary>Prompt</summary>
                    <div class="prompt-content scrollable-content">
                        <pre>{self.prompt or 'Not provided'}</pre>
                    </div>
                </details>
            </details>
            <details>
                <summary>Results</summary>
                <details>
                    <summary>Combined Results</summary>
                    <div class="combined-results">
                        {self.results_to_html()}
                    </div>
                </details>
            </details>
        </div>
        """
        return html

@dataclass
class GPTPersonaAnalysis(GPTPersonaAction):
    def __init__(self, 
                 prompt: Optional[str] = Constants.Prompts.GPT.ANALYSIS_PROMPT,
                 result: Optional[str] = None):
        super().__init__('analysis', "Analyze a powerpoint presentation and provide feedback",
                        prompt or Constants.Prompts.GPT.ANALYSIS_PROMPT, result)

    @classmethod
    def load(cls, action_dict: Dict[str, Any]) -> 'GPTPersonaAnalysis':
        return cls(
            prompt=action_dict.get(f'prompt', Constants.Prompts.GPT.ANALYSIS_PROMPT),
            result=action_dict.get('result', None)
        )

@dataclass
class GPTPersonaQNA(GPTPersonaAction):
    def __init__(self, 
                 prompt: Optional[str] = Constants.Prompts.GPT.QNA_PROMPT,
                 result: Optional[str] = None):
        super().__init__('qna', "Ask questions about a powerpoint presentation",
                        prompt or Constants.Prompts.GPT.QNA_PROMPT, result)

    @classmethod
    def load(cls, action_dict: Dict[str, Any]) -> 'GPTPersonaQNA':
        return cls(
            prompt=action_dict.get(f'prompt', Constants.Prompts.GPT.QNA_PROMPT),
            result=action_dict.get('result', None)
        )
