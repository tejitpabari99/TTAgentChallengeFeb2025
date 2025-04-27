import os, json, logging
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from uuid import uuid4

from backend.utils.utils import _ensure_keys_exist
from tinytroupe.agent import TinyPerson
from tinytroupe.factory import TinyPersonFactory

logger = logging.getLogger(__name__)

@dataclass
class Agent:
    name: str
    description: str
    id: Optional[str] = None
    file: Optional[str] = None
    root_folder: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    tinyPerson: Optional[TinyPerson] = None

    def __init__(self, name: str, description: str, id: Optional[str]=None, file: Optional[str]=None, root_folder: Optional[str]=None, data: Optional[Dict[str, Any]] = None, tinyPerson=None):
        self.id = id or str(uuid4())
        self.name = name
        self.description = description
        self.file = file
        self.root_folder = root_folder
        self.data = data or self._load_agent_data_from_file()
        self.tinyPerson = tinyPerson or self._load_tinyTroupe_agent_from_data()
    
    @classmethod
    def load(cls, file_or_dict: Union[str, Dict[str, str]], root_folder: str = None) -> 'Agent':
        if isinstance(file_or_dict, dict):
            _ensure_keys_exist(file_or_dict, ['id', 'name', 'description', 'file'], 
                               "Agents cannot be loaded without id, name, description and file. If you are creating an agent, using the create method.")
            logger.info(f"Loading Agent from agent dictionary...")
            return cls(
                id=file_or_dict['id'],
                name=file_or_dict['name'],
                description=file_or_dict['description'],
                file=file_or_dict['file'],
                root_folder=root_folder
            )
        elif isinstance(file_or_dict, str):
            logger.info(f"Loading Agent from file {file_or_dict}...")
            
            if root_folder: file_path = Path(root_folder) / file_or_dict
            else: file_path = file_or_dict
            if not os.path.exists(file_path): raise ValueError(f"File {file_or_dict} not found.")
             
            tinyperson:TinyPerson = None
            data:dict = None
            try:
                data = json.load(open(file_path, "r", encoding='utf-8'))
                tinyperson = TinyPerson.load_specification(data, suppress_memory=True)
            except Exception as e:
                raise Exception(f"Error loading agent from file: {file_or_dict}. Error: {e}")
            name = tinyperson.get('name', '')
            description = tinyperson.minibio()
            return cls(id=None, name=name, description=description, file=file_or_dict, root_folder=root_folder, 
                       data=data, tinyPerson=tinyperson)
        
    @classmethod
    def create(cls, prompt_or_tinyPerson: Union[TinyPerson, str]) -> 'Agent':
        try:
            if isinstance(prompt_or_tinyPerson, TinyPerson):
                logger.info(f"Creating Agent from TinyPerson...")
                tinyPerson = prompt_or_tinyPerson
                name = tinyPerson.get('name')
                description = tinyPerson.minibio()
                data = tinyPerson.to_json()
                return cls(id=None, name=name, description=description, file=None, data=data, tinyPerson=tinyPerson)
            elif isinstance(prompt_or_tinyPerson, str):
                logger.info(f"Creating Agent from prompt...")
                prompt = prompt_or_tinyPerson
                tinyPersonFac = TinyPersonFactory(prompt)
                tinyperson:TinyPerson = tinyPersonFac.generate_person()
                name = tinyperson.get('name')
                description = tinyperson.minibio()
                data = tinyperson.to_json()
                return cls(id=None, name=name, description=description, file=None, data=data, tinyPerson=tinyperson)
            else:
                raise ValueError("Prompt must be a TinyPerson object or a string.")
        except Exception as e:
            raise Exception(f"Error creating agent from prompt: {prompt_or_tinyPerson}. Error: {e}")

    def to_dict(self) -> Dict[str, str]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'file': self.file,
        }

    def save(self, file=None) -> None:
        logger.info(f"Saving Agent {self.name} to {file}...")
        if not file: file = self.file
        if not file: raise ValueError("Agent file not valid.")
        self.file = file
        # Data is already checked since creating any TinyTroupe class instance creates data
        with open(file, "w", encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        return self.to_dict()

    def _load_agent_data_from_file(self):
        if self.file: 
            file_path = Path(self.root_folder) / self.file
            return json.load(open(file_path, "r", encoding='utf-8'))

    def _load_tinyTroupe_agent_from_data(self):
        if self.data: return TinyPerson.load_specification(self.data, suppress_memory=True)

    def to_html(self) -> str:
        html = f"""
        <div class="agent">
            <details>
                <summary>Agent: {self.name}</summary>
                <p><strong>ID:</strong> {self.id}</p>
                <p><strong>Description:</strong> {self.description}</p>
            </details>
        </div>
        """
        return html
