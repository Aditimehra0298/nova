#!/usr/bin/env python3
"""
Influencer Authentication
Handles influencer login, registration, and profile management
"""

import os
import hashlib
import json
from typing import Dict, Optional
from data_manager import InfluencerDataManager
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class InfluencerAuth:
    """Handle influencer authentication and profile management"""
    
    USERS_FILE = 'influencer_users.json'
    
    def __init__(self):
        self.data_manager = InfluencerDataManager()
        self.users = self._load_users()
        self.llm = None
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key and openai_api_key != 'your_openai_api_key_here':
            try:
                self.llm = ChatOpenAI(
                    model_name="gpt-4o-mini",
                    temperature=0.3,
                    openai_api_key=openai_api_key
                )
            except:
                pass
    
    def _load_users(self) -> Dict:
        """Load registered users"""
        if os.path.exists(self.USERS_FILE):
            try:
                with open(self.USERS_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_users(self):
        """Save users to file"""
        with open(self.USERS_FILE, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, email: str, password: str, profile_data: Dict) -> Dict:
        """Register new influencer"""
        email_lower = email.lower()
        
        if email_lower in self.users:
            return {"success": False, "error": "Email already registered"}
        
        user_id = f"inf_{len(self.users) + 1}"
        
        self.users[email_lower] = {
            "id": user_id,
            "email": email,
            "password_hash": self._hash_password(password),
            "profile": profile_data,
            "registered_at": str(os.popen('date').read().strip())
        }
        
        self._save_users()
        
        return {
            "success": True,
            "influencer_id": user_id,
            "message": "Registration successful"
        }
    
    def login(self, email: str, password: str) -> Dict:
        """Login influencer"""
        email_lower = email.lower()
        
        if email_lower not in self.users:
            return {"success": False, "error": "Email not found"}
        
        user = self.users[email_lower]
        if user['password_hash'] != self._hash_password(password):
            return {"success": False, "error": "Invalid password"}
        
        return {
            "success": True,
            "influencer_id": user['id'],
            "email": email
        }
    
    def get_profile(self, influencer_id: str) -> Dict:
        """Get influencer profile"""
        for email, user in self.users.items():
            if user['id'] == influencer_id:
                return {
                    "id": influencer_id,
                    "email": user['email'],
                    "profile": user.get('profile', {})
                }
        return {}
    
    def analyze_and_reconfirm_profile(self, influencer_id: str) -> Dict:
        """
        Analyze influencer profile and reconfirm:
        - Industry
        - Target audience
        - Collaboration opportunities
        """
        profile = self.get_profile(influencer_id)
        if not profile:
            return {"error": "Profile not found"}
        
        profile_data = profile.get('profile', {})
        
        if self.llm:
            analysis = self._ai_analyze_profile(profile_data)
        else:
            analysis = self._rule_based_analysis(profile_data)
        
        return {
            "influencer_id": influencer_id,
            "confirmed_industry": analysis.get('industry', ''),
            "target_audience": analysis.get('target_audience', []),
            "collaboration_opportunities": analysis.get('opportunities', []),
            "recommendations": analysis.get('recommendations', [])
        }
    
    def _ai_analyze_profile(self, profile_data: Dict) -> Dict:
        """Use AI to analyze and reconfirm profile"""
        try:
            prompt = f"""Analyze this influencer profile:

Profile Data:
{json.dumps(profile_data, indent=2)}

Reconfirm and identify:
1. Primary industry
2. Target audience (detailed)
3. Content collaboration opportunities
4. Recommended collaboration types

Return as JSON."""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return self._parse_analysis(response.content)
        except:
            return self._rule_based_analysis(profile_data)
    
    def _rule_based_analysis(self, profile_data: Dict) -> Dict:
        """Rule-based profile analysis"""
        job_title = profile_data.get('job_title', '').lower()
        
        industry = 'technology'
        if 'marketing' in job_title:
            industry = 'marketing'
        elif 'media' in job_title or 'journalist' in job_title:
            industry = 'media'
        
        return {
            "industry": industry,
            "target_audience": ["professionals", "tech enthusiasts"],
            "opportunities": ["content creation", "expert interviews"],
            "recommendations": ["Focus on educational content", "Build long-term partnerships"]
        }
    
    def _parse_analysis(self, ai_response: str) -> Dict:
        """Parse AI analysis"""
        try:
            import json
            if '```json' in ai_response:
                json_str = ai_response.split('```json')[1].split('```')[0].strip()
            else:
                json_str = ai_response
            return json.loads(json_str)
        except:
            return {"industry": "", "target_audience": [], "opportunities": []}

