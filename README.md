# PhishDetect
## AI-powered Phishing email Detector

A Streamlit application that uses the Groq API with Llama model (llama3-70b-8192) to detect phishing emails.

## Features

- Real-time phishing email analysis.
- User-friendly Streamlit interface.
- Detailed analysis results (Displays **classification (Phishing/Legitimate)** with explanations.
- Logging system for tracking usage. (Logs analyses in `phishing_detector.log` with timestamps and errors.)
- Helpful tips for identifying phishing emails

## Setup

1. Clone this repository.
   ```bash
   git clone https://github.com/krishnarhajil/PhishDetect.git
   cd PhishDetect
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Executing the Application

To run the application, execute:
```bash
streamlit run app.py
```
or if Streamlit is not globally recognized in your environment, execute:
```bash
python streamlit run app.py
```

The application will open in your default web browser.

## Usage

1. Paste the email text you want to analyze into the text area
2. Click the "Analyze Email" button
3. View the analysis results and recommendations

## Logging

The application logs all analyses to `phishing_detector.log`. This includes:
- Timestamp of each analysis
- Success/failure of the analysis
- Any errors that occur during processing

## Security Note

- This tool is part of my personal project and is intended for educational and demonstration purposes only. 
- Always exercise caution when handling suspicious emails.  
- Verify the authenticity of important communications through official channels.  
