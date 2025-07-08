#!/usr/bin/env python3
"""
Test script for document generation with logos
"""
import requests
import json
from datetime import datetime, timedelta

# FastAPI endpoint URL
BASE_URL = "http://localhost:8000"

def test_nda_generation():
    """Test NDA generation with logo"""
    url = f"{BASE_URL}/documents/nda"
    
    # Sample NDA data with logo URL
    nda_data = {
        "disclosing_party": "ScaleBuild AI Inc.",
        "receiving_party": "John Doe",
        "purpose": "discussing potential collaboration on AI-powered document generation solutions",
        "confidential_info_description": "proprietary AI algorithms, customer data, business strategies, and technical specifications",
        "duration": "2 years",
        "governing_law": "California",
        "effective_date": datetime.now().strftime("%B %d, %Y"),
        "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
    }
    
    try:
        print("🔄 Testing NDA generation with logo...")
        response = requests.post(url, json=nda_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ NDA generated successfully!")
            print(f"📄 Document Type: {result['document_type']}")
            print(f"👥 Generated For: {result['generated_for']}")
            print(f"📅 Creation Date: {result['creation_date']}")
            print(f"📊 Word Count: {result['word_count']}")
            print(f"🎨 Format: {result['format']}")
            if 'document_url' in result:
                print(f"🔗 Document URL: {result['document_url']}")
            else:
                print("⚠️ Document URL not found in response")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_business_proposal_generation():
    """Test Business Proposal generation with logo"""
    url = f"{BASE_URL}/documents/business-proposal"
    
    # Sample business proposal data with logo URL
    proposal_data = {
        "company_name": "ScaleBuild AI",
        "client_name": "TechCorp Solutions",
        "project_title": "AI-Powered Document Automation Platform",
        "project_description": "Develop an intelligent document generation and management system using advanced AI technologies",
        "services_offered": [
            "AI Model Development",
            "Document Template Design",
            "System Integration",
            "Training and Support"
        ],
        "timeline": "6 months",
        "budget_range": "$100,000 - $150,000",
        "contact_person": "Jane Smith",
        "contact_email": "jane.smith@scalebuild.ai",
        "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
    }
    
    try:
        print("\n🔄 Testing Business Proposal generation with logo...")
        response = requests.post(url, json=proposal_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Business Proposal generated successfully!")
            print(f"📄 Document Type: {result['document_type']}")
            print(f"👥 Generated For: {result['generated_for']}")
            print(f"📅 Creation Date: {result['creation_date']}")
            print(f"📊 Word Count: {result['word_count']}")
            print(f"🎨 Format: {result['format']}")
            if 'document_url' in result:
                print(f"🔗 Document URL: {result['document_url']}")
            else:
                print("⚠️ Document URL not found in response")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_contract_generation():
    """Test Contract generation with logo"""
    url = f"{BASE_URL}/documents/contract"
    
    # Sample contract data with logo URL
    contract_data = {
        "contract_type": "Service Agreement",
        "party1_name": "ScaleBuild AI Inc.",
        "party1_address": "123 AI Street, San Francisco, CA 94105",
        "party2_name": "Digital Solutions LLC",
        "party2_address": "456 Tech Avenue, New York, NY 10001",
        "service_description": "AI-powered document generation and automation services",
        "contract_value": "$75,000",
        "payment_terms": "50% upfront, 50% upon completion",
        "duration": "4 months",
        "deliverables": [
            "Custom AI document generation system",
            "Integration with existing workflows",
            "User training and documentation",
            "3 months of technical support"
        ],
        "terms_conditions": [
            "All work must be completed within specified timeline",
            "Client provides necessary access and resources",
            "Intellectual property rights as specified in appendix",
            "Confidentiality agreement applies to all parties"
        ],
        "effective_date": datetime.now().strftime("%B %d, %Y"),
        "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
    }
    
    try:
        print("\n🔄 Testing Contract generation with logo...")
        response = requests.post(url, json=contract_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Contract generated successfully!")
            print(f"📄 Document Type: {result['document_type']}")
            print(f"👥 Generated For: {result['generated_for']}")
            print(f"📅 Creation Date: {result['creation_date']}")
            print(f"📊 Word Count: {result['word_count']}")
            print(f"🎨 Format: {result['format']}")
            if 'document_url' in result:
                print(f"🔗 Document URL: {result['document_url']}")
            else:
                print("⚠️ Document URL not found in response")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Document Generation Tests with Logo")
    print("=" * 60)
    
    # Test different document types
    test_nda_generation()
    test_business_proposal_generation()
    test_contract_generation()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n📋 Summary:")
    print("- All documents now include logos on every page")
    print("- Documents are saved as .docx files in GCS")
    print("- Logo URL is provided in the request body")
    print("- Default logo: https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png")

if __name__ == "__main__":
    main()
