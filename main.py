import streamlit as st
import LangChainHelper
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="SportStore AI - Intelligent Sports Business Assistant",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .demo-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_demo_response(sport, location=None):
    """Generate demo response for testing without API key."""
    demo_data = {
        "Basketball": {
            "store_name": "🏀 Hoops Haven",
            "tagline": "Where Champions Shop",
            "products": ["Basketballs", "Jerseys", "Sneakers", "Training Equipment", "Court Gear"],
            "branding": "Modern, energetic brand with orange and black colors",
            "marketing": "Social media campaigns, local team partnerships, community events",
            "strategy": "Focus on youth leagues and amateur tournaments"
        },
        "Soccer": {
            "store_name": "⚽ Goal Getter Pro",
            "tagline": "Score Your Dreams",
            "products": ["Soccer Balls", "Cleats", "Jerseys", "Training Cones", "Goal Posts"],
            "branding": "Professional green and white theme with European influence",
            "marketing": "Academy partnerships, tournament sponsorships, online presence",
            "strategy": "Target youth development and competitive leagues"
        },
        "Tennis": {
            "store_name": "🎾 Ace Tennis Elite",
            "tagline": "Serve Your Passion",
            "products": ["Tennis Rackets", "Balls", "Court Shoes", "Apparel", "Training Aids"],
            "branding": "Elegant white and gold design with premium positioning",
            "marketing": "Club partnerships, tournament gear, coaching programs",
            "strategy": "Premium equipment and coaching services"
        }
    }
    
    sport_data = demo_data.get(sport, demo_data["Basketball"])
    
    return {
        "comprehensive_analysis": {
            "structured_analysis": f"""
Store Analysis:
- Store Name: {sport_data['store_name']}
- Tagline: {sport_data['tagline']}
- Target Audience: Sports enthusiasts and athletes
- Price Range: Mid to premium
- Unique Selling Proposition: Specialized {sport} expertise

Product Recommendations:
- Category: Equipment and Apparel
- Items: {', '.join(sport_data['products'])}
- Description: Comprehensive {sport} gear for all skill levels

Market Insights:
- Trend Analysis: Growing interest in {sport} participation
- Competitive Landscape: Focus on specialized expertise
- Opportunities: Local community engagement
- Challenges: Competition from big-box retailers

Success Factors:
- Key Factors: Expert staff, quality products, community involvement
- Risk Mitigation: Diversified product mix, strong online presence
- Growth Potential: Youth programs and tournament partnerships
            """
        },
        "branding_package": f"""
BRANDING PACKAGE FOR {sport.upper()} STORE

Store Name: {sport_data['store_name']}
Tagline: {sport_data['tagline']}
Brand Colors: {sport_data['branding']}
Target Audience: {sport} enthusiasts of all ages
Brand Personality: Professional, passionate, community-focused
            """,
        "marketing_strategy": f"""
MARKETING STRATEGY

{sport_data['marketing']}

Key Channels:
• Social Media Marketing
• Local Community Events
• Partnership Programs
• Online Advertising
• Email Campaigns

Budget Allocation:
• Digital Marketing: 40%
• Local Advertising: 30%
• Community Events: 20%
• Partnerships: 10%
            """,
        "product_strategy": f"""
PRODUCT STRATEGY

Core Products: {', '.join(sport_data['products'])}

{sport_data['strategy']}

Inventory Management:
• Seasonal planning
• Trend analysis
• Supplier relationships
• Quality control
            """,
        "token_usage": {
            "total_tokens": 1500,
            "total_cost": 0.045
        }
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">🏀 SportStore AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent Sports Business Assistant with Multi-Agent Workflows</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Sport selection
        sport = st.selectbox(
            "🏈 Select Sport",
            ["Basketball", "Soccer", "Baseball", "Cricket", "Tennis", "Football", 
             "Hockey", "Volleyball", "Golf", "Swimming", "Running", "Cycling"]
        )
        
        # Location input
        location = st.text_input("📍 Location (Optional)", placeholder="e.g., New York, NY")
        
        # Analysis type
        analysis_type = st.radio(
            "📊 Analysis Type",
            ["Basic (Store Name + Products)", "Comprehensive (Multi-Agent Analysis)"],
            help="Basic: Quick store name and products\nComprehensive: Full business plan with branding, marketing, and strategy"
        )
        
        # Demo mode toggle
        demo_mode = st.checkbox("🎮 Demo Mode", value=False, 
                              help="Try the app without an API key (limited sports)")
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            api_key = st.text_input("🔑 OpenAI API Key", type="password", 
                                  help="Leave empty to use environment variable")
            
            temperature = st.slider("🌡️ Creativity Level", 0.0, 1.0, 0.7, 0.1,
                                  help="Higher values = more creative, Lower values = more focused")
            
            enable_memory = st.checkbox("🧠 Enable Memory", value=True,
                                      help="Remember conversation context")
        
        st.markdown("---")
    
    # Main content area
    if sport:
        # Check for API key or demo mode
        api_key_to_use = api_key if api_key else os.getenv("OPENAI_API_KEY")
        
        if not api_key_to_use and not demo_mode:
            st.markdown('<div class="error-message">❌ OpenAI API Key Required</div>', unsafe_allow_html=True)
            st.markdown("""
            **To use SportStore AI, you need to provide an OpenAI API key:**
            
            1. **Get an API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
            2. **Add it to the sidebar** in the "Advanced Options" section
            3. **Or set it as an environment variable** in your `.env` file
            4. **Or enable Demo Mode** to try the app without an API key
            
            ```bash
            # In your .env file
            OPENAI_API_KEY=sk-your-actual-api-key-here
            ```
            """)
            return
        
        # Initialize helper only when needed
        helper = None
        if not demo_mode:
            try:
                helper = LangChainHelper.AdvancedLangChainHelper(api_key_to_use)
            except Exception as e:
                st.markdown('<div class="error-message">❌ Error Initializing AI Assistant</div>', unsafe_allow_html=True)
                st.error(f"Failed to initialize AI assistant: {str(e)}")
                st.info("Please check your API key and internet connection, or enable Demo Mode.")
                return
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_button = st.button("🚀 Generate Business Plan", type="primary", use_container_width=True)
        
        if generate_button:
            with st.spinner("🤖 AI agents are working on your business plan..."):
                try:
                    if demo_mode:
                        st.markdown('<div class="demo-message">🎮 Demo Mode: Showing sample data</div>', unsafe_allow_html=True)
                        response = generate_demo_response(sport, location)
                    else:
                        if analysis_type == "Basic (Store Name + Products)":
                            # Basic analysis
                            response = helper.generate_store_name_and_items(sport)
                            
                            # Display results
                            st.markdown('<h2 class="sub-header">🏪 Store Concept</h2>', unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### Store Name")
                                st.success(response['store'].strip())
                            
                            with col2:
                                st.markdown("### Products")
                                goods_name = response['goods_name'].strip().split(",")
                                for item in goods_name:
                                    st.write(f"• {item.strip()}")
                            
                            return
                        else:
                            # Comprehensive analysis
                            response = helper.generate_comprehensive_store_analysis(sport, location)
                            
                            if "error" in response:
                                st.error(f"❌ Error: {response['error']}")
                                if "fallback" in response:
                                    st.info("🔄 Using fallback analysis...")
                                    fallback = response['fallback']
                                    st.success(f"Store Name: {fallback['store']}")
                                    st.write("Products:", fallback['goods_name'])
                                return
                    
                    # Display comprehensive results
                    st.markdown('<div class="success-message">✅ Business plan generated successfully!</div>', unsafe_allow_html=True)
                    
                    # Token usage metrics
                    if "token_usage" in response:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Tokens", f"{response['token_usage']['total_tokens']:,}")
                        with col2:
                            st.metric("Total Cost", f"${response['token_usage']['total_cost']:.4f}")
                        with col3:
                            st.metric("Analysis Type", "Multi-Agent" if not demo_mode else "Demo")
                    
                    # Create tabs for organized display
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏪 Store & Branding", "📦 Products", "📈 Marketing", "📊 Analysis", "💾 Export"])
                    
                    with tab1:
                        st.markdown('<h3 class="sub-header">Store & Branding</h3>', unsafe_allow_html=True)
                        st.markdown("### Branding Package")
                        st.write(response['branding_package'])
                    
                    with tab2:
                        st.markdown('<h3 class="sub-header">Product Strategy</h3>', unsafe_allow_html=True)
                        st.markdown("### Product Recommendations")
                        st.write(response['product_strategy'])
                    
                    with tab3:
                        st.markdown('<h3 class="sub-header">Marketing Strategy</h3>', unsafe_allow_html=True)
                        st.markdown("### Marketing Approach")
                        st.write(response['marketing_strategy'])
                    
                    with tab4:
                        st.markdown('<h3 class="sub-header">Comprehensive Analysis</h3>', unsafe_allow_html=True)
                        if "comprehensive_analysis" in response:
                            analysis = response['comprehensive_analysis']
                            st.markdown("### Structured Analysis")
                            st.write(analysis.get('structured_analysis', 'Analysis not available'))
                    
                    with tab5:
                        st.markdown('<h3 class="sub-header">Export Options</h3>', unsafe_allow_html=True)
                        
                        # Export buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📄 Export as JSON"):
                                json_data = json.dumps(response, indent=2) if demo_mode else helper.export_analysis(response, "json")
                                st.download_button(
                                    label="⬇️ Download JSON",
                                    data=json_data,
                                    file_name=f"sportstore_analysis_{sport}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json"
                                )
                        
                        with col2:
                            if st.button("📝 Export as Text"):
                                text_data = f"""
SPORTS STORE ANALYSIS
====================

Sport: {sport}
Location: {location or 'N/A'}

BRANDING PACKAGE:
{response.get('branding_package', 'N/A')}

MARKETING STRATEGY:
{response.get('marketing_strategy', 'N/A')}

PRODUCT STRATEGY:
{response.get('product_strategy', 'N/A')}

STRUCTURED ANALYSIS:
{response.get('comprehensive_analysis', {}).get('structured_analysis', 'N/A')}
                                """ if demo_mode else helper.export_analysis(response, "txt")
                                st.download_button(
                                    label="⬇️ Download Text",
                                    data=text_data,
                                    file_name=f"sportstore_analysis_{sport}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                        
                        # Conversation history
                        if "conversation_history" in response and response['conversation_history']:
                            st.markdown("### 💬 Conversation History")
                            with st.expander("View conversation history"):
                                for msg in response['conversation_history']:
                                    st.write(f"**{msg.type}**: {msg.content}")
                
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("💡 Please check your API key and internet connection, or try Demo Mode.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>Built with ❤️ using LangChain, OpenAI, and Streamlit</p>
        <p>SportStore AI - Intelligent Sports Business Assistant</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
        