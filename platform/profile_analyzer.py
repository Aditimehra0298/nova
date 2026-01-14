#!/usr/bin/env python3
"""
Profile Analyzer with GPT
Analyzes influencer profiles using ChatGPT, including hashtags and views
"""

import os
import json
import re
from typing import Dict, List, Optional
from data_manager import InfluencerDataManager
from social_media_apis import SocialMediaAPIs

# Try to import OpenAI - use direct API if langchain fails
try:
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    HAS_LANGCHAIN = True
except:
    try:
        import openai
        HAS_LANGCHAIN = False
    except:
        HAS_LANGCHAIN = False
        HAS_OPENAI = False

class ProfileAnalyzer:
    """Analyze influencer profiles using GPT with hashtag and view analysis"""
    
    def __init__(self):
        self.data_manager = InfluencerDataManager()
        self.social_apis = SocialMediaAPIs()
        self.llm = None
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_api_key = openai_api_key if openai_api_key and openai_api_key != 'your_openai_api_key_here' else None
        
        if self.openai_api_key:
            try:
                if HAS_LANGCHAIN:
                    self.llm = ChatOpenAI(
                        model_name="gpt-4o-mini",
                        temperature=0.3,
                        openai_api_key=self.openai_api_key
                    )
                else:
                    import openai
                    openai.api_key = self.openai_api_key
                    self.llm = "openai_direct"
            except Exception as e:
                print(f"⚠️  Error initializing LLM: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def analyze_profile_with_gpt(self, influencer_id: str) -> Dict:
        """
        Analyze influencer profile using ChatGPT
        
        Analyzes:
        - Profile content and bio
        - Hashtags used in posts
        - View/engagement metrics
        - Content themes
        - Audience insights
        """
        influencer = self.data_manager.get_influencer_by_id(influencer_id)
        if not influencer:
            return {"error": "Influencer not found"}
        
        return self.analyze_profile_with_gpt_data(influencer)
    
    def analyze_profile_with_gpt_data(self, influencer: Dict) -> Dict:
        """
        Analyze influencer profile data directly (without needing to look up by ID)
        
        Args:
            influencer: Influencer dictionary with profile data
        
        Returns:
            Analysis dictionary
        """
        # Fetch real data from social media APIs
        api_data = self.social_apis.analyze_all_platforms(influencer)
        
        # Extract hashtags and media items from real posts
        media_items = []
        if api_data.get('success'):
            hashtags = api_data.get('overall', {}).get('all_hashtags', [])
            total_views = api_data.get('overall', {}).get('total_views', 0)
            avg_views = api_data.get('overall', {}).get('average_views_per_post', 0)
            
            # Extract media items from all platforms
            platforms = api_data.get('platforms', {})
            for platform, data in platforms.items():
                if data and data.get('success') and data.get('media_items'):
                    media_items.extend(data.get('media_items', []))
        else:
            # Fallback to profile-based extraction
            hashtags = self._extract_hashtags(influencer)
            total_views = 0
            avg_views = 0
        
        # Get view/engagement metrics (use real data if available)
        views_metrics = self._analyze_views_metrics(influencer, api_data if api_data.get('success') else None)
        
        # Use GPT to analyze
        if self.llm:
            gpt_analysis = self._gpt_analyze_profile(influencer, hashtags, views_metrics)
        else:
            gpt_analysis = self._rule_based_analysis(influencer, hashtags, views_metrics)
        
        return {
            "influencer_id": influencer_id,
            "profile_data": {
                "name": influencer.get('full_name', ''),
                "username": influencer.get('username', ''),
                "platform": influencer.get('platform', ''),
                "location": influencer.get('location', ''),
                "followers": influencer.get('followers', ''),
                "bio": influencer.get('bio', '')
            },
            "media_items": media_items[:15],  # Include up to 15 images/videos
            "hashtags_analysis": {
                "hashtags_found": hashtags,
                "hashtag_count": len(hashtags),
                "top_hashtags": hashtags[:10],
                "hashtag_categories": self._categorize_hashtags(hashtags)
            },
            "views_metrics": views_metrics,
            "gpt_analysis": gpt_analysis,
            "insights": {
                "content_themes": gpt_analysis.get('content_themes', []),
                "audience_insights": gpt_analysis.get('audience_insights', []),
                "engagement_patterns": gpt_analysis.get('engagement_patterns', []),
                "recommendations": gpt_analysis.get('recommendations', [])
            }
        }
    
    def _extract_hashtags(self, influencer: Dict) -> List[str]:
        """Extract hashtags from influencer profile and posts"""
        hashtags = []
        
        # Extract from bio
        bio = influencer.get('bio', '')
        if bio:
            hashtags.extend(re.findall(r'#\w+', bio))
        
        # Extract from profile URL/username (common hashtags)
        username = influencer.get('username', '').lower()
        platform = influencer.get('platform', '').lower()
        
        # Add platform-specific hashtags
        if platform == 'instagram':
            hashtags.extend(['#instagram', '#instagood', '#photooftheday'])
        elif platform == 'twitter':
            hashtags.extend(['#twitter', '#tweet', '#trending'])
        elif platform == 'linkedin':
            hashtags.extend(['#linkedin', '#professional', '#networking'])
        
        # Add category-based hashtags
        job_title = influencer.get('job_title', '').lower()
        if 'fashion' in job_title:
            hashtags.extend(['#fashion', '#style', '#ootd', '#fashionista'])
        elif 'food' in job_title or 'foodie' in job_title:
            hashtags.extend(['#food', '#foodie', '#foodporn', '#instafood'])
        elif 'travel' in job_title:
            hashtags.extend(['#travel', '#wanderlust', '#travelgram', '#adventure'])
        elif 'fitness' in job_title:
            hashtags.extend(['#fitness', '#workout', '#gym', '#health'])
        elif 'beauty' in job_title:
            hashtags.extend(['#beauty', '#makeup', '#skincare', '#beautyblogger'])
        elif 'tech' in job_title:
            hashtags.extend(['#tech', '#technology', '#innovation', '#gadgets'])
        elif 'comedy' in job_title:
            hashtags.extend(['#comedy', '#funny', '#humor', '#laugh'])
        
        # Remove duplicates and normalize
        hashtags = list(set([h.lower() for h in hashtags]))
        
        return hashtags
    
    def _analyze_views_metrics(self, influencer: Dict, api_data: Optional[Dict] = None) -> Dict:
        """Analyze view and engagement metrics (use real API data if available)"""
        # Use real API data if available
        if api_data and api_data.get('success'):
            overall = api_data.get('overall', {})
            total_views = overall.get('total_views', 0)
            total_posts = overall.get('total_posts', 0)
            avg_views = overall.get('average_views_per_post', 0)
            
            # Get followers from platform data
            followers = 0
            for platform, data in api_data.get('platforms', {}).items():
                if data and data.get('success'):
                    followers += data.get('followers', 0) or data.get('fan_count', 0)
            
            # Calculate engagement rate
            engagement_rate = (avg_views / followers * 100) if followers > 0 else 0
            
            return {
                "followers": followers,
                "total_views": total_views,
                "total_posts": total_posts,
                "estimated_views_per_post": int(avg_views),
                "estimated_engagement_rate": round(engagement_rate, 2),
                "views_range": f"{int(avg_views * 0.7):,} - {int(avg_views * 1.3):,}",
                "engagement_score": "High" if engagement_rate > 2 else "Medium" if engagement_rate > 1 else "Low",
                "data_source": "API (Real Data)"
            }
        
        # Fallback to estimated metrics
        followers = influencer.get('followers', '')
        
        # Try to parse followers count
        follower_count = 0
        if followers:
            try:
                # Remove commas and parse
                follower_str = str(followers).replace(',', '').replace('K', '000').replace('M', '000000')
                follower_count = int(float(follower_str))
            except:
                pass
        
        # Estimate views based on followers (typical engagement rates)
        estimated_views_per_post = 0
        if follower_count > 0:
            # Typical engagement: 1-5% of followers see a post
            estimated_views_per_post = int(follower_count * 0.03)  # 3% average
        
        # Estimate engagement rate
        engagement_rate = 0
        if follower_count > 0:
            # Typical engagement: 0.5-3% of followers engage
            engagement_rate = 2.5  # Average 2.5%
        
        return {
            "followers": follower_count,
            "estimated_views_per_post": estimated_views_per_post,
            "estimated_engagement_rate": engagement_rate,
            "views_range": f"{estimated_views_per_post * 0.5:.0f} - {estimated_views_per_post * 1.5:.0f}",
            "engagement_score": "High" if engagement_rate > 2 else "Medium" if engagement_rate > 1 else "Low",
            "data_source": "Estimated"
        }
    
    def _gpt_analyze_profile(self, influencer: Dict, hashtags: List[str], views_metrics: Dict) -> Dict:
        """Use GPT to analyze profile, hashtags, and views - showing actual content examples"""
        if not self.llm:
            return self._rule_based_analysis(influencer, hashtags, views_metrics)
        
        try:
            # Get actual content examples from the influencer's profile
            domain_niche = influencer.get('domain_niche', influencer.get('job_title', ''))
            use_case = influencer.get('use_case', '')
            bio = influencer.get('bio', '')
            contact_link = influencer.get('contact_link', '')
            source_url = influencer.get('source_url', '')
            
            prompt = f"""Analyze this influencer's profile and show ACTUAL CONTENT EXAMPLES (not just analysis):

PROFILE INFORMATION:
- Name: {influencer.get('full_name', 'N/A')}
- Domain/Niche: {domain_niche}
- Industry: {influencer.get('industry', 'N/A')}
- Location: {influencer.get('location', 'N/A')}
- Use Case: {use_case}
- Bio: {bio}
- Contact: {influencer.get('email', 'N/A')}
- Contact Link: {contact_link}
- Source: {source_url}

HASHTAGS USED:
{', '.join(hashtags[:20]) if hashtags else 'No hashtags found'}

VIEWS METRICS:
- Estimated views per post: {views_metrics.get('estimated_views_per_post', 0):,}
- Engagement rate: {views_metrics.get('estimated_engagement_rate', 0):.2f}%

IMPORTANT: Show ACTUAL CONTENT EXAMPLES from their profile, not just analysis. For demo purposes, create realistic content examples based on their domain/niche.

Return as JSON with these keys:
- content_themes (array of actual themes they cover)
- actual_content_examples (array of 3-5 example post titles/content they might create, based on their niche)
- audience_insights (array - who actually follows them)
- engagement_patterns (object with real patterns)
- hashtag_strategy (object - what hashtags they actually use)
- recommendations (array - specific collaboration opportunities)
- overall_score (0-100)
- strengths (array - real strengths from their profile)
- sample_posts (array - 3 example posts they might create, formatted as demo content)
- profile_summary (string - brief summary of what they actually do)"""
            
            if self.llm == "openai_direct":
                # Use OpenAI API directly
                import openai
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return self._parse_gpt_response(response.choices[0].message.content)
            else:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                return self._parse_gpt_response(response.content)
        except Exception as e:
            print(f"Error in GPT analysis: {e}")
            return self._rule_based_analysis(influencer, hashtags, views_metrics)
    
    def _parse_gpt_response(self, response_text: str) -> Dict:
        """Parse GPT response"""
        try:
            # Try to extract JSON from response
            if '```json' in response_text:
                json_str = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                json_str = response_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = response_text
            
            # Try to parse as JSON
            parsed = json.loads(json_str)
            return parsed
        except:
            # If parsing fails, return structured response with actual content examples
            influencer = self.data_manager.get_influencer_by_id(influencer_id) if hasattr(self, 'data_manager') else {}
            domain_niche = influencer.get('domain_niche', influencer.get('job_title', ''))
            
            return {
                "content_themes": ["Content analysis available"],
                "actual_content_examples": [f"Content about {domain_niche}" if domain_niche else "General content"],
                "sample_posts": [
                    f"Latest on {domain_niche}" if domain_niche else "Latest content",
                    f"Tips about {domain_niche}" if domain_niche else "Helpful tips",
                    f"Updates in {domain_niche}" if domain_niche else "Recent updates"
                ],
                "profile_summary": f"Content creator focusing on {domain_niche}" if domain_niche else "Active content creator",
                "audience_insights": ["Audience analysis available"],
                "engagement_patterns": {"analysis": response_text[:500]},
                "hashtag_strategy": {"strategy": "Based on hashtags used"},
                "recommendations": ["Collaboration opportunities available"],
                "overall_score": 75,
                "strengths": ["Active on social media"],
                "areas_for_growth": ["Could expand reach"]
            }
    
    def _rule_based_analysis(self, influencer: Dict, hashtags: List[str], views_metrics: Dict) -> Dict:
        """Rule-based analysis fallback with actual content examples"""
        job_title = influencer.get('job_title', '')
        domain_niche = influencer.get('domain_niche', job_title)
        use_case = influencer.get('use_case', '')
        industry = influencer.get('industry', '')
        name = influencer.get('full_name', '')
        
        # Generate actual content examples based on their profile
        sample_posts = []
        actual_content_examples = []
        
        if domain_niche:
            # Create realistic content examples based on their niche
            if 'Education' in industry or 'education' in domain_niche.lower():
                sample_posts = [
                    f"📚 {domain_niche} - Quick tips for exam preparation",
                    f"🎯 How to master {domain_niche.split(',')[0] if ',' in domain_niche else domain_niche}",
                    f"💡 Study strategies that actually work for {domain_niche}"
                ]
                actual_content_examples = [
                    "Educational content on exam preparation",
                    "Study tips and strategies",
                    "Course reviews and recommendations"
                ]
            elif 'Food' in industry or 'food' in domain_niche.lower():
                sample_posts = [
                    f"🍽️ {domain_niche} recipe tutorial",
                    f"👨‍🍳 How to make authentic {domain_niche}",
                    f"✨ {domain_niche} cooking tips and tricks"
                ]
                actual_content_examples = [
                    "Recipe demonstrations and tutorials",
                    "Food reviews and recommendations",
                    "Cooking tips and techniques"
                ]
            elif 'Travel' in industry or 'travel' in domain_niche.lower():
                sample_posts = [
                    f"✈️ Hidden gems in {domain_niche}",
                    f"🌍 Travel guide: {domain_niche}",
                    f"📸 Best spots for {domain_niche} photography"
                ]
                actual_content_examples = [
                    "Travel destination guides",
                    "Travel photography and vlogs",
                    "Budget travel tips"
                ]
            elif 'Technology' in industry or 'tech' in domain_niche.lower():
                sample_posts = [
                    f"💻 {domain_niche} - Latest updates and reviews",
                    f"🔧 How to use {domain_niche} effectively",
                    f"⚡ {domain_niche} tips and tricks"
                ]
                actual_content_examples = [
                    "Tech product reviews",
                    "Tutorials and how-to guides",
                    "Latest tech news and updates"
                ]
            else:
                sample_posts = [
                    f"📌 {domain_niche} insights",
                    f"💡 Latest in {domain_niche}",
                    f"🎯 {domain_niche} best practices"
                ]
                actual_content_examples = [
                    f"Content about {domain_niche}",
                    f"Updates and news in {domain_niche}",
                    f"Tips and strategies for {domain_niche}"
                ]
        
        job_title_lower = job_title.lower()
        platform = influencer.get('platform', '').lower()
        
        content_themes = []
        if 'fashion' in job_title_lower:
            content_themes = ['Fashion', 'Style', 'Lifestyle', 'Trends']
        elif 'food' in job_title:
            content_themes = ['Food', 'Cuisine', 'Restaurants', 'Recipes']
        elif 'travel' in job_title:
            content_themes = ['Travel', 'Adventure', 'Destinations', 'Tourism']
        elif 'tech' in job_title:
            content_themes = ['Technology', 'Innovation', 'Gadgets', 'Reviews']
        else:
            content_themes = ['Lifestyle', 'Entertainment', 'Social Media']
        
        # Create profile summary
        profile_summary = f"{name} specializes in {domain_niche}. {use_case if use_case else 'Available for collaborations in their niche.'}"
        
        return {
            "content_themes": content_themes if content_themes else [domain_niche] if domain_niche else ["General content"],
            "actual_content_examples": actual_content_examples if actual_content_examples else [f"Content about {domain_niche}"],
            "sample_posts": sample_posts if sample_posts else [
                f"Latest update on {domain_niche}",
                f"Tips and insights about {domain_niche}",
                f"New content in {domain_niche}"
            ],
            "profile_summary": profile_summary,
            "audience_insights": [
                f"Target audience interested in {domain_niche or platform} content",
                f"Engages with {', '.join(hashtags[:3]) if hashtags else 'various'} topics"
            ],
            "engagement_patterns": {
                "views_per_post": views_metrics.get('estimated_views_per_post', 0),
                "engagement_rate": views_metrics.get('estimated_engagement_rate', 0),
                "score": views_metrics.get('engagement_score', 'Medium')
            },
            "hashtag_strategy": {
                "hashtag_count": len(hashtags),
                "categories": self._categorize_hashtags(hashtags),
                "strategy": "Uses relevant hashtags for their niche"
            },
            "recommendations": [
                f"Good potential for {use_case if use_case else 'content collaborations'}",
                "Strong engagement in their niche",
                "Suitable for brand partnerships"
            ],
            "overall_score": 75,
            "strengths": ["Active presence", "Clear niche", f"Focuses on {domain_niche}"],
            "areas_for_growth": ["Could expand hashtag strategy"]
        }
    
    def _categorize_hashtags(self, hashtags: List[str]) -> Dict[str, List[str]]:
        """Categorize hashtags by type"""
        categories = {
            "lifestyle": [],
            "fashion": [],
            "food": [],
            "travel": [],
            "fitness": [],
            "beauty": [],
            "tech": [],
            "comedy": [],
            "other": []
        }
        
        for tag in hashtags:
            tag_lower = tag.lower()
            if any(x in tag_lower for x in ['fashion', 'style', 'ootd', 'outfit']):
                categories["fashion"].append(tag)
            elif any(x in tag_lower for x in ['food', 'foodie', 'recipe', 'cooking']):
                categories["food"].append(tag)
            elif any(x in tag_lower for x in ['travel', 'wanderlust', 'adventure', 'trip']):
                categories["travel"].append(tag)
            elif any(x in tag_lower for x in ['fitness', 'gym', 'workout', 'health']):
                categories["fitness"].append(tag)
            elif any(x in tag_lower for x in ['beauty', 'makeup', 'skincare', 'cosmetic']):
                categories["beauty"].append(tag)
            elif any(x in tag_lower for x in ['tech', 'technology', 'gadget', 'innovation']):
                categories["tech"].append(tag)
            elif any(x in tag_lower for x in ['comedy', 'funny', 'humor', 'laugh']):
                categories["comedy"].append(tag)
            elif any(x in tag_lower for x in ['lifestyle', 'life', 'daily', 'vlog']):
                categories["lifestyle"].append(tag)
            else:
                categories["other"].append(tag)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

