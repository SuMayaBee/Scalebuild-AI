# Document Generation API - Request & Response Examples

## 1. NDA (Non-Disclosure Agreement)

### Request Body
```json
{
  "disclosing_party": "ScaleBuild AI Inc.",
  "receiving_party": "John Doe",
  "purpose": "discussing potential collaboration on AI-powered document generation solutions and exploring business partnership opportunities",
  "confidential_info_description": "proprietary AI algorithms, customer data, business strategies, technical specifications, source code, and trade secrets",
  "duration": "2 years",
  "governing_law": "California",
  "effective_date": "January 8, 2025",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "NON-DISCLOSURE AGREEMENT (NDA)\n\nThis Agreement is made and entered into on this January 8, 2025, by and between:\n\nScaleBuild AI Inc.\n(hereinafter referred to as the \"Disclosing Party\" or \"Company\")\n\nAND\n\nJohn Doe\n(hereinafter referred to as the \"Receiving Party\" or \"Employee\")\n\n1. Purpose\n\nThis Agreement is entered into for the purpose of discussing potential collaboration on AI-powered document generation solutions and exploring business partnership opportunities...",
  "document_url": "https://storage.googleapis.com/deck123/Non-Disclosure_Agreement_ScaleBuild_AI_Inc._&_John_Doe.docx",
  "document_type": "Non-Disclosure Agreement",
  "generated_for": "ScaleBuild AI Inc. & John Doe",
  "creation_date": "2025-07-08 12:30:45",
  "word_count": 1542,
  "format": "DOCX with logo"
}
```

---

## 2. Business Proposal

### Request Body
```json
{
  "company_name": "ScaleBuild AI",
  "client_name": "TechCorp Solutions",
  "project_title": "AI-Powered Document Automation Platform",
  "project_description": "Develop an intelligent document generation and management system using advanced AI technologies including GPT-4, natural language processing, and automated workflow integration",
  "services_offered": [
    "AI Model Development and Fine-tuning",
    "Custom Document Template Design",
    "System Integration and API Development",
    "User Training and Ongoing Support",
    "Performance Monitoring and Optimization"
  ],
  "timeline": "6 months (January 2025 - June 2025)",
  "budget_range": "$100,000 - $150,000",
  "contact_person": "Jane Smith",
  "contact_email": "jane.smith@scalebuild.ai",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "BUSINESS PROPOSAL\n\nAI-POWERED DOCUMENT AUTOMATION PLATFORM\n\nPrepared for: TechCorp Solutions\nPrepared by: ScaleBuild AI\nDate: January 8, 2025\n\n1. EXECUTIVE SUMMARY\n\nScaleBuild AI is pleased to present this comprehensive proposal for developing an AI-Powered Document Automation Platform for TechCorp Solutions...",
  "document_url": "https://storage.googleapis.com/deck123/Business_Proposal_TechCorp_Solutions.docx",
  "document_type": "Business Proposal",
  "generated_for": "TechCorp Solutions",
  "creation_date": "2025-07-08 12:31:12",
  "word_count": 2156,
  "format": "DOCX with logo"
}
```

---

## 3. Service Contract

### Request Body
```json
{
  "contract_type": "Service Agreement",
  "party1_name": "ScaleBuild AI Inc.",
  "party1_address": "123 AI Street, San Francisco, CA 94105, United States",
  "party2_name": "Digital Solutions LLC",
  "party2_address": "456 Tech Avenue, New York, NY 10001, United States",
  "service_description": "AI-powered document generation and automation services including custom model development, template creation, system integration, and ongoing technical support",
  "contract_value": "$75,000 USD",
  "payment_terms": "50% ($37,500) upfront upon contract signing, 50% ($37,500) upon project completion and client acceptance",
  "duration": "4 months from contract execution date",
  "deliverables": [
    "Custom AI document generation system tailored to client specifications",
    "Integration with existing client workflows and systems",
    "Comprehensive user training and documentation package",
    "3 months of technical support and maintenance",
    "Performance analytics and reporting dashboard"
  ],
  "terms_conditions": [
    "All work must be completed within the specified timeline",
    "Client must provide necessary system access and resources",
    "Intellectual property rights as specified in appendix A",
    "Confidentiality agreement applies to all parties and subcontractors",
    "Changes to scope require written approval and may affect timeline/cost"
  ],
  "effective_date": "January 15, 2025",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "SERVICE AGREEMENT\n\nThis Service Agreement (\"Agreement\") is entered into on January 15, 2025, between:\n\nSCALEBUILD AI INC.\n123 AI Street, San Francisco, CA 94105, United States\n(\"Service Provider\")\n\nAND\n\nDIGITAL SOLUTIONS LLC\n456 Tech Avenue, New York, NY 10001, United States\n(\"Client\")\n\n1. CONTRACT OVERVIEW AND SCOPE...",
  "document_url": "https://storage.googleapis.com/deck123/Service_Agreement_ScaleBuild_AI_Inc._&_Digital_Solutions_LLC.docx",
  "document_type": "Service Agreement Contract",
  "generated_for": "ScaleBuild AI Inc. & Digital Solutions LLC",
  "creation_date": "2025-07-08 12:31:45",
  "word_count": 2834,
  "format": "DOCX with logo"
}
```

