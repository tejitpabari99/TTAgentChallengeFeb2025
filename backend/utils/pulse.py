from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
import json, os, logging
from tinytroupe.environment import TinyWorld
from backend.utils.Persona import Persona
from backend.utils.PPT import PPT
from uuid import uuid4

logger = logging.getLogger(__name__)

@dataclass
class Pulse:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    ppt: Optional[PPT] = None
    personas: Optional[List[Persona]] = None
    debug: Optional[bool] = False

    default_population_size = 5

    def __init__(self, name:str = None, description:str =None, ppt:PPT=None, personas:List[Persona]=[], 
                 id: str=None, debug: bool=False) -> None:
        self.id = id or str(uuid4())
        self.name = name
        self.description = description
        self.ppt = ppt
        self.personas = personas
        self.debug = debug
        if self.ppt:
            for persona in self.personas:
                persona.add_ppt(self.ppt)
    
    @classmethod
    def load(cls, path_or_dict: Union[str, Dict[str, Any]], root_folder=None) -> 'Pulse':
        logger.info("Loading Pulse...")
        if isinstance(path_or_dict, str):
            if not root_folder:
                root_folder = os.path.dirname(path_or_dict)  # Get parent directory path
            if os.path.isdir(path_or_dict):
                path_or_dict = os.path.join(path_or_dict, 'pulse_spec.json')
            if not os.path.exists(path_or_dict): raise ValueError(f"File {path_or_dict} not found.")
            path_or_dict = json.load(open(path_or_dict, "r", encoding='utf-8'))
        ppt = path_or_dict.get('ppt', {})
        pul = cls(
            id=path_or_dict.get('id', None),
            name=path_or_dict.get('name', ''),
            description=path_or_dict.get('description', ''),
            ppt=PPT.load(ppt) if ppt else None,
            personas=[Persona.load(persona, root_folder=root_folder) for persona in path_or_dict.get('personas', [])]
        )
        for persona in pul.personas:
            persona.add_ppt(pul.ppt)
        return pul
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ppt': self.ppt.to_dict(),
            'personas': [persona.to_dict() for persona in self.personas]
        }
    
    def save(self, folder: str, save_to_html=True) -> None:
        logger.info(f"Saving Pulse {self.id} to {folder}...")
        if not os.path.exists(folder):
            raise ValueError(f"Folder {folder} does not exist.")
        pulse_folder = os.path.join(folder, str(self.id))
        os.makedirs(pulse_folder, exist_ok=True)
        
        logger.debug(f"Saving Pulse {self.id} personas.")
        for persona in self.personas:
            persona.save(pulse_folder)
        
        logger.debug(f"Saving Pulse {self.id} spec.")
        with open(os.path.join(pulse_folder, 'pulse_spec.json'), 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f)
        if save_to_html:
            self.save_html(os.path.join(pulse_folder, 'pulse_html.html'))
    
    def save_html(self, file:str) -> None:
        logger.info(f"Saving Pulse {self.id} to HTML {file}...")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(self.to_html())

    def run(self):
        self.id = str(uuid4())
        logger.info(f"Running Pulse {self.id}...")
        for persona in self.personas:
            persona.run()
    
    def reset(self):
        logger.info(f"Resetting Pulse {self.id}...")
        for persona in self.personas:
            persona.reset()

    def to_html(self) -> str:
        import markdown2

        result_html = '\n'.join(
                    f"""<details open>
                        <summary>{persona.name.capitalize()}</summary>
                        <details>
                            <summary>Analysis Results</summary>
                            <div class="combined-results">
                                {markdown2.markdown(persona.analysis.combined_result) if persona.analysis and persona.analysis.combined_result else 'No analysis results'}
                            </div>
                        </details>
                        <details>
                            <summary>QNA Results</summary>
                            <div class="combined-results">
                                {markdown2.markdown(persona.qna.combined_result) if persona.qna and persona.qna.combined_result else 'No QNA results'}
                            </div>
                        </details>
                    </details>"""
                    for persona in (self.personas or [])
                )
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{f"{self.name} - " if self.name else ""}Pulse ({self.id})</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                details {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                summary {{ cursor: pointer; padding: 5px; }}
                pre {{ white-space: pre-wrap; background: #f5f5f5; padding: 10px; }}
                .combined-results {{ margin: 10px 0; }}
                .scrollable-content {{
                    max-height: 12em;  /* approximately 8 lines */
                    overflow-y: auto;
                    border: 1px solid #eee;
                    padding: 10px;
                    margin: 5px 0;
                }}
                .ppt-content, .prompt-content, .result-content {{
                    max-height: 12em;
                    overflow-y: auto;
                    border: 1px solid #eee;
                    padding: 10px;
                    margin: 5px 0;
                }}
            </style>
            <script defer src="https://unpkg.com/pretty-json-custom-element/index.js"></script>
        </head>
        <body>
            <h1>{f"{self.name} - " if self.name else ""}Pulse ({self.id})</h1>

            <details>
                <summary>Pulse Information</summary>
                {f"<p><strong>Name:</strong> {self.name}</p>" if self.name else ""}
                {f"<p><strong>Description:</strong> {self.description}</p>" if self.description else ""}
            </details>

            {self.ppt.to_html() if self.ppt else ""}

            <div class="personas">
                <h2>Personas</h2>
                {''.join([persona.to_html() for persona in self.personas]) if self.personas else 'No personas'}
            </div>

            <div class="results">
                <h2>Results</h2>
                {result_html}
            </div>
        </body>
        </html>
        """
        return html

    def add_name(self, name: str) -> None: self.name = name
    def add_description(self, description: str) -> None: self.description = description
    def add_ppt(self, ppt: Union[PPT, Dict[str, Any]]) -> None: 
        if isinstance(ppt, dict):
            self.ppt = PPT.load(ppt)
        else:
            self.ppt = ppt

    def add_persona(self, persona: Union[Dict[str, Any], Persona]) -> None: 
        if isinstance(persona, dict):
            persona = Persona.load(persona)
        self.personas.append(self._add_persona_defaults(persona))
    def _add_persona_defaults(self, persona:Persona) -> 'Persona':
        persona.add_ppt(self.ppt)
        return persona
    def add_personas(self, personas: List[Persona]) -> None: self.personas.extend(personas)
    def remove_personas(self) -> None: self.personas = []
