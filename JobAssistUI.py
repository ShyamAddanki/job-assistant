{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "826beb9a-cfc1-4a10-9c2e-84c7801a56d0",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-12-06 20:09:15.764 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.278 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\Ash\\anaconda3\\lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2024-12-06 20:09:16.279 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.282 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.283 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.285 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.289 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.292 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.295 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.297 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.299 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.301 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.310 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.312 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.315 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.317 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.318 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.321 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.322 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.324 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.355 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.359 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.361 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2024-12-06 20:09:16.364 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "\n",
    "# App Title\n",
    "st.title(\"Interactive Job Assistant\")\n",
    "\n",
    "# File Upload for Job Links\n",
    "st.subheader(\"Step 1: Upload Job Links\")\n",
    "job_file = st.file_uploader(\"Upload a text file containing job links (e.g., LinkedIn jobs)\")\n",
    "\n",
    "# File Upload for Resume\n",
    "st.subheader(\"Step 2: Upload Your Resume\")\n",
    "resume_file = st.file_uploader(\"Upload your resume (PDF or DOCX format)\")\n",
    "\n",
    "# Process Inputs\n",
    "if st.button(\"Generate Tailored Resumes\"):\n",
    "    if job_file and resume_file:\n",
    "        st.write(\"Processing files... Please wait.\")  # Display feedback\n",
    "        # Call backend logic to process job links and resume\n",
    "        # Simulated backend processing\n",
    "        tailored_resume_data = \"This would be the tailored resumes in a ZIP or PDF.\"\n",
    "\n",
    "        # Provide download link\n",
    "        st.success(\"Resumes tailored successfully!\")\n",
    "        st.download_button(\n",
    "            label=\"Download Tailored Resumes\",\n",
    "            data=tailored_resume_data,\n",
    "            file_name=\"tailored_resumes.zip\"\n",
    "        )\n",
    "    else:\n",
    "        st.error(\"Please upload both the job links file and your resume.\")\n",
    "\n",
    "# Footer\n",
    "st.info(\"This app tailors your resume for up to 10 job profiles based on job descriptions.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "03f69f88-6163-420d-b478-816c0a264582",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.19"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
