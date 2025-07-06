from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

from third_paties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")


    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. Tell me if is currntly working and in wich company
    3. gime me his email and telephone to reach him
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = init_chat_model(model="gemma-3n-e2b-it", model_provider="google-genai")
    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/jfisherr/",
        mock=True
    )
    #  print(linkedin_data)
    res = chain.invoke(input={"information": linkedin_data})
    from rich.markdown import Markdown
    from rich.console import Console
    
    console = Console()
    markdown = Markdown(res.content)
    console.print(markdown)
