from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_docx_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- Terms of Service Template ---
terms_of_service_template = """You are a legal document specialist. Create comprehensive Terms of Service based on the following information:

Company Name: {company_name}
Website URL: {website_url}
Company Address: {company_address}
Service Description: {service_description}
User Responsibilities: {user_responsibilities}
Prohibited Activities: {prohibited_activities}
Payment Terms: {payment_terms}
Cancellation Policy: {cancellation_policy}
Limitation of Liability: {limitation_of_liability}
Governing Law: {governing_law}
Contact Email: {contact_email}

Generate comprehensive Terms of Service that include:

1. Acceptance of Terms
2. Description of Service
3. User Accounts and Registration
4. User Responsibilities and Conduct
5. Prohibited Uses
6. Payment Terms and Billing
7. Cancellation and Refunds
8. Intellectual Property Rights
9. Privacy and Data Protection
10. Limitation of Liability
11. Indemnification
12. Termination
13. Governing Law and Disputes
14. Changes to Terms
15. Contact Information

Use clear, legally sound language appropriate for online services."""

terms_of_service_prompt = PromptTemplate.from_template(terms_of_service_template)
terms_of_service_chain = terms_of_service_prompt | model | StrOutputParser()

async def generate_terms_of_service(data: dict):
    """Generate Terms of Service document using GPT-4o and save as .docx with logo"""
    try:
        user_responsibilities_list = ", ".join(data.get("user_responsibilities", []))
        prohibited_activities_list = ", ".join(data.get("prohibited_activities", []))
        
        document_content = ""
        async for chunk in terms_of_service_chain.astream({
            "company_name": data.get("company_name"),
            "website_url": data.get("website_url"),
            "company_address": data.get("company_address"),
            "service_description": data.get("service_description"),
            "user_responsibilities": user_responsibilities_list,
            "prohibited_activities": prohibited_activities_list,
            "payment_terms": data.get("payment_terms"),
            "cancellation_policy": data.get("cancellation_policy"),
            "limitation_of_liability": data.get("limitation_of_liability"),
            "governing_law": data.get("governing_law"),
            "contact_email": data.get("contact_email")
        }):
            document_content += chunk
        
        # Save the document as .docx to GCS with logo
        logo_url = data.get("logo_url")
        document_url = await save_docx_to_gcs(
            document_content, 
            "Terms of Service", 
            data.get("company_name"),
            logo_url
        )
        
        return {
            "document_content": document_content.strip(),
            "document_url": document_url,
            "document_type": "Terms of Service",
            "generated_for": data.get("company_name"),
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split()),
            "format": "DOCX with logo"
        }
    except Exception as e:
        print(f"Error in Terms of Service generation: {e}")
        raise e
