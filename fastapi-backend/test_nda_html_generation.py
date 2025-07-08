#!/usr/bin/env python3
"""
Test script for NDA generation with HTML-to-DOCX conversion
Tests the enhanced NDA service that generates professional HTML first, then converts to DOCX
"""

import asyncio
import json
from services.nda_service import generate_nda
from datetime import datetime

async def test_enhanced_nda_generation():
    """Test the enhanced NDA generation with HTML-to-DOCX conversion"""
    
    # Test data
    test_data = {
        "disclosing_party": "ScaleBuild AI Technologies Inc.",
        "receiving_party": "Jane Smith",
        "purpose": "consulting services and product development collaboration",
        "confidential_info_description": "proprietary AI algorithms, customer data, business strategies, and technical specifications",
        "duration": "3 years from the date of signing",
        "governing_law": "State of California",
        "effective_date": datetime.now().strftime("%B %d, %Y"),
        "logo_url": "https://example.com/logo.png"
    }
    
    print("🔄 Testing Enhanced NDA Generation with HTML-to-DOCX Conversion")
    print("=" * 60)
    
    try:
        # Generate NDA
        print("📄 Generating NDA with HTML formatting...")
        result = await generate_nda(test_data)
        
        print("\n✅ NDA Generation Successful!")
        print(f"📊 Document Type: {result['document_type']}")
        print(f"👥 Generated For: {result['generated_for']}")
        print(f"📅 Creation Date: {result['creation_date']}")
        print(f"📝 Word Count: {result['word_count']}")
        print(f"📄 Format: {result['format']}")
        print(f"🔗 Document URL: {result['document_url']}")
        
        # Show HTML content preview (first 500 characters)
        content_preview = result['document_content'][:500] + "..." if len(result['document_content']) > 500 else result['document_content']
        print(f"\n📋 HTML Content Preview:")
        print("-" * 40)
        print(content_preview)
        print("-" * 40)
        
        # Verify HTML structure
        html_content = result['document_content']
        html_checks = {
            "Contains DOCTYPE": "<!DOCTYPE html>" in html_content,
            "Contains CSS styles": "<style>" in html_content,
            "Contains header section": 'class="header"' in html_content,
            "Contains parties section": 'class="parties"' in html_content,
            "Contains sections": 'class="section"' in html_content,
            "Contains signature section": 'class="signature-section"' in html_content,
            "Contains proper HTML structure": "<html" in html_content and "</html>" in html_content
        }
        
        print(f"\n🔍 HTML Structure Verification:")
        for check, passed in html_checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}")
        
        # Check if all required data is included
        data_checks = {
            "Disclosing Party": test_data["disclosing_party"] in html_content,
            "Receiving Party": test_data["receiving_party"] in html_content,
            "Purpose": test_data["purpose"] in html_content,
            "Duration": test_data["duration"] in html_content,
            "Governing Law": test_data["governing_law"] in html_content,
            "Effective Date": test_data["effective_date"] in html_content
        }
        
        print(f"\n📋 Data Inclusion Verification:")
        for check, passed in data_checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}")
        
        # Overall success
        all_html_checks = all(html_checks.values())
        all_data_checks = all(data_checks.values())
        
        if all_html_checks and all_data_checks:
            print(f"\n🎉 All tests passed! Enhanced NDA generation is working correctly.")
            print(f"📄 The HTML-to-DOCX conversion should produce a professional document.")
        else:
            print(f"\n⚠️  Some tests failed. Please check the implementation.")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during NDA generation: {e}")
        raise e

async def test_multiple_nda_scenarios():
    """Test NDA generation with different scenarios"""
    
    scenarios = [
        {
            "name": "Corporate NDA",
            "data": {
                "disclosing_party": "TechCorp Industries Ltd.",
                "receiving_party": "John Doe",
                "purpose": "merger and acquisition discussions",
                "confidential_info_description": "financial statements, strategic plans, and proprietary technology",
                "duration": "5 years from the date of signing",
                "governing_law": "State of New York",
                "effective_date": "January 15, 2024",
                "logo_url": "https://example.com/techcorp-logo.png"
            }
        },
        {
            "name": "Startup NDA",
            "data": {
                "disclosing_party": "InnovateTech Startup",
                "receiving_party": "Sarah Johnson",
                "purpose": "product development and marketing consultation",
                "confidential_info_description": "startup business model, user data, and technical architecture",
                "duration": "2 years from the date of signing",
                "governing_law": "State of Delaware",
                "effective_date": "March 1, 2024",
                "logo_url": "https://example.com/innovate-logo.png"
            }
        }
    ]
    
    print("\n🔄 Testing Multiple NDA Scenarios")
    print("=" * 60)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print("-" * 30)
        
        try:
            result = await generate_nda(scenario['data'])
            print(f"✅ {scenario['name']} generated successfully!")
            print(f"📄 Document URL: {result['document_url']}")
            print(f"📝 Word Count: {result['word_count']}")
            
        except Exception as e:
            print(f"❌ Error generating {scenario['name']}: {e}")

if __name__ == "__main__":
    print("🚀 Starting Enhanced NDA Generation Tests")
    print("=" * 60)
    
    asyncio.run(test_enhanced_nda_generation())
    asyncio.run(test_multiple_nda_scenarios())
    
    print("\n🏁 All tests completed!")
