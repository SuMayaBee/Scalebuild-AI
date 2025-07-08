#!/usr/bin/env python3
"""
Quick test script to verify HTML processing fix
"""

import asyncio
from services.document_utils import process_html_content
from docx import Document
import tempfile
import os

async def test_html_processing():
    """Test the fixed HTML processing function"""
    
    # Sample HTML content similar to what the NDA service generates
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
    </head>
    <body>
        <div class="header">
            <div class="title">Test Agreement</div>
            <div class="subtitle">Professional Document</div>
        </div>
        
        <div class="parties">
            <div>This is a test document between:</div>
            <div class="party">Company A</div>
            <div>AND</div>
            <div class="party">Company B</div>
        </div>
        
        <div class="section">
            <div class="section-title">1. Introduction</div>
            <div>This is a test section with some content.</div>
            <div class="subsection">
                <div class="bullet-point">First bullet point</div>
                <div class="bullet-point">Second bullet point</div>
            </div>
        </div>
        
        <div class="signature-section">
            <div class="section-title">Signatures</div>
            <div>Please sign below:</div>
        </div>
    </body>
    </html>
    """
    
    print("🔄 Testing HTML Processing Fix")
    print("=" * 50)
    
    try:
        # Create a new Word document
        doc = Document()
        
        # Process the HTML content
        print("📄 Processing HTML content...")
        await process_html_content(doc, sample_html)
        
        # Save to temporary file to verify it works
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            doc.save(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        print(f"✅ HTML processing completed successfully!")
        print(f"📄 Document saved to: {tmp_file_path}")
        print(f"📊 Document contains {len(doc.paragraphs)} paragraphs")
        
        # Clean up
        os.unlink(tmp_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during HTML processing test: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_html_processing())
    if success:
        print("\n🎉 HTML processing fix is working correctly!")
    else:
        print("\n❌ HTML processing still has issues.")
