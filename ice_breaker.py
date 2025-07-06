import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

if __name__ == "__main__":
    print("Hello, world! This is an ice breaker script.")
    print("Let's get started with Python programming!")

    prompt_template = """
        Given an input text {text}, do the next things:
        1. Identify the main topic.
        2. Tell a joke related to that topic.

    """
    summary_prompt = PromptTemplate(
        input_variables=["text"],
        template=prompt_template
    )

    llm = init_chat_model(model="gemma-3n-e2b-it", model_provider="google_genai")
    chain = summary_prompt | llm

    # Example usage
    input_text = "Python is a versatile programming language."
    result = chain.invoke({"text": input_text})
    print(result.content)