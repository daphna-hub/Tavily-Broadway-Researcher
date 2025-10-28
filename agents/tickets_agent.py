"""
Agent to find the best ticket purchasing options
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_openai import ChatOpenAI

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4.1", temperature=0)


class FindTicketsState(TypedDict):
    """State for ticket search"""
    show_name: str
    ticket_info_content: str
    ticket_recommendations: str


class FindTicketsAgent:
    """Agent that finds the best places to purchase tickets"""
    
    def __init__(self):
        self.tavily_client = tavily_client
        self.llm = llm
    
    def search_ticket_options(self, show_name: str) -> str:
        """Search for ticket purchasing options using Tavily"""
        query = f"where to buy tickets for {show_name} Broadway show best prices 2024"
        response = self.tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        
        return "\n\n".join([
            f"Source: {result['url']}\n{result['content']}" 
            for result in response.get("results", [])
        ])
    
    def analyze_ticket_options(self, show_name: str, ticket_info: str) -> str:
        """Use LLM to analyze and provide ticket purchasing recommendations"""
        prompt = f"""Based on the following search results, provide recommendations for where to purchase tickets for {show_name} this week.

TICKET INFORMATION:
{ticket_info[:3000]}

Please provide:
1. Official box office or primary ticket sellers
2. Recommended ticket vendors (e.g., Ticketmaster, StubHub, Broadway.com, etc.)
3. Tips for getting good prices
4. Any special offers or promotions mentioned
5. Current ticket availability status
6. Best times to purchase tickets
7. Any warnings about scalpers or resellers to avoid"""

        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def find(self, show_name: str) -> dict:
        """
        Find ticket purchasing options for a Broadway show
        
        Args:
            show_name: Standardized Broadway show name
            
        Returns:
            dict with ticket_info_content and ticket_recommendations
        """
        print(f"🎫 Searching for ticket options for '{show_name}'...")
        
        # Search for ticket information
        ticket_info_content = self.search_ticket_options(show_name)
        
        # Analyze and get recommendations
        ticket_recommendations = self.analyze_ticket_options(show_name, ticket_info_content)
        
        return {
            "ticket_info_content": ticket_info_content[:2000],
            "ticket_recommendations": ticket_recommendations
        }
    
    def __call__(self, state: FindTicketsState) -> FindTicketsState:
        """Execute the ticket search"""
        result = self.find(state["show_name"])
        
        return {
            "ticket_info_content": result["ticket_info_content"],
            "ticket_recommendations": result["ticket_recommendations"]
        }
