import json
from tinytroupe.environment import TinyWorld
from backend.utils.persona import Persona
from backend.utils.ppt import PPT
from uuid import uuid4

class Pulse:

    default_population_size = 5

    def __init__(self, name:str=None, ppt:PPT=None, pulse_id=None, 
                 pulse_folder=None, load_from_folder=False):
        self.name = name
        self.pulse_id = pulse_id if pulse_id else str(uuid4())
        self.ppt = ppt

        self.personas = {}

    def load_pulse_spec(self, pulse_spec_file):
        pulse_spec = json.load(open(pulse_spec_file, "r", encoding='utf-8'))
        self.name = pulse_spec.get('name', None)
        self.pulse_id = pulse_spec.get('pulse_id', None)
        self.ppt = PPT(pulse_spec.get('ppt_details', None), pulse_spec.get('ppt_json', None))

    def save_pulse_spec(self, pulse_spec_file):
        pulse_spec = {
            'name': self.name,
            'pulse_id': self.pulse_id,
            'ppt_details': self.ppt.ppt_details,
            'ppt_json': self.ppt.ppt_json,
        }
        with open(pulse_spec_file, "w", encoding='utf-8') as f:
            json.dump(pulse_spec, f, indent=4)

    def load_pulse_from_folder(self, pulse_folder):
        self.load_pulse_spec(f"{self.pulse_folder}/pulse_spec.json")
        for file in os.listdir(self.pulse_folder):
            if file.endswith(".json") and file != "pulse_spec.json":
                persona = Persona.load_persona_specification(f"{self.pulse_folder}/{file}")
                self.personas.append(persona)

    def create_persona(self, persona_type, persona_guidelines, population_size=default_population_size,
                 prompt_folder=None, generate_from_prompt_folder=False,
                 persona_folder=None, load_persona_from_persona_folder=False):
        return Persona(persona_type, persona_guidelines, 
                       self.ppt, population_size, 
                       prompt_folder, generate_from_prompt_folder, 
                       persona_folder, load_persona_from_persona_folder)

    def load_personas(self, persona_spec_file, persona_folder):


