// TypeScript examples for document generation with logos
// All documents now include logos on every page and are saved as .docx files in GCS

import axios from 'axios';

// Base URL for FastAPI backend
const BASE_URL = 'http://localhost:8000';

// Default logo URL
const DEFAULT_LOGO_URL = 'https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png';

// Type definitions for document requests
interface BaseDocumentRequest {
  logo_url?: string;
}

interface NDARequest extends BaseDocumentRequest {
  disclosing_party: string;
  receiving_party: string;
  purpose: string;
  confidential_info_description: string;
  duration: string;
  governing_law: string;
  effective_date: string;
}

interface BusinessProposalRequest extends BaseDocumentRequest {
  company_name: string;
  client_name: string;
  project_title: string;
  project_description: string;
  services_offered: string[];
  timeline: string;
  budget_range: string;
  contact_person: string;
  contact_email: string;
}

interface ContractRequest extends BaseDocumentRequest {
  contract_type: string;
  party1_name: string;
  party1_address: string;
  party2_name: string;
  party2_address: string;
  service_description: string;
  contract_value: string;
  payment_terms: string;
  duration: string;
  deliverables: string[];
  terms_conditions: string[];
  effective_date: string;
}

interface DocumentResponse {
  document_content: string;
  document_url: string;
  document_type: string;
  generated_for: string;
  creation_date: string;
  word_count: number;
  format: string;
}

// NDA Generation with Logo
export const generateNDA = async (data: NDARequest): Promise<DocumentResponse> => {
  try {
    const response = await axios.post(`${BASE_URL}/documents/nda`, {
      ...data,
      logo_url: data.logo_url || DEFAULT_LOGO_URL
    });
    
    return response.data;
  } catch (error) {
    console.error('Error generating NDA:', error);
    throw error;
  }
};

// Business Proposal Generation with Logo
export const generateBusinessProposal = async (data: BusinessProposalRequest): Promise<DocumentResponse> => {
  try {
    const response = await axios.post(`${BASE_URL}/documents/business-proposal`, {
      ...data,
      logo_url: data.logo_url || DEFAULT_LOGO_URL
    });
    
    return response.data;
  } catch (error) {
    console.error('Error generating business proposal:', error);
    throw error;
  }
};

// Contract Generation with Logo
export const generateContract = async (data: ContractRequest): Promise<DocumentResponse> => {
  try {
    const response = await axios.post(`${BASE_URL}/documents/contract`, {
      ...data,
      logo_url: data.logo_url || DEFAULT_LOGO_URL
    });
    
    return response.data;
  } catch (error) {
    console.error('Error generating contract:', error);
    throw error;
  }
};

// Example usage functions
export const exampleNDAGeneration = async () => {
  const ndaData: NDARequest = {
    disclosing_party: "ScaleBuild AI Inc.",
    receiving_party: "John Doe",
    purpose: "discussing potential collaboration on AI-powered document generation solutions",
    confidential_info_description: "proprietary AI algorithms, customer data, business strategies, and technical specifications",
    duration: "2 years",
    governing_law: "California",
    effective_date: new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }),
    logo_url: DEFAULT_LOGO_URL
  };

  try {
    const result = await generateNDA(ndaData);
    console.log('NDA generated successfully:', result);
    
    // The result includes:
    // - document_content: Full text of the document
    // - document_url: Direct link to the .docx file in GCS
    // - document_type: "Non-Disclosure Agreement"
    // - generated_for: "ScaleBuild AI Inc. & John Doe"
    // - creation_date: "2025-01-08 12:00:00"
    // - word_count: Number of words in the document
    // - format: "DOCX with logo"
    
    return result;
  } catch (error) {
    console.error('Failed to generate NDA:', error);
    throw error;
  }
};

