#!/usr/bin/env python3
"""
Platform Manager
Manages different social media platforms and allows adding new ones
"""

import json
import os
from typing import List, Dict, Optional

class PlatformManager:
    """Manage social media platforms"""
    
    PLATFORMS_FILE = 'platforms.json'
    
    DEFAULT_PLATFORMS = [
        {
            "id": "linkedin",
            "name": "LinkedIn",
            "domain": "linkedin.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 100
            }
        },
        {
            "id": "twitter",
            "name": "Twitter/X",
            "domain": "twitter.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 100
            }
        },
        {
            "id": "instagram",
            "name": "Instagram",
            "domain": "instagram.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 50
            }
        },
        {
            "id": "youtube",
            "name": "YouTube",
            "domain": "youtube.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 100
            }
        },
        {
            "id": "tiktok",
            "name": "TikTok",
            "domain": "tiktok.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 50
            }
        },
        {
            "id": "facebook",
            "name": "Facebook",
            "domain": "facebook.com",
            "api_endpoint": None,
            "config": {
                "requires_auth": True,
                "rate_limit": 100
            }
        }
    ]
    
    def __init__(self):
        self.platforms = self._load_platforms()
    
    def _load_platforms(self) -> List[Dict]:
        """Load platforms from file or use defaults"""
        if os.path.exists(self.PLATFORMS_FILE):
            try:
                with open(self.PLATFORMS_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Save defaults
        self._save_platforms(self.DEFAULT_PLATFORMS)
        return self.DEFAULT_PLATFORMS
    
    def _save_platforms(self, platforms: List[Dict]):
        """Save platforms to file"""
        with open(self.PLATFORMS_FILE, 'w') as f:
            json.dump(platforms, f, indent=2)
    
    def get_all_platforms(self) -> List[Dict]:
        """Get all platforms"""
        return self.platforms
    
    def get_platform(self, platform_id: str) -> Optional[Dict]:
        """Get platform by ID"""
        for platform in self.platforms:
            if platform.get('id') == platform_id:
                return platform
        return None
    
    def add_platform(self, name: str, domain: str, api_endpoint: Optional[str] = None,
                    config: Dict = None) -> Dict:
        """Add new platform from backend"""
        platform_id = name.lower().replace(' ', '_')
        
        new_platform = {
            "id": platform_id,
            "name": name,
            "domain": domain,
            "api_endpoint": api_endpoint,
            "config": config or {}
        }
        
        # Check if exists
        existing = self.get_platform(platform_id)
        if existing:
            # Update existing
            for i, p in enumerate(self.platforms):
                if p.get('id') == platform_id:
                    self.platforms[i] = new_platform
                    break
        else:
            # Add new
            self.platforms.append(new_platform)
        
        self._save_platforms(self.platforms)
        return new_platform


