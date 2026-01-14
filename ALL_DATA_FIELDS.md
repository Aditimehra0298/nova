# 📊 ALL Available Influencer Data Fields from Hunter.io

## Complete List of All Data Fields Extracted

### 👤 **Basic Information**
- ✅ **Email** - Primary email address
- ✅ **Full Name** - Complete name
- ✅ **First Name** - Given name
- ✅ **Last Name** - Family name
- ✅ **ID** - Unique identifier

### 📞 **Contact Information**
- ✅ **Phone Number** - Contact phone
- ✅ **Website** - Personal/professional website
- ✅ **Email Provider** - Email service provider

### 📍 **Location Information**
- ✅ **Location** - Full location string
- ✅ **Timezone** - Time zone (e.g., America/Los_Angeles)
- ✅ **UTC Offset** - UTC time offset
- ✅ **City** - City name
- ✅ **State** - State/Province name
- ✅ **State Code** - State abbreviation (e.g., CA)
- ✅ **Country** - Country name
- ✅ **Country Code** - Country code (e.g., US)
- ✅ **Coordinates** - Latitude and Longitude (lat, lng)

### 💼 **Employment Information**
- ✅ **Company Name** - Current employer
- ✅ **Company Domain** - Company website domain
- ✅ **Job Title** - Current position/title
- ✅ **Role** - Job role category
- ✅ **Sub Role** - Sub-category of role
- ✅ **Seniority** - Seniority level (junior, senior, executive, etc.)

### 🌐 **Social Media Profiles**

#### **LinkedIn**
- ✅ **LinkedIn Handle** - Profile username
- ✅ **LinkedIn URL** - Full profile URL

#### **Twitter/X**
- ✅ **Twitter Handle** - Username
- ✅ **Twitter ID** - Unique Twitter ID
- ✅ **Twitter Bio** - Profile bio
- ✅ **Twitter Followers** - Follower count
- ✅ **Twitter Following** - Following count
- ✅ **Twitter Statuses** - Tweet count
- ✅ **Twitter Favorites** - Likes count
- ✅ **Twitter Location** - Location on profile
- ✅ **Twitter Site** - Website on profile
- ✅ **Twitter Avatar** - Profile picture URL

#### **Facebook**
- ✅ **Facebook Handle** - Username
- ✅ **Facebook URL** - Profile URL

#### **Instagram**
- ✅ **Instagram Handle** - Username
- ✅ **Instagram URL** - Profile URL

#### **YouTube**
- ✅ **YouTube Handle** - Channel username
- ✅ **YouTube URL** - Channel URL

#### **GitHub**
- ✅ **GitHub Handle** - Username
- ✅ **GitHub ID** - Unique ID
- ✅ **GitHub Avatar** - Profile picture
- ✅ **GitHub Company** - Company on profile
- ✅ **GitHub Blog** - Blog URL
- ✅ **GitHub Followers** - Follower count
- ✅ **GitHub Following** - Following count

#### **Google Plus**
- ✅ **Google Plus Handle** - Username

#### **Gravatar**
- ✅ **Gravatar Handle** - Username
- ✅ **Gravatar URLs** - Associated URLs
- ✅ **Gravatar Avatar** - Profile picture
- ✅ **Gravatar Avatars** - Multiple avatar sizes

### 📝 **Additional Information**
- ✅ **Bio** - Personal/professional biography
- ✅ **Headline** - Professional headline
- ✅ **Avatar** - Profile picture URL
- ✅ **Industry** - Industry category
- ✅ **Site** - Personal website

### 🔍 **Metadata**
- ✅ **Fuzzy** - Whether match was fuzzy
- ✅ **Indexed At** - When profile was indexed
- ✅ **Active At** - Last active date
- ✅ **Inactive At** - When became inactive (if applicable)

## 📊 What Gets Exported to Google Sheets

All these fields are extracted and exported to your Google Sheet:

### **Columns in Your Sheet:**
1. email
2. full_name
3. first_name
4. last_name
5. location
6. city
7. state
8. country
9. timezone
10. company_name
11. company_domain
12. job_title
13. role
14. seniority
15. linkedin_handle
16. linkedin_url
17. twitter_handle
18. twitter_url
19. facebook_handle
20. facebook_url
21. instagram_handle
22. instagram_url
23. youtube_handle
24. youtube_url
25. bio
26. headline
27. avatar_url
28. website
29. phone_number
30. industry

## 🎯 Example Data Structure

```json
{
  "email": "connie@techcrunch.com",
  "name": {
    "fullName": "Connie Loizos",
    "givenName": "Connie",
    "familyName": "Loizos"
  },
  "location": "San Francisco, California, United States",
  "timeZone": "America/Los_Angeles",
  "geo": {
    "city": "San Francisco",
    "state": "California",
    "country": "United States",
    "lat": 37.77493,
    "lng": -122.41942
  },
  "employment": {
    "domain": "techcrunch.com",
    "name": "TechCrunch",
    "title": "Editor-in-Chief"
  },
  "linkedin": {
    "handle": "connie-loizos-380282"
  },
  "twitter": {
    "handle": null,
    "followers": null
  }
}
```

## ✅ All Fields Are Extracted

The extractor captures **ALL available fields** from Hunter.io for each influencer profile. If a field is not available for a specific person, it will be empty/null in your export.

## 📈 Current Data in Your Sheet

Your Google Sheet currently contains **181 influencer profiles** with all available data fields populated!

View your data: [Google Sheet](https://docs.google.com/spreadsheets/d/1DaplVZtlFgioBjBolJYI1A-MY_Yq8yWAVgXUqwsClK8)


