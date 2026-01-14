#!/usr/bin/env python3
"""
Email Manager
Drafts and sends collaboration emails
"""

import os
import json
from typing import Dict, Optional
from data_manager import InfluencerDataManager
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class EmailManager:
    """Manage email drafting and sending"""
    
    def __init__(self):
        self.data_manager = InfluencerDataManager()
        self.llm = None
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key and openai_api_key != 'your_openai_api_key_here':
            try:
                self.llm = ChatOpenAI(
                    model_name="gpt-4o-mini",
                    temperature=0.7,  # More creative for email writing
                    openai_api_key=openai_api_key
                )
            except:
                pass
    
    def draft_email(self, influencer_id: str, collaboration_type: str, 
                   company_info: Dict) -> Dict:
        """
        Draft collaboration email
        
        Focus: Content collaboration, NOT promotion
        """
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return {"error": "Influencer not found"}
        
        if self.llm:
            email = self._ai_draft_email(influencer, collaboration_type, company_info)
        else:
            email = self._template_email(influencer, collaboration_type, company_info)
        
        return {
            "influencer_id": influencer_id,
            "to": influencer.get('email', ''),
            "subject": email.get('subject', ''),
            "body": email.get('body', ''),
            "collaboration_type": collaboration_type
        }
    
    def _ai_draft_email(self, influencer: Dict, collaboration_type: str, 
                       company_info: Dict) -> Dict:
        """Use AI to draft personalized email"""
        try:
            prompt = f"""Draft a professional collaboration email:

To: {influencer.get('full_name', '')}
Their Role: {influencer.get('job_title', '')}

Company: {company_info.get('name', 'Company')}
Collaboration Type: {collaboration_type}

IMPORTANT:
- Focus on CONTENT collaboration, NOT promotion
- Emphasize mutual value and authentic content
- Be professional but friendly
- Keep it concise (2-3 paragraphs)

Include:
1. Personal greeting
2. Why you're reaching out
3. Collaboration idea (content-focused)
4. Value proposition for both parties
5. Next steps

Return as JSON with 'subject' and 'body' fields."""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return self._parse_email(response.content)
        except:
            return self._template_email(influencer, collaboration_type, company_info)
    
    def _template_email(self, influencer: Dict, collaboration_type: str, 
                       company_info: Dict) -> Dict:
        """Template-based email"""
        subject = f"Content Collaboration Opportunity - {company_info.get('name', 'Our Company')}"
        
        body = f"""Hi {influencer.get('first_name', influencer.get('full_name', 'there'))},

I hope this email finds you well. I came across your work as a {influencer.get('job_title', 'professional')} and was impressed by your content.

We're interested in exploring a content collaboration opportunity that would be valuable for both our audiences. This would focus on creating authentic, educational content together - not promotional material.

The collaboration would involve:
- Co-creating valuable content
- Sharing expertise and insights
- Providing value to both audiences

Would you be open to a brief conversation to discuss this further?

Best regards,
{company_info.get('sender_name', 'Team')}
{company_info.get('name', 'Company')}"""
        
        return {"subject": subject, "body": body}
    
    def _parse_email(self, ai_response: str) -> Dict:
        """Parse AI-generated email"""
        try:
            import json
            if '```json' in ai_response:
                json_str = ai_response.split('```json')[1].split('```')[0].strip()
            else:
                json_str = ai_response
            return json.loads(json_str)
        except:
            return {"subject": "Collaboration Opportunity", "body": ai_response}
    
    def send_email(self, influencer_id: str, subject: str, content: str) -> Dict:
        """Send email to influencer"""
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return {"success": False, "message": "Influencer not found"}
        
        email = influencer.get('email', '')
        if not email:
            return {"success": False, "message": "No email address found"}
        
        # In production, would integrate with email service (SendGrid, Mailgun, etc.)
        # For now, return success (email would be sent)
        
        return {
            "success": True,
            "message": f"Email drafted for {email}",
            "to": email,
            "subject": subject,
            "note": "Email service integration needed for actual sending"
        }

