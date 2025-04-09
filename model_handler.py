from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PhishingDetector:
    def __init__(self):

        self.model_name = "llama3-70b-8192" 
        print("Loading model and tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=2,  # Binary classification: phishing or not
            torch_dtype=torch.float32  # Use float32 for better compatibility
        )
        print("Model loaded successfully!")
    
    def predict(self, email_content):
        # Handle both dictionary and string inputs
        if isinstance(email_content, dict):
            # Combine header and body information
            text = f"{email_content['headers']['subject']} {email_content['headers']['from']} {email_content['body']}"
        else:
            # If raw text, use as is
            text = str(email_content)
        
        # Tokenize and prepare input
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        # Get the probability of phishing
        phishing_score = predictions[0][1].item()
        is_phishing = int(phishing_score > 0.5)
        
        return is_phishing, phishing_score 