export const exampleBusinessProposalGeneration = async () => {
  const proposalData: BusinessProposalRequest = {
    company_name: "ScaleBuild AI",
    client_name: "TechCorp Solutions",
    project_title: "AI-Powered Document Automation Platform",
    project_description: "Develop an intelligent document generation and management system using advanced AI technologies",
    services_offered: [
      "AI Model Development",
      "Document Template Design",
      "System Integration",
      "Training and Support"
    ],
    timeline: "6 months",
    budget_range: "$100,000 - $150,000",
    contact_person: "Jane Smith",
    contact_email: "jane.smith@scalebuild.ai",
    logo_url: DEFAULT_LOGO_URL
  };

  try {
    const result = await generateBusinessProposal(proposalData);
    console.log('Business proposal generated successfully:', result);
    return result;
  } catch (error) {
    console.error('Failed to generate business proposal:', error);
    throw error;
  }
};

export const exampleContractGeneration = async () => {
  const contractData: ContractRequest = {
    contract_type: "Service Agreement",
    party1_name: "ScaleBuild AI Inc.",
    party1_address: "123 AI Street, San Francisco, CA 94105",
    party2_name: "Digital Solutions LLC",
    party2_address: "456 Tech Avenue, New York, NY 10001",
    service_description: "AI-powered document generation and automation services",
    contract_value: "$75,000",
    payment_terms: "50% upfront, 50% upon completion",
    duration: "4 months",
    deliverables: [
      "Custom AI document generation system",
      "Integration with existing workflows",
      "User training and documentation",
      "3 months of technical support"
    ],
    terms_conditions: [
      "All work must be completed within specified timeline",
      "Client provides necessary access and resources",
      "Intellectual property rights as specified in appendix",
      "Confidentiality agreement applies to all parties"
    ],
    effective_date: new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }),
    logo_url: DEFAULT_LOGO_URL
  };

  try {
    const result = await generateContract(contractData);
    console.log('Contract generated successfully:', result);
    return result;
  } catch (error) {
    console.error('Failed to generate contract:', error);
    throw error;
  }
};

// React component example (JSX)
// Note: This would typically be in a .tsx file with proper React imports

/*
import React, { useState } from 'react';

export const DocumentGenerationComponent: React.FC = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDocument, setGeneratedDocument] = useState<DocumentResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateNDA = async () => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const result = await exampleNDAGeneration();
      setGeneratedDocument(result);
    } catch (err) {
      setError('Failed to generate NDA. Please try again.');
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="document-generation">
      <h2>Document Generation with Logo</h2>
      
      <button 
        onClick={handleGenerateNDA}
        disabled={isGenerating}
        className="btn btn-primary"
      >
        {isGenerating ? 'Generating...' : 'Generate NDA with Logo'}
      </button>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {generatedDocument && (
        <div className="generated-document">
          <h3>Generated Document</h3>
          <p><strong>Type:</strong> {generatedDocument.document_type}</p>
          <p><strong>Generated For:</strong> {generatedDocument.generated_for}</p>
          <p><strong>Creation Date:</strong> {generatedDocument.creation_date}</p>
          <p><strong>Word Count:</strong> {generatedDocument.word_count}</p>
          <p><strong>Format:</strong> {generatedDocument.format}</p>
          
          {generatedDocument.document_url && (
            <a 
              href={generatedDocument.document_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn btn-success"
            >
              Download .docx File
            </a>
          )}
        </div>
      )}
    </div>
  );
};
*/

// Key Features:
// ✅ All documents now include logos on every page
// ✅ Documents are saved as .docx files in Google Cloud Storage
// ✅ Logo URL is configurable via request body
// ✅ Default logo provided: https://storage.googleapis.com/deck123/no_bg_logo_Brilliant_Crown.png.png
// ✅ Automatic fallback to text header if logo fails to load
// ✅ Professional document formatting with proper headers and footers
// ✅ Support for all document types: NDA, Business Proposal, Contract, Partnership Agreement, Terms of Service, Privacy Policy
