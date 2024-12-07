import streamlit as st
from fpdf import FPDF
import os
import zipfile
from PyPDF2 import PdfReader
import re
import requests

# Helper Functions
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ''.join([page.extract_text() or '' for page in reader.pages])
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def sanitize_text(content):
    """Remove unsupported characters."""
    return re.sub(r'[^\x00-\x7F]+', ' ', content)  # Replace non-ASCII characters with a space

def tailor_resume(resume_content, job_description):
    """Generate tailored content for the resume."""
    return f"Tailored Resume Content:\n\n{resume_content}\n\nJob Description Alignment:\n\n{job_description}"

def format_as_bullets(content):
    """Format content as bullets."""
    lines = content.split('\n')
    return "\n".join([f"• {line.strip()}" if line.strip() else '' for line in lines])

@st.cache_resource
def download_and_setup_font():
    """Download and setup the required font for PDF generation."""
    font_url = "https://github.com/diegodelemos/fpdf2/raw/main/examples/DejaVuSans.ttf"
    font_path = "fonts/DejaVuSans.ttf"
    os.makedirs("fonts", exist_ok=True)
    if not os.path.exists(font_path):
        response = requests.get(font_url, stream=True)
        with open(font_path, "wb") as f:
            f.write(response.content)
    return font_path

def generate_pdf(content, output_path):
    """Create a PDF with clean formatting."""
    try:
        # Set up font
        font_path = download_and_setup_font()

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_font("DejaVu", style="", fname=font_path, uni=True)
        pdf.set_font("DejaVu", size=12)

        # Sanitize and format content
        sanitized_content = sanitize_text(content)
        bulleted_content = format_as_bullets(sanitized_content)

        # Debugging content before writing to PDF
        st.write("Content being written to PDF (debug):", bulleted_content)

        # Add content to PDF
        for line in bulleted_content.split('\n'):
            pdf.multi_cell(0, 10, str(line) if line else "")  # Ensure line is a string
        pdf.output(output_path, 'F')
    except Exception as e:
        st.error(f"Error generating PDF: {e}")

def create_zip_file(output_dir, output_zip_path):
    """Create a ZIP file containing PDFs."""
    try:
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    if file.endswith('.pdf'):  # Include only PDFs
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.basename(file_path))
        return output_zip_path
    except Exception as e:
        st.error(f"Error creating ZIP file: {e}")
        return None

# Streamlit App
st.title("Job Assistant")

# File Upload Section
st.subheader("Upload Files")
job_links_file = st.file_uploader("Upload a text file with job links (.txt)", type="txt")
resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# Process Button
if st.button("Process"):
    if job_links_file and resume_file:
        st.write("Processing your files...")
        
        # Create directories
        os.makedirs("uploaded_files", exist_ok=True)
        tailored_resumes_dir = "uploaded_files/tailored_resumes"
        os.makedirs(tailored_resumes_dir, exist_ok=True)

        # Save uploaded files
        job_links_path = f"uploaded_files/{job_links_file.name}"
        resume_path = f"uploaded_files/{resume_file.name}"
        with open(job_links_path, "wb") as f:
            f.write(job_links_file.read())
        with open(resume_path, "wb") as f:
            f.write(resume_file.read())

        try:
            # Extract resume content
            st.write("Extracting resume content...")
            resume_content = extract_text_from_pdf(resume_path)

            # Read and sanitize job links
            st.write("Fetching job descriptions...")
            with open(job_links_path, 'r', encoding='utf-8') as f:
                job_links = [line.strip() for line in f.readlines() if line.strip()]
            job_descriptions = [f"Sample job description for {link}" for link in job_links]

            # Generate tailored resumes
            st.write("Tailoring resumes...")
            for i, job_description in enumerate(job_descriptions, start=1):
                tailored_content = tailor_resume(resume_content, job_description)
                output_pdf_path = os.path.join(tailored_resumes_dir, f"tailored_resume_{i}.pdf")
                generate_pdf(tailored_content, output_pdf_path)

            # Zip tailored resumes
            st.write("Creating ZIP file...")
            zip_file_path = create_zip_file(tailored_resumes_dir, "uploaded_files/tailored_resumes.zip")

            # Provide download link
            if zip_file_path:
                with open(zip_file_path, "rb") as f:
                    st.download_button(
                        label="Download Tailored Resumes",
                        data=f,
                        file_name="tailored_resumes.zip",
                        mime="application/zip"
                    )
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
    else:
        st.error("Please upload both files to proceed.")
