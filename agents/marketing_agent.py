from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import List
import os

class MarketingAgent:
    """Specialized agent for generating marketing strategies and campaigns."""
    
    def __init__(self, api_key: str = None):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo for cost efficiency
            temperature=0.7,
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[BaseTool]:
        """Create specialized tools for marketing strategies."""
        from langchain.tools import tool
        
        @tool
        def generate_social_media_strategy(store_name: str, sport: str) -> str:
            """Generate a comprehensive social media marketing strategy."""
            return f"Social media strategy for {store_name} - {sport} store"
        
        @tool
        def create_marketing_campaign(store_name: str, target_audience: str) -> str:
            """Create a multi-channel marketing campaign."""
            return f"Marketing campaign for {store_name} targeting {target_audience}"
        
        @tool
        def suggest_promotional_events(sport: str, location: str) -> str:
            """Suggest promotional events and partnerships."""
            return f"Promotional events for {sport} store in {location}"
        
        @tool
        def analyze_competition(sport: str, location: str) -> str:
            """Analyze local competition and market positioning."""
            return f"Competitive analysis for {sport} market in {location}"
        
        return [generate_social_media_strategy, create_marketing_campaign, 
                suggest_promotional_events, analyze_competition]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the marketing agent with specialized prompts."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sports marketing expert specializing in retail marketing strategies.
            Your expertise includes:
            - Digital marketing and social media strategies
            - Local market campaigns and community engagement
            - Sports event marketing and partnerships
            - Customer acquisition and retention strategies
            - Brand awareness and positioning
            
            Always consider:
            - Target audience behavior and preferences
            - Local sports culture and community
            - Seasonal marketing opportunities
            - Budget-friendly marketing tactics
            - Measurable marketing objectives"""),
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
    
    def generate_marketing_strategy(self, store_name: str, sport: str, location: str = None) -> dict:
        """Generate comprehensive marketing strategy for a sports store."""
        prompt = f"""
        Create a comprehensive marketing strategy for {store_name}, a {sport} store{f" in {location}" if location else ""}.
        
        Please provide:
        1. Social media marketing strategy
        2. Local community engagement tactics
        3. Seasonal marketing campaigns
        4. Partnership opportunities
        5. Customer retention strategies
        6. Budget allocation recommendations
        7. Success metrics and KPIs
        
        Focus on practical, actionable strategies that drive foot traffic and online sales.
        """
        
        response = self.agent.invoke({"input": prompt})
        return {
            "store_name": store_name,
            "sport": sport,
            "location": location,
            "marketing_strategy": response["output"],
            "agent_type": "marketing"
        } 