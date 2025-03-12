class Prompts:

  TINY_TROUPE_INFO = """
I am using a package called TInyTroupe in my project, to analyze a powerpoint and simulate real-person persona based feedback.

Here is some detail about the TinyTroupe package:
*TinyTroupe* is an experimental Python library that allows the **simulation** of people with specific personalities, interests, and goals. These artificial agents - `TinyPerson`s - can listen to us and one another, reply back, and go about their lives in simulated `TinyWorld` environments. This is achieved by leveraging the power of Large Language Models (LLMs), notably GPT-4, to generate realistic simulated behavior. This allows us to investigate a wide range of **convincing interactions** and **consumer types**, with **highly customizable personas**, under **conditions of our choosing**. The focus is thus on *understanding* human behavior and not on directly *supporting it* (like, say, AI assistants do) -- this results in, among other things, specialized mechanisms that make sense only in a simulation setting. Further, unlike other *game-like* LLM-based simulation approaches, TinyTroupe aims at enlightening productivity and business scenarios, thereby contributing to more successful projects and products. Here are some application ideas to **enhance human imagination**:

  - **Advertisement:** TinyTroupe can **evaluate digital ads (e.g., Bing Ads)** offline with a simulated audience before spending money on them!
  - **Software Testing:** TinyTroupe can **provide test input** to systems (e.g., search engines, chatbots or copilots) and then **evaluate the results**.
  - **Training and exploratory data:** TinyTroupe can generate realistic **synthetic data** that can be later used to train models or be subject to opportunity analyses.
  - **Product and project management:** TinyTroupe can **read project or product proposals** and **give feedback** from the perspective of **specific personas** (e.g., physicians, lawyers, and knowledge workers in general).
  - **Brainstorming:** TinyTroupe can simulate **focus groups** and deliver great product feedback at a fraction of the cost!

In all of the above, and many others, we hope experimenters can **gain insights** about their domain of interest, and thus make better decisions. 
-----
You are tasked with helping me with different tasks related to this package.
"""

  TINY_TROUPE_PERSONA_GPT_PROMPT = """
Help me create a prompt to generate a Tiny Troupe persona for {persona_name} which is described by {persona_description}. The details in the persona description are fixed and must influence persona creation. Infer any other characteristics that the persona must have, to create a prompt based on the powerpoint description and intent. Personas must be diverse to ensure they can evaluate the powerpoint presentation and powerpoint_content (both) effectively and from all angles. Persona created must also keep in mind diversity and accessibility.
Create {persona_population_size} number of personas only.
---------  
You can base your prompt off this sample prompt (which was used to create persona of a customer for a technical product pitch):
 
A diverse group of customers with varying
- Need of product (High, low, none)
- Usage intensive (light, moderate, heavy)
- Technical comfort levels (novice, intermediate, advance, power users)
- Pain points and challenges
- Decision-making influence 
- Technology adoption preferences (Early adopters, pragmatic users, conservative users, skeptical users)
- Different budget authorities and Resource constraints  
- Industry sectors
- Age demographic
- Geographical location
- Cultural background
- Success criterias (must have features, deal breakers, open to anything)  

Some of the customers must:  
- Have used the product in the past (or an interation of the product).  
- Have used similar products in the past.  
- Have strong opinions about the product or similar products.  

Ensure they have:  
- Realistic usage scenarios.  
- Clear preferences based on their background.  
- Specific frustrations with current solutions (if they have used similar products).  
- Unique perspectives on value.  
- Natural biases and concerns.  
----------  
"""

  TINY_TROUPE_ANALYSIS_GPT_PROMPT = """
Tiny Troupe personas are asked to CRITICALLY evaluate a presentation with the above presentation details. The goal is to generate feedback on the content of the presentation and the presentation itself.

Help me create a prompt to pass to these personas to ask them to evaluate the powerpoint presentation and its content.  
- Agents must evaluate the powerpoint presentation and its content.
- IMPORTANT Agents have access only to the presentation text, not to the presentation itself. This means they cannot see the presentation and don't know of any visual elements or media in it.
- The prompt must define, in clear terms, the different categories for feedback and what feedback is to be given for each category.
- Where possible reference the slide number or content of the presentation to make the feedback more specific.
- Ensure that the feedback is not generic, but highly specific to the persona's personality and background. It must be critical feedback that will improve the presentation and must leverage the fact that personas have different interests, behaviors, personalities etc to improve the feedback provided to make it personalized and subjective.
-------
You can use this as a sample to create the evaluation prompt (used for a presrnation given to a customer for a technical product pitch):
From your perspective as a potential user/customer, analyze this presentation:
1. Value & Relevance:
   - How well does this address your needs and pain points?
   - Are the benefits clear and meaningful to you?
   - What aspects matter most to your situation?
2. Practical Application:
   - How would this fit into your current workflow?
   - What challenges do you see in adopting this?
   - What support or resources would you need?
3. Cost & Benefit Analysis:
   - Is the value proposition compelling for your needs?
   - What return on investment do you anticipate?
   - What hidden costs or efforts do you foresee?
4. Comparison & Alternatives:
   - How does this compare to your current solution?
   - What advantages stand out to you?
   - What concerns would prevent you from adopting this?
Remember (IMPORTANT):
- Your feedback should be based on your real-world needs and experiences while considering the presentation's stated purpose.
- Giving feedback on all above categories is not important. If there is no feedback, return an empty array for that category.
- You must give atleast one feedback.
-------
Remember
- Agents don't have access to visual elements of media in the presentation. Only text of the presentation
- Agents MUST mention the slide number or content of the presentation to make the feedback more specific. REFERENCE THE SLIDE NUMBER OR CONTENT.
"""

  TINY_TROUPE_QNA_GPT_PROMPT = """
Tiny Troupe personas are asked to ask critical questions about the content of the presentation to help the presenter prepare for a real presentation. The goal is to generate questions that the presenter must be prepared to answer.
 
Help me create a prompt to pass to these personas to prompt them to ask questions about the powerpoint presentation.  
- Agents must ask questions about the content of the presentation.
- Agents have been asked to analyze the presentation before (to provide critical feedback) and are aware of the analysis they have provided.
- Ensure that the questions asked are not generic, but highly specific to the persona's personality and background. They must be critical questions which will help the presenter improve the presentation and prepare for the real one and MUST leverage the fact that personas have different interests, behaviors, personalities etc to generate the questions, making them personalized and subjective.
- Agents must consider questions around addressing diversity and accessibility in the presentation content.
- IMPORTANT Agents have access only to the presentation text, not to the presentation itself. This means they cannot see the presentation and don't know of any visual elements or media in it. 
- The prompt must specify, in clear terms, what kind of questions are the agents expected to ask the presenter.  
- The prompt must also specify that the result should be a list of questions.
-------  
You can use this as a sample to create the qna prompt (used for a presrnation given to a customer for a technical product pitch):

Drawing from your experience and needs, review this presentation and formulate questions that would:  
1. Clarify how this addresses your specific needs  
2. Address practical implementation concerns  
3. Validate assumptions about user benefits  
 
Ensure your questions:  
- Reflect your real needs and concerns  
- Address practical usage considerations  
- Focus on value and implementation  
- Help you make an informed decision  
  
Remember (IMPORTANT)  
- You must ask atleast one question.   
----------  
Remember  
- Agents don't have access to visual elements of media in the presentation. Only text of the presentation.
"""

  TINY_TROUPE_ANALYSIS_SUMMARIZATION_GPT_PROMPT = """
TinyTroupe agents were created for a persona named {persona_name} which is described by {persona_description}
The agents were tasked with critically analysing a powerpoint presentation. Here are the powerpoint details:      
{ppt_details}
-------      
Here is the prompt that the agent was given, to analyze the powerpoint presentation:      
{analysis_prompt} 
----------      
Here is the response from all the agent:      
{analysis_result}
----------
Can you help summarize the unique feedback provided by the agents, for the presentation.     
- I want to present unique feedback for all agents together.     
- If two agents have overlapping/same feedback, combine it and take unique feedback.
- DO NOT REPEAT FEEDBACK POINTS.
- IMPORTANT: DO NOT MAKE UP FEEDBACK. Only take feedback asked by the agents. Your job is to summarize, NOT ANALYZE the content.
- Ensure feedback is succinct and not overly wordy. If needed summarize the feedback to make its intent clearer.  
- Split feedback into strengths and improvements - discussing the positive feedback in former and improvements in the latter.
  - For feedback's strength, present the top 6 or less strengths. (No strengths is also a valid response). Less and concise is better.
	- For feedback's improvements, present the top 6 or less improvements only. (No improvements is also a valid response). Less and concise is better.
	- Select the analysis that are top amongst all reviewers, since that defines the priority of feedback given.
- Each feedback given should have a title and then description of what the feedback is.
- IMPORTANT, try to keep the persona of the agent giving that feedback alive. Especially if the feedback is subjective.
- IMPORTANT, If feedback mentions slide number of slide content, ensure it is present in the summary. REFERENCE THE SLIDE NUMBER OR CONTENT MENITONED IN THE FEEDBACK.
"""

  TINY_TROUPE_QNA_SUMMARIZATION_GPT_PROMPT = """
TinyTroupe agents were created for a persona named {persona_name} which is described by {persona_description}
The agents were tasked with asking critical questions about the content of the powerpoint presentation. Here are the powerpoint details:
{ppt_details}
-----
Here is the prompt that the agent was given, to ask questions about the powerpoint presentation:      
{qna_prompt}
--------  
Here is the response from all agents:  
{qna_result}
-----------  
Can you help identify combined unique questions given by the agents, for the powerpoint presentation.       
- I want combined unique questions asked by all agents under the given two umbrellas.
- Questions are meant to be critical, use your judgement and knowledge about persona and presentation to identify such questions. They must be intelligent and pertinent to the presentation content.
- If two agents have overlapping/same questions, combine it and take unique question.
- DO NOT REPEAT QUESTIONS.
- IMPORTANT: DO NOT MAKE UP QUESTIONS. Only take questions asked by the agents.
- Ensure questions are asked succinct and not overly wordy.
- IMPORTANT: Take the questions marked as questions (or under the array or json object called questions) OR are asked as questions (with a question mark at the end or phrased as questions) first, before inferring questions from the response.
- Give at most 10 questions (or less). Less and concise is better. 
"""

class Config:
  MAX_RETRY_DEFAULT = 3

