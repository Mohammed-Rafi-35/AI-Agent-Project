Career Navigator AI
Overview
Career Navigator AI is a sophisticated, AI-driven web application developed to empower professionals in advancing their careers. Leveraging Streamlit and integrated with cutting-edge language models, this platform offers comprehensive resume analysis, Applicant Tracking System (ATS) compatibility feedback, professional summary generation, and tailored interview simulations based on individual resume content.
Key Features

Resume Analysis: Conduct a thorough evaluation of your resume, highlighting strengths and identifying areas for enhancement.
ATS Feedback: Receive a detailed compatibility score with ATS platforms, accompanied by actionable optimization recommendations.
Resume Summary: Generate a polished, concise professional summary derived from your resume data.
Interview Simulation: Engage in AI-powered interview practice with role-specific questions and in-depth feedback on responses.

System Requirements

Python 3.8 or later
Required Python dependencies (detailed in requirements.txt):
streamlit==1.38.0
PyMuPDF==1.24.7
python-docx==1.1.2
python-dotenv==1.0.1
transformers==4.44.2
langchain==0.2.16
langchain-groq==0.1.9



Installation Instructions

Clone the repository to your local environment:git clone https://github.com/Mohammed-Raf-35/career-navigation-ai.git
cd career-navigation-ai


Install the necessary dependencies:pip install -r requirements.txt


Configure your GROQ API key:
Create a .env file in the project directory.
Insert your GROQ API key: GROQ_API_KEY=your_api_key_here.


Launch the application locally:streamlit run cn_ai.py



Usage Guidelines

Upload your resume in PDF or DOCX format through the application interface.
Utilize the sidebar navigation to access available features:
Resume Analysis: Review a detailed assessment of your resume.
ATS Feedback: Assess ATS compatibility and receive improvement suggestions.
Resume Summary: Create and export a professional summary.
Interview Simulation: Initiate a customized AI interview practice session.


Input your GROQ API key via the sidebar to activate the AI backend.

Deployment Information
This application is hosted on Streamlit Community Cloud and is accessible at https://career-navigation-ai.streamlit.app/. Last updated: July 26, 2025.
Contribution Guidelines
We welcome contributions from the community. Please fork the repository and submit pull requests for proposed enhancements or bug fixes. Ensure adherence to the project’s coding standards and include comprehensive documentation.
Licensing
This project is distributed under the MIT License. For full terms, refer to the LICENSE file.
Acknowledgements

Developed using Streamlit.
Enhanced by Grok through LangChain integration.
Relies on PyMuPDF for PDF processing and python-docx for DOCX support.
