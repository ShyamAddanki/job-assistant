import streamlit as st
from fpdf import FPDF
import os
import zipfile
from PyPDF2 import PdfReader
import re
import os
import requests
# Define Helper Functions
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
    return text

def sanitize_text(content):
    """Remove or replace unsupported characters."""
    sanitized_content = re.sub(r'[^\x00-\x7F]+', ' ', content)  # Replace non-ASCII characters with a space
    return sanitized_content

def tailor_resume(resume_content, job_description):
    """Generate tailored content for the resume."""
    tailored_content = f"Tailored Resume Content:\n\n{resume_content}\n\nJob Description Alignment:\n\n{job_description}"
    return tailored_content

def format_as_bullets(content):
    """Add bullet points to content where appropriate."""
    lines = content.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("•"):  # Add a bullet if it isn't already a bullet
            formatted_lines.append(f"• {line}")
        else:
            formatted_lines.append(line)  # Keep existing bullets
    return "\n".join(formatted_lines)

def generate_pdf(content, output_path):
    """Create a PDF file with clean formatting and bullets."""
    
    font_url = "https://github.com/diegodelemos/fpdf2/raw/main/examples/DejaVuSans.ttf"
    font_path = "fonts/DejaVuSans.ttf"

    os.makedirs("fonts", exist_ok=True)
    if not os.path.exists(font_path):
    with open(font_path, "wb") as f:
        response = requests.get(font_url)
        f.write(response.content)

    pdf.add_font("DejaVu", style="", fname=font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    font_path = "fonts/DejaVuSans.ttf"
    # Set up Unicode font
    pdf.add_font("DejaVu", style="", fname=font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
   
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)

    # Sanitize and format content
    sanitized_content = sanitize_text(content)
    bulleted_content = format_as_bullets(sanitized_content)

    # Add the formatted content to the PDF
    for line in bulleted_content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path, 'F')

def create_zip_file(output_dir, output_zip_path):
    """Zip the tailored resumes into a single archive."""
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.pdf'):  # Include only PDFs
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=os.path.basename(file_path))
    return output_zip_path

# App Title
st.title("Job Assistant")

# Upload Files Section
st.subheader("Upload Files")
job_links_file = st.file_uploader("Upload a text file with job links (.txt)", type="txt")
resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# Processing Section
if st.button("Process"):
    if job_links_file and resume_file:
        st.write("Processing your files...")

        # Save uploaded files locally
        os.makedirs("uploaded_files", exist_ok=True)
        job_links_path = f"uploaded_files/{job_links_file.name}"
        resume_path = f"uploaded_files/{resume_file.name}"
        
        try:
            # Save job links file
            with open(job_links_path, "wb") as f:
                f.write(job_links_file.read())
            
            # Save resume file
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            # Extract resume content
            st.write("Extracting resume content...")
            resume_content = extract_text_from_pdf(resume_path)

            # Simulate job description scraping
            st.write("Fetching job descriptions...")
            with open(job_links_path, 'r', encoding='utf-8') as f:
                job_links = f.read().splitlines()
            job_descriptions = [f"Sample job description for {link}" for link in job_links]

            # Tailor resumes
            st.write("Tailoring resumes...")
            tailored_resumes_dir = "uploaded_files/tailored_resumes"
            os.makedirs(tailored_resumes_dir, exist_ok=True)
            for i, job_description in enumerate(job_descriptions, start=1):
                tailored_content = tailor_resume(resume_content, job_description)
                output_pdf_path = os.path.join(tailored_resumes_dir, f"tailored_resume_{i}.pdf")
                generate_pdf(tailored_content, output_pdf_path)

            # Create ZIP file
            st.write("Zipping tailored resumes...")
            zip_file_path = create_zip_file(tailored_resumes_dir, "uploaded_files/tailored_resumes.zip")

            # Provide download link
            with open(zip_file_path, "rb") as f:
                st.download_button(
                    label="Download Tailored Resumes",
                    data=f,
                    file_name="tailored_resumes.zip",
                    mime="application/zip"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload both files to proceed.")
