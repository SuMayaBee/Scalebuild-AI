from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_document_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- NDA Template ---
nda_template = """You are a legal document specialist. Create a comprehensive Non-Disclosure Agreement (NDA) with the following EXACT structure and formatting:

**IMPORTANT FORMATTING REQUIREMENTS:**
- Include HTML structure with proper styling
- Add a small logo placeholder on the left side of each page header
- Use professional formatting with proper spacing and typography
- Include page numbers at the bottom
- Maintain consistent styling throughout

Generate the NDA with this EXACT structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Non-Disclosure Agreement</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        
        .header {{
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 15px;
        }}
        
        .logo {{
            width: 60px;
            height: 60px;
            margin-right: 20px;
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMjgiIHN0cm9rZT0iIzMzNzNkYyIgc3Ryb2tlLXdpZHRoPSI0Ii8+Cjx0ZXh0IHg9IjMwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0iIzMzNzNkYyIgdGV4dC1hbmNob3I9Im1pZGRsZSI+U0E8L3RleHQ+Cjwvc3ZnPgo=') no-repeat center;
            background-size: contain;
        }}
        
        .title-section {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .subtitle {{
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .parties {{
            margin-bottom: 30px;
        }}
        
        .party {{
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .section {{
            margin-bottom: 25px;
        }}
        
        .section-title {{
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .section-content {{
            margin-left: 20px;
            text-align: justify;
        }}
        
        .list-item {{
            margin-bottom: 8px;
            text-align: justify;
        }}
        
        .footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 15px;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        @media print {{
            .header {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: white;
                z-index: 1000;
            }}
            
            body {{
                margin-top: 100px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo"></div>
        <div>
            <strong>ScaleBuild AI</strong><br>
            <small>Legal Document Management System</small>
        </div>
    </div>

    <div class="title-section">
        <div class="title">NON-DISCLOSURE AGREEMENT (NDA)</div>
        <div class="subtitle">This Agreement is made and entered into on this {effective_date}, by and between:</div>
    </div>

    <div class="parties">
        <div class="party">
            <strong>{disclosing_party}</strong><br>
            (hereinafter referred to as the "Disclosing Party" or "Company")
        </div>
        
        <div style="text-align: center; margin: 15px 0;"><strong>AND</strong></div>
        
        <div class="party">
            <strong>{receiving_party}</strong><br>
            (hereinafter referred to as the "Receiving Party" or "Employee")
        </div>
    </div>

    <div class="section">
        <div class="section-title">1. Purpose</div>
        <div class="section-content">
            This Agreement is entered into for the purpose of {purpose}. The Disclosing Party may disclose confidential and proprietary information to the Receiving Party in connection with this purpose.
        </div>
    </div>

    <div class="section">
        <div class="section-title">2. Definition of Confidential Information</div>
        <div class="section-content">
            For purposes of this Agreement, "Confidential Information" shall include, but is not limited to:
            <div style="margin-top: 10px;">
                <div class="list-item">• {confidential_info_description}</div>
                <div class="list-item">• Technical data, trade secrets, know-how, research, product plans, products, services, customers, customer lists, markets, software, developments, inventions, processes, formulas, technology, designs, drawings, engineering, hardware configuration information, marketing, finances, or other business information.</div>
                <div class="list-item">• All material and non-public information shared by the Disclosing Party in the course of business discussions and evaluations.</div>
                <div class="list-item">• Any data or insights obtained through observation or interaction with the Disclosing Party's internal systems.</div>
            </div>
            <div style="margin-top: 15px;">
                Confidential Information may be in oral, written, digital, visual, or any other form, and shall remain protected regardless of the format or mode of delivery.
            </div>
        </div>
    </div>

    <div class="page-break"></div>
    
    <div class="header">
        <div class="logo"></div>
        <div>
            <strong>ScaleBuild AI</strong><br>
            <small>Page 2</small>
        </div>
    </div>

    <div class="section">
        <div class="section-title">3. Obligations of the Receiving Party</div>
        <div class="section-content">
            The Receiving Party agrees that:
            <div style="margin-top: 10px;">
                <div class="list-item">• She shall hold all Confidential Information in the strictest confidence and shall not disclose, share, or discuss it with <strong>anyone</strong>, including but not limited to <strong>employees, contractors, or management</strong>, without express prior written consent from the Disclosing Party.</div>
                <div class="list-item">• She shall use the Confidential Information <strong>solely for the purpose of performing assigned work</strong> in connection with the Disclosing Party's projects.</div>
                <div class="list-item">• She shall take all reasonable steps to protect the confidentiality of such information and prevent unauthorized use or disclosure.</div>
                <div class="list-item">• She shall immediately report any known or suspected breach of this Agreement to the Disclosing Party.</div>
            </div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">4. Exclusions</div>
        <div class="section-content">
            Confidential Information does not include information that:
            <div style="margin-top: 10px;">
                <div class="list-item">• Is publicly known through no fault or breach of the Receiving Party;</div>
                <div class="list-item">• Is lawfully obtained by the Receiving Party from a third party without obligation of confidentiality;</div>
                <div class="list-item">• Is independently developed without use of or reference to the Disclosing Party's Confidential Information.</div>
            </div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">5. Term</div>
        <div class="section-content">
            This Agreement shall remain in effect for a period of <strong>{duration}</strong> and shall continue to bind the Receiving Party following the termination of that engagement.
        </div>
    </div>

    <div class="section">
        <div class="section-title">6. Return or Destruction of Information</div>
        <div class="section-content">
            Upon completion of work or upon request by the Disclosing Party, the Receiving Party agrees to promptly return or destroy all materials containing Confidential Information, including digital copies.
        </div>
    </div>

    <div class="section">
        <div class="section-title">7. Remedies</div>
        <div class="section-content">
            The Receiving Party acknowledges that any breach of this Agreement may cause irreparable harm to the Disclosing Party, for which monetary damages may be inadequate. Therefore, the Disclosing Party shall be entitled to seek equitable relief, including injunction and specific performance, in addition to all other remedies available at law or in equity.
        </div>
    </div>

    <div class="section">
        <div class="section-title">8. Governing Law</div>
        <div class="section-content">
            This Agreement shall be governed by and construed in accordance with the laws of {governing_law}, without regard to its conflict of laws principles.
        </div>
    </div>

    <div class="section">
        <div class="section-title">9. Signatures</div>
        <div class="section-content">
            By signing below, both parties acknowledge that they have read, understood, and agree to be bound by the terms and conditions of this Agreement.
            
            <div style="margin-top: 40px;">
                <div style="display: flex; justify-content: space-between;">
                    <div style="width: 45%;">
                        <div style="border-bottom: 1px solid #333; margin-bottom: 5px; height: 30px;"></div>
                        <strong>Disclosing Party:</strong> {disclosing_party}<br>
                        <strong>Date:</strong> ________________
                    </div>
                    <div style="width: 45%;">
                        <div style="border-bottom: 1px solid #333; margin-bottom: 5px; height: 30px;"></div>
                        <strong>Receiving Party:</strong> {receiving_party}<br>
                        <strong>Date:</strong> ________________
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        ScaleBuild AI Confidential - Page 2 of 2
    </div>
</body>
</html>
```

Fill in the following information:
- Disclosing Party: {disclosing_party}
- Receiving Party: {receiving_party}
- Purpose: {purpose}
- Confidential Information Description: {confidential_info_description}
- Duration: {duration}
- Governing Law: {governing_law}
- Effective Date: {effective_date}

Generate the complete HTML document with all the styling and proper formatting as shown above."""

nda_prompt = PromptTemplate.from_template(nda_template)
nda_chain = nda_prompt | model | StrOutputParser()

async def generate_nda(data: dict):
    """Generate an NDA document using GPT-4o with professional HTML formatting"""
    try:
        document_content = ""
        async for chunk in nda_chain.astream({
            "disclosing_party": data.get("disclosing_party"),
            "receiving_party": data.get("receiving_party"),
            "purpose": data.get("purpose"),
            "confidential_info_description": data.get("confidential_info_description"),
            "duration": data.get("duration"),
            "governing_law": data.get("governing_law"),
            "effective_date": data.get("effective_date")
        }):
            document_content += chunk
        
        # Save the HTML document to GCS
        filename = f"nda_{data.get('disclosing_party', 'company').lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        document_url = await save_document_to_gcs(document_content, filename, "text/html")
        
        return {
            "document_content": document_content.strip(),
            "document_url": document_url,
            "document_type": "Non-Disclosure Agreement",
            "generated_for": f"{data.get('disclosing_party')} & {data.get('receiving_party')}",
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split()),
            "format": "HTML with embedded CSS and logo"
        }
    except Exception as e:
        print(f"Error in NDA generation: {e}")
        raise e
