from typing import List

from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Old Tavily Method
# from tavily import TavilyClient
# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Tool that searches over the internet
#     :param query: The query to search for
#     :return: The search result
#     """
#     print(f"Searching for {query}")
#     return tavily.search(query=query)
# tools = [search]


# new Tavily Method
from langchain_tavily import TavilySearch
class Source(BaseModel):
    """Schema for a source used by the agent"""
    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="This is the agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer"
    )

tools = [TavilySearch()]
llm = ChatOpenAI()
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

def main():
    print("Starting LangChainSearchAgent")
    # result = agent.invoke({"messages":HumanMessage(content="What is the weather in Tokyo")})
    result = agent.invoke({
        "messages": HumanMessage(
            content="search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details"
        )
    })
    print(result)

if __name__ == "__main__":
    main()

