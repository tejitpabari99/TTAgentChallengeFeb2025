import os, json, logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Union, Dict, List, Optional, Any
from uuid import uuid4
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.environment import TinyWorld
from tinytroupe.extraction import ResultsExtractor

from backend.utils.PersonaAction import PersonaAnalysis, PersonaQNA
from backend.utils.PPT import PPT
from backend.utils.Agent import Agent
from backend.utils.GPT import GPT
from backend.utils import Constants
from backend.utils.utils import _ensure_keys_exist, _get_prompt

default_criteria = "Return an array of json objects."
default_population_size = 5

logger = logging.getLogger(__name__)

@dataclass
class Persona:
    name: str
    description: str
    id: Optional[str] = None
    prompt: Optional[str] = None
    gpt_prompt: Optional[str] = None
    population_size: Optional[int] = default_population_size
    agents: Optional[List[Agent]] = None
    analysis: Optional[PersonaAnalysis] = None
    qna: Optional[PersonaQNA] = None
    ppt: Optional[PPT] = None
    mapping: Optional[Dict[str, str]] = None
    mappingDict: Optional[Any] = None


    def __init__(self, name: str, description: str, id: Optional[str]=None, 
                 prompt: Optional[str] = '', gpt_prompt: Optional[str] = '',
                 population_size: int = default_population_size, agents: Optional[List[Agent]] = [],
                 analysis: Optional[PersonaAnalysis] = None, qna: Optional[PersonaQNA] = None,
                 ppt: Optional[PPT] = None) -> None:
        self.id = id or str(uuid4())
        self.name = name
        self.description = description
        self.prompt = prompt
        self.gpt_prompt = gpt_prompt
        self.population_size = population_size
        self.agents = agents
        self.analysis = analysis
        self.qna = qna
        self.ppt = ppt
        self.gpt = GPT(f"GPT Assistant {self.name}", Constants.Prompts.TINY_TROUPE_INFO)
        self._set_mapping()
        self.mappingDict = defaultdict(lambda: "MISSING", self.mapping)
        self.tinyWorld = None
        self.tinyFactory = None

    @classmethod
    def load(cls, persona_dict: Dict[str, Any], root_folder: str = None) -> 'Persona':
        _ensure_keys_exist(persona_dict, ['name', 'description'], 
                               "Personas must have name and description.")
        logger.info(f"Loading Persona {persona_dict.get('name')}...")
        return cls(
            id=persona_dict.get('id', None),
            name=persona_dict.get('name', ''),
            description=persona_dict.get('description', ''),
            prompt=persona_dict.get('prompt', ''),
            gpt_prompt=persona_dict.get('gpt_prompt', ''),
            population_size=persona_dict.get('population_size', default_population_size),
            agents=[Agent.load(s, root_folder=root_folder) for s in persona_dict.get('agents', [])],
            analysis=PersonaAnalysis.load(persona_dict.get('analysis', {})),
            qna=PersonaQNA.load(persona_dict.get('qna', {}))
        )
        
    def save(self, folder:str):
        logger.info(f"Saving Persona {self.name} to {folder}...")
        if not os.path.exists(folder): raise ValueError(f"Folder {folder} not found.")
        
        persona_folder = f"{folder}/{self.name.replace(' ', '_')}"
        if not os.path.exists(persona_folder): os.makedirs(persona_folder)
        
        agent_folder = f"{persona_folder}/agents"
        if not os.path.exists(agent_folder): os.makedirs(agent_folder)
        logger.debug(f"Saving Persona Agents to {agent_folder}...")
        
        for agent in self.agents:
            agent.save(f"{agent_folder}/{agent.name.replace(' ', '_')}.json")
        return self.to_dict()


    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'prompt': self.prompt,
            'gpt_prompt': self.gpt_prompt,
            'population_size': self.population_size,
            'agents': [s.to_dict() for s in self.agents],
            'analysis': self.analysis.to_dict(),
            'qna': self.qna.to_dict()
        }

    def add_prompt(self, prompt: str) -> None: self.prompt = prompt
    def remove_prompt(self): self.prompt = ''
    def add_gpt_prompt(self, gpt_prompt: str) -> None: self.gpt_prompt = gpt_prompt
    def remove_gpt_prompt(self): self.gpt_prompt = ''
    def reset_prompts(self):
        self.remove_prompt()
        self.remove_gpt_prompt()

    def set_population_size(self, population_size: int) -> None: self.population_size = population_size
    def add_ppt(self, ppt: PPT) -> None:
        self.ppt = ppt
        self.analysis.add_ppt(ppt)
        self.qna.add_ppt(ppt)
    def add_agents(self, agents: List[Agent]) -> None: 
        self.agents.extend(agents)
    def add_agent(self, agent: Agent) -> None: 
        return self.add_agents([agent])
    def remove_agents(self): self.agents = []
    def reset_agents(self): self.agents = []

    def create_tiny_world(self): return TinyWorld(f"TinyWorld {self.name}", 
                                                  [agent.tinyPerson for agent in self.agents], 
                                                  broadcast_if_no_target=False)

    def reset(self):
        self.reset_prompts()
        self.reset_agents()
        self.analysis.reset()
        self.qna.reset()
        self.update_mapping()

    def _set_mapping(self) -> None:
        self.mapping = {
            f'persona_name': self.name,
            f'persona_description': self.description,
            f'persona_prompt': self.prompt,
            f'persona_gpt_prompt': self.gpt_prompt,
            f'persona_population_size': str(self.population_size),
        }
        if self.analysis: self.mapping.update(self.analysis.update_mapping())
        if self.qna: self.mapping.update(self.qna.update_mapping())
        if self.ppt: self.mapping.update(self.ppt.update_mapping())
        self.mappingDict = defaultdict(lambda: "MISSING", self.mapping)

    def update_mapping(self) -> Dict[str, str]:
        self._set_mapping()
        return self.mappingDict

    def run(self, use_existing_agents:bool=True):
        self.id = str(uuid4())
        logger.info(f"Running Persona {self.name}...")
        
        # Check if PPT is provided
        if not self.ppt: raise ValueError("PPT must be provided to persona.")
        additional_prompts = [self.ppt.ppt_and_slide_prompt()]
        
        self.update_mapping() # Update mapping of variables to substitute in prompts

        if self.agents and use_existing_agents:
            logger.debug("Using existing agents...")
            # Agents should already be added to the tiny world
        else:
            # Update prompt and gpt_prompt with the mapping values and get a persona prompt to use
            if self.prompt: self.add_prompt(self.prompt.format_map(self.mappingDict))
            if not self.gpt_prompt: self.gpt_prompt = Constants.Prompts.TINY_TROUPE_PERSONA_GPT_PROMPT.format_map(self.mappingDict)
            if self.gpt_prompt: self.add_gpt_prompt(self.gpt_prompt.format_map(self.mappingDict))
            self.prompt = _get_prompt(gpt = self.gpt, gpt_prompt = self.gpt_prompt, prompt = self.prompt,
                                        additional_prompts=additional_prompts)
            logger.debug(f"Generating {self.population_size} new agents with prompt {self.prompt}")
            
            # Generate agents with persona prompt
            tinyPersonFac = TinyPersonFactory(self.prompt)
            self.agents = [Agent.create(t) for t in tinyPersonFac.generate_people(self.population_size)]
        
        # After agents have been created, create tiny world with agents.
        self.tinyWorld = self.create_tiny_world()

        # Analyze and summarize
        logger.debug("Analyzing and summarizing...")
        self.update_mapping() # Update mapping of variables to substitute in prompts
        self.analysis.run(tinyWorld = self.tinyWorld, updateDict=self.mappingDict)
        
        # Ask questions and summarize
        logger.debug("Asking questions and summarizing...")
        self.update_mapping() # Update mapping of variables to substitute in prompts
        self.qna.run(tinyWorld = self.tinyWorld, updateDict=self.mappingDict)

    def to_html(self) -> str:
        html = f"""
        <div class="persona">
            <details>
                <summary>{self.name.capitalize()}</summary>
                
                <div class="persona-prompts">
                    <details>
                        <summary>Persona Prompts</summary>
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
                    </details>
                </div>

                <div class="agents">
                    <details>
                        <summary>Agents (Population size: {self.population_size})</summary>
                        {''.join([agent.to_html() for agent in self.agents]) if self.agents else 'No agents'}
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
