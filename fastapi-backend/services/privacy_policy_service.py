from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_document_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- Privacy Policy Template ---
privacy_policy_template = """You are a legal document specialist. Create a comprehensive Privacy Policy based on the following information:

Company Name: {company_name}
Website URL: {website_url}
Company Address: {company_address}
Data Collected: {data_collected}
Data Usage Purpose: {data_usage_purpose}
Third Party Sharing: {third_party_sharing}
Data Retention Period: {data_retention_period}
User Rights: {user_rights}
Cookies Usage: {cookies_usage}
Contact Email: {contact_email}
Governing Law: {governing_law}
Effective Date: {effective_date}

Generate a comprehensive Privacy Policy that includes:

1. Information We Collect
2. How We Use Your Information
3. Information Sharing and Disclosure
4. Data Security
5. Data Retention
6. Your Rights and Choices
7. Cookies and Tracking Technologies
8. Children's Privacy
9. International Data Transfers
10. Changes to Privacy Policy
11. Contact Information
12. Compliance with Laws (GDPR, CCPA, etc.)

Ensure compliance with major privacy regulations and use clear, accessible language."""

privacy_policy_prompt = PromptTemplate.from_template(privacy_policy_template)
privacy_policy_chain = privacy_policy_prompt | model | StrOutputParser()

async def generate_privacy_policy(data: dict):
    """Generate Privacy Policy document using GPT-4o"""
    try:
        data_collected_list = ", ".join(data.get("data_collected", []))
        data_usage_list = ", ".join(data.get("data_usage_purpose", []))
        user_rights_list = ", ".join(data.get("user_rights", []))
        
        document_content = ""
        async for chunk in privacy_policy_chain.astream({
            "company_name": data.get("company_name"),
            "website_url": data.get("website_url"),
            "company_address": data.get("company_address"),
            "data_collected": data_collected_list,
            "data_usage_purpose": data_usage_list,
            "third_party_sharing": data.get("third_party_sharing"),
            "data_retention_period": data.get("data_retention_period"),
            "user_rights": user_rights_list,
            "cookies_usage": data.get("cookies_usage"),
            "contact_email": data.get("contact_email"),
            "governing_law": data.get("governing_law"),
            "effective_date": data.get("effective_date")
        }):
            document_content += chunk
        
        return {
            "document_content": document_content.strip(),
            "document_type": "Privacy Policy",
            "generated_for": data.get("company_name"),
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split())
        }
    except Exception as e:
        print(f"Error in Privacy Policy generation: {e}")
        raise e
