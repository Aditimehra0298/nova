#!/usr/bin/env python3
"""
Competitor Analyzer
Analyzes top competitors and their collaboration strategies
"""

import os
import json
from typing import Dict, List
from data_manager import InfluencerDataManager
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class CompetitorAnalyzer:
    """Analyze competitors and their collaboration strategies"""
    
    def __init__(self):
        self.data_manager = InfluencerDataManager()
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
    
    def analyze(self, target_audience: str, industry: str) -> Dict:
        """
        Analyze top competitors in target audience
        
        Identifies:
        - Top competitors
        - Their collaboration strategies
        - What they're doing with influencers
        - Opportunities to differentiate
        """
        # Get influencers in the same industry/audience
        all_influencers = self.data_manager.get_all_influencers()
        
        # Filter by industry/audience
        competitors = []
        for inf in all_influencers:
            if industry.lower() in inf.get('industry', '').lower() or \
               industry.lower() in inf.get('job_title', '').lower():
                competitors.append(inf)
        
        # Analyze their strategies
        if self.llm:
            analysis = self._ai_analyze_competitors(competitors, target_audience, industry)
        else:
            analysis = self._rule_based_analysis(competitors, target_audience, industry)
        
        return {
            "target_audience": target_audience,
            "industry": industry,
            "competitors_analyzed": len(competitors),
            "top_competitors": competitors[:10],
            "collaboration_strategies": analysis.get('strategies', []),
            "insights": analysis.get('insights', []),
            "opportunities": analysis.get('opportunities', [])
        }
    
    def _ai_analyze_competitors(self, competitors: List[Dict], 
                               target_audience: str, industry: str) -> Dict:
        """Use AI to analyze competitor strategies"""
        try:
            competitors_summary = json.dumps(competitors[:10], indent=2)
            
            prompt = f"""Analyze competitor collaboration strategies:

Target Audience: {target_audience}
Industry: {industry}

Competitors:
{competitors_summary}

Analyze:
1. What collaboration strategies are they using?
2. What types of content collaborations?
3. What can we learn from their approach?
4. Opportunities to differentiate

Focus on CONTENT collaborations, not promotional.

Return as JSON with:
- strategies (list)
- insights (list)
- opportunities (list)"""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return self._parse_analysis(response.content)
        except:
            return self._rule_based_analysis(competitors, target_audience, industry)
    
    def _rule_based_analysis(self, competitors: List[Dict], 
                            target_audience: str, industry: str) -> Dict:
        """Rule-based competitor analysis"""
        return {
            "strategies": [
                "Content co-creation",
                "Expert interviews",
                "Educational series"
            ],
            "insights": [
                "Most competitors focus on educational content",
                "Video content performs best",
                "Long-term partnerships are more effective"
            ],
            "opportunities": [
                "Focus on unique content formats",
                "Build deeper relationships",
                "Create series rather than one-offs"
            ]
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
            return {"strategies": [], "insights": [], "opportunities": []}

