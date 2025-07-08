from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.document_generation import (
    BusinessProposalRequest,
    PartnershipAgreementRequest,
    NDARequest,
    ContractRequest,
    TermsOfServiceRequest,
    PrivacyPolicyRequest,
    DocumentResponse,
    DocumentGenerationRequest
)
from services.document_generation_service import (
    generate_business_proposal,
    generate_partnership_agreement,
    generate_nda,
    generate_contract,
    generate_terms_of_service,
    generate_privacy_policy
)
import json

router = APIRouter()

@router.post("/documents/business-proposal", response_model=DocumentResponse)
async def create_business_proposal(request: BusinessProposalRequest):
    """Generate a comprehensive business proposal document using GPT-4o"""
    try:
        result = await generate_business_proposal(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/partnership-agreement", response_model=DocumentResponse)
async def create_partnership_agreement(request: PartnershipAgreementRequest):
    """Generate a comprehensive partnership agreement document using GPT-4o"""
    try:
        result = await generate_partnership_agreement(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/nda", response_model=DocumentResponse)
async def create_nda(request: NDARequest):
    """Generate a comprehensive Non-Disclosure Agreement using GPT-4o"""
    try:
        result = await generate_nda(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/contract", response_model=DocumentResponse)
async def create_contract(request: ContractRequest):
    """Generate a comprehensive Contract using GPT-4o"""
    try:
        result = await generate_contract(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/terms-of-service", response_model=DocumentResponse)
async def create_terms_of_service(request: TermsOfServiceRequest):
    """Generate comprehensive Terms of Service using GPT-4o"""
    try:
        result = await generate_terms_of_service(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/privacy-policy", response_model=DocumentResponse)
async def create_privacy_policy(request: PrivacyPolicyRequest):
    """Generate a comprehensive Privacy Policy using GPT-4o"""
    try:
        result = await generate_privacy_policy(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentGenerationRequest):
    """Universal endpoint to generate any type of document"""
    try:
        if request.document_type == "business_proposal":
            result = await generate_business_proposal(request.document_data)
        elif request.document_type == "partnership_agreement":
            result = await generate_partnership_agreement(request.document_data)
        elif request.document_type == "nda":
            result = await generate_nda(request.document_data)
        elif request.document_type == "contract":
            result = await generate_contract(request.document_data)
        elif request.document_type == "terms_of_service":
            result = await generate_terms_of_service(request.document_data)
        elif request.document_type == "privacy_policy":
            result = await generate_privacy_policy(request.document_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid document type")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/business-proposal-stream")
async def create_business_proposal_stream(request: BusinessProposalRequest):
    """Generate a business proposal with streaming response"""
    async def stream_proposal():
        try:
            yield "data: " + json.dumps({
                "status": "generating", 
                "message": f"Creating business proposal for {request.client_name}..."
            }) + "\n\n"
            
            result = await generate_business_proposal(request.dict())
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_proposal(), media_type="text/plain")

@router.post("/documents/partnership-agreement-stream")
async def create_partnership_agreement_stream(request: PartnershipAgreementRequest):
    """Generate a partnership agreement with streaming response"""
    async def stream_agreement():
        try:
            yield "data: " + json.dumps({
                "status": "generating", 
                "message": f"Creating partnership agreement for {request.party1_name} & {request.party2_name}..."
            }) + "\n\n"
            
            result = await generate_partnership_agreement(request.dict())
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_agreement(), media_type="text/plain")

@router.post("/documents/nda-stream")
async def create_nda_stream(request: NDARequest):
    """Generate an NDA with streaming response"""
    async def stream_nda():
        try:
            yield "data: " + json.dumps({
                "status": "generating", 
                "message": f"Creating NDA for {request.disclosing_party} & {request.receiving_party}..."
            }) + "\n\n"
            
            result = await generate_nda(request.dict())
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_nda(), media_type="text/plain")

@router.get("/documents/types")
async def get_document_types():
    """Get all available document types"""
    return {
        "document_types": [
            {
                "type": "business_proposal",
                "name": "Business Proposal",
                "description": "Comprehensive business proposals for client projects"
            },
            {
                "type": "partnership_agreement",
                "name": "Partnership Agreement",
                "description": "Legal partnership agreements between two parties"
            },
            {
                "type": "nda",
                "name": "Non-Disclosure Agreement",
                "description": "Confidentiality agreements to protect sensitive information"
            },
            {
                "type": "contract",
                "name": "Contract",
                "description": "Various types of contracts (service, employment, vendor)"
            },
            {
                "type": "terms_of_service",
                "name": "Terms of Service",
                "description": "Legal terms governing the use of websites and services"
            },
            {
                "type": "privacy_policy",
                "name": "Privacy Policy",
                "description": "Legal documents outlining data collection and privacy practices"
            }
        ]
    }
