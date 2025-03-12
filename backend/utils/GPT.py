import os, json, time, logging
from openai import AzureOpenAI
from dotenv import load_dotenv
from backend.utils import Constants
load_dotenv()

logger = logging.getLogger(__name__)

class GPT:
    def __init__(self, name="GPT Assistant", default_prompt="You are an AI assistant that helps people find information."):
        """Initialize GPT with Azure OpenAI client setup and default prompt"""
        self.client = self.setup()
        self.name = name
        self.default_prompt = default_prompt
        # Create assistant immediately during initialization
        self.assistant = self.create_assistant()

    def setup(self):
        logger.debug("Setting up Azure OpenAI client...")
        """Set up Azure OpenAI client with proper authentication"""
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_CLIENT_SECRET"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-05-01-preview"
        )
        return client

    def create_assistant(self, name=None, model="gpt-4o", temperature=0.7):
        logger.debug("Creating new assistant...")
        """Create a new assistant with the default prompt"""
        return self.client.beta.assistants.create(
            name=name or self.name,
            instructions=self.default_prompt,
            model=model,
            temperature=temperature
        )

    def run_conversation(self, user_prompt: str, thread_id: str = None) -> dict:
        logger.debug("Running conversation with assistant...")
        """Run a conversation with the assistant
        If thread_id is provided, continues that conversation
        If thread_id is None, starts a new conversation
        """
        # Use existing thread or create new one
        thread = (self.client.beta.threads.retrieve(thread_id) 
                 if thread_id 
                 else self.client.beta.threads.create())

        # Add the user's message to the thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )

        # Wait for completion
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status == "completed":
                break
            time.sleep(1)

        # Get the assistant's response
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Return the latest assistant message and thread ID for continuation
        latest_message = messages.data[0]
        return {
            'response': latest_message.content[0].text.value,
            'thread_id': thread.id
        }

    def continue_conversation(self, user_prompt: str, thread_id: str) -> dict:
        """Continue an existing conversation thread"""
        return self.run_conversation(user_prompt, thread_id)
