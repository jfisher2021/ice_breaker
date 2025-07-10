from tools.tools import get_profile_url_tavily
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool


from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)

from langchain import hub

def lookup(name:str) -> str:
    # llm = init_chat_model(
    #     "gpt-4o-mini",
    #     temperature=0,
    # )
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google-genai")
    template = """ given the full name {name_of_person} I want you to get me the LinkedIn profile URL of that person.
        you should return only the URL of the LinkedIn profile.
    """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when u need to get de linkedin URL of someone",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent,verbose=True)

    result = agent_executor.invoke(
        input={
           "input":prompt_template.format_prompt(name_of_person=name)
        }
    )
    
    linkedin_proflie_url = result["output"]
    return linkedin_proflie_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Jonathan Fisher España")
    print(linkedin_url)
    # linkedin_url = "https://www.linkedin.com/in/eden-marco/"
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    # print(linkedin_data)