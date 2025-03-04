import os, json
from uuid import uuid4
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsExtractor
from tinytroupe.agent import TinyPerson

default_criteria = "Return an array of json objects."
default_population_size = 5

class Persona:
    def __init__(self, persona_type=None, persona_description=None, persona_id=None, population_size = default_population_size, persona_folder=None):
        if persona_folder:
            self.load_persona(persona_folder)
            return
        elif persona_type and persona_description:
            self.persona_spec = {
                'persona_type': persona_type,
                'persona_description': persona_description,
                'persona_id': persona_id or str(uuid4()),
                'population_size': population_size,
                'population_folder': None,
                'prompts': {}
            }
            self.factory: TinyPersonFactory = None
            self.population:list[TinyPerson] = []
            print(f"Persona created with id: {self.persona_spec['persona_id']} type: {self.persona_spec['persona_type']}, description: {self.persona_spec['persona_description']}")
        else:
            raise ValueError("Persona type and description or persona spec file must be provided to create a persona.")

    def load_persona(self, persona_folder):
        persona_spec_file = f"{persona_folder}/persona_spec.json"
        if not os.path.exists(persona_spec_file):
            raise ValueError("Persona spec file not found in persona folder.")
        self.load_specifications(persona_spec_file)
        self.load_population()
        if not self.persona_spec.get('persona_type', None):
            raise ValueError("Persona type not found in persona spec.")
        if not self.persona_spec.get('persona_description', None):
            raise ValueError("Persona description not found in persona spec.")
        if not self.persona_spec.get('persona_id', None):
            raise ValueError("Persona id not found in persona spec.")
        print(f"Persona loaded with id: {self.persona_spec['persona_id']} type: {self.persona_spec['type']}, description: {self.persona_spec['description']}")

    def save_persona(self, persona_folder=None):
        if not persona_folder: persona_folder = f"persona_{self.persona_spec['persona_type'].replace(' ', '_')}_{self.persona_spec['persona_id']}"
        if not os.path.exists(persona_folder): os.makedirs(persona_folder)

        persona_spec_file = f"{persona_folder}/persona_spec.json"
        self.save_specificatons(persona_spec_file)
        self.save_population(self.persona_spec.get('population_folder', f"{persona_folder}/population"))
        
        return persona_folder

    def load_specifications(self, persona_spec_file):
        self.persona_spec = json.load(open(persona_spec_file, "r", encoding='utf-8'))
        return self.persona_spec

    def save_specificatons(self, persona_spec_file):
        json.dump(self.persona_spec, open(persona_spec_file, "w", encoding='utf-8'), indent=4)

    def get_specification(self):
        return self.persona_spec

    def load_population(self, population_folder=None):
        population_folder = self._get_folder('population_folder', population_folder)
        self.persona_spec['population_folder'] = population_folder

        self.population = []
        for file in os.listdir(population_folder):
            if file.endswith(".json"):
                self.population.append(TinyPerson.load_specification(f"{population_folder}/{file}"))
        return self.population
    
    def save_population(self, population_folder=None, include_memory=False):
        population_folder = self._get_folder('population_folder', population_folder)
        for pop in self.population:
            name = pop.get('name')
            pop.save_specification(f"{population_folder}/{name.strip().replace(' ', '_')}.json", include_memory=include_memory)

    def _get_folder(self, folder_name, folder=None):
        if not folder: folder = self.persona_spec.get(folder_name, None)
        if not folder: 
            raise ValueError(f"{folder_name} not provided or found in persona_spec.")
        if not os.path.exists(folder):
            raise ValueError(f"{folder_name} folder not found.")
        return folder

    def load_prompts(self, prompts_dict=None):
        """Load prompts from a dictionary or use empty prompts if not provided"""
        if not prompts_dict:
            prompts_dict = {}
        
        self.persona_spec['prompts'] = {
            'persona_prompt': prompts_dict.get('persona_prompt', ''),
            'persona_gpt_prompt': prompts_dict.get('persona_gpt_prompt', ''),
            'analysis_prompt': prompts_dict.get('analysis_prompt', ''),
            'analysis_gpt_prompt': prompts_dict.get('analysis_gpt_prompt', ''),
            'analysis_criteria': prompts_dict.get('analysis_criteria', default_criteria),
            'qna_prompt': prompts_dict.get('qna_prompt', ''),
            'qna_gpt_prompt': prompts_dict.get('qna_gpt_prompt', ''),
            'qna_criteria': prompts_dict.get('qna_criteria', default_criteria)
        }

    def update_prompts(self, prompts_dict):
        """Update specific prompts in the persona spec"""
        if not self.persona_spec.get('prompts'):
            self.persona_spec['prompts'] = {}
        
        for key, value in prompts_dict.items():
            if key in ['persona_prompt', 'persona_gpt_prompt', 
                      'analysis_prompt', 'analysis_gpt_prompt', 'analysis_criteria',
                      'qna_prompt', 'qna_gpt_prompt', 'qna_criteria']:
                self.persona_spec['prompts'][key] = value

    def change_population_size(self, population_size):
        self.persona_spec['population_size'] = population_size

    def create_factory(self):
        persona_prompt = self.persona_spec.get('persona_prompt', None)
        if not persona_prompt:
            raise ValueError("Persona prompt not found in persona spec.")
        return TinyPersonFactory(persona_prompt)

    def create_population(self, force=False):
        if not force and self.population:
            raise ValueError("Population already exists. Use force=True to recreate population.")
        if not self.factory:
            self.factory = self.create_factory()
        population_size = self.persona_spec.get('population_size', default_population_size)
        self.population = self.factory.generate_people(population_size)
        return self.population

    def analysis_result_extractor(self, extraction_objective=None, situation=None, fields=None, fields_hints=None, verbose=False):
        if not extraction_objective:
            extraction_objective = self.persona_spec['prompts'].get('analysis_criteria', default_criteria)
        if not situation:
            situation = "The agent was tasked with analyzing a powerpoint presentation to provide feedback on the content of the presentation and the presentation itself."
        if not fields:
            fields = ['analysis']
        if not field_hints:
            field_hints = {'analysis': self.persona_spec['prompts'].get('analysis_criteria', default_criteria)}
        return ResultsExtractor(extraction_objective=extraction_objective, situation=situation, 
                                fields=fields, field_hints=field_hints, verbose=verbose)
    
    def qna_result_extractor(self, extraction_objective=None, situation=None, fields=None, fields_hints=None, verbose=False):
        if not extraction_objective:
            extraction_objective = self.persona_spec['prompts'].get('qna_criteria', default_criteria)
        if not situation:
            situation = "The agent was tasked with asking questions after analyzing powerpoint presentation, about the content of the presentation and the presentation itself."
        if not fields:
            fields = ['qna']
        if not field_hints:
            field_hints = {'qna': self.persona_spec['prompts'].get('qna_criteria', default_criteria)}
        return ResultsExtractor(extraction_objective=extraction_objective, situation=situation, 
                                fields=fields, field_hints=field_hints, verbose=verbose)
