from backend.utils.GPT import GPT
from backend.utils.Constants import Prompts
import time

def time_it(func, name=None):
    start_time = time.time()
    result = func()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Function {name or func.__name__} execution time: {execution_time:.2f} seconds")
    return result

def test_gpt_conversation():
    # Initialize GPT
    gpt = GPT(name="TinyTroupe", default_prompt=Prompts.TINY_TROUPE_INFO)
    
    # Start a new conversation
    result = time_it(
        lambda: (
            gpt := GPT(name="TinyTroupe", default_prompt=Prompts.TINY_TROUPE_INFO),
            gpt.run_conversation("Tell me about TinyTroupe's capabilities for product testing in 50 words or less"))[1],
        "run_conversation"
    )
    print("First Response:", result['response'])

    print("\nTiming it again, to check reuse of existing assistant")
    # Start a new conversation
    result = time_it(
        lambda: gpt.run_conversation("Tell me about TinyTroupe's capabilities for product testing in 50 words or less"),
        "run_conversation (again)"
    )
    print("Second Response:", result['response'])

    print("\nFolllow-up conversation")
    # Continue the conversation using the same thread
    follow_up = time_it(
        lambda: gpt.continue_conversation(
            "How can it help with brainstorming? In 50 words or less",
            result['thread_id']
        ),
        "continue_conversation"
    )
    print("Follow-up Response:", follow_up['response'])

if __name__ == "__main__":
    test_gpt_conversation()
