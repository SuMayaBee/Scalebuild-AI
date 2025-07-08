from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_docx_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- NDA HTML Template ---
nda_html_template = """You are a legal document specialist. Create a comprehensive Non-Disclosure Agreement (NDA) as professional HTML with proper styling for conversion to .docx format.

Generate a complete HTML document with the following structure and styling:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Non-Disclosure Agreement</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background-color: #fff;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .subtitle {{
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }}
        .parties {{
            background-color: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }}
        .party {{
            margin: 10px 0;
            font-weight: bold;
        }}
        .section {{
            margin: 25px 0;
            page-break-inside: avoid;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 15px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        .subsection {{
            margin: 15px 0;
        }}
        .bullet-point {{
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }}
        .bullet-point::before {{
            content: "•";
            color: #007bff;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        .signature-section {{
            margin-top: 50px;
            border-top: 1px solid #ddd;
            padding-top: 30px;
        }}
        .signature-block {{
            display: inline-block;
            width: 45%;
            margin: 20px 0;
            vertical-align: top;
        }}
        .signature-line {{
            border-bottom: 1px solid #333;
            width: 200px;
            margin: 10px 0;
            height: 20px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">Non-Disclosure Agreement</div>
        <div class="subtitle">Confidential Information Protection Agreement</div>
    </div>

    <div class="parties">
        <div>This Agreement is made and entered into on <strong>{effective_date}</strong>, by and between:</div>
        <div class="party">{disclosing_party}</div>
        <div>(hereinafter referred to as the "Disclosing Party" or "Company")</div>
        <div style="margin: 20px 0; text-align: center; font-weight: bold;">AND</div>
        <div class="party">{receiving_party}</div>
        <div>(hereinafter referred to as the "Receiving Party" or "Employee")</div>
    </div>

    <div class="section">
        <div class="section-title">1. Purpose</div>
        <div>This Agreement is entered into for the purpose of <strong>{purpose}</strong>. The Disclosing Party may disclose confidential and proprietary information to the Receiving Party in connection with this purpose.</div>
    </div>

    <div class="section">
        <div class="section-title">2. Definition of Confidential Information</div>
        <div>For purposes of this Agreement, "Confidential Information" shall include, but is not limited to:</div>
        <div class="subsection">
            <div class="bullet-point"><strong>{confidential_info_description}</strong></div>
            <div class="bullet-point">Technical data, trade secrets, know-how, research, product plans, products, services, customers, customer lists, markets, software, developments, inventions, processes, formulas, technology, designs, drawings, engineering, hardware configuration information, marketing, finances, or other business information.</div>
            <div class="bullet-point">All material and non-public information shared by the Disclosing Party in the course of business discussions and evaluations.</div>
            <div class="bullet-point">Any data or insights obtained through observation or interaction with the Disclosing Party's internal systems.</div>
        </div>
        <div>Confidential Information may be in oral, written, digital, visual, or any other form, and shall remain protected regardless of the format or mode of delivery.</div>
    </div>

    <div class="section">
        <div class="section-title">3. Obligations of the Receiving Party</div>
        <div>The Receiving Party agrees that:</div>
        <div class="subsection">
            <div class="bullet-point">She shall hold all Confidential Information in the strictest confidence and shall not disclose, share, or discuss it with anyone, including but not limited to employees, contractors, or management, without express prior written consent from the Disclosing Party.</div>
            <div class="bullet-point">She shall use the Confidential Information solely for the purpose of performing assigned work in connection with the Disclosing Party's projects.</div>
            <div class="bullet-point">She shall take all reasonable steps to protect the confidentiality of such information and prevent unauthorized use or disclosure.</div>
            <div class="bullet-point">She shall immediately report any known or suspected breach of this Agreement to the Disclosing Party.</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">4. Exclusions</div>
        <div>Confidential Information does not include information that:</div>
        <div class="subsection">
            <div class="bullet-point">Is publicly known through no fault or breach of the Receiving Party;</div>
            <div class="bullet-point">Is lawfully obtained by the Receiving Party from a third party without obligation of confidentiality;</div>
            <div class="bullet-point">Is independently developed without use of or reference to the Disclosing Party's Confidential Information.</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">5. Term</div>
        <div>This Agreement shall remain in effect for a period of <strong>{duration}</strong> and shall continue to bind the Receiving Party following the termination of that engagement.</div>
    </div>

    <div class="section">
        <div class="section-title">6. Return or Destruction of Information</div>
        <div>Upon completion of work or upon request by the Disclosing Party, the Receiving Party agrees to promptly return or destroy all materials containing Confidential Information, including digital copies.</div>
    </div>

    <div class="section">
        <div class="section-title">7. Remedies</div>
        <div>The Receiving Party acknowledges that any breach of this Agreement may cause irreparable harm to the Disclosing Party, for which monetary damages may be inadequate. Therefore, the Disclosing Party shall be entitled to seek equitable relief, including injunction and specific performance, in addition to all other remedies available at law or in equity.</div>
    </div>

    <div class="section">
        <div class="section-title">8. Governing Law</div>
        <div>This Agreement shall be governed by and construed in accordance with the laws of <strong>{governing_law}</strong>, without regard to its conflict of laws principles.</div>
    </div>

    <div class="signature-section">
        <div class="section-title">9. Signatures</div>
        <div style="margin-bottom: 20px;">By signing below, both parties acknowledge that they have read, understood, and agree to be bound by the terms and conditions of this Agreement.</div>
        
        <div class="signature-block">
            <div><strong>Disclosing Party:</strong> {disclosing_party}</div>
            <div class="signature-line"></div>
            <div>Date: ________________</div>
        </div>
        
        <div class="signature-block" style="margin-left: 5%;">
            <div><strong>Receiving Party:</strong> {receiving_party}</div>
            <div class="signature-line"></div>
            <div>Date: ________________</div>
        </div>
    </div>

    <div class="footer">
        <div>This document was generated on {effective_date}</div>
        <div>Non-Disclosure Agreement - Confidential</div>
    </div>
</body>
</html>

Generate the complete HTML document with all the content filled in properly and professional styling."""

nda_prompt = PromptTemplate.from_template(nda_html_template)
nda_chain = nda_prompt | model | StrOutputParser()

async def generate_nda(data: dict):
    """Generate an NDA document using GPT-4o, first as HTML then convert to .docx with logo"""
    try:
        # Generate HTML content first
        html_content = ""
        async for chunk in nda_chain.astream({
            "disclosing_party": data.get("disclosing_party"),
            "receiving_party": data.get("receiving_party"),
            "purpose": data.get("purpose"),
            "confidential_info_description": data.get("confidential_info_description"),
            "duration": data.get("duration"),
            "governing_law": data.get("governing_law"),
            "effective_date": data.get("effective_date")
        }):
            html_content += chunk
        
        # Save the HTML document as .docx to GCS with logo
        logo_url = data.get("logo_url")
        document_url = await save_docx_to_gcs(
            html_content, 
            "Non-Disclosure Agreement", 
            f"{data.get('disclosing_party')} & {data.get('receiving_party')}",
            logo_url,
            content_type="html"  # Indicate this is HTML content
        )
        
        return {
            "document_content": html_content.strip(),
            "document_url": document_url,
            "document_type": "Non-Disclosure Agreement",
            "generated_for": f"{data.get('disclosing_party')} & {data.get('receiving_party')}",
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(html_content.split()),
            "format": "DOCX with logo (HTML-based)"
        }
    except Exception as e:
        print(f"Error in NDA generation: {e}")
        raise e
