from typing import Union, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain.chat_models import init_chat_model


load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters just in case

    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # Test 1: ChatOpenAI directo
    print("=== Test 1: ChatOpenAI directo ===")
    try:
        openai_llm = ChatOpenAI(temperature=0, stop=["Observation"])
        chain = prompt | openai_llm
        # Using invoke directly on the LLM
        response = chain.invoke("Which is the length of the word 'hello'?")
        print(f"OpenAI Response: {response.content}")
    except Exception as e:
        print(f"Error with OpenAI: {e}")

    print("\n" + "="*50)

    # Test 2: Google Gemini con init_chat_model  
    print("=== Test 2: Google Gemini con init_chat_model ===")
    try:
        gemini_llm = init_chat_model(
            model="gemini-2.5-pro", 
            model_provider="google-genai",
            model_kwargs={"stop": ["Observation"]}
        )
        chain = prompt | gemini_llm
        response = chain.invoke("Which is the length of the word 'hello'?")
        print(f"Gemini Response: {response.content}")
    except Exception as e:
        print(f"Error with Gemini: {e}")

    print("\n" + "="*50)

    # Test 3: Google Gemini directo (sin init_chat_model)
    print("=== Test 3: Google Gemini directo ===")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        direct_gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            model_kwargs={"stop": ["Observation"]}

        )
        chain = prompt | direct_gemini
        response = chain.invoke("Which is the length of the word 'hello'?")
        print(f"Direct Gemini Response: {response.content}")
    except Exception as e:
        print(f"Error with Direct Gemini: {e}")
