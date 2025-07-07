from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_document_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- Contract Template ---
contract_template = """You are a legal document specialist. Create a comprehensive Contract based on the following information:

Contract Type: {contract_type}
Party 1 Name: {party1_name}
Party 1 Address: {party1_address}
Party 2 Name: {party2_name}
Party 2 Address: {party2_address}
Service Description: {service_description}
Contract Value: {contract_value}
Payment Terms: {payment_terms}
Duration: {duration}
Deliverables: {deliverables}
Terms & Conditions: {terms_conditions}
Effective Date: {effective_date}

Generate a formal Contract that includes:

1. Contract Overview and Scope
2. Parties Involved
3. Services/Deliverables
4. Payment Terms and Schedule
5. Timeline and Milestones
6. Terms and Conditions
7. Termination Clauses
8. Intellectual Property Rights
9. Liability and Indemnification
10. Dispute Resolution
11. Governing Law
12. Signatures

Use proper legal language and ensure the contract is comprehensive and enforceable."""

contract_prompt = PromptTemplate.from_template(contract_template)
contract_chain = contract_prompt | model | StrOutputParser()

async def generate_contract(data: dict):
    """Generate a contract document using GPT-4o"""
    try:
        deliverables_list = ", ".join(data.get("deliverables", []))
        terms_list = ", ".join(data.get("terms_conditions", []))
        
        document_content = ""
        async for chunk in contract_chain.astream({
            "contract_type": data.get("contract_type"),
            "party1_name": data.get("party1_name"),
            "party1_address": data.get("party1_address"),
            "party2_name": data.get("party2_name"),
            "party2_address": data.get("party2_address"),
            "service_description": data.get("service_description"),
            "contract_value": data.get("contract_value"),
            "payment_terms": data.get("payment_terms"),
            "duration": data.get("duration"),
            "deliverables": deliverables_list,
            "terms_conditions": terms_list,
            "effective_date": data.get("effective_date")
        }):
            document_content += chunk
        
        return {
            "document_content": document_content.strip(),
            "document_type": f"{data.get('contract_type', 'Service')} Contract",
            "generated_for": f"{data.get('party1_name')} & {data.get('party2_name')}",
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split())
        }
    except Exception as e:
        print(f"Error in contract generation: {e}")
        raise e
