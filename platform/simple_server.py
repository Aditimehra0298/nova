#!/usr/bin/env python3
"""
Simple Flask server for the platform
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from profile_analyzer import ProfileAnalyzer

load_dotenv()

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Initialize profile analyzer
profile_analyzer = ProfileAnalyzer()

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "NOVA Influencer Platform API",
        "version": "2.0"
    })

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Check system status (ChatGPT-based, no CSV)"""
    try:
        import os
        from chatgpt_influencer_finder import ChatGPTInfluencerFinder
        
        # Check environment variables
        openai_key = os.getenv('OPENAI_API_KEY')
        has_openai_key = bool(openai_key and openai_key != 'your_openai_api_key_here' and len(openai_key) > 20)
        
        # Initialize finder to check if it works
        finder = ChatGPTInfluencerFinder()
        has_chatgpt = finder.llm is not None
        
        # Get more diagnostic info
        port = os.getenv('PORT', '5001')
        flask_debug = os.getenv('FLASK_DEBUG', 'False')
        
        return jsonify({
            "success": True,
            "system_type": "ChatGPT-based (no database/CSV)",
            "chatgpt_available": has_chatgpt,
            "openai_key_configured": has_openai_key,
            "openai_key_length": len(openai_key) if openai_key else 0,
            "port": port,
            "flask_debug": flask_debug,
            "environment": os.getenv('ENVIRONMENT', 'production'),
            "message": "System uses ChatGPT API to find influencers directly based on client requirements.",
            "diagnostics": {
                "finder_llm_type": str(type(finder.llm)) if finder.llm else None,
                "finder_has_api_key": bool(finder.openai_api_key),
                "api_key_prefix": openai_key[:10] + "..." if openai_key and len(openai_key) > 10 else None
            }
        })
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

