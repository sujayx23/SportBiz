
import os
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import PydanticOutputParser
from langchain_community.callbacks import get_openai_callback
from pydantic import BaseModel, Field
from agents.naming_agent import NamingAgent
from agents.marketing_agent import MarketingAgent
from agents.product_agent import ProductAgent
import json

# Pydantic models for structured output
class StoreAnalysis(BaseModel):
    store_name: str = Field(description="Creative store name")
    tagline: str = Field(description="Catchy tagline")
    target_audience: str = Field(description="Primary target audience")
    price_range: str = Field(description="Price positioning")
    unique_selling_proposition: str = Field(description="What makes this store unique")

class ProductRecommendation(BaseModel):
    category: str = Field(description="Product category")
    items: List[str] = Field(description="Specific product recommendations")
    description: str = Field(description="Why these products are recommended")

class MarketInsight(BaseModel):
    trend_analysis: str = Field(description="Current market trends")
    competitive_landscape: str = Field(description="Competition analysis")
    opportunities: str = Field(description="Market opportunities")
    challenges: str = Field(description="Potential challenges")

class SuccessFactor(BaseModel):
    key_factors: List[str] = Field(description="Critical success factors")
    risk_mitigation: str = Field(description="Risk mitigation strategies")
    growth_potential: str = Field(description="Growth opportunities")

class ComprehensiveAnalysis(BaseModel):
    store_analysis: StoreAnalysis
    products: List[ProductRecommendation]
    market_insights: MarketInsight
    success_factors: SuccessFactor
    branding_package: str = Field(description="Complete branding strategy")
    marketing_strategy: str = Field(description="Marketing approach")
    product_strategy: str = Field(description="Product and inventory strategy")

class AdvancedLangChainHelper:
    """Enhanced LangChain helper with multi-agent orchestration and advanced features."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo for cost efficiency
            temperature=0.7,
            api_key=self.api_key
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize specialized agents
        self.naming_agent = NamingAgent(self.api_key)
        self.marketing_agent = MarketingAgent(self.api_key)
        self.product_agent = ProductAgent(self.api_key)
        
        # Initialize output parser
        self.output_parser = PydanticOutputParser(pydantic_object=ComprehensiveAnalysis)
        
    def generate_store_name_and_items(self, sport: str) -> Dict:
        """Basic store name and items generation (backward compatibility)."""
        try:
            # Use the naming agent for store name
            branding_result = self.naming_agent.generate_complete_branding(sport)
            
            # Use the product agent for items
            product_result = self.product_agent.generate_product_strategy(sport, "Store", None)
            
            return {
                'store': branding_result.get('branding_package', 'Store Name'),
                'goods_name': product_result.get('product_strategy', 'Product List')
            }
        except Exception as e:
            return {
                'store': f"Error generating store name: {str(e)}",
                'goods_name': f"Error generating products: {str(e)}"
            }
    
    def generate_comprehensive_store_analysis(self, sport: str, location: str = None) -> Dict:
        """Generate comprehensive analysis using multi-agent orchestration."""
        try:
            with get_openai_callback() as cb:
                # Step 1: Generate branding with naming agent
                branding_result = self.naming_agent.generate_complete_branding(sport, location)
                
                # Extract store name from branding result
                store_name = self._extract_store_name(branding_result['branding_package'])
                
                # Step 2: Generate marketing strategy
                marketing_result = self.marketing_agent.generate_marketing_strategy(
                    store_name, sport, location
                )
                
                # Step 3: Generate product strategy
                product_result = self.product_agent.generate_product_strategy(
                    sport, store_name, location
                )
                
                # Step 4: Generate comprehensive analysis
                comprehensive_analysis = self._generate_structured_analysis(
                    sport, store_name, location, branding_result, marketing_result, product_result
                )
                
                return {
                    "comprehensive_analysis": comprehensive_analysis,
                    "branding_package": branding_result['branding_package'],
                    "marketing_strategy": marketing_result['marketing_strategy'],
                    "product_strategy": product_result['product_strategy'],
                    "token_usage": {
                        "total_tokens": cb.total_tokens,
                        "total_cost": cb.total_cost
                    },
                    "conversation_history": self.memory.chat_memory.messages
                }
                
        except Exception as e:
            return {
                "error": f"Error in comprehensive analysis: {str(e)}",
                "fallback": self.generate_store_name_and_items(sport)
            }
    
    def _extract_store_name(self, branding_package: str) -> str:
        """Extract store name from branding package."""
        try:
            # Simple extraction - look for patterns like "Store Name:" or "Name:"
            lines = branding_package.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['store name:', 'name:', 'brand name:']):
                    return line.split(':')[-1].strip()
            return "Sports Store"  # Fallback
        except:
            return "Sports Store"
    
    def _generate_structured_analysis(self, sport: str, store_name: str, location: str,
                                   branding_result: Dict, marketing_result: Dict, product_result: Dict) -> Dict:
        """Generate structured analysis using the main LLM."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sports business consultant. Create a structured analysis of a sports store concept.
            Provide detailed, actionable insights in the following format:
            
            Store Analysis:
            - Store Name: [Creative name]
            - Tagline: [Catchy tagline]
            - Target Audience: [Specific demographics]
            - Price Range: [Budget, mid-range, premium]
            - Unique Selling Proposition: [What makes this store special]
            
            Product Recommendations:
            - Category: [Equipment/Apparel/Accessories]
            - Items: [Specific product list]
            - Description: [Why these products are recommended]
            
            Market Insights:
            - Trend Analysis: [Current market trends]
            - Competitive Landscape: [Competition analysis]
            - Opportunities: [Market opportunities]
            - Challenges: [Potential challenges]
            
            Success Factors:
            - Key Factors: [Critical success factors]
            - Risk Mitigation: [Risk strategies]
            - Growth Potential: [Growth opportunities]"""),
            ("human", f"""
            Sport: {sport}
            Store Name: {store_name}
            Location: {location or 'General'}
            
            Branding Package: {branding_result['branding_package']}
            Marketing Strategy: {marketing_result['marketing_strategy']}
            Product Strategy: {product_result['product_strategy']}
            
            Please provide a comprehensive, structured analysis.
            """)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        return {
            "structured_analysis": response.content,
            "sport": sport,
            "store_name": store_name,
            "location": location
        }
    
    def get_conversation_history(self) -> List:
        """Get conversation history for context."""
        return self.memory.chat_memory.messages
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()
    
    def export_analysis(self, analysis: Dict, format: str = "json") -> str:
        """Export analysis in specified format."""
        if format.lower() == "json":
            return json.dumps(analysis, indent=2)
        elif format.lower() == "txt":
            # Convert to readable text format
            text_output = f"""
SPORTS STORE ANALYSIS
====================

Sport: {analysis.get('sport', 'N/A')}
Store Name: {analysis.get('store_name', 'N/A')}
Location: {analysis.get('location', 'N/A')}

BRANDING PACKAGE:
{analysis.get('branding_package', 'N/A')}

MARKETING STRATEGY:
{analysis.get('marketing_strategy', 'N/A')}

PRODUCT STRATEGY:
{analysis.get('product_strategy', 'N/A')}

STRUCTURED ANALYSIS:
{analysis.get('comprehensive_analysis', {}).get('structured_analysis', 'N/A')}
            """
            return text_output
        else:
            return str(analysis)

# Backward compatibility function
def generate_store_name_and_items(sport: str) -> Dict:
    """Legacy function for backward compatibility."""
    helper = AdvancedLangChainHelper()
    return helper.generate_store_name_and_items(sport)
