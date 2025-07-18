import os
import fitz  # PyMuPDF
import docx
import logging
from dotenv import load_dotenv
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from typing import List, Dict, Tuple, Any
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CareerNavigatorBackend:
    def __init__(self, groq_api_key: str):
        """Initialize the Career Navigator with API key"""
        self.groq_api_key = groq_api_key
        self.llm = None
        self.chains = {}
        self.ner_model = None
        self._setup_llm()
        self._setup_chains()
        self._setup_ner_model()

    def _setup_llm(self):
        """Configure the LLM"""
        try:
            self.llm = ChatGroq(
                model_name="llama3-8b-8192",
                temperature=0.3,
                api_key=self.groq_api_key
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def _setup_chains(self):
        """Setup all LLM chains"""
        role_prompt = PromptTemplate.from_template(
            """Analyze this resume and identify the most likely job role/position this person is seeking or qualified for.
            Consider their experience, skills, and background.
            
            Resume:
            {resume}
            
            Return only the specific job role title (e.g., "Software Engineer", "Data Scientist", "Marketing Manager"):"""
        )

        interview_question_prompt = PromptTemplate.from_template(
            """Generate a technical interview question for a {role} position.
            The question should be:
            - Relevant to the role
            - Moderately challenging
            - Practical and realistic
            
            
            Return only the question without any additional text:"""
        )

        evaluate_prompt = PromptTemplate.from_template(
            """Evaluate this interview answer for a {role} position:
            
            Question: {question}
            Answer: {answer}
            
            Provide:
            1. Score out of 10
            2. Brief explanation of strengths and weaknesses
            3. Suggestions for improvement
            
            Format your response as:
            Score: X/10
            Evaluation: [Your detailed feedback]"""
        )

        ats_prompt = PromptTemplate.from_template(
            """You are an ATS (Applicant Tracking System) analyzing this resume.
            
            Resume:
            {resume}
            
            Provide:
            1. Overall ATS score out of 100
            2. Key strengths identified
            3. Areas needing improvement
            4. Specific recommendations to improve ATS compatibility
            
            Format your response as:
            ATS Score: X/100
            Strengths: [List key strengths]
            Areas for Improvement: [List improvement areas]
            Recommendations: [Specific actionable recommendations]"""
        )

        summarize_prompt = PromptTemplate.from_template(
            """Create a concise professional summary of this resume:
            
            Resume:
            {resume}
            
            Provide:
            1. Professional summary (2-3 sentences)
            2. Key skills and expertise
            3. Years of experience
            4. Notable achievements
            
            Format your response clearly and professionally."""
        )

        self.chains = {
            'role': LLMChain(prompt=role_prompt, llm=self.llm),
            'question': LLMChain(prompt=interview_question_prompt, llm=self.llm),
            'evaluate': LLMChain(prompt=evaluate_prompt, llm=self.llm),
            'ats': LLMChain(prompt=ats_prompt, llm=self.llm),
            'summarize': LLMChain(prompt=summarize_prompt, llm=self.llm)
        }

    @st.cache_resource
    def _setup_ner_model(_self):
        """Setup NER model for keyword extraction"""
        try:
            return pipeline("ner", model="dslim/bert-base-NER")
        except Exception as e:
            logger.error(f"Failed to load NER model: {e}")
            return None

    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from uploaded file"""
        try:
            if uploaded_file.type == "application/pdf":
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                doc = fitz.open("temp.pdf")
                text = "\n".join([page.get_text() for page in doc])
                doc.close()
                os.remove("temp.pdf")
                return text
                
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                with open("temp.docx", "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                doc = docx.Document("temp.docx")
                text = "\n".join([p.text for p in doc.paragraphs])
                os.remove("temp.docx")
                return text
                
            else:
                raise ValueError("Unsupported file format. Please upload PDF or DOCX files.")
                
        except Exception as e:
            logger.error(f"Failed to extract text from file: {e}")
            raise

    def extract_keywords(self, resume_text: str) -> List[str]:
        """Extract keywords using NER model"""
        try:
            if self.ner_model is None:
                self.ner_model = self._setup_ner_model()
            
            if self.ner_model is None:
                return []
                
            entities = self.ner_model(resume_text)
            keywords = list(set(ent["word"] for ent in entities if ent["entity"].startswith("B-")))
            
            keywords = [kw.replace("##", "").strip() for kw in keywords if len(kw) > 2]
            return keywords[:20]  
        except Exception as e:
            logger.error(f"Failed to extract keywords: {e}")
            return []

    def identify_role(self, resume_text: str) -> str:
        """Identify the most likely job role from resume"""
        try:
            role = self.chains['role'].run({"resume": resume_text}).strip()
            return role
        except Exception as e:
            logger.error(f"Failed to identify role: {e}")
            return "General Professional"

    def get_ats_feedback(self, resume_text: str) -> str:
        """Get ATS feedback and scoring"""
        try:
            feedback = self.chains['ats'].run({"resume": resume_text}).strip()
            return feedback
        except Exception as e:
            logger.error(f"Failed to get ATS feedback: {e}")
            return "Unable to generate ATS feedback at this time."

    def summarize_resume(self, resume_text: str) -> str:
        """Generate resume summary"""
        try:
            summary = self.chains['summarize'].run({"resume": resume_text}).strip()
            return summary
        except Exception as e:
            logger.error(f"Failed to summarize resume: {e}")
            return "Unable to generate resume summary at this time."

    def generate_interview_question(self, role: str) -> str:
        """Generate interview question for specific role"""
        try:
            question = self.chains['question'].run({"role": role}).strip()
            return question
        except Exception as e:
            logger.error(f"Failed to generate interview question: {e}")
            return f"Tell me about your experience in {role}?"

    def evaluate_answer(self, role: str, question: str, answer: str) -> str:
        """Evaluate interview answer"""
        try:
            evaluation = self.chains['evaluate'].run({
                "role": role,
                "question": question,
                "answer": answer
            }).strip()
            return evaluation
        except Exception as e:
            logger.error(f"Failed to evaluate answer: {e}")
            return "Score: 5/10\nEvaluation: Unable to evaluate answer at this time."

    def analyze_resume(self, uploaded_file) -> Dict[str, Any]:
        """Complete resume analysis pipeline"""
        try:
            resume_text = self.extract_text_from_file(uploaded_file)
            
            role = self.identify_role(resume_text)
            ats_feedback = self.get_ats_feedback(resume_text)
            summary = self.summarize_resume(resume_text)
            keywords = self.extract_keywords(resume_text)
            
            return {
                "resume_text": resume_text,
                "role": role,
                "ats_feedback": ats_feedback,
                "summary": summary,
                "keywords": keywords,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze resume: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def conduct_interview_session(self, role: str) -> Dict[str, str]:
        """Generate a single interview question for the session"""
        try:
            question = self.generate_interview_question(role)
            return {
                "question": question,
                "success": True
            }
        except Exception as e:
            logger.error(f"Failed to conduct interview: {e}")
            return {
                "success": False,
                "error": str(e)
            }