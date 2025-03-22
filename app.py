import streamlit as st
import groq
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='phishing_detector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# Initialize Groq client
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
#print(client.models.list())

def analyze_email(email_text):
    try:
        prompt = f"""You are an expert in phishing email detection. Analyze the following email text and determine if it's a phishing attempt or legitimate.
        Consider these factors:
        1. Urgency or pressure tactics
        2. Suspicious links or attachments
        3. Poor grammar or spelling
        4. Impersonation attempts
        5. Unusual sender behavior
        6. Requests for sensitive information
        7. Threats or consequences
        8. Unprofessional formatting
        
        Respond in this exact format:
        CLASSIFICATION: [PHISHING/LEGITIMATE]
        CONFIDENCE: [0-100%]
        EXPLANATION: [2-3 sentences explaining your decision]
        
        Email text:
        {email_text}"""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in cybersecurity and phishing detection. Your task is to analyze emails and determine if they are phishing attempts or legitimate. Be thorough in your analysis and provide clear explanations."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
            temperature=0.1,
        )

        response = chat_completion.choices[0].message.content
        logging.info(f"Analysis completed for email: {email_text[:100]}...")
        return response

    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="Phishing Email Detector",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Phishing Email Detector")
    st.markdown("""
    This application uses AI to analyze email content and determine if it's a phishing attempt.
    Simply paste the email text below and click 'Analyze'.
    """)

    # Create a text area for email input
    email_text = st.text_area("Enter the email text:", height=200)

    if st.button("Analyze Email"):
        if email_text.strip():
            with st.spinner("Analyzing email..."):
                result = analyze_email(email_text)
                
                # Parse the result
                try:
                    classification = result.split("CLASSIFICATION:")[1].split("\n")[0].strip()
                    confidence = result.split("CONFIDENCE:")[1].split("\n")[0].strip()
                    explanation = result.split("EXPLANATION:")[1].strip()
                    
                    # Display result with appropriate styling
                    if "PHISHING" in classification.upper():
                        st.error("⚠️ PHISHING DETECTED!")
                    else:
                        st.success("✅ LEGITIMATE EMAIL")
                    
                    st.markdown("### Analysis Result:")
                    st.markdown(f"**Classification:** {classification}")
                    st.markdown(f"**Confidence:** {confidence}")
                    st.markdown(f"**Explanation:** {explanation}")
                    
                except:
                    st.error("Error parsing the analysis result")
                    st.write(result)
                
                # Log the analysis
                logging.info(f"Analysis completed for email: {email_text[:100]}...")
        else:
            st.warning("Please enter some email text to analyze.")

    # Add some helpful tips
    with st.expander("Tips for Identifying Phishing Emails"):
        st.markdown("""
        - Check for suspicious sender addresses
        - Look for urgent or threatening language
        - Verify links before clicking
        - Check for poor grammar and spelling
        - Be wary of requests for sensitive information
        - Verify the company name and branding
        - Watch for pressure tactics or threats
        - Check for unprofessional formatting
        - Verify the email domain matches the company
        - Be cautious of unexpected attachments
        """)

if __name__ == "__main__":
    main() 