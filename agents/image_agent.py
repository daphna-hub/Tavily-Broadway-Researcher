"""
Agent to find Broadway show images
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class FindImageState(TypedDict):
    """State for image search"""
    show_name: str
    image_url: str


class FindImageAgent:
    """Agent that searches for Broadway show images"""
    
    def __init__(self):
        self.tavily_client = tavily_client
    
    def find_image_url(self, show_name: str) -> str:
        """Search for images using Tavily"""
        query = f"{show_name} Broadway show poster official image"
        response = self.tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_images=True
        )
        
        # Try to get image from results
        results = response.get("results", [])
        for result in results:
            images = result.get("images", [])
            if images and len(images) > 0:
                return images[0]
        
        return ""
    
    def find(self, show_name: str) -> dict:
        """
        Find an image URL for a Broadway show
        
        Args:
            show_name: Standardized Broadway show name
            
        Returns:
            dict with image_url
        """
        image_url = self.find_image_url(show_name)
        
        return {
            "image_url": image_url
        }
    
    def __call__(self, state: FindImageState) -> FindImageState:
        """Execute the image search"""
        result = self.find(state["show_name"])
        
        return {
            "image_url": result["image_url"]
        }