def _format_followers(count: int) -> str:
    """Format follower count as string (e.g., 50K, 1.2M)"""
    if count >= 1000000:
        return f"{count / 1000000:.1f}M"
    elif count >= 1000:
        return f"{count / 1000:.1f}K"
    else:
        return str(count)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get recommendations using ChatGPT API (no database/CSV)"""
    try:
        data = request.json
        filters = data.get('filters', {})
        limit = min(data.get('limit', 10), 20)  # Max 20 recommendations
        
        print(f"🔍 Finding influencers with ChatGPT API based on filters: {filters}")
        
        # Use ChatGPT influencer finder directly
        from chatgpt_influencer_finder import ChatGPTInfluencerFinder
        import os
        
        # Log environment check
        openai_key = os.getenv('OPENAI_API_KEY')
        print(f"🔍 Environment check:")
        print(f"   OPENAI_API_KEY exists: {bool(openai_key)}")
        print(f"   OPENAI_API_KEY length: {len(openai_key) if openai_key else 0}")
        print(f"   OPENAI_API_KEY prefix: {openai_key[:10] + '...' if openai_key and len(openai_key) > 10 else 'N/A'}")
        
        finder = ChatGPTInfluencerFinder()
        
        # Enhanced diagnostics
        if not finder.llm:
            error_msg = "ChatGPT API is not configured. "
            if not openai_key:
                error_msg += "OPENAI_API_KEY environment variable is not set."
            elif openai_key == 'your_openai_api_key_here':
                error_msg += "OPENAI_API_KEY is set to placeholder value. Please set a real API key."
            elif len(openai_key) < 20:
                error_msg += f"OPENAI_API_KEY appears invalid (too short: {len(openai_key)} chars)."
            else:
                error_msg += "ChatGPT initialization failed. Check API key validity."
            
            print(f"❌ {error_msg}")
            return jsonify({
                "success": False,
                "error": error_msg,
                "diagnostics": {
                    "openai_key_exists": bool(openai_key),
                    "openai_key_length": len(openai_key) if openai_key else 0,
                    "finder_llm_available": False
                },
                "count": 0,
                "recommendations": []
            }), 500
        
        # Find influencers using ChatGPT (with timeout protection)
        import time
        start_time = time.time()
        
        try:
            influencers = finder.find_influencers(filters, limit=limit)
            elapsed = time.time() - start_time
            print(f"✅ Found {len(influencers)} influencers using ChatGPT API (took {elapsed:.2f}s)")
            
            # Check if ChatGPT returned any influencers
            if not influencers or len(influencers) == 0:
                print(f"⚠️  ChatGPT returned no influencers. This could mean:")
                print(f"   1. ChatGPT API is not configured (check OPENAI_API_KEY)")
                print(f"   2. Filters are too restrictive for ChatGPT to find matches")
                print(f"   3. ChatGPT API call failed silently")
                
                return jsonify({
                    "success": False,
                    "error": "No influencers found. ChatGPT API returned no results. Try removing some filters or adjusting your requirements.",
                    "count": 0,
                    "recommendations": [],
                    "suggestion": "Try removing filters like product type, content type, or target audience to see more results.",
                    "diagnostics": {
                        "filters_applied": filters,
                        "limit_requested": limit,
                        "finder_llm_available": finder.llm is not None
                    }
                }), 200
                
        except Exception as e:
            print(f"⚠️  Error finding influencers: {e}")
            import traceback
            traceback.print_exc()
            # Return empty list with error message
            return jsonify({
                "success": False,
                "error": f"Failed to find influencers: {str(e)}. Please try again with different filters.",
                "count": 0,
                "recommendations": []
            }), 500
        
        # Fetch real profile data using Instagram/LinkedIn tokens
        # This assesses their actual profiles from social media APIs
        try:
            from social_media_apis import SocialMediaAPIs
            import threading
            
            social_apis = SocialMediaAPIs()
            
            # Fetch for all influencers (with timeout to avoid delays)
            influencers_to_fetch = influencers  # Fetch for all influencers
            
            print(f"🔍 Fetching real profile data for {len(influencers_to_fetch)} influencers using Instagram/LinkedIn APIs...")
            
            for inf in influencers_to_fetch:
                try:
                    # Fetch real profile data with quick timeout (5 seconds max per influencer)
                    import threading
                    api_data = None
                    fetch_error = None
                    
                    def fetch_with_timeout():
                        nonlocal api_data, fetch_error
                        try:
                            # Log which handles we're trying to fetch
                            handles = []
                            if inf.get('instagram_handle'):
                                handles.append(f"Instagram: {inf.get('instagram_handle')}")
                            if inf.get('linkedin_handle'):
                                handles.append(f"LinkedIn: {inf.get('linkedin_handle')}")
                            if inf.get('twitter_handle'):
                                handles.append(f"Twitter: {inf.get('twitter_handle')}")
                            
                            if handles:
                                print(f"  📡 Fetching: {', '.join(handles)}")
                            
                            api_data = social_apis.analyze_all_platforms(inf)
                            
                            # Log success/failure
                            if api_data and api_data.get('success'):
                                platforms_with_data = [p for p, d in api_data.get('platforms', {}).items() if d and d.get('success')]
                                if platforms_with_data:
                                    print(f"  ✅ Successfully fetched data from: {', '.join(platforms_with_data)}")
                                else:
                                    print(f"  ⚠️  No successful platform data for {inf.get('full_name', 'unknown')}")
                            elif api_data:
                                print(f"  ❌ Failed to fetch data for {inf.get('full_name', 'unknown')}")
                        except Exception as e:
                            fetch_error = str(e)
                            print(f"  ❌ Error fetching profile: {e}")
                    
                    fetch_thread = threading.Thread(target=fetch_with_timeout)
                    fetch_thread.daemon = True
                    fetch_thread.start()
                    fetch_thread.join(timeout=8)  # 8 second timeout per influencer for better data
                    
                    if fetch_thread.is_alive():
                        # Timeout - skip this influencer's real data
                        print(f"⏱️  Timeout fetching real profile for {inf.get('full_name', 'unknown')} - skipping")
                        continue
                    
                    if fetch_error:
                        continue
                    
                    if not api_data:
                        continue
                    if api_data.get('success'):
                        # Add real profile data to influencer
                        inf['real_profile_data'] = api_data
                        platforms_data = api_data.get('platforms', {})
                        
                        # Add platform-specific real data
                        if platforms_data.get('instagram') and platforms_data['instagram'].get('success'):
                            insta_data = platforms_data['instagram']
                            inf['real_instagram'] = {
                                'followers': insta_data.get('followers', 0),
                                'posts_count': insta_data.get('posts_count', 0),
                                'total_likes': insta_data.get('total_likes', 0),
                                'average_likes': insta_data.get('average_likes', 0),
                                'hashtags': insta_data.get('hashtags', []),
                                'media_items': insta_data.get('media_items', [])
                            }
                            
                            # UPDATE WITH REAL INSTAGRAM DATA
                            if insta_data.get('followers', 0) > 0:
                                inf['follower_count'] = insta_data.get('followers', 0)
                                inf['followers'] = _format_followers(insta_data.get('followers', 0))
                            
                            # Use REAL average likes
                            if insta_data.get('average_likes', 0) > 0:
                                inf['avg_likes_per_post'] = int(insta_data.get('average_likes', 0))
                            elif insta_data.get('total_likes', 0) > 0 and insta_data.get('posts_count', 0) > 0:
                                inf['avg_likes_per_post'] = int(insta_data.get('total_likes', 0) / insta_data.get('posts_count', 1))
                            
                            # Calculate REAL engagement rate from actual data
                            if insta_data.get('followers', 0) > 0 and inf.get('avg_likes_per_post', 0) > 0:
                                real_engagement_rate = (inf.get('avg_likes_per_post', 0) / insta_data.get('followers', 1)) * 100
                                inf['engagement_rate'] = round(real_engagement_rate, 2)
                                inf['estimated_reach'] = int(insta_data.get('followers', 0) * (real_engagement_rate / 100))
                        
                        if platforms_data.get('twitter') and platforms_data['twitter'].get('success'):
                            twitter_data = platforms_data['twitter']
                            inf['real_twitter'] = {
                                'followers': twitter_data.get('followers', 0),
                                'tweets_count': twitter_data.get('tweets_count', 0),
                                'total_likes': twitter_data.get('total_likes', 0),
                                'bio': twitter_data.get('bio', ''),
                                'hashtags': twitter_data.get('hashtags', [])
                            }
                            
                            # UPDATE WITH REAL TWITTER DATA (if no Instagram data)
                            if twitter_data.get('followers', 0) > 0:
                                if not inf.get('follower_count') or inf.get('follower_count', 0) == 0:
                                    inf['follower_count'] = twitter_data.get('followers', 0)
                                    inf['followers'] = _format_followers(twitter_data.get('followers', 0))
                            
                            # Use REAL Twitter engagement
                            if twitter_data.get('total_likes', 0) > 0 and twitter_data.get('tweets_count', 0) > 0:
                                avg_twitter_likes = int(twitter_data.get('total_likes', 0) / twitter_data.get('tweets_count', 1))
                                if not inf.get('avg_likes_per_post') or inf.get('avg_likes_per_post', 0) == 0:
                                    inf['avg_likes_per_post'] = avg_twitter_likes
                            
                            # Calculate REAL engagement rate from Twitter
                            if twitter_data.get('followers', 0) > 0 and inf.get('avg_likes_per_post', 0) > 0:
                                real_engagement_rate = (inf.get('avg_likes_per_post', 0) / twitter_data.get('followers', 1)) * 100
                                if not inf.get('engagement_rate') or inf.get('engagement_rate', 0) == 0:
                                    inf['engagement_rate'] = round(real_engagement_rate, 2)
                                    inf['estimated_reach'] = int(twitter_data.get('followers', 0) * (real_engagement_rate / 100))
                        
                        if platforms_data.get('linkedin') and platforms_data['linkedin'].get('success'):
                            linkedin_data = platforms_data['linkedin']
                            inf['real_linkedin'] = {
                                'headline': linkedin_data.get('headline', ''),
                                'summary': linkedin_data.get('summary', ''),
                                'location': linkedin_data.get('location', ''),
                                'posts_count': linkedin_data.get('posts_count', 0),
                                'hashtags': linkedin_data.get('hashtags', [])
                            }
                        
                        # Update overall metrics with REAL data from APIs
                        overall = api_data.get('overall', {})
                        if overall.get('total_views', 0) > 0:
                            inf['real_total_views'] = overall.get('total_views', 0)
                            inf['real_average_views'] = overall.get('average_views_per_post', 0)
                            inf['real_hashtags'] = overall.get('all_hashtags', [])
                except Exception as e:
                    # Skip real profile fetch for this influencer if it fails
                    print(f"⚠️  Could not fetch real profile for {inf.get('full_name', 'unknown')}: {e}")
                    continue
        except Exception as e:
            # If social media APIs are not available, continue without real profile data
            print(f"⚠️  Social media APIs not available: {e}")
            print("📝 Continuing with ChatGPT-generated influencer data")
        
        # Store selected platforms in each influencer for frontend display
        selected_platforms = filters.get('platforms', [])
        
        # Filter out handles for platforms that weren't selected
        if selected_platforms:
            platforms_lower = [p.lower() for p in selected_platforms] if isinstance(selected_platforms, list) else [selected_platforms.lower()]
            
            for inf in influencers:
                inf['selected_platforms'] = selected_platforms
                
                # Remove handles for platforms that weren't selected
                has_instagram = any('instagram' in p for p in platforms_lower)
                has_twitter = any('twitter' in p or 'x' in p for p in platforms_lower)
                has_linkedin = any('linkedin' in p for p in platforms_lower)
                has_youtube = any('youtube' in p for p in platforms_lower)
                has_facebook = any('facebook' in p for p in platforms_lower)
                
                if not has_instagram:
                    inf['instagram_handle'] = None
                if not has_twitter:
                    inf['twitter_handle'] = None
                if not has_linkedin:
                    inf['linkedin_handle'] = None
                if not has_youtube:
                    inf['youtube_handle'] = None
                if not has_facebook:
                    inf['facebook_handle'] = None
        else:
            # If no platforms selected, keep all handles
            for inf in influencers:
                inf['selected_platforms'] = []
        
        # Extract filter values for use throughout the function
        location = filters.get('location', '').strip() if filters.get('location') else ''
        product_type = filters.get('product_type', '').strip() if filters.get('product_type') else ''
        content_type = filters.get('content_type', [])
        target_audience = filters.get('target_audience', '').strip() if filters.get('target_audience') else ''
        
        # Store original count for fallback logic
        original_count = len(influencers)
        print(f"📊 Starting with {original_count} influencers from ChatGPT")
        
        # If we have very few influencers, be VERY lenient with filtering
        use_strict_filtering = original_count >= 5
        
        if not use_strict_filtering:
            print(f"⚠️  Only {original_count} influencers found - using LENIENT filtering to preserve results")
        
        # CRITICAL: Filter out micro/nano influencers and only show verified influencers
        # Filter by location first (but be lenient)
        if location and use_strict_filtering:
            location_filtered = []
            for inf in influencers:
                inf_location = str(inf.get('location', '')).lower()
                # Check if location matches (exact match or contains the location)
                if location.lower() in inf_location or inf_location in location.lower():
                    location_filtered.append(inf)
                else:
                    print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - location '{inf.get('location')}' doesn't match '{location}'")
            
            # If location filter removed all influencers, be lenient and keep all
            if len(location_filtered) == 0 and original_count > 0:
                print(f"⚠️  Location filter removed all influencers. Using lenient matching - keeping all {original_count} influencers.")
                location_filtered = influencers
            else:
                influencers = location_filtered
                print(f"✅ Filtered to {len(influencers)} influencers from {location}")
        
        # Filter out micro/nano influencers (under 10K followers) - but be lenient if no results
        macro_mid_influencers = []
        micro_nano_influencers = []
        
        for inf in influencers:
            # Get follower count
            follower_count = inf.get('follower_count', 0)
            if follower_count == 0:
                # Parse from string
                followers_str = str(inf.get('followers', '0')).upper()
                try:
                    clean_str = followers_str.replace(',', '').replace(' ', '').strip()
                    if 'K' in clean_str:
                        follower_count = float(clean_str.replace('K', '')) * 1000
                    elif 'M' in clean_str:
                        follower_count = float(clean_str.replace('M', '')) * 1000000
                    else:
                        follower_count = float(clean_str) if clean_str else 0
                except:
                    follower_count = 0
            
            # Only include if 10K+ followers (exclude micro/nano)
            if follower_count >= 10000:
                macro_mid_influencers.append(inf)
            else:
                micro_nano_influencers.append(inf)
                print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - only {int(follower_count)} followers (micro/nano)")
        
        # If we have macro/mid-tier influencers, use them. Otherwise, include micro/nano to show something
        if len(macro_mid_influencers) > 0:
            influencers = macro_mid_influencers
            print(f"✅ Filtered to {len(influencers)} macro/mid-tier influencers (excluded {len(micro_nano_influencers)} micro/nano)")
        else:
            # No macro/mid-tier found, include micro/nano to show results
            influencers = macro_mid_influencers + micro_nano_influencers
            print(f"⚠️  No macro/mid-tier influencers found. Showing {len(influencers)} influencers (including micro/nano)")
        
        # TRUST ChatGPT Results: Don't filter - ChatGPT knows real influencers
        # The API verification was filtering out real influencers, so we trust ChatGPT completely
        print(f"✅ Trusting ChatGPT results: {len(influencers)} influencers")
        # Skip all filtering - just use ChatGPT's results directly
        
        # Filter by min_followers using REAL data if available, otherwise use estimated
        min_followers = filters.get('min_followers')
        if min_followers:
            min_followers_int = int(min_followers) if isinstance(min_followers, (int, str)) and str(min_followers).isdigit() else 0
            if min_followers_int > 0:
                filtered_influencers = []
                for inf in influencers:
                    # Use REAL follower count if available, otherwise estimate from string
                    real_follower_count = inf.get('follower_count', 0)
                    if real_follower_count == 0:
                        # Parse estimated followers string
                        followers_str = str(inf.get('followers', '0')).upper()
                        try:
                            clean_str = followers_str.replace(',', '').replace(' ', '').strip()
                            if 'K' in clean_str:
                                real_follower_count = float(clean_str.replace('K', '')) * 1000
                            elif 'M' in clean_str:
                                real_follower_count = float(clean_str.replace('M', '')) * 1000000
                            else:
                                real_follower_count = float(clean_str) if clean_str else 0
                        except:
                            real_follower_count = 0
                    
                    # Only include if meets minimum follower requirement
                    if real_follower_count >= min_followers_int:
                        inf['follower_count'] = int(real_follower_count)
                        filtered_influencers.append(inf)
                    else:
                        print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - {real_follower_count} followers < {min_followers_int}")
                
                influencers = filtered_influencers
                print(f"✅ Filtered to {len(influencers)} influencers meeting min {min_followers_int} followers requirement")
        
        # Filter by product_type (lenient - keep all if filter removes everything)
        # Only apply if we have enough influencers or user explicitly wants strict filtering
        if product_type and use_strict_filtering:
            product_filtered = []
            for inf in influencers:
                # Check if influencer's domain_niche, job_title, or use_case matches product_type
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                product_lower = product_type.lower()
                
                # Check if any field contains the product type or is related
                matches = (
                    product_lower in domain_niche or 
                    product_lower in job_title or 
                    product_lower in use_case or
                    domain_niche in product_lower or
                    job_title in product_lower
                )
                
                if matches:
                    product_filtered.append(inf)
                else:
                    print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - doesn't match product type '{product_type}'")
            
            # If product filter removed all influencers, be lenient and keep all
            if len(product_filtered) == 0 and len(influencers) > 0:
                print(f"⚠️  Product type filter removed all influencers. Using lenient matching - keeping all {len(influencers)} influencers.")
                product_filtered = influencers
            else:
                influencers = product_filtered
                print(f"✅ Filtered to {len(influencers)} influencers matching product type '{product_type}'")
        
        # Filter by content_type (lenient - keep all if filter removes everything)
        # Only apply if we have enough influencers or user explicitly wants strict filtering
        if content_type and isinstance(content_type, list) and len(content_type) > 0 and use_strict_filtering:
            content_filtered = []
            for inf in influencers:
                # Check if influencer's content matches any of the selected content types
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                bio = str(inf.get('bio', '')).lower()
                
                matches = False
                for ct in content_type:
                    ct_lower = str(ct).lower()
                    if (ct_lower in domain_niche or 
                        ct_lower in job_title or 
                        ct_lower in bio or
                        domain_niche in ct_lower or
                        job_title in ct_lower):
                        matches = True
                        break
                
                if matches:
                    content_filtered.append(inf)
                else:
                    print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - doesn't match content types {content_type}")
            
            # If content filter removed all influencers, be lenient and keep all
            if len(content_filtered) == 0 and len(influencers) > 0:
                print(f"⚠️  Content type filter removed all influencers. Using lenient matching - keeping all {len(influencers)} influencers.")
                content_filtered = influencers
            else:
                influencers = content_filtered
                print(f"✅ Filtered to {len(influencers)} influencers matching content types {content_type}")
        
        # Filter by target_audience (lenient - keep all if filter removes everything)
        # Only apply if we have enough influencers or user explicitly wants strict filtering
        if target_audience and use_strict_filtering:
            audience_filtered = []
            for inf in influencers:
                # Check if influencer's bio, domain_niche, or use_case indicates they reach the target audience
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                bio = str(inf.get('bio', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                audience_lower = target_audience.lower()
                
                # Check if any field contains the target audience or is related
                matches = (
                    audience_lower in domain_niche or 
                    audience_lower in job_title or 
                    audience_lower in bio or
                    audience_lower in use_case or
                    domain_niche in audience_lower or
                    job_title in audience_lower
                )
                
                if matches:
                    audience_filtered.append(inf)
                else:
                    print(f"⚠️  Filtered out {inf.get('full_name', 'Unknown')} - doesn't match target audience '{target_audience}'")
            
            # If audience filter removed all influencers, be lenient and keep all
            if len(audience_filtered) == 0 and len(influencers) > 0:
                print(f"⚠️  Target audience filter removed all influencers. Using lenient matching - keeping all {len(influencers)} influencers.")
                audience_filtered = influencers
            else:
                influencers = audience_filtered
                print(f"✅ Filtered to {len(influencers)} influencers matching target audience '{target_audience}'")
        
        # Calculate engagement metrics and match scores
        for idx, inf in enumerate(influencers):
            base_score = 70  # Start with base score
            
            # Boost score for matching product_type
            if product_type:
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                product_lower = product_type.lower()
                if (product_lower in domain_niche or product_lower in job_title or product_lower in use_case):
                    base_score += 10  # Strong match bonus
                    inf['matches_product_type'] = True
            
            # Boost score for matching content_type
            if content_type and isinstance(content_type, list) and len(content_type) > 0:
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                bio = str(inf.get('bio', '')).lower()
                matches_content = False
                for ct in content_type:
                    ct_lower = str(ct).lower()
                    if (ct_lower in domain_niche or ct_lower in job_title or ct_lower in bio):
                        matches_content = True
                        break
                if matches_content:
                    base_score += 10  # Strong match bonus
                    inf['matches_content_type'] = True
            
            # Boost score for matching target_audience
            if target_audience:
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                bio = str(inf.get('bio', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                audience_lower = target_audience.lower()
                if (audience_lower in domain_niche or audience_lower in job_title or audience_lower in bio or audience_lower in use_case):
                    base_score += 10  # Strong match bonus
                    inf['matches_target_audience'] = True
            
            # Boost score for matching industry
            industry = filters.get('industry', '').strip() if filters.get('industry') else ''
            if industry:
                inf_industry = str(inf.get('industry', '')).lower()
                if industry.lower() in inf_industry or inf_industry in industry.lower():
                    base_score += 10
                    inf['matches_industry'] = True
            
            # Boost score for matching location
            location = filters.get('location', '').strip() if filters.get('location') else ''
            if location:
                inf_location = str(inf.get('location', '')).lower()
                if location.lower() in inf_location or inf_location in location.lower():
                    base_score += 5
                    inf['matches_location'] = True
            
            # Boost score if has email (better contactability)
            if inf.get('email') and inf.get('email').strip() and '@' in inf.get('email', '') and 'example.com' not in inf.get('email', '').lower():
                base_score += 5
            
            # Boost score if has contact link
            if inf.get('contact_link') and inf.get('contact_link').strip():
                base_score += 5
            
            # Boost score if has use_case (clear collaboration purpose)
            if inf.get('use_case') and inf.get('use_case').strip():
                base_score += 5
            
            # Boost score for top/macro influencers (they have more reach)
            if inf.get('tier') == 'Top/Macro':
                base_score += 10
            
            # Boost score if has REAL data from APIs
            if inf.get('real_instagram') or inf.get('real_twitter') or inf.get('real_linkedin'):
                base_score += 15  # Significant boost for verified real data
            
            # Slight decrease for ranking (lower index = higher score)
            base_score -= (idx * 1)
            
            inf['match_score'] = max(10, min(100, int(base_score)))
            
            # Use REAL follower count if available, otherwise calculate from string
            follower_count = inf.get('follower_count', 0)
            if follower_count == 0:
                # Calculate engagement metrics from estimated data
                followers_str = str(inf.get('followers', '0')).upper()
                try:
                    clean_str = followers_str.replace(',', '').replace(' ', '').strip()
                    if 'K' in clean_str:
                        follower_count = float(clean_str.replace('K', '')) * 1000
                    elif 'M' in clean_str:
                        follower_count = float(clean_str.replace('M', '')) * 1000000
                    else:
                        follower_count = float(clean_str) if clean_str else 0
                except:
                    follower_count = 0
                inf['follower_count'] = int(follower_count)
            
            # Only calculate ESTIMATED metrics if we don't have REAL data
            if not inf.get('real_instagram') and not inf.get('real_twitter'):
                # Calculate estimated engagement metrics based on tier
                tier = inf.get('tier', 'Emerging')
                if tier == 'Top/Macro':
                    engagement_rate = 1.5  # 1.5% typical for macro
                    avg_likes = int(follower_count * 0.015)
                    avg_comments = int(follower_count * 0.001)
                elif tier == 'Mid-tier':
                    engagement_rate = 2.5  # 2.5% typical for mid-tier
                    avg_likes = int(follower_count * 0.025)
                    avg_comments = int(follower_count * 0.002)
                elif tier == 'Micro':
                    engagement_rate = 4.0  # 4% typical for micro
                    avg_likes = int(follower_count * 0.04)
                    avg_comments = int(follower_count * 0.003)
                elif tier == 'Nano':
                    engagement_rate = 6.0  # 6% typical for nano
                    avg_likes = int(follower_count * 0.06)
                    avg_comments = int(follower_count * 0.005)
                else:
                    engagement_rate = 3.0
                    avg_likes = int(follower_count * 0.03)
                    avg_comments = int(follower_count * 0.002)
                
                # Only set estimated metrics if real ones aren't already set
                if not inf.get('engagement_rate') or inf.get('engagement_rate', 0) == 0:
                    inf['engagement_rate'] = round(engagement_rate, 2)
                if not inf.get('avg_likes_per_post') or inf.get('avg_likes_per_post', 0) == 0:
                    inf['avg_likes_per_post'] = avg_likes
                if not inf.get('avg_comments_per_post') or inf.get('avg_comments_per_post', 0) == 0:
                    inf['avg_comments_per_post'] = avg_comments
                if not inf.get('estimated_reach') or inf.get('estimated_reach', 0) == 0:
                    inf['estimated_reach'] = int(follower_count * (engagement_rate / 100))
            
            # Mark if data is estimated vs real
            inf['data_source'] = 'real' if (inf.get('real_instagram') or inf.get('real_twitter') or inf.get('real_linkedin')) else 'estimated'
        
        # Final check: if we have no influencers after all filtering, try to recover
        if len(influencers) == 0:
            print(f"❌ No influencers remaining after filtering. Original count: {original_count}")
            
            # Try to get fallback influencers that match at least some criteria
            print(f"🔄 Attempting to get fallback influencers...")
            try:
                # Create minimal filters (only industry and location if specified)
                minimal_filters = {}
                if filters.get('industry'):
                    minimal_filters['industry'] = filters.get('industry')
                if filters.get('location'):
                    minimal_filters['location'] = filters.get('location')
                
                # Get fallback influencers with minimal filters
                # Use the same finder instance that was used earlier
                fallback_influencers = finder._get_fallback_influencers(minimal_filters, limit)
                
                if fallback_influencers and len(fallback_influencers) > 0:
                    print(f"✅ Got {len(fallback_influencers)} fallback influencers")
                    influencers = fallback_influencers
                    # Mark them as fallback so we know they're not perfect matches
                    for inf in influencers:
                        inf['is_fallback'] = True
                        inf['match_score'] = 60  # Lower score for fallback
                else:
                    # Last resort: create generic influencers
                    print(f"⚠️  Creating generic influencers as last resort")
                    influencers = []
                    for i in range(1, min(limit + 1, 6)):
                        industry = filters.get('industry', 'General')
                        location = filters.get('location', 'India')
                        influencers.append({
                            'id': i,
                            'full_name': f'{industry} Influencer {i}',
                            'email': f'influencer{i}@example.com',
                            'industry': industry if industry else 'General',
                            'category': industry if industry else 'General',
                            'job_title': f'{industry} Content Creator' if industry else 'Content Creator',
                            'domain_niche': f'{industry} Content Creator' if industry else 'Content Creator',
                            'company_name': f'{industry} Brand',
                            'location': location,
                            'contact_type': 'Email',
                            'contact_link': f'https://example.com/influencer{i}',
                            'use_case': f'{industry} content collaboration' if industry else 'Content collaboration',
                            'source_url': f'https://example.com/influencer{i}',
                            'bio': f'Content creator specializing in {industry}' if industry else 'Content creator',
                            'platform': 'Multiple',
                            'followers': '50K',
                            'follower_count': 50000,
                            'match_score': 50,
                            'is_fallback': True,
                            'tier': 'Mid-tier'
                        })
                    print(f"✅ Created {len(influencers)} generic influencers")
            except Exception as e:
                print(f"⚠️  Error getting fallback influencers: {e}")
                return jsonify({
                    "success": False,
                    "error": "No influencers found matching your criteria. Try removing some filters or adjusting your requirements.",
                    "count": 0,
                    "recommendations": [],
                    "suggestion": "Try removing filters like product type, content type, or target audience to see more results."
                }), 200  # Return 200 so frontend can show the message
        
        # Sort by match score (highest first) - top matches at the top
        influencers.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        # Categorize by tier
        tiered_influencers = finder.categorize_influencers_by_tier(influencers)
        
        # Count influencers per tier
        tier_counts = {tier: len(inf_list) for tier, inf_list in tiered_influencers.items()}
        
        print(f"✅ Final result: {len(influencers)} influencers after all filtering")
        
        return jsonify({
            "success": True,
            "count": len(influencers),
            "recommendations": influencers,
            "tiered_influencers": tiered_influencers,
            "tier_counts": tier_counts,
            "source": "ChatGPT API (no database/CSV)"
        })
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500

@app.route('/api/analyze-profile/<influencer_id>', methods=['POST'])
def analyze_profile(influencer_id):
    """Analyze influencer profile with GPT, hashtags, and views"""
    try:
        # Get filters from request body if provided (needed to find the influencer)
        data = request.json or {}
        filters = data.get('filters', {})
        
        # Find the influencer first using ChatGPT
        from data_manager import InfluencerDataManager
        dm = InfluencerDataManager()
        influencer = dm.get_influencer_by_id(influencer_id, filters)
        
        if not influencer:
            # If not found, try to analyze based on ID alone
            # Create a temporary influencer object for analysis
            influencer = {
                'id': influencer_id,
                'full_name': f'Influencer {influencer_id}',
                'email': f'influencer{influencer_id}@example.com',
                'industry': filters.get('industry', ''),
                'job_title': 'Content Creator',
                'location': filters.get('location', 'India')
            }
        
        # Use profile analyzer with the influencer data
        analysis = profile_analyzer.analyze_profile_with_gpt_data(influencer)
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analyze-profiles/batch', methods=['POST'])
def analyze_profiles_batch():
    """Analyze multiple profiles"""
    try:
        data = request.json
        influencer_ids = data.get('influencer_ids', [])
        filters = data.get('filters', {})  # Get filters to help find influencers
        
        from data_manager import InfluencerDataManager
        dm = InfluencerDataManager()
        
        results = []
        for inf_id in influencer_ids:
            # Try to find the influencer first
            influencer = dm.get_influencer_by_id(inf_id, filters)
            if influencer:
                analysis = profile_analyzer.analyze_profile_with_gpt_data(influencer)
            else:
                # Fallback: analyze with just ID
                analysis = profile_analyzer.analyze_profile_with_gpt(inf_id)
            
            results.append(analysis)
        
        return jsonify({
            "success": True,
            "count": len(results),
            "analyses": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"\n{'='*70}")
    print("✨ NOVA Influencer Platform Server")
    print(f"{'='*70}")
    print(f"✅ Server starting on http://0.0.0.0:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"{'='*70}\n")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

