from dataclasses import dataclass
from typing import Optional, Dict, Any
from uuid import uuid4
import logging
import os

from backend.utils.Persona import Persona, PersonaType
from backend.utils.GPTPersonaAction import GPTPersonaAnalysis, GPTPersonaQNA
from backend.utils.PPT import PPT
from backend.utils.GPT import GPT
from backend.utils import Constants

logger = logging.getLogger(__name__)

@dataclass
class GPTPersona(Persona):
    prompt: Optional[str] = None
    result: Optional[str] = None
    analysis: Optional[GPTPersonaAnalysis] = None
    qna: Optional[GPTPersonaQNA] = None
    ppt: Optional[PPT] = None
    mapping: Optional[Dict[str, str]] = None
    mappingDict: Optional[Any] = None

    def __init__(self, name: str, description: str, 
                 id: Optional[str]=None,
                 prompt: Optional[str] = '', result: Optional[str] = '',
                 analysis: Optional[GPTPersonaAnalysis] = None, qna: Optional[GPTPersonaQNA] = None,
                 ppt: Optional[PPT] = None, gpt: Optional[GPT] = None) -> None:
        super().__init__(name=name, description=description, id=id, type=PersonaType.GPT)
        self.prompt = prompt
        self.result = result
        self.gpt = GPT()
        self.analysis = analysis or GPTPersonaAnalysis()
        self.qna = qna or GPTPersonaQNA()
        self.ppt = ppt
        self.gpt = gpt or GPT(f"GPT Assistant {self.type}", Constants.Prompts.GPT.GPT_INFO)
        self._set_mapping()

    @classmethod
    def load(cls, persona_dict: Dict[str, Any], root_folder: str = None) -> 'GPTPersona':
        return cls(
            id=persona_dict.get('id', None),
            name=persona_dict.get('name', ''),
            description=persona_dict.get('description', ''),
            prompt=persona_dict.get('prompt', ''),
            result=persona_dict.get('result', ''),
            analysis=GPTPersonaAnalysis.load(persona_dict.get('analysis', {})),
            qna=GPTPersonaQNA.load(persona_dict.get('qna', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type.value,
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'prompt': self.prompt,
            'result': self.result,
            'analysis': self.analysis.to_dict(),
            'qna': self.qna.to_dict()
        }

    def add_prompt(self, prompt: str) -> None: self.prompt = prompt
    def remove_prompt(self): self.prompt = ''
    def add_result(self, result: str) -> None: self.result = result
    def remove_result(self) -> None: self.result = ''
    def add_ppt(self, ppt: PPT) -> None: self.ppt = ppt
    def remove_ppt(self) -> None: self.ppt = None
    def add_gpt(self, gpt: GPT) -> None: self.gpt = gpt
    def remove_gpt(self) -> None: self.gpt = None
    def reset_prompts(self):
        self.remove_prompt()

    def add_ppt(self, ppt: PPT) -> None:
        self.ppt = ppt
        self.analysis.add_ppt(ppt)
        self.qna.add_ppt(ppt)

    def reset(self):
        self.reset_prompts()
        self.analysis.reset()
        self.qna.reset()
        self.update_mapping()

    def _set_mapping(self) -> None:
        self.mapping = {
            'persona_name': self.name,
            'persona_description': self.description,
            'persona_prompt': self.prompt,
            'persona_result': self.result
        }
        if self.analysis: self.mapping.update(self.analysis.update_mapping())
        if self.qna: self.mapping.update(self.qna.update_mapping())
        if self.ppt: self.mapping.update(self.ppt.update_mapping())
        self.mappingDict = dict(self.mapping)

    def update_mapping(self) -> Dict[str, str]:
        self._set_mapping()
        return self.mappingDict

    def save(self, folder: str=None):
        return self.to_dict()

    def run(self):
        self.id = str(uuid4())
        logger.info(f"Running GPT Persona {self.name}...")
        
        if not self.ppt:
            raise ValueError("PPT must be provided to persona.")
        
        self.update_mapping()

        # Generate Persona
        logger.debug("Generating persona...")
        if not self.gpt: self.gpt = GPT(f"GPT Assistant {self.type}", Constants.Prompts.GPT.GPT_INFO)
        self.analysis.add_gpt(self.gpt) # Set GPT to continue conversation
        self.qna.add_gpt(self.gpt) # Set GPT to continue conversation

        if not self.prompt: self.prompt = Constants.Prompts.GPT.PERSONA_PROMPT
        self.add_prompt(self.prompt.format_map(self.mappingDict))
        logger.debug("GPT Persona Prompt: " + self.prompt)

        self.result = self.gpt.run_conversation(self.ppt.ppt_prompt() + self.prompt)['response']
        logger.debug("GPT Persona Result: " + self.result)

        # Run analysis
        logger.debug("Running analysis...")
        self.update_mapping()
        self.analysis.run(updateDict=self.mappingDict)
        
        # Run QNA
        logger.debug("Running QNA...")
        self.update_mapping()
        self.qna.run(updateDict=self.mappingDict)

    def to_html(self) -> str:
        html = f"""
        <div class="persona">
            <details>
                <summary>{self.name.capitalize()}</summary>
                
                <div class="persona-prompts">
                    <details>
                        <summary>Persona Prompts</summary>
                        <details>
                            <summary>Prompt</summary>
                            <div class="prompt-content scrollable-content">
                                <pre>{self.prompt or 'Not provided'}</pre>
                            </div>
                        </details>
                        <details>
                            <summary>Persona</summary>
                            <div class="prompt-content scrollable-content">
                                <pre>{self.result or 'Not provided'}</pre>
                            </div>
                        </details>
                    </details>
                </div>

                <div class="analysis">
                    <details>
                        <summary>Analysis</summary>
                        {self.analysis.to_html() if self.analysis else 'No analysis'}
                    </details>
                </div>

                <div class="qna">
                    <details>
                        <summary>QNA</summary>
                        {self.qna.to_html() if self.qna else 'No QNA'}
                    </details>
                </div>
            </details>
        </div>
        """
        return html
