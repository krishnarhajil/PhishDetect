import re
from email.parser import Parser
from email.policy import default

class EmailPreprocessor:
    def __init__(self):
        self.email_parser = Parser(policy=default)
    
    def preprocess(self, email_content):
        """
        Preprocess the email content by:
        1. Parsing email headers and body
        2. Extracting URLs and email addresses
        3. Cleaning and normalizing text
        4. Removing HTML tags
        """
        # Parse the email content
        email = self.email_parser.parsestr(email_content)
        
        # Extract headers
        headers = {
            'subject': email.get('subject', ''),
            'from': email.get('from', ''),
            'to': email.get('to', ''),
            'date': email.get('date', '')
        }
        
        # Extract body
        body = ""
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_content()
                    break
        else:
            body = email.get_content()
        
        # Clean the body text
        cleaned_body = self._clean_text(body)
        
        # Extract URLs and email addresses
        urls = self._extract_urls(body)
        email_addresses = self._extract_email_addresses(body)
        
        # Combine all information
        processed_content = {
            'headers': headers,
            'body': cleaned_body,
            'urls': urls,
            'email_addresses': email_addresses
        }
        
        return processed_content
    
    def _clean_text(self, text):
        """Clean and normalize the text content."""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        return text.strip()
    
    def _extract_urls(self, text):
        """Extract URLs from the text."""
        if not text:
            return []
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def _extract_email_addresses(self, text):
        """Extract email addresses from the text."""
        if not text:
            return []
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, text) 