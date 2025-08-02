#!/usr/bin/env python3
"""
Test script for SportStore AI enhanced features.
This script demonstrates the multi-agent architecture and advanced capabilities.
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from LangChainHelper import AdvancedLangChainHelper
from agents.naming_agent import NamingAgent
from agents.marketing_agent import MarketingAgent
from agents.product_agent import ProductAgent
from tools.market_research import MarketResearchTool, CompetitorAnalysisTool

def test_basic_functionality():
    """Test basic store name and items generation."""
    print("🧪 Testing Basic Functionality...")
    
    helper = AdvancedLangChainHelper()
    sport = "Basketball"
    
    try:
        result = helper.generate_store_name_and_items(sport)
        print(f"✅ Basic test passed for {sport}")
        print(f"Store: {result['store']}")
        print(f"Products: {result['goods_name']}")
        return True
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def test_multi_agent_system():
    """Test the multi-agent system."""
    print("\n🤖 Testing Multi-Agent System...")
    
    try:
        # Test naming agent
        naming_agent = NamingAgent()
        branding_result = naming_agent.generate_complete_branding("Soccer", "New York")
        print("✅ Naming agent test passed")
        
        # Test marketing agent
        marketing_agent = MarketingAgent()
        marketing_result = marketing_agent.generate_marketing_strategy("Test Store", "Soccer", "New York")
        print("✅ Marketing agent test passed")
        
        # Test product agent
        product_agent = ProductAgent()
        product_result = product_agent.generate_product_strategy("Soccer", "Test Store", "New York")
        print("✅ Product agent test passed")
        
        return True
    except Exception as e:
        print(f"❌ Multi-agent test failed: {e}")
        return False

def test_comprehensive_analysis():
    """Test comprehensive analysis with all agents."""
    print("\n📊 Testing Comprehensive Analysis...")
    
    helper = AdvancedLangChainHelper()
    sport = "Tennis"
    location = "Los Angeles"
    
    try:
        result = helper.generate_comprehensive_store_analysis(sport, location)
        
        if "error" in result:
            print(f"❌ Comprehensive analysis failed: {result['error']}")
            return False
        
        print("✅ Comprehensive analysis test passed")
        print(f"Sport: {sport}")
        print(f"Location: {location}")
        
        if "token_usage" in result:
            print(f"Token Usage: {result['token_usage']['total_tokens']} tokens")
            print(f"Cost: ${result['token_usage']['total_cost']:.4f}")
        
        return True
    except Exception as e:
        print(f"❌ Comprehensive analysis test failed: {e}")
        return False

def test_market_research_tools():
    """Test market research tools."""
    print("\n🔍 Testing Market Research Tools...")
    
    try:
        # Test market research tool
        market_tool = MarketResearchTool()
        market_result = market_tool._run("Basketball", "Chicago")
        print("✅ Market research tool test passed")
        
        # Test competitor analysis tool
        competitor_tool = CompetitorAnalysisTool()
        competitor_result = competitor_tool._run("Basketball", "Chicago")
        print("✅ Competitor analysis tool test passed")
        
        return True
    except Exception as e:
        print(f"❌ Market research tools test failed: {e}")
        return False

def test_memory_and_export():
    """Test memory functionality and export capabilities."""
    print("\n💾 Testing Memory and Export...")
    
    helper = AdvancedLangChainHelper()
    sport = "Baseball"
    
    try:
        # Generate analysis
        result = helper.generate_comprehensive_store_analysis(sport)
        
        # Test memory
        history = helper.get_conversation_history()
        print(f"✅ Memory test passed - {len(history)} messages in history")
        
        # Test export
        json_export = helper.export_analysis(result, "json")
        txt_export = helper.export_analysis(result, "txt")
        
        print("✅ Export test passed")
        print(f"JSON export length: {len(json_export)} characters")
        print(f"Text export length: {len(txt_export)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Memory and export test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and fallback mechanisms."""
    print("\n🛡️ Testing Error Handling...")
    
    try:
        # Test with invalid sport
        helper = AdvancedLangChainHelper()
        result = helper.generate_store_name_and_items("InvalidSport123")
        
        # Should still return something (fallback)
        if result and 'store' in result and 'goods_name' in result:
            print("✅ Error handling test passed - fallback mechanism working")
            return True
        else:
            print("❌ Error handling test failed - no fallback")
            return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_performance_benchmark():
    """Run a performance benchmark."""
    print("\n⚡ Running Performance Benchmark...")
    
    import time
    
    sports = ["Basketball", "Soccer", "Tennis", "Baseball"]
    helper = AdvancedLangChainHelper()
    
    start_time = time.time()
    total_tokens = 0
    total_cost = 0
    
    for sport in sports:
        try:
            result = helper.generate_store_name_and_items(sport)
            if "token_usage" in result:
                total_tokens += result["token_usage"]["total_tokens"]
                total_cost += result["token_usage"]["total_cost"]
        except Exception as e:
            print(f"Warning: Failed to process {sport}: {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Performance benchmark completed")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Sports processed: {len(sports)}")
    print(f"Average time per sport: {duration/len(sports):.2f} seconds")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Total cost: ${total_cost:.4f}")

def main():
    """Run all tests."""
    print("🚀 SportStore AI - Enhanced Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Multi-Agent System", test_multi_agent_system),
        ("Comprehensive Analysis", test_comprehensive_analysis),
        ("Market Research Tools", test_market_research_tools),
        ("Memory and Export", test_memory_and_export),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
    
    # Run performance benchmark
    run_performance_benchmark()
    
    print("\n✨ Test suite completed!")

if __name__ == "__main__":
    main() 