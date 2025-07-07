from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_document_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- Business Proposal Template ---
business_proposal_template = """You are a professional business consultant specializing in creating compelling business proposals. Generate a comprehensive business proposal document based on the following information:

Company Name: {company_name}
Client Name: {client_name}
Project Title: {project_title}
Project Description: {project_description}
Services Offered: {services_offered}
Timeline: {timeline}
Budget Range: {budget_range}
Contact Person: {contact_person}
Contact Email: {contact_email}

Create a professional business proposal that includes:

1. Executive Summary
2. Company Overview
3. Project Understanding
4. Proposed Solution
5. Services & Deliverables
6. Timeline & Milestones
7. Investment & Budget
8. Why Choose Us
9. Next Steps
10. Contact Information

The proposal should be persuasive, professional, and tailored to win the client's business. Use formal business language and structure."""

business_proposal_prompt = PromptTemplate.from_template(business_proposal_template)
business_proposal_chain = business_proposal_prompt | model | StrOutputParser()

async def generate_business_proposal(data: dict):
    """Generate a business proposal document using GPT-4o"""
    try:
        services_list = ", ".join(data.get("services_offered", []))
        
        document_content = ""
        async for chunk in business_proposal_chain.astream({
            "company_name": data.get("company_name"),
            "client_name": data.get("client_name"),
            "project_title": data.get("project_title"),
            "project_description": data.get("project_description"),
            "services_offered": services_list,
            "timeline": data.get("timeline"),
            "budget_range": data.get("budget_range"),
            "contact_person": data.get("contact_person"),
            "contact_email": data.get("contact_email")
        }):
            document_content += chunk
        
        return {
            "document_content": document_content.strip(),
            "document_type": "Business Proposal",
            "generated_for": data.get("client_name"),
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split())
        }
    except Exception as e:
        print(f"Error in business proposal generation: {e}")
        raise e
