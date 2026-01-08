#!/usr/bin/env python3
"""
Social Media API Integrations
Fetches real data from Instagram, LinkedIn, Twitter, and Facebook APIs
"""

import os
import requests
from typing import Dict, List, Optional
import json

class SocialMediaAPIs:
    """Integrate with social media APIs to fetch real profile data"""
    
    def __init__(self):
        # API Keys from environment
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    def analyze_instagram_profile(self, username: str) -> Dict:
        """Analyze Instagram profile using Instagram Graph API"""
        try:
            if not self.instagram_token:
                return {"success": False, "error": "Instagram token not configured"}
            
            # Remove @ if present and clean username
            username = username.lstrip('@').strip()
            if not username:
                return {"success": False, "error": "Instagram username is required"}
            
            print(f"🔍 Fetching Instagram profile for: {username}")
            
            # Instagram Graph API - Try to get user by username
            # Note: Instagram Graph API requires the username to be associated with a Business/Creator account
            # First, try to get user ID from username using Instagram Basic Display API or Graph API
            
            # Method 1: Try Instagram Graph API with username
            # This works if the token has permissions to access the user
            url = f"https://graph.instagram.com/{username}"
            params = {
                'fields': 'id,username,account_type,media_count,followers_count,follows_count',
                'access_token': self.instagram_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # If that fails, try alternative methods
            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                print(f"⚠️  Instagram API Error for {username}: {error_msg}")
                
                # Try alternative: Use Instagram Basic Display API endpoint
                # This might work if the token is a user access token
                alt_url = f"https://graph.instagram.com/me"
                alt_params = {'fields': 'id,username', 'access_token': self.instagram_token}
                alt_response = requests.get(alt_url, params=alt_params, timeout=10)
                
                if alt_response.status_code == 200:
                    # Token is valid but can't access other users - return partial data
                    return {"success": False, "error": f"Cannot access user {username}. Token may only have access to own account."}
                else:
                    return {"success": False, "error": f"Instagram API Error: {error_msg}. Username '{username}' may not exist or token lacks permissions."}
            
            if response.status_code == 200:
                profile_data = response.json()
                
                # Get recent media with media URLs
                media_url = f"https://graph.instagram.com/{profile_data.get('id')}/media"
                media_params = {
                    'fields': 'id,caption,like_count,comments_count,timestamp,media_type,permalink,media_url,thumbnail_url',
                    'access_token': self.instagram_token,
                    'limit': 25
                }
                
                media_response = requests.get(media_url, params=media_params, timeout=10)
                posts = []
                media_items = []  # Store actual images/videos
                hashtags = []
                total_views = 0
                total_likes = 0
                
                if media_response.status_code == 200:
                    media_data = media_response.json()
                    posts = media_data.get('data', [])
                    
                    for post in posts:
                        caption = post.get('caption', '')
                        if caption:
                            # Extract hashtags
                            import re
                            hashtags.extend(re.findall(r'#\w+', caption))
                        
                        # Get media URL (image or video)
                        media_url_item = post.get('media_url') or post.get('thumbnail_url')
                        if media_url_item:
                            media_items.append({
                                'url': media_url_item,
                                'type': post.get('media_type', 'IMAGE'),
                                'caption': caption[:100] if caption else '',
                                'likes': post.get('like_count', 0),
                                'comments': post.get('comments_count', 0),
                                'permalink': post.get('permalink', '')
                            })
                        
                        # Get view count (for videos)
                        if post.get('media_type') == 'VIDEO':
                            media_id = post.get('id')
                            insights_url = f"https://graph.instagram.com/{media_id}/insights"
                            insights_params = {
                                'metric': 'impressions,reach',
                                'access_token': self.instagram_token
                            }
                            insights_response = requests.get(insights_url, params=insights_params, timeout=10)
                            if insights_response.status_code == 200:
                                insights = insights_response.json()
                                total_views += insights.get('data', [{}])[0].get('values', [{}])[0].get('value', 0)
                        
                        total_likes += post.get('like_count', 0)
                
                return {
                    "success": True,
                    "platform": "instagram",
                    "username": username,
                    "followers": profile_data.get('followers_count', 0),
                    "posts_count": len(posts),
                    "hashtags": list(set(hashtags)),
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "average_views": total_views / len(posts) if posts else 0,
                    "average_likes": total_likes / len(posts) if posts else 0,
                    "recent_posts": posts[:10],
                    "media_items": media_items[:12]  # Return up to 12 images/videos
                }
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_twitter_profile(self, username: str) -> Dict:
        """Analyze Twitter/X profile using Twitter API v2"""
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            # Get user ID
            user_url = f"https://api.twitter.com/2/users/by/username/{username}"
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer}'
            }
            
            user_response = requests.get(user_url, headers=headers, timeout=10)
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                user_id = user_data.get('data', {}).get('id')
                
                if not user_id:
                    return {"success": False, "error": "User not found"}
                
                # Get user details
                user_details_url = f"https://api.twitter.com/2/users/{user_id}"
                user_details_params = {
                    'user.fields': 'public_metrics,description,created_at'
                }
                user_details_response = requests.get(user_details_url, headers=headers, params=user_details_params, timeout=10)
                
                user_info = user_details_response.json().get('data', {})
                metrics = user_info.get('public_metrics', {})
                
                # Get recent tweets
                tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
                tweets_params = {
                    'max_results': 25,
                    'tweet.fields': 'public_metrics,created_at,text',
                    'expansions': 'author_id'
                }
                tweets_response = requests.get(tweets_url, headers=headers, params=tweets_params, timeout=10)
                
                tweets = []
                hashtags = []
                total_views = 0
                total_likes = 0
                total_retweets = 0
                
                if tweets_response.status_code == 200:
                    tweets_data = tweets_response.json()
                    tweets = tweets_data.get('data', [])
                    
                    for tweet in tweets:
                        text = tweet.get('text', '')
                        if text:
                            import re
                            hashtags.extend(re.findall(r'#\w+', text))
                        
                        tweet_metrics = tweet.get('public_metrics', {})
                        total_views += tweet_metrics.get('impression_count', 0)
                        total_likes += tweet_metrics.get('like_count', 0)
                        total_retweets += tweet_metrics.get('retweet_count', 0)
                
                return {
                    "success": True,
                    "platform": "twitter",
                    "username": username,
                    "followers": metrics.get('followers_count', 0),
                    "tweets_count": len(tweets),
                    "hashtags": list(set(hashtags)),
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_retweets": total_retweets,
                    "average_views": total_views / len(tweets) if tweets else 0,
                    "average_likes": total_likes / len(tweets) if tweets else 0,
                    "recent_tweets": tweets[:10]
                }
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_linkedin_profile(self, username: str) -> Dict:
        """Analyze LinkedIn profile using LinkedIn API"""
        try:
            # LinkedIn API endpoint
            url = f"https://api.linkedin.com/v2/people/(vanityName:{username})"
            headers = {
                'Authorization': f'Bearer {self.linkedin_token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            params = {
                'projection': '(id,firstName,lastName,headline,summary,location,profilePicture(displayImage~:playableStreams))'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                profile_data = response.json()
                
                # Get posts (activity)
                posts_url = "https://api.linkedin.com/v2/ugcPosts"
                posts_params = {
                    'q': 'authors',
                    'authors': f"List({profile_data.get('id')})"
                }
                posts_response = requests.get(posts_url, headers=headers, params=posts_params, timeout=10)
                
                posts = []
                hashtags = []
                total_views = 0
                
                if posts_response.status_code == 200:
                    posts_data = posts_response.json()
                    posts = posts_data.get('elements', [])
                    
                    for post in posts:
                        text = post.get('specificContent', {}).get('shareContent', {}).get('text', {}).get('text', '')
                        if text:
                            import re
                            hashtags.extend(re.findall(r'#\w+', text))
                        
                        # Get view count
                        stats = post.get('distribution', {}).get('linkedInDistributionTarget', {}).get('viewCount', 0)
                        total_views += stats
                
                return {
                    "success": True,
                    "platform": "linkedin",
                    "username": username,
                    "headline": profile_data.get('headline', ''),
                    "posts_count": len(posts),
                    "hashtags": list(set(hashtags)),
                    "total_views": total_views,
                    "average_views": total_views / len(posts) if posts else 0,
                    "recent_posts": posts[:10]
                }
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_facebook_profile(self, page_id: str) -> Dict:
        """Analyze Facebook page using Facebook Graph API"""
        try:
            # Facebook Graph API endpoint
            url = f"https://graph.facebook.com/v18.0/{page_id}"
            params = {
                'fields': 'id,name,fan_count,posts.limit(25){message,created_time,likes.summary(true),comments.summary(true),shares}',
                'access_token': self.facebook_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                page_data = response.json()
                posts = page_data.get('posts', {}).get('data', [])
                
                hashtags = []
                total_views = 0
                total_likes = 0
                total_comments = 0
                total_shares = 0
                
                for post in posts:
                    message = post.get('message', '')
                    if message:
                        import re
                        hashtags.extend(re.findall(r'#\w+', message))
                    
                    likes = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                    comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                    shares = post.get('shares', {}).get('count', 0)
                    
                    total_likes += likes
                    total_comments += comments
                    total_shares += shares
                    total_views += likes + comments + shares  # Estimate views
                
                return {
                    "success": True,
                    "platform": "facebook",
                    "page_id": page_id,
                    "name": page_data.get('name', ''),
                    "followers": page_data.get('fan_count', 0),
                    "posts_count": len(posts),
                    "hashtags": list(set(hashtags)),
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "total_shares": total_shares,
                    "average_views": total_views / len(posts) if posts else 0,
                    "recent_posts": posts[:10]
                }
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_all_platforms(self, influencer_data: Dict) -> Dict:
        """Analyze influencer across all platforms"""
        results = {
            "instagram": None,
            "twitter": None,
            "linkedin": None,
            "facebook": None
        }
        
        # Analyze Instagram
        if influencer_data.get('instagram_handle'):
            results['instagram'] = self.analyze_instagram_profile(influencer_data['instagram_handle'])
        
        # Analyze Twitter
        if influencer_data.get('twitter_handle'):
            results['twitter'] = self.analyze_twitter_profile(influencer_data['twitter_handle'])
        
        # Analyze LinkedIn
        if influencer_data.get('linkedin_handle'):
            results['linkedin'] = self.analyze_linkedin_profile(influencer_data['linkedin_handle'])
        
        # Analyze Facebook
        if influencer_data.get('facebook_handle'):
            results['facebook'] = self.analyze_facebook_profile(influencer_data['facebook_handle'])
        
        # Calculate overall metrics
        all_hashtags = []
        total_views = 0
        total_posts = 0
        
        for platform, data in results.items():
            if data and data.get('success'):
                all_hashtags.extend(data.get('hashtags', []))
                total_views += data.get('total_views', 0)
                total_posts += data.get('posts_count', 0) or data.get('tweets_count', 0)
        
        return {
            "success": True,
            "platforms": results,
            "overall": {
                "total_views": total_views,
                "total_posts": total_posts,
                "average_views_per_post": total_views / total_posts if total_posts > 0 else 0,
                "all_hashtags": list(set(all_hashtags)),
                "hashtag_count": len(set(all_hashtags))
            }
        }


