import os, json, logging
from backend.utils.logging import setup_logging
from backend.utils.Pulse import Pulse

setup_logging(log_level=logging.INFO)
logger = logging.getLogger(__name__)

def pulse_create_and_run():
    pulse = Pulse()

    ppt_content_file = "backend/tests/data/audience_pulse.json"
    ppt_content = json.load(open(ppt_content_file, "r", encoding='utf-8'))
    ppt_details = {
        "title": "Audience Pulse",
        "description": """
A hackathon project demo for a new PowerPoint feature that allows presenters to generate a mock audience using AI before their actual presentation.
The presenter can use this audience to get feedback and revise potential questions ahead of time.
""",
        "intent": "To gain interest from leadership team of PowerPoint to potentially fund this project.",
        "content": ppt_content
    }
    pulse.add_ppt(ppt_details)

    pulse.add_persona({
        "name": "Hui_persona",
        "description": """
The personas must match this person: Principal Architect at Microsoft, specializing in service architecture and engineering design. 
- Her expertise in developing robust architectural solutions has significantly contributed to enhancing backend systems
- IMPORTANT, FEATURES OF THIS PERSONA MUST THE GIVEN DESCRIPTION. You can fill in the rest.
""",
        "population_size": 5
    })

    pulse.add_persona({
        "name": "Elena_persona",
        "description": """
The personas must match this person: Principal Software Engineering Manager at Microsoft, leading a team with a focus on software engineering and responsible AI initiatives. 
- Elena's leadership and deep technical knowledge have been pivotal in driving improvements in accessibility and AI.
- IMPORTANT, FEATURES OF THIS PERSONA MUST THE GIVEN DESCRIPTION. You can fill in the rest.
""",
        "population_size": 2
    })

    pulse.add_persona({
        "name": "Jess_persona",
        "description": """
The personas must match this person: Senior Product Manager at Microsoft, focusing on product management and user experience. 
- Their strategic insights and innovative approaches have played a crucial role in advancing user experience and product features.
- IMPORTANT, FEATURES OF THIS PERSONA MUST THE GIVEN DESCRIPTION. You can fill in the rest.
""",
        "population_size": 2
    })

    pulse_save_folder = "backend/tests/results"
    pulse.run()
    pulse.save(pulse_save_folder)

def pulse_create_and_run2():
    pulse = Pulse()

    ppt_content_file = "backend/tests/data/diversity_slide_content.json"
    ppt_content = json.load(open(ppt_content_file, "r", encoding='utf-8'))
    ppt_details = {
        "title": "Organizing a Christmas Party at the Office: A Step-by-Step Guide : Essential steps for a successful festive celebration",
        "description": """A holiday party planning presentation.""",
        "intent": "To suggest ideas for planning a holiday party for employees and coordinate planning efforts with other employees.",
        "content": ppt_content
    }
    pulse.add_ppt(ppt_details)

    pulse.add_persona({
        "name": "diversity_persona",
        "description": """Every persona MUST BE based on: Diversity expert focusing on creating inclusive environments and promoting diversity in the workplace. Focuses on diverse perspectives around culture, gender, religion, workplace environment, accessibility, and more.""",
        "population_size": 5
    })

    pulse.add_persona({
        "name": "ethics_persona",
        "description": """Every persona MUST BE based on: Ethics focus focusing on ethical aspect of the presentation and product.""",
        "population_size": 5
    })

    pulse.add_persona({
        "name": "HR_Persona",
        "description": """Every persona MUST BE based on: Working at HR, looking to ensure that diversity and inclusivity is maintained in the presentation. Must ensure that the presentation is inclusive and accessible to all employees. Also looking out for the company image to ensure nothing controversial is included. Focuse on all aspects of diversity.""",
        "population_size": 5
    })

    pulse_save_folder = "backend/tests/results"
    pulse.run()
    pulse.save(pulse_save_folder)

def pulse_load_and_run():
    pulse_folder = "backend/tests/results/6adf607d-8da3-4e6b-af47-6cde7d6adf1e"
    pulse_save_folder = "backend/tests/results"
    pulse = Pulse.load(pulse_folder)
    for persona in pulse.personas:
        persona.set_population_size(5)
        persona.reset()
    pulse.run()
    pulse.save(pulse_save_folder)

def pulse_to_html():
    pulse_folder = "backend/tests/results/c360d9e6-160f-4d07-99a0-c8d434861b80"
    pulse = Pulse.load(pulse_folder)
    pulse.save_html("backend/tests/results/c360d9e6-160f-4d07-99a0-c8d434861b80/pulse_html.html")


if __name__ == "__main__":
    pulse_create_and_run2()