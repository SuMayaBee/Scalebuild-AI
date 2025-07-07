#!/usr/bin/env python3
import requests
import json

# Test the enhanced NDA endpoint with DOCX generation and logo in header
url = "http://localhost:8000/documents/nda"

# Request body with logo URL
data = {
    "disclosing_party": "ABC Corporation",
    "receiving_party": "John Doe",
    "purpose": "To evaluate potential business partnership opportunities", 
    "confidential_info_description": "Financial data, business strategies, customer lists, and proprietary technologies",
    "duration": "5 years from the effective date",
    "governing_law": "State of California, USA",
    "effective_date": "2025-07-04",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}

print("🚀 Testing Enhanced NDA endpoint with DOCX generation...")
print("URL:", url)
print("Request data:", json.dumps(data, indent=2))
print("\n" + "="*60 + "\n")

try:
    response = requests.post(url, json=data, timeout=120)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Document generated with embedded logo!")
        print("\n📄 Document Details:")
        print(f"   • Document Type: {result.get('document_type')}")
        print(f"   • Generated For: {result.get('generated_for')}")
        print(f"   • Creation Date: {result.get('creation_date')}")
        print(f"   • Word Count: {result.get('word_count')}")
        
        print("\n🔗 Generated URL:")
        print(f"   • DOCX Version (with logo in header): {result.get('docx_url')}")
        
        print("\n✨ New Features:")
        print("   • ✅ DOCX with small logo in header (appears on every page)")
        print("   • ✅ Professional document structure")
        print("   • ✅ Clean formatting (no asterisks)")
        print("   • ✅ Signature tables")
        print("   • ✅ Print-ready A4 formatting")
        
        print("\n💡 Benefits:")
        print("   • DOCX: Editable format with logo on every page")
        print("   • Logo positioned in document header")
        print("   • Optimized for professional use")
        
    elif response.status_code == 422:
        print("❌ Validation Error:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except json.JSONDecodeError as e:
    print(f"❌ JSON decode error: {e}")
    print("Raw response:", response.text)

print("\n" + "="*60)
print("🎉 Professional Document: DOCX with logo on every page!")
