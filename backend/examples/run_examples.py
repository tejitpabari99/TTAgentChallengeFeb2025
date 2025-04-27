import os, json, logging, time
from backend.utils.logging import setup_logging
from backend.utils.Pulse import Pulse
from backend.examples.pulse_tinytroupe_create import *
from backend.examples.pulse_gpt_create import *

setup_logging(log_level=logging.INFO)
logger = logging.getLogger(__name__)

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
    st = time.time()
    pulse_tinytroupe_create_and_run3()
    logger.info(f"Elapsed time: {time.time() - st} seconds")