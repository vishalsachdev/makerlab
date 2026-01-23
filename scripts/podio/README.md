# Podio Blog Generator

Monthly workflow to extract MakerLab orders from Podio and generate blog post drafts.

## Setup (One-time)

1. Get Podio API credentials from https://developers.podio.com/api-key
   - Application name: `claude` (or any name)
   - Domain: `localhost`

2. Create `.env` file:
   ```
   PODIO_CLIENT_ID=your_client_id
   PODIO_CLIENT_SECRET=your_client_secret
   PODIO_USERNAME=uimakerlab@illinois.edu
   PODIO_PASSWORD=your_password
   ```

3. Install dependencies:
   ```bash
   pip install requests python-dotenv
   ```

## Monthly Workflow

Run this workflow at the start of each month to find blog-worthy orders from the previous month.

### Step 1: Extract Orders
```bash
cd /Users/vishal/code/podio
python extract_orders.py
```
This creates `orders_extract.json` with the 50 most recent orders.

### Step 2: Analyze with Claude Code
Open Claude Code and ask:
```
Analyze orders_extract.json and identify blog-worthy orders.
Look for research projects, student innovations, interesting applications,
or compelling stories. Draft blog posts for the best candidates.
```

### Step 3: Fetch Images
Edit `fetch_images.py` to update the `BLOG_ORDERS` list with item IDs of orders you want images for, then:
```bash
python fetch_images.py
```
Images download to `/Users/vishal/code/makerlab/images/blog/`

### Step 4: Review & Publish
- Blog posts are created in `/Users/vishal/code/makerlab/blog/`
- Review drafts, add images where marked `<!-- TODO -->`
- Commit and push to publish

## Useful Commands

```bash
# Test connection / list all workspaces and apps
python podio_client.py

# Deep-dive into a specific order
python inspect_order.py <item_id>
```

## Key IDs

- **Organization**: Illinois MakerLab (528575)
- **Workspace**: Daily Activities (1801600)
- **Orders App**: 6976602

## Notes

- GlobiMail integrates emails as comments on orders
- Most "images" in Podio are email signature icons - filter by size >10KB for real photos
- Blog posts use order date + 15 days as publication date
