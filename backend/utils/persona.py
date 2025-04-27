import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, Union
from enum import Enum
from uuid import uuid4

from backend.utils.utils import _ensure_keys_exist

logger = logging.getLogger(__name__)

class PersonaType(Enum):
    GPT = "gpt"
    TINY_TROUPE = "tinytroupe"

default_type = PersonaType.GPT

@dataclass
class Persona:
    """Base Persona class with core attributes. Specialized personas like TinyTroupePersona inherit from this."""
    name: str
    description: str
    id: Optional[str] = None
    type: Optional[PersonaType] = None

    def __new__(cls, name: str, description: str,
                id: Optional[str]=None, type: Optional[Union[PersonaType, str]] = None, **kwargs):
        """Create a new persona instance of the appropriate type."""
        if type and cls == Persona:
            # If type is specified and we're creating directly from Persona class
            if isinstance(type, str):
                type = PersonaType(type.lower().strip())
            if type == PersonaType.TINY_TROUPE:
                from backend.utils.TinyTroupePersona import TinyTroupePersona
                return TinyTroupePersona(name=name, description=description, id=id, **kwargs)
            elif type == PersonaType.GPT:
                from backend.utils.GPTPersona import GPTPersona
                return GPTPersona(name=name, description=description, id=id, **kwargs)
        # Otherwise proceed with normal instance creation
        return super().__new__(cls)

    def __init__(self, name: str, description: str, 
                 id: Optional[str]=None, type: Optional[Union[PersonaType, str]] = None, **kwargs) -> None:
        if type and isinstance(type, str):
            type = PersonaType(type.lower().strip())
        self.type = type if type else default_type
        self.id = id or str(uuid4())
        self.name = name
        self.description = description

    @classmethod
    def create(cls, name: str, description: str, type: Union[PersonaType, str] = None, **kwargs) -> Union['Persona', Any]:
        """Factory method to create a persona of the specified type."""
        return cls(name=name, description=description, type=type, **kwargs)

    @classmethod
    def load(cls, persona_dict: Dict[str, Any], root_folder: str = None) -> Union['Persona', Any]:
        """Load a persona from a dictionary. Returns either a base Persona or a specialized type based on the 'type' field."""
        _ensure_keys_exist(persona_dict, ['name', 'description'], 
                         "Personas must have name and description.")
        
        persona_type = persona_dict.get('type', default_type)
        if isinstance(persona_type, str):
            persona_type = PersonaType(persona_type.lower().strip())

        # Import here to avoid circular imports
        if persona_type == PersonaType.TINY_TROUPE:
            from backend.utils.TinyTroupePersona import TinyTroupePersona
            return TinyTroupePersona.load(persona_dict, root_folder)
        elif persona_type == PersonaType.GPT:
            from backend.utils.GPTPersona import GPTPersona
            return GPTPersona.load(persona_dict, root_folder)
        else:
            return cls(
                id=persona_dict.get('id', None),
                name=persona_dict.get('name', ''),
                description=persona_dict.get('description', ''),
                type=persona_type
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary representation."""
        return {
            'type': self.type.value,
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def add_type(self, type: Union[PersonaType, str]) -> None:
        """Set the persona type."""
        if isinstance(type, str):
            type = PersonaType(type.lower().strip())
        self.type = type
        return self.convert_to(self.type)

    def convert_to(self, type: Union[PersonaType, str]) -> Union['Persona', Any]:
        """Convert this persona to a different type."""
        if isinstance(type, str):
            type = PersonaType(type.lower().strip())
        
        if type == self.type:
            return self
            
        # Create a new persona of the desired type with the same base attributes
        return Persona.create(
            name=self.name,
            description=self.description,
            id=self.id,
            type=type
        )

    # Stub methods that specialized personas implement
    def add_ppt(self, ppt: Any) -> None:
        """Add a PPT to the persona. Implemented by specialized personas."""
        raise NotImplementedError("This persona type does not support PPT.")

    def run(self, **kwargs) -> None:
        """Run the persona. Implemented by specialized personas."""
        raise NotImplementedError("This persona type does not support running.")

    def save(self, folder: str) -> Dict[str, Any]:
        """Save the persona. Implemented by specialized personas."""
        raise NotImplementedError("This persona type does not support saving.")

    def to_html(self) -> str:
        """Convert persona to HTML representation. Implemented by specialized personas."""
        return f"""
        <div class="persona">
            <details>
                <summary>{self.name.capitalize()}</summary>
                <p>Type: {self.type.value}</p>
                <p>Description: {self.description}</p>
            </details>
        </div>
        """
