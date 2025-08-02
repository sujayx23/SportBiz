from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import List
import os

class NamingAgent:
    """Specialized agent for generating creative store names and branding elements."""
    
    def __init__(self, api_key: str = None):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo for cost efficiency
            temperature=0.8,
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[BaseTool]:
        """Create specialized tools for naming and branding."""
        from langchain.tools import tool
        
        @tool
        def generate_store_name(sport: str) -> str:
            """Generate a creative and memorable store name for a sports business."""
            return f"Generated store name for {sport}"
        
        @tool
        def create_tagline(store_name: str, sport: str) -> str:
            """Create a catchy tagline for the store."""
            return f"Tagline for {store_name} - {sport} store"
        
        @tool
        def suggest_brand_colors(sport: str) -> str:
            """Suggest brand colors that match the sport's energy and appeal."""
            return f"Brand colors for {sport} store"
        
        return [generate_store_name, create_tagline, suggest_brand_colors]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the naming agent with specialized prompts."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a creative branding expert specializing in sports business naming and branding.
            Your expertise includes:
            - Creating memorable, marketable store names
            - Developing catchy taglines and slogans
            - Suggesting brand colors and visual identity
            - Understanding sports culture and fan psychology
            
            Always consider:
            - Target audience demographics
            - Local market appeal
            - Brand memorability
            - SEO-friendly naming
            - Trademark availability (mention if needed)"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    def generate_complete_branding(self, sport: str, location: str = None) -> dict:
        """Generate complete branding package for a sports store."""
        prompt = f"""
        Create a complete branding package for a {sport} store{f" in {location}" if location else ""}.
        
        Please provide:
        1. A creative store name
        2. A catchy tagline
        3. Brand color suggestions
        4. Brand personality description
        5. Target audience analysis
        
        Make it market-ready and appealing to sports enthusiasts.
        """
        
        response = self.agent.invoke({"input": prompt})
        return {
            "sport": sport,
            "location": location,
            "branding_package": response["output"],
            "agent_type": "naming"
        } 