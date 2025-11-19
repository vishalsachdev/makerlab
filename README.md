# Illinois MakerLab Website

A complete replica of the Illinois MakerLab website (https://makerlab.illinois.edu/) built with static HTML, CSS, and JavaScript.

**🚀 Live Site**: [https://vishalsachdev.github.io/makerlab/](https://vishalsachdev.github.io/makerlab/)

> 📖 **New to GitHub Pages?** See [docs/deployment/DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md) for detailed step-by-step deployment instructions.

## About

The Illinois MakerLab is the world's first business school 3D printing lab at the University of Illinois at Urbana-Champaign. This website showcases:

- **Learn. Make. Share.** - Our core philosophy
- Information about our 3D printing services and equipment
- Course offerings (on-campus and online)
- Summer camps for youth
- Blog with 291+ posts from 2012-2025
- Resources, workshops, and tutorials

## Project Structure

```
makerlab/
├── index.html              # Homepage
├── about-us.html          # About page
├── courses.html           # Courses overview
├── pricingservices.html   # Services & pricing
├── resources.html         # 3D printing resources
├── contact.html           # Contact information
├── lab-hours.html         # Lab hours
├── [40+ more pages]       # Additional pages
├── blog/
│   ├── index.html        # Blog listing page
│   └── [291 posts].html  # Individual blog posts
├── courses/
│   ├── digital-making.html
│   └── making-things.html
├── summer/
│   └── [camp pages].html
├── css/
│   └── style.css         # Main stylesheet
├── js/
│   └── main.js          # JavaScript functionality
└── images/              # Image assets
```

## Features

✅ **45 Complete Pages** - All content from original site
✅ **291 Blog Posts** - Full blog archive from 2012-2025
✅ **Responsive Design** - Mobile-friendly layout
✅ **Illinois Brand Toolkit** - Integrated with official campus toolkit (v3.x)
✅ **Illinois Branding** - Official orange (#FF5F05) and blue (#13294B) colors
✅ **Accessible Navigation** - Sticky header with mobile menu
✅ **Clean Modern Design** - Card layouts, smooth transitions
✅ **SEO Friendly** - Semantic HTML, meta tags

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript** - No dependencies
- **Responsive Design** - Mobile-first approach
- **Illinois Campus Brand Toolkit** - Official UI components and styling (v3.x)

## Brand Toolkit Integration

The site integrates the official [University of Illinois Campus Brand Toolkit](https://builder3.toolkit.illinois.edu/) to ensure campus-wide visual consistency and accessibility standards.

**Integrated Resources:**
- Toolkit CSS: `//cdn.toolkit.illinois.edu/3/toolkit.css`
- Toolkit JS: `//cdn.toolkit.illinois.edu/3/toolkit.js`

**Brand Compliance:**
- ✅ Official Illinois Orange (#FF5F05) and Blue (#13294B)
- ✅ Toolkit components available for future enhancements
- ✅ Accessibility best practices
- 📋 Typography update planned (Montserrat/Source Sans Pro)

For detailed integration documentation, see [docs/integration/BRAND_TOOLKIT_INTEGRATION.md](docs/integration/BRAND_TOOLKIT_INTEGRATION.md). Run `python3 scripts/add_toolkit.py` whenever you regenerate or add HTML so every page continues to load the toolkit CSS/JS before the MakerLab assets.

## Pages Included

### Main Pages
- Home
- About Us
- What We Offer
- Courses (Digital Making, Making Things, Online Courses)
- Summer Camps
- Blog
- Resources
- Lab Hours
- Contact
- FAQ
- Workshops
- Gallery
- Lab Staff
- Partners

### Additional Pages
- Online Ordering
- Birthday Parties
- 3D Printing Conference
- Free Print Wednesdays
- Internship Database
- Practicum
- Certificate Program
- Volunteer Information
- Give to MakerLab
- Summer Jobs
- COVID-19 Response
- And more...

## Deployment

### GitHub Pages (Recommended)

This site is configured for automatic deployment to GitHub Pages using GitHub Actions:

#### Setup Instructions:

1. **Push your changes** to the `main` branch
2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: Select **"GitHub Actions"**
   - Click **Save**
3. **Automatic Deployment**:
   - The GitHub Actions workflow (`.github/workflows/static.yml`) will automatically deploy your site
   - Check the **Actions** tab to monitor deployment progress
   - Once complete, your site will be live!

Your site will be available at: `https://vishalsachdev.github.io/makerlab/`

#### Manual Trigger:
You can also manually trigger deployment from the **Actions** tab by running the "Deploy static content to Pages" workflow.

#### Custom Domain (Optional):
To use a custom domain:
1. Add a `CNAME` file with your domain name to the repository root
2. Configure your domain's DNS settings to point to GitHub Pages
3. In GitHub Settings → Pages, enter your custom domain

### Other Hosting

This is a static site and can be hosted anywhere:
- Netlify
- Vercel
- AWS S3
- Any web server

Simply upload all files maintaining the directory structure.

## Local Development

To view locally, you can use any static server:

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx http-server

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000` in your browser.

## Content Source

Content was exported from the original Squarespace site on 11/18/2025 using the WordPress export format (WXR). All content, including images, is preserved from the original site.

## Images

Images are now hosted locally in the `/images` directory, organized by category:
- `images/blog/` - Blog post images (737 images)
- `images/general/` - General site images
- `images/summer/` - Summer camp images
- `images/events/` - Event and workshop images
- `images/staff/` - Staff photos

All Squarespace CDN URLs have been replaced with local GitHub paths.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Credits

**Original Site:** Illinois MakerLab
**Executive Director:** Dr. Aric Rindfleisch
**Director:** Dr. Vishal Sachdev
**Location:** Business Instructional Facility, Room 3030, UIUC

## License

Content © Illinois MakerLab. All rights reserved.

## Contact

For questions about the MakerLab:
- Email: uimakerlab@illinois.edu
- Location: Room 3030, Business Instructional Facility, 515 East Gregory Drive, Champaign, IL 61820
- Instagram: [@uimakerlab](https://www.instagram.com/uimakerlab/)
- Facebook: [Illinois MakerLab](https://www.facebook.com/uimakerlab/)

---

**Built with ❤️ for the Maker Movement**
