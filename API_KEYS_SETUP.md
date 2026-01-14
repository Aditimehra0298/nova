# API Keys Setup

## Environment Variables

Add these to your `.env` file in the project root:

```bash
# OpenAI API Key for ChatGPT Influencer Finder
OPENAI_API_KEY=your_openai_api_key_here

# Instagram API Token
INSTAGRAM_ACCESS_TOKEN=IGAARw02AmdR1BZAGJOb0ZAySG1qcHNhdVRPRjA1aWxHWEQ5blo0WU9SRnFsZAk9lczVUNXZAnMXhNUU9ZAUHBsNE9CWFpDdTZAPT1V0VVpuXzZA6NkxKY3NzOTl5Nk1qV25lTHNjSWZAtdy12ZAWJpS2E5MXRQaGRQS2FmS0syV3l5bzkxUQZDZD

# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=77pypxmkqgve0y
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here  # Replace with your actual secret

# LinkedIn Access Token (get this via OAuth flow)
# LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here

# Twitter API (if available)
TWITTER_BEARER_TOKEN=

# Facebook API (if available)
FACEBOOK_ACCESS_TOKEN=
```

## LinkedIn OAuth Setup

LinkedIn requires OAuth 2.0 authentication. To get an access token:

1. Go to https://www.linkedin.com/developers/apps
2. Create or select your app
3. Use the Client ID and Client Secret provided
4. Follow OAuth 2.0 flow to get an access token
5. Add the access token to `LINKEDIN_ACCESS_TOKEN` in `.env`

## Instagram Token

The Instagram token is already provided and should work with Instagram Graph API.