---

## 4. Partnership Agreement

### Request Body
```json
{
  "party1_name": "ScaleBuild AI Inc.",
  "party1_address": "123 AI Street, San Francisco, CA 94105, United States",
  "party2_name": "Innovation Labs LLC",
  "party2_address": "789 Innovation Drive, Austin, TX 78701, United States",
  "partnership_purpose": "Joint development and commercialization of AI-powered business solutions for enterprise document management and automation",
  "partnership_duration": "3 years with automatic renewal option",
  "profit_sharing_ratio": "60% ScaleBuild AI, 40% Innovation Labs",
  "responsibilities_party1": [
    "Provide AI technology platform and expertise",
    "Handle all technical development and maintenance",
    "Manage intellectual property and patent applications",
    "Provide technical support and training resources"
  ],
  "responsibilities_party2": [
    "Provide market access and established sales channels",
    "Handle customer acquisition and relationship management",
    "Manage business operations and administrative functions",
    "Provide marketing and promotional support"
  ],
  "effective_date": "February 1, 2025",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "PARTNERSHIP AGREEMENT\n\nThis Partnership Agreement (\"Agreement\") is entered into on February 1, 2025, between:\n\nSCALEBUILD AI INC.\n123 AI Street, San Francisco, CA 94105, United States\n(\"Party 1\")\n\nAND\n\nINNOVATION LABS LLC\n789 Innovation Drive, Austin, TX 78701, United States\n(\"Party 2\")\n\n1. PARTNERSHIP FORMATION...",
  "document_url": "https://storage.googleapis.com/deck123/Partnership_Agreement_ScaleBuild_AI_Inc._&_Innovation_Labs_LLC.docx",
  "document_type": "Partnership Agreement",
  "generated_for": "ScaleBuild AI Inc. & Innovation Labs LLC",
  "creation_date": "2025-07-08 12:32:18",
  "word_count": 2567,
  "format": "DOCX with logo"
}
```

---

## 5. Terms of Service

### Request Body
```json
{
  "company_name": "ScaleBuild AI",
  "website_url": "https://scalebuild.ai",
  "company_address": "123 AI Street, San Francisco, CA 94105, United States",
  "service_description": "AI-powered document generation and automation platform that enables businesses to create professional documents using advanced artificial intelligence and natural language processing technologies",
  "user_responsibilities": [
    "Provide accurate and truthful information when using our services",
    "Use our services responsibly and in compliance with applicable laws",
    "Maintain the security and confidentiality of your account credentials",
    "Comply with our usage policies and community guidelines",
    "Report any suspected security breaches or unauthorized access immediately"
  ],
  "prohibited_activities": [
    "Attempting unauthorized access to our systems or other users' accounts",
    "Using our AI services for malicious, illegal, or harmful purposes",
    "Violating intellectual property rights of ScaleBuild AI or third parties",
    "Sending spam, harassment, or inappropriate content through our platform",
    "Reverse engineering, copying, or redistributing our proprietary technology"
  ],
  "payment_terms": "Monthly subscription billing with 30-day payment cycle. Annual plans available with discount.",
  "cancellation_policy": "Users may cancel their subscription at any time with 30 days written notice. No refunds for partial months.",
  "limitation_of_liability": "ScaleBuild AI's total liability is limited to the subscription fees paid by the user in the 12 months preceding the claim",
  "governing_law": "California, United States",
  "contact_email": "legal@scalebuild.ai",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "TERMS OF SERVICE\n\nScaleBuild AI Platform\n\nEffective Date: January 8, 2025\nLast Updated: January 8, 2025\n\n1. ACCEPTANCE OF TERMS\n\nWelcome to ScaleBuild AI. These Terms of Service (\"Terms\") govern your use of the ScaleBuild AI platform, website, and services located at https://scalebuild.ai...",
  "document_url": "https://storage.googleapis.com/deck123/Terms_of_Service_ScaleBuild_AI.docx",
  "document_type": "Terms of Service",
  "generated_for": "ScaleBuild AI",
  "creation_date": "2025-07-08 12:32:52",
  "word_count": 3124,
  "format": "DOCX with logo"
}
```

