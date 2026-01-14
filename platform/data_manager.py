#!/usr/bin/env python3
"""
Influencer Data Manager
Manages influencer data using ChatGPT API (no database or CSV)
"""

from typing import List, Dict, Optional
from chatgpt_influencer_finder import ChatGPTInfluencerFinder

class InfluencerDataManager:
    """Manage influencer data using ChatGPT API - no database or CSV needed"""
    
    def __init__(self):
        self.finder = ChatGPTInfluencerFinder()
        print("✅ Influencer Data Manager initialized (ChatGPT-based, no database)")
    
    def get_all_influencers(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Get influencers using ChatGPT API based on filters
        
        Args:
            filters: Optional filters dict (if None, returns empty list - need filters to find influencers)
        
        Returns:
            List of influencer dictionaries
        """
        if filters:
            return self.finder.find_influencers(filters, limit=50)
        return []
    
    def get_influencer_by_id(self, influencer_id: str, filters: Optional[Dict] = None) -> Optional[Dict]:
        """
        Get influencer by ID, email, or name
        
        Note: Since we use ChatGPT API, we need to search within recently found influencers.
        For best results, provide filters to find the influencer first.
        """
        influencers = self.get_all_influencers(filters)
        
        # Try by numeric ID
        try:
            idx = int(influencer_id) - 1
            if 0 <= idx < len(influencers):
                return influencers[idx]
        except:
            pass
        
        # Try by email
        for inf in influencers:
            if inf.get('email', '').lower() == influencer_id.lower():
                return inf
        
        # Try by name
        for inf in influencers:
            if inf.get('full_name', '').lower() == influencer_id.lower():
                return inf
        
        return None
    
    def get_filter_options(self) -> Dict:
        """Get available filter options (from ChatGPT finder)"""
        return self.finder.get_filter_options()

