# Instagram Feed API Setup Guide

This guide explains how to set up automatic Instagram post fetching for the website.

## Overview

The website can automatically display the latest 3 Instagram posts from `@uimakerlab`. Since Instagram's API requires server-side authentication, you'll need to set up a backend proxy.

## Option 1: Serverless Function (Recommended)

### Using Vercel

1. **Create a serverless function** in your project:

Create `api/instagram.js`:

```javascript
export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Option A: Use Instagram Basic Display API
    // You'll need to set up Instagram App and get access token
    const ACCESS_TOKEN = process.env.INSTAGRAM_ACCESS_TOKEN;
    const USER_ID = process.env.INSTAGRAM_USER_ID;
    
    if (!ACCESS_TOKEN || !USER_ID) {
      return res.status(500).json({ error: 'Instagram credentials not configured' });
    }

    const response = await fetch(
      `https://graph.instagram.com/${USER_ID}/media?fields=id,caption,media_url,permalink,timestamp&access_token=${ACCESS_TOKEN}&limit=3`
    );

    if (!response.ok) {
      throw new Error(`Instagram API error: ${response.status}`);
    }

    const data = await response.json();
    
    // Transform to our format
    const posts = data.data.map(post => ({
      id: post.id,
      permalink: post.permalink,
      media_url: post.media_url,
      caption: post.caption || '',
      timestamp: post.timestamp
    }));

    return res.status(200).json({ posts });
    
  } catch (error) {
    console.error('Instagram API error:', error);
    return res.status(500).json({ error: 'Failed to fetch Instagram posts' });
  }
}
```

2. **Set up environment variables** in Vercel:
   - `INSTAGRAM_ACCESS_TOKEN`: Your Instagram access token
   - `INSTAGRAM_USER_ID`: Your Instagram user ID

3. **Update `js/main.js`**:
   ```javascript
   const INSTAGRAM_API_URL = 'https://your-domain.vercel.app/api/instagram';
   ```

### Using Netlify Functions

1. **Create `netlify/functions/instagram.js`**:

```javascript
exports.handler = async function(event, context) {
  // Similar code as Vercel function above
  // ...
};
```

2. **Set environment variables** in Netlify dashboard
3. **Update `js/main.js`** with your Netlify function URL

## Option 2: Instagram oEmbed API (Simpler, but requires post IDs)

This method uses Instagram's public oEmbed API. It's simpler but requires you to know the post IDs in advance.

### Setup:

1. **Get Instagram post IDs** from your recent posts (the shortcode in the URL)
   - Example: `https://www.instagram.com/p/CLTDNYFLLkA/` → ID is `CLTDNYFLLkA`

2. **Update `js/main.js`**:
   ```javascript
   const INSTAGRAM_POST_IDS = ['CLTDNYFLLkA', 'CLDrKwYLVUE', 'CKpCwXwrGLU'];
   ```

3. **Limitations**:
   - Requires manual updates when you want to change posts
   - Not truly "automatic" - you need to update IDs manually
   - Works for public posts only

### Pros:
- ✅ No authentication required
- ✅ No backend needed
- ✅ Simple to implement

### Cons:
- ❌ Requires manual post ID updates
- ❌ Not automatic for latest posts

## Option 3: Instagram Basic Display API Setup

1. **Create a Facebook App**:
   - Go to https://developers.facebook.com/
   - Create a new app
   - Add "Instagram Basic Display" product

2. **Get Access Token**:
   - Follow Instagram's authentication flow
   - Get a long-lived access token (valid for 60 days)
   - Set up token refresh mechanism

3. **Get User ID**:
   - Use Graph API Explorer or API call to get your user ID

## Option 4: Third-Party Services

### Using EmbedSocial or Similar Services

1. Sign up for a service like EmbedSocial, Tagembed, or Curator
2. Connect your Instagram account
3. Get the embed code/widget
4. Replace the Instagram section HTML with the widget code

### Example with EmbedSocial:

```html
<div class="embedsocial-hashtag" data-ref="..." data-widget-id="..."></div>
<script>(function(d, s, id){var js; if (d.getElementById(id)) {return;} js = d.createElement(s); js.id = id; js.src = "https://embedsocial.com/embedscript/hashtag.js"; d.getElementsByTagName("head")[0].appendChild(js);}(document, "script", "EmbedSocialHashtagScript"));</script>
```

## Option 5: RSS Feed (If Available)

Some Instagram RSS services exist, but Instagram doesn't officially support RSS. You could use:
- RSS.app
- Zapier
- IFTTT

## Current Implementation

Currently, the site uses **hardcoded fallback posts**. The JavaScript will:
1. Try to fetch from the API if `INSTAGRAM_API_URL` is configured
2. Fall back to hardcoded posts if API fails or isn't configured
3. Display up to 3 posts

## Testing

1. Configure your API endpoint in `js/main.js`
2. Test locally: `python3 -m http.server 8000`
3. Check browser console for any errors
4. Verify posts load correctly

## Notes

- Instagram access tokens expire (short-lived: 1 hour, long-lived: 60 days)
- You'll need to implement token refresh for production
- Rate limits apply (200 requests per hour per user)
- Consider caching responses to reduce API calls

## Security

- Never expose access tokens in client-side code
- Always use environment variables for sensitive data
- Implement rate limiting on your API endpoint
- Use HTTPS for all API calls

