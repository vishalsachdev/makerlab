/**
 * Illinois MakerLab - Main JavaScript
 */

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mainNav = document.querySelector('.main-nav');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
      mainNav.classList.toggle('active');
      const isOpen = mainNav.classList.contains('active');
      menuToggle.setAttribute('aria-expanded', isOpen);
      menuToggle.innerHTML = isOpen ? '&times;' : '&#9776;';
    });
  }

  // Active navigation link
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.main-nav a');

  navLinks.forEach(link => {
    const linkPath = new URL(link.href).pathname;
    if (linkPath === currentPath ||
        (currentPath.includes('/blog/') && linkPath.includes('/blog'))) {
      link.classList.add('active');
    }
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href !== '#') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // Gallery lightbox (simple implementation)
  const galleryItems = document.querySelectorAll('.gallery-item img');
  galleryItems.forEach(img => {
    img.addEventListener('click', function() {
      // Simple lightbox - just open in new window
      // Can be enhanced with a proper lightbox library
      window.open(this.src, '_blank');
    });
  });

  // Form validation (if forms exist)
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const requiredFields = this.querySelectorAll('[required]');
      let isValid = true;

      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('error');
        } else {
          field.classList.remove('error');
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert('Please fill in all required fields.');
      }
    });
  });

  // Back to top button (if added)
  const backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    });

    backToTop.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // External links - open in new tab
  const externalLinks = document.querySelectorAll('a[href^="http"]');
  externalLinks.forEach(link => {
    if (!link.href.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });

  // Load Instagram feed
  loadInstagramFeed();
});

/**
 * Load Instagram feed - fetches latest 3 posts
 * 
 * Options:
 * 1. Use Instagram Basic Display API via backend proxy (set INSTAGRAM_API_URL)
 * 2. Use Instagram oEmbed API for specific posts (set INSTAGRAM_POST_IDS)
 * 3. Use fallback hardcoded posts (default)
 */
async function loadInstagramFeed() {
  const feedContainer = document.getElementById('instagram-feed');
  if (!feedContainer) return;

  // Configuration Options:
  
  // Option 1: Backend API endpoint (serverless function)
  // Set this to your API endpoint URL
  const INSTAGRAM_API_URL = ''; // e.g., 'https://your-domain.vercel.app/api/instagram'
  
  // Option 2: Specific Instagram post IDs to fetch via oEmbed
  // Format: ['post_id_1', 'post_id_2', 'post_id_3']
  // Update these IDs to show different posts
  const INSTAGRAM_POST_IDS = ['CLTDNYFLLkA', 'CLDrKwYLVUE', 'CKpCwXwrGLU'];
  
  // Try Option 1: Backend API
  if (INSTAGRAM_API_URL) {
    try {
      const response = await fetch(INSTAGRAM_API_URL, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });

      if (response.ok) {
        const data = await response.json();
        
        // Expected API response format:
        // {
        //   "posts": [
        //     {
        //       "id": "post_id",
        //       "permalink": "https://www.instagram.com/p/...",
        //       "media_url": "https://...",
        //       "caption": "Post caption...",
        //       "timestamp": "2024-01-01T00:00:00Z"
        //     }
        //   ]
        // }

        if (data.posts && Array.isArray(data.posts) && data.posts.length > 0) {
          feedContainer.innerHTML = '';
          const postsToShow = data.posts.slice(0, 3);
          postsToShow.forEach(post => {
            const postElement = createInstagramPostElement(post);
            feedContainer.appendChild(postElement);
          });
          return; // Success, exit early
        }
      }
    } catch (error) {
      console.error('Error loading Instagram feed from API:', error);
    }
  }

  // Try Option 2: oEmbed API (for specific posts)
  if (INSTAGRAM_POST_IDS.length > 0) {
    try {
      const posts = await Promise.all(
        INSTAGRAM_POST_IDS.slice(0, 3).map(async (postId) => {
          try {
            const response = await fetch(
              `https://api.instagram.com/oembed/?url=https://www.instagram.com/p/${postId}/&omitscript=true`
            );
            if (response.ok) {
              const data = await response.json();
              return {
                id: postId,
                permalink: `https://www.instagram.com/p/${postId}/`,
                media_url: data.thumbnail_url,
                caption: data.title || ''
              };
            }
          } catch (e) {
            console.error(`Error fetching post ${postId}:`, e);
          }
          return null;
        })
      );

      const validPosts = posts.filter(post => post !== null);
      if (validPosts.length > 0) {
        feedContainer.innerHTML = '';
        validPosts.forEach(post => {
          const postElement = createInstagramPostElement(post);
          feedContainer.appendChild(postElement);
        });
        return; // Success, exit early
      }
    } catch (error) {
      console.error('Error loading Instagram feed via oEmbed:', error);
    }
  }

  // Option 3: Fallback - keep hardcoded posts
  console.log('Using fallback Instagram posts. Configure INSTAGRAM_API_URL or INSTAGRAM_POST_IDS to enable automatic fetching.');
}

/**
 * Create Instagram post HTML element
 */
function createInstagramPostElement(post) {
  const link = document.createElement('a');
  link.href = post.permalink || `https://www.instagram.com/p/${post.id}/`;
  link.className = 'instagram-item';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';

  const img = document.createElement('img');
  img.src = post.media_url || post.thumbnail_url || '';
  img.alt = post.caption ? post.caption.substring(0, 100) : 'Instagram post';
  img.loading = 'lazy';

  link.appendChild(img);
  return link;
}

// Utility function to format dates
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

// Utility function to create slugs from titles
function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-');
}
