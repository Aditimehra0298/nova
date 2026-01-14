#!/usr/bin/env python3
"""
ChatGPT-based Influencer Finder
Finds influencers directly using ChatGPT API based on client requirements
No database or CSV files needed
"""

import os
import json
from typing import List, Dict, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env from platform directory
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Try parent directory
        load_dotenv()
except ImportError:
    pass  # dotenv not available, will use system env vars

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


class ChatGPTInfluencerFinder:
    """Find influencers using ChatGPT API based on client requirements"""
    
    def __init__(self):
        self.llm = None
        
        # Try multiple ways to get the API key
        # Priority: 1. Environment variable (works on Render), 2. .env file (local dev)
        openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Debug: Log what we found
        print(f"🔍 Checking for OpenAI API key:")
        print(f"   Environment variable OPENAI_API_KEY: {'Found' if openai_api_key else 'Not found'}")
        if openai_api_key:
            print(f"   Length: {len(openai_api_key)} chars")
            print(f"   Prefix: {openai_api_key[:10]}..." if len(openai_api_key) > 10 else "Too short")
        
        # If not found in environment, try reading from .env file directly (for local dev)
        if not openai_api_key or openai_api_key == 'your_openai_api_key_here':
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            print(f"   Checking .env file at: {env_path}")
            if os.path.exists(env_path):
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith('OPENAI_API_KEY='):
                                openai_api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                print(f"   Found in .env file")
                                break
                except Exception as e:
                    print(f"⚠️  Error reading .env file: {e}")
            else:
                print(f"   .env file not found (this is OK on Render - uses environment variables)")
        
        self.openai_api_key = openai_api_key if openai_api_key and openai_api_key != 'your_openai_api_key_here' else None
        
        if self.openai_api_key:
            print(f"✅ OpenAI API key found (length: {len(self.openai_api_key)} chars)")
            try:
                if HAS_LANGCHAIN:
                    self.llm = ChatOpenAI(
                        model_name="gpt-4o-mini",  # Fast and accurate model
                        temperature=0.7,  # More natural, like normal ChatGPT conversation
                        openai_api_key=self.openai_api_key
                    )
                    print("✅ ChatGPT initialized with LangChain")
                else:
                    import openai
                    openai.api_key = self.openai_api_key
                    self.llm = "openai_direct"
                    print("✅ ChatGPT initialized with direct OpenAI API")
            except Exception as e:
                print(f"⚠️  Error initializing ChatGPT: {e}")
                import traceback
                traceback.print_exc()
                self.llm = None
        else:
            print("❌ OPENAI_API_KEY not found!")
            print("💡 Please set OPENAI_API_KEY in .env file in the platform directory")
            print(f"   Current directory: {os.path.dirname(__file__)}")
            print(f"   Looking for .env at: {os.path.join(os.path.dirname(__file__), '.env')}")
            self.llm = None
    
    def find_influencers(self, filters: Dict, limit: int = 10) -> List[Dict]:
        """
        Find influencers based on client requirements using ChatGPT
        
        Args:
            filters: Client requirements dict with:
                - industry: Industry/category (e.g., "Technology", "Food", "Travel")
                - location: Location (e.g., "India", "Mumbai")
                - content_type: Content types (list)
                - target_audience: Target audience description
                - product_type: Type of product to promote
                - min_followers: Minimum followers (optional)
            limit: Maximum number of influencers to return
        
        Returns:
            List of influencer dictionaries
        """
        if not self.llm:
            print("❌ ChatGPT API not available - using fallback influencers")
            print("💡 To use ChatGPT API, set OPENAI_API_KEY in .env file")
            print(f"   Expected location: {os.path.join(os.path.dirname(__file__), '.env')}")
            return self._get_fallback_influencers(filters, limit)
        
        try:
            # Debug: Print what filters we received
            print(f"📋 Filters received: {json.dumps(filters, indent=2)}")
            
            # Build prompt for ChatGPT
            prompt = self._build_finder_prompt(filters, limit)
            
            # Debug: Print the prompt being sent (first 500 chars)
            print(f"📝 Prompt being sent to ChatGPT (first 500 chars):\n{prompt[:500]}...")
            
            # Use OpenAI Assistant API with the specified assistant ID
            if self.llm == "openai_direct":
                import openai
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=self.openai_api_key)
                    
                    # Use the specified assistant ID
                    assistant_id = "asst_FCWGkak9AJ9iyGdQJAGmAlF4"
                    print(f"🤖 Using Assistant API with ID: {assistant_id}")
                    
                    # Create a thread
                    thread = client.beta.threads.create()
                    
                    # Add the user message to the thread
                    client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=prompt
                    )
                    
                    # Run the assistant
                    run = client.beta.threads.runs.create(
                        thread_id=thread.id,
                        assistant_id=assistant_id
                    )
                    
                    # Wait for the run to complete (with timeout)
                    import time
                    max_wait = 60  # 60 second timeout
                    waited = 0
                    while run.status in ['queued', 'in_progress'] and waited < max_wait:
                        time.sleep(1)
                        waited += 1
                        run = client.beta.threads.runs.retrieve(
                            thread_id=thread.id,
                            run_id=run.id
                        )
                    
                    if run.status == 'completed':
                        # Get the messages from the thread
                        messages = client.beta.threads.messages.list(thread_id=thread.id)
                        # Get the assistant's response (first message is the latest)
                        if messages.data and len(messages.data) > 0:
                            response_text = messages.data[0].content[0].text.value
                            print(f"✅ Assistant API returned response ({len(response_text)} chars)")
                        else:
                            raise Exception("No response from assistant")
                    else:
                        error_msg = f"Assistant run failed with status: {run.status}"
                        if hasattr(run, 'last_error') and run.last_error:
                            error_msg += f" - {run.last_error}"
                        print(f"⚠️  {error_msg}")
                        raise Exception(error_msg)
                        
                except Exception as e:
                    print(f"⚠️  OpenAI Assistant API error: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fallback to regular chat completions
                    print("🔄 Falling back to regular chat completions API...")
                    try:
                        client = OpenAI(api_key=self.openai_api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are helpful and knowledgeable about social media influencers. You know real influencers across Instagram, YouTube, Twitter, LinkedIn, and other platforms."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=4000,
                        )
                        response_text = response.choices[0].message.content
                        print("✅ Used fallback chat completions API")
                    except Exception as e2:
                        print(f"⚠️  Fallback also failed: {e2}")
                        return self._get_fallback_influencers(filters, limit)
            else:
                try:
                    # Use invoke with natural conversation style - like normal ChatGPT
                    response = self.llm.invoke([
                        SystemMessage(content="You are helpful and knowledgeable about social media influencers. You know real influencers across Instagram, YouTube, Twitter, LinkedIn, and other platforms."),
                        HumanMessage(content=prompt)
                    ], timeout=45)  # Increased timeout for better results
                    response_text = response.content
                except Exception as e:
                    print(f"⚠️  LangChain API error: {e}")
                    import traceback
                    traceback.print_exc()
                    return self._get_fallback_influencers(filters, limit)
            
            # Parse response
            influencers = self._parse_chatgpt_response(response_text, filters)
            
            # Limit results
            return influencers[:limit]
            
        except Exception as e:
            print(f"⚠️  Error finding influencers with ChatGPT: {e}")
            return self._get_fallback_influencers(filters, limit)
    
    def _build_finder_prompt(self, filters: Dict, limit: int) -> str:
        """Build a natural, conversational prompt like normal ChatGPT - this is the key to accuracy!"""
        
        industry = filters.get('industry', '').strip() if filters.get('industry') else ''
        location = filters.get('location', '').strip() if filters.get('location') else ''
        content_type = filters.get('content_type', [])
        target_audience = filters.get('target_audience', '').strip() if filters.get('target_audience') else ''
        product_type = filters.get('product_type', '').strip() if filters.get('product_type') else ''
        min_followers = filters.get('min_followers', '')
        platforms = filters.get('platforms', [])
        
        # Build a natural, conversational query - like talking to ChatGPT normally
        query_parts = []
        
        # Handle industry OR product_type (user might use either)
        category = industry or product_type
        if category:
            query_parts.append(f"in the {category} industry/category")
        
        if location:
            query_parts.append(f"from {location}")
        
        # If both product_type and industry are specified, mention product type specifically
        if product_type and industry and product_type != industry:
            query_parts.append(f"who work with {product_type} products")
        
        if content_type:
            content_list = ', '.join(content_type) if isinstance(content_type, list) else content_type
            # Don't add if it's "Any" or empty
            if content_list and content_list.lower() not in ['any', 'any audience', '']:
                query_parts.append(f"who create {content_list} content")
        
        if target_audience:
            # Don't add if it's "Any" or empty
            if target_audience.lower() not in ['any', 'any audience', '']:
                query_parts.append(f"with audience targeting {target_audience}")
        
        if platforms:
            platform_list = ', '.join(platforms) if isinstance(platforms, list) else platforms
            if platform_list and platform_list.lower() not in ['any', '']:
                query_parts.append(f"on {platform_list}")
        
        if min_followers:
            # Format followers nicely
            if isinstance(min_followers, (int, float)):
                min_followers_int = int(min_followers)
                if min_followers_int >= 1000:
                    followers_str = f"{min_followers_int/1000:.0f}K" if min_followers_int % 1000 == 0 else f"{min_followers_int:,}"
                else:
                    followers_str = str(min_followers_int)
            else:
                # Parse string like "25K" or "25000"
                min_followers_str = str(min_followers).upper().replace(',', '')
                if 'K' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('K', '')) * 1000)
                elif 'M' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('M', '')) * 1000000)
                else:
                    min_followers_int = int(min_followers_str) if min_followers_str.isdigit() else 10000
                followers_str = f"{min_followers_int/1000:.0f}K" if min_followers_int >= 1000 and min_followers_int % 1000 == 0 else f"{min_followers_int:,}"
            
            # Calculate a reasonable range (e.g., 25K means 20K-50K, not 1M+)
            if isinstance(min_followers, (int, float)):
                min_followers_int = int(min_followers)
            else:
                min_followers_str = str(min_followers).upper().replace(',', '')
                if 'K' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('K', '')) * 1000)
                elif 'M' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('M', '')) * 1000000)
                else:
                    min_followers_int = int(min_followers_str) if min_followers_str.isdigit() else 10000
            
            # Define follower range - if user wants 25K, give them 20K-50K range, not celebrities
            if min_followers_int < 50000:
                # Micro-influencer range: target ±50% or 20K-50K range
                lower_bound = max(10000, int(min_followers_int * 0.6))
                upper_bound = min(100000, int(min_followers_int * 2))
                query_parts.append(f"with approximately {followers_str} followers (range: {lower_bound:,}-{upper_bound:,}, NO celebrity influencers with 1M+ followers)")
            else:
                query_parts.append(f"with at least {followers_str} followers")
        else:
            query_parts.append("with at least 10,000 followers (no micro/nano influencers)")
        
        # Natural conversation-style prompt - this is what makes ChatGPT accurate!
        natural_query = " ".join(query_parts) if query_parts else "top influencers"
        
        # Determine if user wants micro-influencers (not celebrities)
        wants_micro = False
        if min_followers:
            if isinstance(min_followers, (int, float)):
                min_followers_int = int(min_followers)
            else:
                min_followers_str = str(min_followers).upper().replace(',', '')
                if 'K' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('K', '')) * 1000)
                elif 'M' in min_followers_str:
                    min_followers_int = int(float(min_followers_str.replace('M', '')) * 1000000)
                else:
                    min_followers_int = int(min_followers_str) if min_followers_str.isdigit() else 10000
            wants_micro = min_followers_int < 100000  # Less than 100K = micro-influencer range
        
        prompt = f"""I need you to find {limit} REAL, VERIFIED social media influencers {natural_query}.

CRITICAL REQUIREMENTS:
1. These must be REAL influencers that actually exist and are active on social media
2. They must match ALL the criteria specified above
3. Use your knowledge of actual influencers - do NOT make up fake ones
4. If you can't find enough matching influencers, return fewer real ones rather than fake ones
{f"5. IMPORTANT: Find micro-influencers/mid-tier influencers (NOT celebrities or top-tier with 1M+ followers). Target the specific follower range mentioned above." if wants_micro else "5. Prioritize well-known, verified influencers with significant followings"}

For each influencer, I need:
- Their REAL name or brand name (not generic like "Food Influencer 1")
- Their ACTUAL social media handles (must be real, existing accounts)
- Their REAL follower count (accurate estimate)
- Their actual location
- What they're genuinely known for
- A real email if available (or use contact@[their-domain].com format based on their website)
- Their real profile URL

Please return this as a JSON array with exactly {limit} REAL influencers. Each influencer should have these fields:
- id (number: 1, 2, 3...)
- full_name (real name)
- email (real email or contact@[domain].com)
- industry (the industry they're in)
- category (same as industry)
- job_title (what they do, e.g., "Tech Reviewer", "Food Blogger")
- domain_niche (same as job_title)
- company_name (brand name if they have one)
- location (where they're from)
- contact_type ("Email" or "Instagram DM" etc)
- contact_link (their main social profile URL)
- use_case (what they can help with, e.g., "Product reviews")
- source_url (main profile URL)
- bio (brief description)
- platform ("Instagram", "Twitter", "LinkedIn", "YouTube", "Facebook", or "Multiple")
- followers (as string like "50K" or "1.2M")
- instagram_handle (username without @)
- twitter_handle (username without @)
- linkedin_handle (username/vanity)
- youtube_handle (channel name)
- facebook_handle (page username)

VERY IMPORTANT:
- Only return REAL influencers that actually exist - verified accounts with real followers
- DO NOT create generic names like "Food Influencer 1" or "Tech Influencer 2"
- DO NOT make up fake influencers
- Use your knowledge of actual, real influencers from the specified location and industry
- If you cannot find {limit} real matching influencers, return fewer REAL ones (not fake ones)
- All social media handles must be REAL, existing accounts
{f"- CRITICAL: Match the follower count range specified. If the range is around 25K, give influencers with 20K-50K followers, NOT celebrities with 1M+ followers. Avoid top-tier/celebrity influencers when a specific lower follower count is requested." if wants_micro else ""}

Return ONLY the JSON array, no other text."""
        
        return prompt
    
    def _parse_chatgpt_response(self, response_text: str, filters: Dict) -> List[Dict]:
        """Parse ChatGPT response into influencer list"""
        try:
            # Try to extract JSON from response
            if '```json' in response_text:
                json_str = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                json_str = response_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = response_text.strip()
            
            # Try to parse as JSON
            influencers = json.loads(json_str)
            
            # Ensure it's a list
            if not isinstance(influencers, list):
                influencers = [influencers]
            
            # Validate and normalize influencer data
            platforms = filters.get('platforms', [])
            normalized = []
            for idx, inf in enumerate(influencers, 1):
                platform = inf.get('platform', 'Multiple')
                
                # STRICT platform filtering - only show influencers from selected platforms
                if platforms:
                    platforms_lower = [p.lower() for p in platforms] if isinstance(platforms, list) else [platforms.lower()]
                    platform_lower = platform.lower()
                    
                    # Check if influencer has handles for selected platforms
                    has_instagram = bool(inf.get('instagram_handle')) and any('instagram' in p for p in platforms_lower)
                    has_twitter = bool(inf.get('twitter_handle')) and any('twitter' in p or 'x' in p for p in platforms_lower)
                    has_linkedin = bool(inf.get('linkedin_handle')) and any('linkedin' in p for p in platforms_lower)
                    has_youtube = bool(inf.get('youtube_handle')) and any('youtube' in p for p in platforms_lower)
                    has_facebook = bool(inf.get('facebook_handle')) and any('facebook' in p for p in platforms_lower)
                    
                    # Also check if platform field matches
                    platform_matches = any(
                        req_platform in platform_lower or 
                        platform_lower in req_platform
                        for req_platform in platforms_lower
                    )
                    
                    # Must have at least one matching platform handle OR platform field match
                    matches_platform = has_instagram or has_twitter or has_linkedin or has_youtube or has_facebook or platform_matches
                    
                    # STRICT: Skip if doesn't match platform requirements
                    if not matches_platform:
                        print(f"⚠️  Skipping {inf.get('full_name', 'Unknown')} - doesn't match platform requirements: {platforms}")
                        continue
                
                # Validate email - prefer real emails, avoid example.com
                email = inf.get('email', '')
                if not email or 'example.com' in email.lower():
                    # Try to construct email from name/domain if available
                    name = inf.get('full_name', inf.get('name', '')).lower().replace(' ', '')
                    if name and len(name) > 2:
                        email = f"contact@{name}.com"  # Better than example.com
                    else:
                        email = f"contact{idx}@influencer.com"  # Better than example.com
                
                normalized_inf = {
                    'id': inf.get('id', idx),
                    'full_name': inf.get('full_name', inf.get('name', 'Unknown Influencer')),
                    'email': email,
                    'industry': inf.get('industry', filters.get('industry', '')),
                    'category': inf.get('category', inf.get('industry', filters.get('industry', ''))),
                    'job_title': inf.get('job_title', inf.get('domain_niche', '')),
                    'domain_niche': inf.get('domain_niche', inf.get('job_title', '')),
                    'company_name': inf.get('company_name', inf.get('full_name', '')),
                    'location': inf.get('location', filters.get('location', 'India')),
                    'contact_type': inf.get('contact_type', 'Email'),
                    'contact_link': inf.get('contact_link', inf.get('source_url', '')),
                    'use_case': inf.get('use_case', 'Content collaboration'),
                    'source_url': inf.get('source_url', inf.get('contact_link', '')),
                    'bio': inf.get('bio', f"{inf.get('full_name', '')} - {inf.get('job_title', 'Content Creator')}"),
                    'platform': platform,
                    'followers': inf.get('followers', '10K'),
                    'match_score': 85,  # Default match score
                    # Platform-specific handles - clean and validate
                    'instagram_handle': inf.get('instagram_handle', '').lstrip('@').strip(),
                    'twitter_handle': inf.get('twitter_handle', '').lstrip('@').strip(),
                    'linkedin_handle': inf.get('linkedin_handle', '').lstrip('in/').lstrip('/').strip(),
                    'youtube_handle': inf.get('youtube_handle', '').lstrip('@').lstrip('/').strip(),
                    'facebook_handle': inf.get('facebook_handle', '').strip()
                }
                normalized.append(normalized_inf)
            
            # Categorize influencers by tier
            for inf in normalized:
                inf['tier'] = self._categorize_influencer_tier(inf)
            
            return normalized
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing ChatGPT response as JSON: {e}")
            print(f"Response text: {response_text[:500]}")
            return self._get_fallback_influencers(filters, 10)
        except Exception as e:
            print(f"⚠️  Error processing ChatGPT response: {e}")
            return self._get_fallback_influencers(filters, 10)
    
    def _get_fallback_influencers(self, filters: Dict, limit: int) -> List[Dict]:
        """Fallback influencers if ChatGPT is not available"""
        industry = filters.get('industry', '').strip() if filters.get('industry') else 'General'
        location = filters.get('location', '').strip() if filters.get('location') else 'India'
        
        # Generate basic fallback influencers
        influencers = []
        for i in range(1, min(limit + 1, 6)):
            influencers.append({
                'id': i,
                'full_name': f'{industry} Influencer {i}',
                'email': f'influencer{i}@example.com',
                'industry': industry if industry else 'General',
                'category': industry if industry else 'General',
                'job_title': f'{industry} Content Creator',
                'domain_niche': f'{industry} Content Creator',
                'company_name': f'{industry} Brand',
                'location': location,
                'contact_type': 'Email',
                'contact_link': f'https://example.com/influencer{i}',
                'use_case': f'{industry} content collaboration',
                'source_url': f'https://example.com/influencer{i}',
                'bio': f'Content creator specializing in {industry}',
                'platform': 'Multiple',
                'followers': '50K',
                'match_score': 70
            })
        
        return influencers
    
    def _categorize_influencer_tier(self, influencer: Dict) -> str:
        """Categorize influencer by follower count tier"""
        followers_str = str(influencer.get('followers', '0')).upper()
        
        # Parse follower count
        try:
            # Remove commas and spaces
            clean_str = followers_str.replace(',', '').replace(' ', '').strip()
            
            # Handle K (thousands) and M (millions)
            if 'K' in clean_str:
                count = float(clean_str.replace('K', '')) * 1000
            elif 'M' in clean_str:
                count = float(clean_str.replace('M', '')) * 1000000
            else:
                count = float(clean_str) if clean_str else 0
        except:
            count = 0
        
        # Categorize by tier
        if count >= 1000000:
            return "Top/Macro"
        elif count >= 100000:
            return "Mid-tier"
        elif count >= 10000:
            return "Micro"
        elif count >= 1000:
            return "Nano"
        else:
            return "Emerging"
    
    def categorize_influencers_by_tier(self, influencers: List[Dict]) -> Dict[str, List[Dict]]:
        """Group influencers by tier"""
        tiers = {
            "Top/Macro": [],
            "Mid-tier": [],
            "Micro": [],
            "Nano": [],
            "Emerging": []
        }
        
        for inf in influencers:
            tier = inf.get('tier', 'Emerging')
            if tier in tiers:
                tiers[tier].append(inf)
            else:
                tiers["Emerging"].append(inf)
        
        return tiers
    
    def get_filter_options(self) -> Dict:
        """Get available filter options (for compatibility with existing frontend)"""
        # Return common industries and locations
        return {
            "industries": [
                "Technology",
                "Food",
                "Travel",
                "Education",
                "Fashion",
                "Fitness",
                "Beauty",
                "Entertainment",
                "Business",
                "Property/Real Estate",
                "Software Products",
                "Technology Creators",
                "Digital Products"
            ],
            "categories": [
                "Technology",
                "Food",
                "Travel",
                "Education",
                "Fashion",
                "Fitness",
                "Beauty",
                "Entertainment",
                "Business",
                "Property/Real Estate",
                "Software Products",
                "Technology Creators",
                "Digital Products"
            ],
            "locations": [
                "India",
                "Mumbai",
                "Delhi",
                "Bangalore",
                "Hyderabad",
                "Chennai",
                "Kolkata",
                "Pune"
            ],
            "job_titles": [
                "Content Creator",
                "Influencer",
                "Blogger",
                "Vlogger",
                "YouTuber",
                "Social Media Manager"
            ],
            "total_influencers": 0  # Dynamic, not stored
        }

