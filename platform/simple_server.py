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

@app.route('/api/reload-csv', methods=['POST'])
def reload_csv():
    """Reload CSV data (useful when CSV file is updated)"""
    try:
        from data_manager import InfluencerDataManager
        dm = InfluencerDataManager()
        dm.reload_csv_data()
        influencers = dm.get_all_influencers()
        csv_count = len(dm.csv_data) if dm.csv_data else 0
        return jsonify({
            "success": True,
            "message": "CSV data reloaded successfully",
            "total_influencers": len(influencers),
            "csv_influencers": csv_count,
            "csv_file_path": dm.CSV_FILE_PATH
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/csv-status', methods=['GET'])
def csv_status():
    """Check CSV file status and count"""
    try:
        from data_manager import InfluencerDataManager
        import os
        dm = InfluencerDataManager()
        csv_exists = os.path.exists(dm.CSV_FILE_PATH)
        csv_count = len(dm.csv_data) if dm.csv_data else 0
        
        return jsonify({
            "success": True,
            "csv_file_path": dm.CSV_FILE_PATH,
            "csv_exists": csv_exists,
            "csv_influencers_count": csv_count,
            "message": f"CSV file is {'accessible' if csv_exists else 'not found'}. {csv_count} influencers loaded from CSV."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get recommendations"""
    try:
        data = request.json
        filters = data.get('filters', {})
        limit = min(data.get('limit', 10), 20)  # Max 20 recommendations
        
        # Import data manager
        from data_manager import InfluencerDataManager
        dm = InfluencerDataManager()
        influencers = dm.get_all_influencers()
        
        print(f"📊 Total influencers loaded: {len(influencers)}")
        print(f"🔍 Filters applied: {filters}")
        
        # Skip header row if first row looks like headers
        if influencers and isinstance(influencers[0].get('full_name'), str) and influencers[0].get('full_name') in ['email', 'full_name', 'Full Name']:
            influencers = influencers[1:]
            print(f"📋 Skipped header row, {len(influencers)} influencers remaining")
        
        # Handle product type and image if provided
        product_type = filters.get('product_type', '').strip() if filters.get('product_type') else ''
        product_image = filters.get('product_image')  # Base64 encoded image
        
        # Filter influencers
        filtered = []
        for inf in influencers:
            # Skip if this looks like a header row or empty entry
            if not inf.get('full_name') and not inf.get('email'):
                continue
            if inf.get('full_name', '').strip() in ['Name/Brand', 'Name', 'Full Name', '']:
                continue
            if inf.get('email', '').strip() in ['email', 'Email', 'EMAIL', 'Public Email']:
                continue
                
            match = True
            
            # Industry/Category filter - STRICT: Must match exactly, show ONLY selected industry
            # This is the PRIMARY filter - if industry is selected, ONLY show that industry
            if filters.get('industry') and filters['industry'].strip():
                industry_filter = filters['industry'].lower().strip()
                industry_value = str(inf.get('industry', '')).lower()
                category_value = str(inf.get('category', '')).lower()
                
                # Create keyword mappings for exact industry matching
                keyword_mappings = {
                    'property': ['property/real estate'],
                    'property/real estate': ['property/real estate'],
                    'real estate': ['property/real estate'],
                    'food': ['food'],
                    'education': ['education'],
                    'software products': ['software products'],
                    'technology creators': ['technology creators'],
                    'digital products': ['digital products'],
                    'travel': ['travel'],
                    'tech': ['software products', 'technology creators', 'digital products'],
                    'technology': ['software products', 'technology creators', 'digital products'],
                    'software': ['software products', 'technology creators', 'digital products'],
                }
                
                # Get exact category matches for the filter
                matching_categories = keyword_mappings.get(industry_filter, [industry_filter])
                
                # STRICT MATCHING: Check if influencer's category matches the selected industry
                found_match = False
                
                # Check exact category match first (most important)
                for match_category in matching_categories:
                    if match_category == industry_value or match_category == category_value:
                        found_match = True
                        break
                    # Also check if category contains the match (for "Property/Real Estate" matching "property")
                    if match_category in industry_value or match_category in category_value:
                        found_match = True
                        break
                    if industry_value in match_category or category_value in match_category:
                        found_match = True
                        break
                
                # If no exact match, check if filter word is in category
                if not found_match:
                    if industry_filter in industry_value or industry_filter in category_value:
                        found_match = True
                    elif industry_value in industry_filter or category_value in industry_filter:
                        found_match = True
                
                # STRICT: If industry doesn't match, exclude this influencer
                if not found_match:
                    match = False
                else:
                    # Debug: Log successful matches
                    print(f"✅ Industry match: {inf.get('full_name', 'Unknown')} - Category: {inf.get('category', 'N/A')} (Filter: {industry_filter})")
            
            # Location filter (case-insensitive partial match) - make it optional/lenient
            if filters.get('location') and filters['location'].strip():
                location_filter = filters['location'].lower().strip()
                location_value = str(inf.get('location', '')).lower()
                country_value = str(inf.get('country', '')).lower()
                
                # Make location filter lenient - if no location data, don't exclude
                location_match = (location_filter in location_value or 
                                location_value in location_filter or
                                location_filter in country_value or
                                country_value in location_filter)
                
                # If influencer has no location data, don't exclude them
                if not location_match and (not location_value or location_value == 'india' or location_value == ''):
                    pass  # Don't exclude if no location data - it's optional
                elif not location_match:
                    match = False  # Only exclude if they have location data that doesn't match
            
            # Content type filter (check domain_niche, job_title, use_case) - make it lenient
            if filters.get('content_type'):
                content_filter = [c.lower().strip() for c in filters['content_type']]
                domain_niche = str(inf.get('domain_niche', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                
                content_match = False
                for cf in content_filter:
                    if (cf in domain_niche or cf in job_title or cf in use_case or
                        domain_niche in cf or job_title in cf or use_case in cf):
                        content_match = True
                        break
                
                # Make content type optional - don't exclude if no match
                # This way it's a preference, not a hard requirement
                if not content_match:
                    pass  # Don't exclude, just won't get bonus points
            
            # Product type filter (check domain_niche, use_case, job_title) - make it optional/lenient
            if product_type:
                product_filter = product_type.lower().strip()
                domain_niche = str(inf.get('domain_niche', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                industry = str(inf.get('industry', '')).lower()
                
                # Make product type filter lenient - don't exclude if no match, just prefer matches
                # This way it's a preference, not a hard requirement
                product_match = (product_filter in domain_niche or
                               product_filter in use_case or
                               product_filter in job_title or
                               product_filter in industry or
                               domain_niche in product_filter or
                               use_case in product_filter or
                               job_title in product_filter or
                               industry in product_filter)
                
                # Don't exclude based on product type - it's just a preference
                # We'll use this for scoring later
                if not product_match:
                    pass  # Don't exclude, just won't get bonus points
            
            # Target audience filter (check use_case, domain_niche) - make it lenient
            if filters.get('target_audience') and filters['target_audience'].strip():
                audience_filter = filters['target_audience'].lower().strip()
                domain_niche = str(inf.get('domain_niche', '')).lower()
                use_case = str(inf.get('use_case', '')).lower()
                job_title = str(inf.get('job_title', '')).lower()
                
                # Make target audience optional - don't exclude if no match
                # This way it's a preference, not a hard requirement
                audience_match = (audience_filter in domain_niche or
                                audience_filter in use_case or
                                audience_filter in job_title or
                                domain_niche in audience_filter or
                                use_case in audience_filter or
                                job_title in audience_filter)
                
                if not audience_match:
                    pass  # Don't exclude, just won't get bonus points
            
            # Min followers filter (optional, may not be in CSV) - make it lenient
            if filters.get('min_followers'):
                try:
                    min_followers = int(filters['min_followers'])
                    followers_str = str(inf.get('followers', '0')).replace(',', '').replace(' ', '')
                    followers = int(followers_str) if followers_str.isdigit() else 0
                    # If no follower data in CSV, don't exclude - it's optional
                    if followers == 0 and not str(inf.get('followers', '')).strip():
                        pass  # No follower data, don't exclude
                    elif followers < min_followers:
                        match = False  # Only exclude if we have follower data that's too low
                except:
                    pass
            
            if match:
                filtered.append(inf)
        
        print(f"✅ Filtered to {len(filtered)} influencers")
        
        # If no filters applied, show all (up to limit)
        has_filters = any([
            filters.get('industry', '').strip(),
            filters.get('location', '').strip(),
            filters.get('min_followers'),
            filters.get('content_type'),
            filters.get('target_audience', '').strip(),
            product_type
        ])
        
        if not filtered and not has_filters:
            # No filters at all - show all
            filtered = influencers[:limit]
            print(f"📋 No filters, showing first {len(filtered)} influencers")
        elif not filtered and has_filters:
            # Filters were applied but nothing matched
            # STRICT MODE: Only show exact industry matches, don't show all influencers
            if filters.get('industry') and filters['industry'].strip():
                print(f"⚠️  No influencers found for industry: '{filters.get('industry')}'. Showing empty results.")
                print(f"💡 Make sure the industry name matches exactly with CSV categories.")
                filtered = []  # Show empty - strict matching
            else:
                # No industry filter but other filters applied - show all
                filtered = influencers[:limit]
                print(f"📋 No industry filter, showing all influencers")
        
        # Limit results
        filtered = filtered[:limit]
        
        # Add match scores (improved scoring based on filters and data quality)
        for idx, inf in enumerate(filtered):
            base_score = 100 - (idx * 3)  # Decreasing score, but less aggressive
            
            # Boost score if has email (better contactability)
            if inf.get('email') and inf.get('email').strip():
                base_score += 5
            
            # Boost score if has contact link
            if inf.get('contact_link') and inf.get('contact_link').strip():
                base_score += 5
            
            # Boost score if has use_case (clear collaboration purpose)
            if inf.get('use_case') and inf.get('use_case').strip():
                base_score += 5
            
            inf['match_score'] = max(10, min(100, int(base_score)))
        
        return jsonify({
            "success": True,
            "count": len(filtered),
            "recommendations": filtered
        })
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500

@app.route('/api/analyze-profile/<influencer_id>', methods=['GET'])
def analyze_profile(influencer_id):
    """Analyze influencer profile with GPT, hashtags, and views"""
    try:
        analysis = profile_analyzer.analyze_profile_with_gpt(influencer_id)
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
        
        results = []
        for inf_id in influencer_ids:
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

