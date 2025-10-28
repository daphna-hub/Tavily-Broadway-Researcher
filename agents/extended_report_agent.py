"""
Agent to compile extended comprehensive report for download
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1", temperature=0)


class ExtendedReportState(TypedDict):
    """State for extended report compilation"""
    show_name: str
    ratings_summary: str
    ticket_recommendations: str
    extended_report: str


class ExtendedReportAgent:
    """Agent that compiles extended detailed report for download"""
    
    def __init__(self):
        self.llm = llm
    
    def compile(self, show_name: str, ratings_summary: str, ticket_recommendations: str) -> str:
        """
        Compile an extended detailed report
        
        Args:
            show_name: Standardized Broadway show name
            ratings_summary: Summary of reviews and ratings
            ticket_recommendations: Ticket purchasing recommendations
            
        Returns:
            Extended comprehensive report
        """
        prompt = f"""You are an Agent compiling an EXTENDED, DETAILED report about {show_name} for download.

REVIEWS AND RATINGS:
{ratings_summary}

TICKET PURCHASING INFORMATION:
{ticket_recommendations}

Create a comprehensive, detailed report with the following sections:

## Overview
[Write a detailed 3-4 paragraph overview of the show, including its history, significance, and what makes it special]

## Reviews and Critical Reception
**Overall Score:** [rating with scale explanation]
[Expand on the reviews - include specific praise, criticisms, notable quotes, and what critics highlight]

## Key Highlights
[What makes this show noteworthy - performances, production value, music, staging, etc.]

## Where to Buy Tickets
[Provide detailed information on ticket vendors with specific guidance on which to use when]
[Include pricing information, best times to buy, and any insider tips]

## Show Details
[Running time, age recommendations, accessibility info, theater location if relevant]

## Tips for Attendees
[Practical advice for attending the show]

Make this report comprehensive and valuable for someone researching the show."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def __call__(self, state: ExtendedReportState) -> ExtendedReportState:
        """Execute the extended report compilation"""
        result = self.compile(
            state["show_name"],
            state["ratings_summary"],
            state["ticket_recommendations"]
        )
        
        return {
            "extended_report": result
        }
