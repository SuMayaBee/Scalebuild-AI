# Document Generation API Examples with Logos
# All documents now include logos on every page and are saved as .docx files in GCS

# 1. NDA (Non-Disclosure Agreement) with Logo
curl -X POST "http://localhost:8000/documents/nda" \
  -H "Content-Type: application/json" \
  -d '{
    "disclosing_party": "ScaleBuild AI Inc.",
    "receiving_party": "John Doe",
    "purpose": "discussing potential collaboration on AI-powered document generation solutions",
    "confidential_info_description": "proprietary AI algorithms, customer data, business strategies, and technical specifications",
    "duration": "2 years",
    "governing_law": "California",
    "effective_date": "January 8, 2025",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
  }'

# 2. Business Proposal with Logo
curl -X POST "http://localhost:8000/documents/business-proposal" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# 3. Service Contract with Logo
curl -X POST "http://localhost:8000/documents/contract" \
  -H "Content-Type: application/json" \
  -d '{
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
    "effective_date": "January 8, 2025",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
  }'

# 4. Partnership Agreement with Logo
curl -X POST "http://localhost:8000/documents/partnership-agreement" \
  -H "Content-Type: application/json" \
  -d '{
    "party1_name": "ScaleBuild AI Inc.",
    "party1_address": "123 AI Street, San Francisco, CA 94105",
    "party2_name": "Innovation Labs LLC",
    "party2_address": "789 Innovation Drive, Austin, TX 78701",
    "partnership_purpose": "Joint development of AI-powered business solutions",
    "partnership_duration": "3 years",
    "profit_sharing_ratio": "60/40",
    "responsibilities_party1": [
      "Provide AI technology and expertise",
      "Handle technical development",
      "Manage intellectual property"
    ],
    "responsibilities_party2": [
      "Provide market access and sales channels",
      "Handle customer relationships",
      "Manage business operations"
    ],
    "effective_date": "January 8, 2025",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
  }'

# 5. Terms of Service with Logo
curl -X POST "http://localhost:8000/documents/terms-of-service" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ScaleBuild AI",
    "website_url": "https://scalebuild.ai",
    "company_address": "123 AI Street, San Francisco, CA 94105",
    "service_description": "AI-powered document generation and automation platform",
    "user_responsibilities": [
      "Provide accurate information",
      "Use services responsibly",
      "Maintain account security",
      "Comply with usage policies"
    ],
    "prohibited_activities": [
      "Unauthorized access attempts",
      "Malicious use of AI services",
      "Violation of intellectual property rights",
      "Spam or harassment"
    ],
    "payment_terms": "Monthly subscription with 30-day billing cycle",
    "cancellation_policy": "Cancel anytime with 30 days notice",
    "limitation_of_liability": "Limited to subscription fees paid in last 12 months",
    "governing_law": "California",
    "contact_email": "legal@scalebuild.ai",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
  }'

# 6. Privacy Policy with Logo
curl -X POST "http://localhost:8000/documents/privacy-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ScaleBuild AI",
    "website_url": "https://scalebuild.ai",
    "company_address": "123 AI Street, San Francisco, CA 94105",
    "data_collected": [
      "Personal information (name, email)",
      "Usage data and analytics",
      "Document content for processing",
      "Technical information (IP, browser)"
    ],
    "data_usage_purpose": [
      "Provide AI document generation services",
      "Improve service quality",
      "Customer support",
      "Security and fraud prevention"
    ],
    "third_party_sharing": "Limited to service providers under strict confidentiality agreements",
    "data_retention_period": "As long as account is active, plus 90 days",
    "user_rights": [
      "Access your data",
      "Correct inaccurate information",
      "Delete your account",
      "Data portability"
    ],
    "cookies_usage": "Essential cookies for service functionality and optional analytics cookies",
    "contact_email": "privacy@scalebuild.ai",
    "governing_law": "California",
    "effective_date": "January 8, 2025",
    "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
  }'

# Expected Response Format for All Documents:
# {
#   "document_content": "Full document text content...",
#   "document_url": "https://storage.googleapis.com/your-bucket/document.docx",
#   "document_type": "Document Type Name",
#   "generated_for": "Client/Party Name",
#   "creation_date": "2025-01-08 12:00:00",
#   "word_count": 1500,
#   "format": "DOCX with logo"
# }

# Notes:
# - All documents now include the logo on every page
# - Logo URL is required in the request body
# - Documents are saved as .docx files in Google Cloud Storage
# - The logo is automatically resized and positioned in the header
# - If logo fails to load, a text header "ScaleBuild AI" is used instead
