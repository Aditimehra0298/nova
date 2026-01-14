#!/usr/bin/env python3
"""
Influencer Evaluator
Evaluates influencers on outreach, reactions, views, and engagement
"""

import os
from typing import Dict, List, Optional
from data_manager import InfluencerDataManager
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class InfluencerEvaluator:
    """Evaluate influencer performance metrics"""
    
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
    
    def evaluate(self, influencer_id: str, filters: Optional[Dict] = None) -> Dict:
        """
        Evaluate influencer on multiple metrics
        
        Args:
            influencer_id: Influencer ID or influencer data dict
            filters: Optional filters to help find the influencer
        
        Returns:
        {
            "outreach_score": 0-100,
            "reactions_score": 0-100,
            "views_score": 0-100,
            "engagement_rate": 0-100,
            "overall_score": 0-100,
            "metrics": {...}
        }
        """
        # If influencer_id is already a dict, use it directly
        if isinstance(influencer_id, dict):
            influencer = influencer_id
        else:
            influencer = self.data_manager.get_influencer_by_id(influencer_id, filters)
            if not influencer:
                return {"error": "Influencer not found"}
        
        # Calculate metrics
        metrics = self._calculate_metrics(influencer)
        
        # Use AI for advanced evaluation if available
        if self.llm:
            ai_evaluation = self._ai_evaluate(influencer, metrics)
            metrics.update(ai_evaluation)
        
        return metrics
    
    def _calculate_metrics(self, influencer: Dict) -> Dict:
        """Calculate basic metrics"""
        # Outreach score (based on social media presence)
        social_platforms = sum([
            bool(influencer.get('linkedin_handle')),
            bool(influencer.get('twitter_handle')),
            bool(influencer.get('instagram_handle')),
            bool(influencer.get('youtube_handle')),
            bool(influencer.get('facebook_handle'))
        ])
        outreach_score = min(100, social_platforms * 20)
        
        # Reactions score (estimated from social presence)
        # In real implementation, would fetch actual data
        reactions_score = 70 if social_platforms >= 3 else 50
        
        # Views score (estimated)
        views_score = 65 if social_platforms >= 2 else 40
        
        # Engagement rate (estimated)
        engagement_rate = (outreach_score + reactions_score + views_score) / 3
        
        overall_score = (outreach_score + reactions_score + views_score) / 3
        
        return {
            "outreach_score": round(outreach_score, 2),
            "reactions_score": round(reactions_score, 2),
            "views_score": round(views_score, 2),
            "engagement_rate": round(engagement_rate, 2),
            "overall_score": round(overall_score, 2),
            "social_platforms_count": social_platforms,
            "metrics": {
                "linkedin": bool(influencer.get('linkedin_handle')),
                "twitter": bool(influencer.get('twitter_handle')),
                "instagram": bool(influencer.get('instagram_handle')),
                "youtube": bool(influencer.get('youtube_handle')),
                "facebook": bool(influencer.get('facebook_handle'))
            }
        }
    
    def _ai_evaluate(self, influencer: Dict, metrics: Dict) -> Dict:
        """Use AI to provide evaluation insights"""
        try:
            prompt = f"""Evaluate this influencer's potential:

Name: {influencer.get('full_name', '')}
Job Title: {influencer.get('job_title', '')}
Company: {influencer.get('company_name', '')}
Social Platforms: {metrics.get('social_platforms_count', 0)}

Provide:
1. Outreach potential (0-100)
2. Expected reaction rate
3. Expected view rate
4. Overall engagement potential

Return as JSON."""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            # Parse response
            return {"ai_insights": response.content}
        except:
            return {}
    
    def evaluate_batch(self, influencer_ids: List[str]) -> List[Dict]:
        """Evaluate multiple influencers"""
        evaluations = []
        for inf_id in influencer_ids:
            eval_result = self.evaluate(inf_id)
            eval_result['influencer_id'] = inf_id
            evaluations.append(eval_result)
        return evaluations


