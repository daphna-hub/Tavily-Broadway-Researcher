"""
Agent to find reviews and ratings for Broadway shows
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_openai import ChatOpenAI

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4.1", temperature=0)


class FindRatingsState(TypedDict):
    """State for ratings search"""
    show_name: str
    reviews_content: str
    ratings_summary: str


class FindRatingsAgent:
    """Agent that searches for and summarizes reviews and ratings"""
    
    def __init__(self):
        self.tavily_client = tavily_client
        self.llm = llm
    
    def search_reviews(self, show_name: str) -> str:
        """Search for reviews using Tavily"""
        query = f"{show_name} Broadway show reviews 2024"
        response = self.tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        
        return "\n\n".join([
            f"Source: {result['url']}\n{result['content']}" 
            for result in response.get("results", [])
        ])
    
    def search_ratings(self, show_name: str) -> str:
        """Search for ratings and critic reviews using Tavily"""
        query = f"{show_name} Broadway show ratings critic reviews"
        response = self.tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=3
        )
        
        return "\n\n".join([
            f"Source: {result['url']}\n{result['content']}" 
            for result in response.get("results", [])
        ])
    
    def summarize_reviews_and_ratings(self, show_name: str, reviews: str, ratings: str) -> str:
        """Use LLM to summarize the reviews and ratings"""
        prompt = f"""Based on the following information about {show_name}, provide a concise summary of reviews and ratings.

REVIEWS:
{reviews[:3000]}

RATINGS:
{ratings[:3000]}

Please provide:
1. A summary of overall critical reception
2. Key positive points mentioned
3. Any criticisms or concerns
4. Average rating if available (out of 10 or stars)
5. Notable quotes from reviews"""

        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def find(self, show_name: str) -> dict:
        """
        Find reviews and ratings for a Broadway show
        
        Args:
            show_name: Standardized Broadway show name
            
        Returns:
            dict with reviews_content and ratings_summary
        """
        print(f"🔍 Searching for reviews and ratings for '{show_name}'...")
        
        # Search for both reviews and ratings
        reviews_content = self.search_reviews(show_name)
        ratings_content = self.search_ratings(show_name)
        
        # Summarize the findings
        ratings_summary = self.summarize_reviews_and_ratings(
            show_name, 
            reviews_content, 
            ratings_content
        )
        
        return {
            "reviews_content": reviews_content[:2000],  # Keep reasonable size
            "ratings_summary": ratings_summary
        }
    
    def __call__(self, state: FindRatingsState) -> FindRatingsState:
        """Execute the ratings search"""
        result = self.find(state["show_name"])
        
        return {
            "reviews_content": result["reviews_content"],
            "ratings_summary": result["ratings_summary"]
        }
