# GitHub Pages Deployment Guide

This guide provides step-by-step instructions for hosting the Illinois MakerLab website on GitHub Pages.

## 🚀 Quick Start

The repository is already configured for GitHub Pages deployment! You just need to enable it.

## Prerequisites

- A GitHub account
- This repository pushed to GitHub

## Deployment Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/vishalsachdev/makerlab`
2. Click on **Settings** (in the repository menu)
3. In the left sidebar, click **Pages**
4. Under "Build and deployment":
   - **Source**: Select **"GitHub Actions"** from the dropdown
   - (NOT "Deploy from a branch" - that's the old method)
5. The page will refresh - you're done with settings!

### 2. Trigger Deployment

The site will automatically deploy when you push to the `main` branch. However, since the workflow is already set up, you can trigger a manual deployment:

1. Go to the **Actions** tab in your repository
2. Click on **"Deploy static content to Pages"** workflow in the left sidebar
3. Click the **"Run workflow"** button on the right
4. Select the `main` branch
5. Click **"Run workflow"**

### 3. Monitor Deployment

1. Stay on the **Actions** tab
2. You'll see a new workflow run appear
3. Click on it to see the deployment progress
4. Wait for the green checkmark ✅ (usually takes 30-60 seconds)

### 4. Access Your Site

Once deployment is complete:

- Your site will be available at: **`https://vishalsachdev.github.io/makerlab/`**
- The URL is shown in the workflow run completion message
- You can also find it in Settings → Pages

## 🎯 What Was Configured

The repository now includes:

1. **`.github/workflows/static.yml`**: GitHub Actions workflow that automatically deploys the site
2. **`.nojekyll`**: Prevents Jekyll processing (we're using plain HTML)
3. **`.gitignore`**: Excludes temporary files and build artifacts from version control

## 📝 Automatic Deployments

After the initial setup, every push to the `main` branch will automatically trigger a new deployment:

```bash
git add .
git commit -m "Update content"
git push origin main
```

The site will automatically redeploy within 1-2 minutes.

## 🌐 Custom Domain (Optional)

To use a custom domain like `makerlab.illinois.edu`:

### Step 1: Add CNAME File

Create a file named `CNAME` (no extension) in the repository root with your domain:

```
makerlab.illinois.edu
```

### Step 2: Configure DNS

Add DNS records at your domain provider:

For a subdomain (e.g., `makerlab.illinois.edu`):
```
Type: CNAME
Name: makerlab
Value: vishalsachdev.github.io
```

For an apex domain (e.g., `example.com`):
```
Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

### Step 3: Configure in GitHub

1. Go to Settings → Pages
2. Under "Custom domain", enter your domain
3. Click **Save**
4. Wait for DNS check to complete
5. Enable "Enforce HTTPS" (recommended)

## 🔍 Troubleshooting

### Site not loading?

- Check the Actions tab for deployment errors
- Ensure GitHub Pages is enabled in Settings → Pages
- Verify the Source is set to "GitHub Actions"
- Wait 1-2 minutes after deployment completes

### Images not showing?

The site uses images hosted on Squarespace CDN. If images don't load:
- Check your internet connection
- The CDN URLs might have changed - you may need to download images and host them locally

### CSS not loading?

The site uses absolute paths (e.g., `/css/style.css`). These work correctly with GitHub Pages when deployed via Actions.

### 404 errors on navigation?

Ensure all HTML files are committed to the repository. Check that file names match the links exactly (case-sensitive).

## 📊 Monitoring

You can monitor your site's deployment and performance:

1. **Actions Tab**: See all deployment runs and their status
2. **Settings → Pages**: View the current deployment URL and status
3. **Insights → Traffic**: See visitor statistics (after enabling in Settings)

## 🔐 Security

The workflow uses GitHub's built-in security:

- Minimal permissions (read contents, write pages)
- Runs in isolated environment
- No secrets needed for basic deployment

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## ✅ Verification Checklist

Before considering deployment complete:

- [ ] GitHub Pages enabled in Settings → Pages
- [ ] Source set to "GitHub Actions"
- [ ] Workflow run completed successfully (green checkmark)
- [ ] Site accessible at `https://vishalsachdev.github.io/makerlab/`
- [ ] Home page loads correctly
- [ ] Navigation works
- [ ] CSS styles applied
- [ ] Blog pages accessible

## 🆘 Getting Help

If you encounter issues:

1. Check the Actions tab for detailed error messages
2. Review the workflow logs
3. Ensure your repository is public (or GitHub Pages is enabled for private repos)
4. Verify you have the necessary repository permissions

---

**🎉 Congratulations!** Your Illinois MakerLab website is now live on GitHub Pages!
