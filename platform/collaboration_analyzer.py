#!/usr/bin/env python3
"""
Collaboration Analyzer
Detects past collaborations and generates collaboration ideas
"""

import os
import json
from typing import Dict, List, Optional
from data_manager import InfluencerDataManager
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class CollaborationAnalyzer:
    """Analyze and generate collaboration opportunities"""
    
    def __init__(self):
        self.data_manager = InfluencerDataManager()
        self.llm = None
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key and openai_api_key != 'your_openai_api_key_here':
            try:
                self.llm = ChatOpenAI(
                    model_name="gpt-4o-mini",
                    temperature=0.7,  # More creative for idea generation
                    openai_api_key=openai_api_key
                )
            except:
                pass
    
    def detect_past_collaborations(self, influencer_id: str) -> List[Dict]:
        """
        Detect past collaborations from posts/activity
        
        Analyzes posts to identify:
        - Brand mentions
        - Sponsored content indicators
        - Partnership announcements
        - Collaborative projects
        """
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return []
        
        # Use AI to analyze for collaboration patterns
        if self.llm:
            collaborations = self._ai_detect_collaborations(influencer)
        else:
            collaborations = self._rule_based_detection(influencer)
        
        return collaborations
    
    def _ai_detect_collaborations(self, influencer: Dict) -> List[Dict]:
        """Use AI to detect past collaborations"""
        try:
            prompt = f"""Analyze this influencer's profile for past collaborations:

Name: {influencer.get('full_name', '')}
Job Title: {influencer.get('job_title', '')}
Company: {influencer.get('company_name', '')}
Bio: {influencer.get('bio', 'N/A')}
LinkedIn: {influencer.get('linkedin_handle', 'N/A')}
Twitter: {influencer.get('twitter_handle', 'N/A')}

Based on their profile and typical patterns, identify:
1. Likely past collaborations (brands, companies)
2. Collaboration types (content, sponsored, partnerships)
3. Industry sectors they've worked with

Return as JSON array of collaborations with:
- company_name
- collaboration_type
- industry
- likelihood (high/medium/low)"""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            # Parse response
            return self._parse_collaborations(response.content)
        except:
            return []
    
    def _rule_based_detection(self, influencer: Dict) -> List[Dict]:
        """Rule-based collaboration detection"""
        collaborations = []
        
        # Check company associations
        company = influencer.get('company_name', '')
        if company:
            collaborations.append({
                "company_name": company,
                "collaboration_type": "employment",
                "industry": influencer.get('industry', ''),
                "likelihood": "high"
            })
        
        return collaborations
    
    def _parse_collaborations(self, ai_response: str) -> List[Dict]:
        """Parse AI response for collaborations"""
        try:
            if '```json' in ai_response:
                json_str = ai_response.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response:
                json_str = ai_response.split('```')[1].split('```')[0].strip()
            else:
                json_str = ai_response
            
            import json
            return json.loads(json_str)
        except:
            return []
    
    def generate_ideas(self, influencer_id: str, company_type: str, 
                      goals: List[str], focus: str = 'content') -> List[Dict]:
        """
        Generate collaboration ideas
        
        Focus: 'content' (not promotion) - for content collaboration
        """
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return []
        
        if self.llm:
            ideas = self._ai_generate_ideas(influencer, company_type, goals, focus)
        else:
            ideas = self._rule_based_ideas(influencer, company_type, focus)
        
        return ideas
    
    def _ai_generate_ideas(self, influencer: Dict, company_type: str, 
                          goals: List[str], focus: str) -> List[Dict]:
        """Use AI to generate collaboration ideas"""
        try:
            prompt = f"""Generate content collaboration ideas (NOT promotional):

Influencer:
- Name: {influencer.get('full_name', '')}
- Job Title: {influencer.get('job_title', '')}
- Expertise: {influencer.get('job_title', '')}

Company Type: {company_type}
Goals: {', '.join(goals)}
Focus: Content collaboration (NOT promotion)

Generate 5-7 collaboration ideas that:
1. Focus on creating valuable content together
2. Are NOT promotional or sales-focused
3. Provide value to both audiences
4. Are authentic and engaging

For each idea, provide:
- idea_title
- description
- content_format (video, article, podcast, etc.)
- value_proposition
- execution_steps

Return as JSON array."""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return self._parse_ideas(response.content)
        except:
            return []
    
    def _rule_based_ideas(self, influencer: Dict, company_type: str, focus: str) -> List[Dict]:
        """Rule-based idea generation"""
        job_title = influencer.get('job_title', '').lower()
        
        ideas = []
        
        if 'tech' in job_title or 'journalist' in job_title:
            ideas.append({
                "idea_title": "Expert Interview Series",
                "description": "Collaborate on interview content featuring industry insights",
                "content_format": "Video/Podcast",
                "value_proposition": "Educational content for both audiences",
                "execution_steps": ["Plan topics", "Record interviews", "Co-promote"]
            })
        
        if 'content' in job_title or 'creator' in job_title:
            ideas.append({
                "idea_title": "Co-Created Tutorial Series",
                "description": "Create educational tutorials together",
                "content_format": "Video/Article",
                "value_proposition": "Shared expertise benefits both audiences",
                "execution_steps": ["Identify topics", "Create content", "Cross-promote"]
            })
        
        return ideas
    
    def _parse_ideas(self, ai_response: str) -> List[Dict]:
        """Parse AI-generated ideas"""
        try:
            import json
            if '```json' in ai_response:
                json_str = ai_response.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response:
                json_str = ai_response.split('```')[1].split('```')[0].strip()
            else:
                json_str = ai_response
            
            return json.loads(json_str)
        except:
            return []
    
    def find_opportunities(self, influencer_id: str) -> List[Dict]:
        """Find collaboration opportunities for influencer"""
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return []
        
        # Analyze profile to find opportunities
        opportunities = []
        
        # Content collaboration opportunities
        opportunities.append({
            "type": "content_creation",
            "title": "Co-Create Educational Content",
            "description": "Collaborate on creating valuable educational content",
            "suitable_for": ["tech companies", "education platforms", "media companies"]
        })
        
        return opportunities
    
    def identify_company_types(self, influencer_id: str) -> List[str]:
        """Identify compatible company types for collaboration"""
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return []
        
        job_title = influencer.get('job_title', '').lower()
        industry = influencer.get('industry', '').lower()
        
        company_types = []
        
        if 'tech' in job_title or 'tech' in industry:
            company_types.extend(['tech startups', 'SaaS companies', 'tech media'])
        
        if 'marketing' in job_title:
            company_types.extend(['marketing agencies', 'brands', 'advertising companies'])
        
        if 'journalist' in job_title or 'reporter' in job_title:
            company_types.extend(['media companies', 'news outlets', 'publishers'])
        
        return list(set(company_types))
    
    def get_recommendations_for_influencer(self, influencer_id: str) -> List[Dict]:
        """Get collaboration recommendations for logged-in influencer"""
        # Similar to find_opportunities but personalized
        return self.find_opportunities(influencer_id)

