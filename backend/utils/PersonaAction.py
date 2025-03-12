from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, Optional, Any, List
import os,json, logging

from backend.utils.GPT import GPT
from backend.utils.PPT import PPT
from backend.utils import Constants
from backend.utils.utils import _get_prompt

from tinytroupe.environment import TinyWorld
from tinytroupe.extraction import ResultsExtractor

logger = logging.getLogger(__name__)

default_objective = "Return an array of json objects, 1 array entry per agent."

@dataclass
class PersonaAction:
    type: str
    type_intent: str
    gpt_prompt: Optional[str] = None
    prompt: Optional[str] = None
    summarization_gpt_prompt: Optional[str] = None
    result: Optional[Any] = None
    combined_result: Optional[str] = None
    ppt: Optional[PPT] = None
    mapping: Optional[Dict[str, str]] = None

    def __init__(self, type: str, type_intent: str,
                 gpt_prompt: Optional[str] = '', prompt: Optional[str] = '', 
                 summarization_gpt_prompt: Optional[str] = '', 
                 result: Optional[Any] = None, combined_result: Optional[str] = None,
                 ppt: Optional[PPT] = None) -> None:
        self.type = type
        self.type_intent = type_intent
        self.gpt_prompt = gpt_prompt
        self.prompt = prompt
        self.summarization_gpt_prompt = summarization_gpt_prompt
        self.result = result
        self.combined_result = combined_result
        self.ppt = ppt
        self.gpt = GPT(f"GPT Assistant {self.type}", Constants.Prompts.TINY_TROUPE_INFO)
        self._set_mapping()

    @classmethod
    def load(cls, type:str, type_intent: str, action_dict: Dict[str, Any]) -> 'PersonaAction':
        logger.info(f"Loading PersonaAction {type}...")
        return cls(
            type=type,
            type_intent=type_intent,
            gpt_prompt=action_dict.get(f'gpt_prompt', ''),
            prompt=action_dict.get(f'prompt', ''),
            summarization_gpt_prompt=action_dict.get(f'summarization_gpt_prompt', ''),
            result=action_dict.get('result', None),
            combined_result=action_dict.get('combined_result', None),
            ppt=PPT.load(action_dict.get('ppt', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'gpt_prompt': self.gpt_prompt,
            'prompt': self.prompt,
            'summarization_gpt_prompt': self.summarization_gpt_prompt,
            'result': self.result,
            'combined_result': self.combined_result
        }

    def add_prompt(self, prompt: str) -> None: self.prompt = prompt
    def remove_prompt(self) -> None: self.prompt = ''
    def add_gpt_prompt(self, gpt_prompt: str) -> None: self.gpt_prompt = gpt_prompt
    def remove_gpt_prompt(self) -> None: self.gpt_prompt = ''
    def add_summarization_gpt_prompt(self, summarization_gpt_prompt: str) -> None: self.summarization_gpt_prompt = summarization_gpt_prompt
    def remove_summarization_gpt_prompt(self) -> None: self.summarization_gpt_prompt = ''
    def reset(self):
        self.remove_prompt()
        self.remove_gpt_prompt()
        self.remove_summarization_gpt_prompt()
    def add_result(self, result: Any) -> None: self.result = result
    def add_combined_result(self, combined_result: str) -> None: self.combined_result = combined_result
    def add_ppt(self, ppt: PPT) -> None: self.ppt = ppt
    def _set_mapping(self) -> None:
        self.mapping = {
            f'{self.type}_prompt': self.prompt,
            f'{self.type}_gpt_prompt': self.gpt_prompt,
            f'{self.type}_summarization_gpt_prompt': self.summarization_gpt_prompt,
            f'{self.type}_result': self.result,
            f'{self.type}_combined_result': self.combined_result
        }

    def update_mapping(self) -> Dict[str, str]:
        self._set_mapping()
        return self.mapping

    def run(self, tinyWorld:TinyWorld, updateDict:defaultdict) -> None:
        if not self.ppt:
            raise ValueError("No PPT provided to run the action.")
        logger.info(f"Running PersonaAction {self.type}...")

        # Update prompt and gpt_prompt with the mapping values and get a persona prompt to use
        if self.prompt: self.add_prompt(self.prompt.format_map(updateDict))
        if self.gpt_prompt: self.add_gpt_prompt(self.gpt_prompt.format_map(updateDict))
        # Update updateDict with self.update_mapping return
        updateDict.update(self.update_mapping())

        self.prompt = _get_prompt(gpt = self.gpt, gpt_prompt = self.gpt_prompt, prompt = self.prompt)
        logger.debug(f"Running PersonaAction {self.type} with prompt {self.prompt}")
        
        # Broadcast the prompt to the agents and run the tiny world
        logger.debug(f"Broadcasting prompt to agents and running tiny world...")
        tinyWorld.broadcast(self.ppt.ppt_and_slide_prompt())
        tinyWorld.broadcast(self.prompt)
        tinyWorld.run(1)

        # Extract results from agent response
        situation = f"The agent was tasked with {self.type_intent}"
        logger.debug(f"Extracting results from agent response with objective {default_objective} and situation {situation}")
        results_extractor = ResultsExtractor(
            extraction_objective = default_objective,
            situation = situation,
            fields = [self.type],
            verbose = False)
        self.result = results_extractor.extract_results_from_agents(tinyWorld.agents)

        # First format the original prompt
        formatted_prompt = self.summarization_gpt_prompt.format_map(updateDict)
        # Then append the agent response
        self.add_summarization_gpt_prompt(formatted_prompt + f"\nHere is the response from all the agents:\n{self.result}")
        logger.debug(f"Running summarization GPT prompt with prompt {self.summarization_gpt_prompt}")
        
        self.combined_result = self.gpt.run_conversation(self.ppt.ppt_prompt() + self.summarization_gpt_prompt)['response']
        
    def to_html(self) -> str:
        import markdown2
        html = f"""
        <div class="{self.type}-prompts">
            <details>
                <summary>Prompts</summary>
                <details>
                    <summary>GPT Prompt</summary>
                    <div class="prompt-content scrollable-content">
                        <pre>{self.gpt_prompt or 'Not provided'}</pre>
                    </div>
                </details>
                <details>
                    <summary>Prompt</summary>
                    <div class="prompt-content scrollable-content">
                        <pre>{self.prompt or 'Not provided'}</pre>
                    </div>
                </details>
                <details>
                    <summary>Summarization GPT Prompt</summary>
                    <div class="prompt-content scrollable-content">
                        <pre>{self.summarization_gpt_prompt or 'Not provided'}</pre>
                    </div>
                </details>
            </details>
            <details>
                <summary>Results</summary>
                <details>
                    <summary>Agent Results</summary>
                    <pretty-json>
                    {json.dumps(self.result, indent=4) if self.result else '{}'}
                    </pretty-json>
                </details>
                <details>
                    <summary>Combined Results</summary>
                    <div class="combined-results">
                        {markdown2.markdown(self.combined_result) if self.combined_result else 'No combined results'}
                    </div>
                </details>
            </details>
        </div>
        """
        return html

@dataclass
class PersonaAnalysis(PersonaAction):
    def __init__(self, 
                 gpt_prompt: Optional[str] = Constants.Prompts.TINY_TROUPE_ANALYSIS_GPT_PROMPT, prompt: Optional[str] = None, 
                 summarization_gpt_prompt: Optional[str] = Constants.Prompts.TINY_TROUPE_ANALYSIS_SUMMARIZATION_GPT_PROMPT, 
                 result: Optional[Any] = None, combined_result: Optional[str] = None):
        super().__init__('analysis', "Analyze a powerpoint presentation and provide feedback",
                         gpt_prompt, prompt, summarization_gpt_prompt, result, combined_result)

    @classmethod
    def load(cls, action_dict: Dict[str, Any]) -> 'PersonaAnalysis':
        return cls(
            gpt_prompt=action_dict.get(f'gpt_prompt', Constants.Prompts.TINY_TROUPE_ANALYSIS_GPT_PROMPT),
            prompt=action_dict.get(f'prompt', None),
            summarization_gpt_prompt=action_dict.get(f'summarization_gpt_prompt', Constants.Prompts.TINY_TROUPE_ANALYSIS_SUMMARIZATION_GPT_PROMPT),
            result=action_dict.get('result', None),
            combined_result=action_dict.get('combined_result', None)
        )
    
    def reset(self):
        super().reset()
        self.gpt_prompt = Constants.Prompts.TINY_TROUPE_ANALYSIS_GPT_PROMPT
        self.summarization_gpt_prompt = Constants.Prompts.TINY_TROUPE_ANALYSIS_SUMMARIZATION_GPT_PROMPT

@dataclass
class PersonaQNA(PersonaAction):
    def __init__(self, 
                 gpt_prompt: Optional[str] = Constants.Prompts.TINY_TROUPE_QNA_GPT_PROMPT, prompt: Optional[str] = None, 
                 summarization_gpt_prompt: Optional[str] = Constants.Prompts.TINY_TROUPE_QNA_SUMMARIZATION_GPT_PROMPT, 
                 result: Optional[Any] = None, combined_result: Optional[str] = None):
        super().__init__('qna', "Ask questions about a powerpoint presentation",
                         gpt_prompt, prompt, summarization_gpt_prompt, result, combined_result)

    @classmethod
    def load(cls, action_dict: Dict[str, Any]) -> 'PersonaQNA':
        return cls(
            gpt_prompt=action_dict.get(f'gpt_prompt', Constants.Prompts.TINY_TROUPE_QNA_GPT_PROMPT),
            prompt=action_dict.get(f'prompt', None),
            summarization_gpt_prompt=action_dict.get(f'summarization_gpt_prompt', Constants.Prompts.TINY_TROUPE_QNA_SUMMARIZATION_GPT_PROMPT),
            result=action_dict.get('result', None),
            combined_result=action_dict.get('combined_result', None)
        )

    def reset(self):
        super().reset()
        self.gpt_prompt = Constants.Prompts.TINY_TROUPE_QNA_GPT_PROMPT
        self.summarization_gpt_prompt = Constants.Prompts.TINY_TROUPE_QNA_SUMMARIZATION_GPT_PROMPT