---

## 6. Privacy Policy

### Request Body
```json
{
  "company_name": "ScaleBuild AI",
  "website_url": "https://scalebuild.ai",
  "company_address": "123 AI Street, San Francisco, CA 94105, United States",
  "data_collected": [
    "Personal information (name, email address, phone number)",
    "Account and profile information",
    "Usage data and platform analytics",
    "Document content submitted for AI processing",
    "Technical information (IP address, browser type, device information)",
    "Payment and billing information"
  ],
  "data_usage_purpose": [
    "Provide AI document generation and automation services",
    "Improve and optimize our AI models and platform performance",
    "Provide customer support and technical assistance",
    "Process payments and manage billing",
    "Ensure platform security and prevent fraud",
    "Send important service updates and communications"
  ],
  "third_party_sharing": "We do not sell personal data. Limited sharing with trusted service providers under strict confidentiality agreements for essential business operations only.",
  "data_retention_period": "Personal data retained as long as your account is active, plus 90 days after account closure for legal and business purposes",
  "user_rights": [
    "Access and review your personal data",
    "Correct or update inaccurate information",
    "Request deletion of your account and associated data",
    "Data portability - export your data in standard formats",
    "Object to certain data processing activities",
    "Lodge complaints with relevant data protection authorities"
  ],
  "cookies_usage": "We use essential cookies for platform functionality and optional analytics cookies to improve user experience. You can manage cookie preferences in your account settings.",
  "contact_email": "privacy@scalebuild.ai",
  "governing_law": "California, United States",
  "effective_date": "January 8, 2025",
  "logo_url": "https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png"
}
```

### Response Body
```json
{
  "document_content": "PRIVACY POLICY\n\nScaleBuild AI Platform\n\nEffective Date: January 8, 2025\nLast Updated: January 8, 2025\n\n1. INTRODUCTION\n\nScaleBuild AI (\"we,\" \"our,\" or \"us\") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI-powered document generation platform...",
  "document_url": "https://storage.googleapis.com/deck123/Privacy_Policy_ScaleBuild_AI.docx",
  "document_type": "Privacy Policy",
  "generated_for": "ScaleBuild AI",
  "creation_date": "2025-07-08 12:33:25",
  "word_count": 2891,
  "format": "DOCX with logo"
}
```

---

## Common Response Fields Explained

| Field | Description |
|-------|-------------|
| `document_content` | Full text content of the generated document |
| `document_url` | Direct download URL to the .docx file in Google Cloud Storage |
| `document_type` | Type of document generated (e.g., "Non-Disclosure Agreement") |
| `generated_for` | Primary parties or entities the document was created for |
| `creation_date` | Timestamp when the document was generated |
| `word_count` | Total number of words in the document |
| `format` | Document format and features (always "DOCX with logo") |

## Key Features

✅ **Logo Integration**: All documents include the specified logo on every page header  
✅ **Professional Format**: Documents use proper legal/business formatting  
✅ **Cloud Storage**: All files saved to Google Cloud Storage with public URLs  
✅ **Flexible Logo**: Use the default logo or provide your own URL  
✅ **Error Resilience**: Graceful fallback if logo URL fails  
✅ **Multiple Types**: Support for 6 different document types  

## Default Logo URL
```
https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png
```

## API Endpoints
- `POST /documents/nda`
- `POST /documents/business-proposal`
- `POST /documents/contract`
- `POST /documents/partnership-agreement`
- `POST /documents/terms-of-service`
- `POST /documents/privacy-policy`
