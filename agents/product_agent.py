from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import List
import os

class ProductAgent:
    """Specialized agent for generating product recommendations and inventory strategies."""
    
    def __init__(self, api_key: str = None):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo for cost efficiency
            temperature=0.6,
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[BaseTool]:
        """Create specialized tools for product analysis."""
        from langchain.tools import tool
        
        @tool
        def analyze_trending_products(sport: str) -> str:
            """Analyze trending products in the sports market."""
            return f"Trending products analysis for {sport}"
        
        @tool
        def suggest_inventory_mix(sport: str, store_size: str) -> str:
            """Suggest optimal inventory mix based on store size and sport."""
            return f"Inventory mix for {sport} store of {store_size} size"
        
        @tool
        def identify_profit_margins(sport: str, product_category: str) -> str:
            """Identify high-margin product opportunities."""
            return f"Profit margin analysis for {product_category} in {sport}"
        
        @tool
        def recommend_suppliers(sport: str, location: str) -> str:
            """Recommend reliable suppliers and vendors."""
            return f"Supplier recommendations for {sport} store in {location}"
        
        return [analyze_trending_products, suggest_inventory_mix, 
                identify_profit_margins, recommend_suppliers]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the product agent with specialized prompts."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sports retail expert specializing in product strategy and inventory management.
            Your expertise includes:
            - Sports equipment and apparel trends
            - Inventory optimization and stock management
            - Supplier relationships and sourcing
            - Product pricing and margin analysis
            - Seasonal product planning
            
            Always consider:
            - Current market trends and consumer preferences
            - Seasonal demand patterns
            - Price point optimization
            - Quality vs. cost trade-offs
            - Local market preferences
            - E-commerce vs. brick-and-mortar product mix"""),
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
    
    def generate_product_strategy(self, sport: str, store_name: str, location: str = None) -> dict:
        """Generate comprehensive product strategy for a sports store."""
        prompt = f"""
        Create a comprehensive product strategy for {store_name}, a {sport} store{f" in {location}" if location else ""}.
        
        Please provide:
        1. Core product categories and must-have items
        2. Trending products and seasonal items
        3. Inventory mix recommendations (apparel, equipment, accessories)
        4. Pricing strategy and margin analysis
        5. Supplier recommendations and sourcing strategy
        6. Seasonal product planning
        7. E-commerce product selection
        8. Exclusive or private-label opportunities
        
        Focus on profitable, high-demand products that align with the target market.
        """
        
        response = self.agent.invoke({"input": prompt})
        return {
            "sport": sport,
            "store_name": store_name,
            "location": location,
            "product_strategy": response["output"],
            "agent_type": "product"
        } 