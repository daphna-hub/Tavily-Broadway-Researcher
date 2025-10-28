"""
Agent to compile final comprehensive report
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1", temperature=0)


class CompileReportState(TypedDict):
    """State for report compilation"""
    show_name: str
    ratings_summary: str
    ticket_recommendations: str
    final_report: str


class CompileReportAgent:
    """Agent that compiles final comprehensive report"""
    
    def __init__(self):
        self.llm = llm
    
    def compile(self, show_name: str, ratings_summary: str, ticket_recommendations: str) -> str:
        """
        Compile a concise final report
        
        Args:
            show_name: Standardized Broadway show name
            ratings_summary: Summary of reviews and ratings
            ticket_recommendations: Ticket purchasing recommendations
            
        Returns:
            Final concise report
        """
        prompt = f"""You are an Agent. Create a ULTRA-CONCISE report about {show_name}. MAXIMUM 20 lines total.

REVIEWS AND RATINGS:
{ratings_summary}

TICKET PURCHASING INFORMATION:
{ticket_recommendations}

Format (be VERY brief, total under 20 lines):

## Overview
[2 lines max about the show]

## Reviews
**Score:** [number]/10 or [rating]
[3 lines max - key points only]

## Where to Buy Tickets
[2-3 actual ticket vendor links in format: [Vendor Name](URL)]
Examples: Broadway.com, Ticketmaster, ShowTickets.com - use real URLs if available

Keep it scannable. Maximum 20 lines total. Add actual ticket purchase links if available."""

        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def __call__(self, state: CompileReportState) -> CompileReportState:
        """Execute the report compilation"""
        result = self.compile(
            state["show_name"],
            state["ratings_summary"],
            state["ticket_recommendations"]
        )
        
        return {
            "final_report": result
        }
