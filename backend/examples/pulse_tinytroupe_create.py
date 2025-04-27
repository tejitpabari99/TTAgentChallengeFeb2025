import os, json, logging, time
from backend.utils.Pulse import Pulse

logger = logging.getLogger(__name__)

def pulse_tinytroupe_create_and_run():
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

def pulse_tinytroupe_create_and_run2():
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



def pulse_tinytroupe_create_and_run3():
    pulse = Pulse()

    ppt_content_file = "backend/tests/data/audience_pulse.json"
    ppt_content = json.load(open(ppt_content_file, "r", encoding='utf-8'))
    ppt_details = {
        "title": "Audience Pulse",
        "description": """
A hackathon project demo for a new PowerPoint feature that allows presenters to generate a mock audience using AI before their actual presentation.
The presenter can use this audience to get feedback and revise potential questions ahead of time.
""",
        "intent": """
To present to different leaderships at Microsoft to gain interest in the project.
Leadership knows of existing projects at Microsoft related to this project, such as PPT Coach Mode.
""",
        "content": ppt_content
    }
    pulse.add_ppt(ppt_details)

    pulse.add_persona({
        "type": "tinytroupe",
        "name": "Technical Architects and Engineers",
        "description": """
The personas must match a person at a high technical level (such as Principal Architect, or Enigneering Manager) at Microsoft Powerpoint. 
- Specializes in service architecture and engineering design. 
- Expertise in developing robust architectural solutions has significantly contributed to enhancing backend systems.
- Leading a team with a focus on software engineering and responsible AI initiatives
"""
    })

    pulse.add_persona({
        "type": "tinytroupe",
        "name": "Product Managers",
        "description": """
The personas must match a Product Managers at Microsoft Powerpoint. They must have technical expertise and experience in product management and user experience.
- Their strategic insights and innovative approaches have played a crucial role in advancing powerpoint's product growth. 
- They must consider the product integration aspects of the project, including cultural diversity, accesibility, and ethical considerations.
- They must also consider the potential impact of the project on the company's image and reputation.
"""
    })
    
    pulse.add_persona({
        "type": "tinytroupe",
        "name": "Business Executives",
        "description": """
The personas must match a Business Executive at Microsoft Powerpoint. They must have technical knowledge, product knowledge and consider the product from a high level perspective, looking at Powerpoint's business as a whole.
"""
})

    pulse.add_persona({
        "type": "tinytroupe",
        "name": "Diversity Leader",
        "description": """
This persona is a diversity expert at Microsoft Powerpoint. They must focusing on creating inclusive environments and promoting diversity in the workplace. Focuses on diverse perspectives around culture, gender, religion, workplace environment, accessibility, and more.
"""
    })

    pulse_save_folder = "backend/tests/results"
    pulse.run()
    pulse.save(pulse_save_folder)