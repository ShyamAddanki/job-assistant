import streamlit as st
from fpdf import FPDF
import os
import zipfile
from PyPDF2 import PdfReader
import re

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
    """Sanitize text by replacing unsupported characters."""
    if content is None:
        return ""
    # Replace bullet points with dashes or other ASCII characters
    content = content.replace("•", "-")
    # Replace non-ASCII characters with spaces
    content = re.sub(r'[^\x00-\x7F]+', ' ', content)
    return content

def tailor_resume(resume_content, job_description):
    """Generate tailored content for the resume."""
    return f"Tailored Resume Content:\n\n{resume_content}\n\nJob Description Alignment:\n\n{job_description}"

def format_as_bullets(content):
    """Format content as bullets."""
    lines = content.split('\n')
    return "\n".join([f"- {line.strip()}" if line.strip() else '' for line in lines])

def generate_pdf(content, output_path):
    """Create a PDF with clean formatting using the default font."""
    try:
        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Set default font (Arial)
        pdf.set_font("Arial", size=12)

        # Validate and sanitize content
        if not isinstance(content, str):
            raise ValueError("Content passed to generate_pdf must be a string.")

        sanitized_content = sanitize_text(content)
        bulleted_content = format_as_bullets(sanitized_content)

        # Split into lines and ensure each is a string
        lines = bulleted_content.split('\n')
        lines = [str(line) for line in lines]  # Ensure each line is a string

        # Add content to the PDF
        for line in lines:
            pdf.multi_cell(0, 10, line if line else "")  # Add each line to the PDF

        # Save the PDF to the specified output path
        pdf.output(output_path, 'F')
        st.write(f"PDF successfully generated: {output_path}")

    except Exception as e:
        # Handle exceptions gracefully and log the error
        st.error(f"Error generating PDF: {e}")

def create_zip_file(output_dir, output_zip_path):
    """Create a ZIP file containing PDFs."""
    try:
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Check if the file is a non-empty PDF before zipping
                    if file.endswith('.pdf') and os.path.getsize(file_path) > 0:
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
                try:
                    tailored_content = tailor_resume(resume_content, job_description)
                    output_pdf_path = os.path.join(tailored_resumes_dir, f"tailored_resume_{i}.pdf")

                    # Generate the PDF
                    generate_pdf(tailored_content, output_pdf_path)

                    # Confirm PDF generation
                    if os.path.exists(output_pdf_path):
                        st.write(f"PDF successfully generated: {output_pdf_path}")
                    else:
                        st.error(f"PDF generation failed: {output_pdf_path}")

                except Exception as e:
                    st.error(f"An error occurred while processing job description {i}: {e}")

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
