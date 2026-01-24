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

  // Mobile dropdown toggle
  const dropdownToggles = document.querySelectorAll('.nav-dropdown > a');
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      // Only prevent default on mobile
      if (window.innerWidth <= 768) {
        e.preventDefault();
        const parent = this.parentElement;
        parent.classList.toggle('active');
      }
    });
  });

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

  // Implement lazy loading for all images (except those already lazy loaded)
  implementLazyLoading();

  // Generate breadcrumb navigation
  generateBreadcrumbs();

  // Initialize blog search and pagination if on blog page
  initBlogSearch();
  initBlogPagination();
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

/**
 * Implement lazy loading for images
 * Adds loading="lazy" attribute to all images that don't already have it
 */
function implementLazyLoading() {
  // Get all images on the page
  const images = document.querySelectorAll('img');

  images.forEach(img => {
    // Only add lazy loading if it doesn't already have it
    if (!img.hasAttribute('loading')) {
      img.setAttribute('loading', 'lazy');
    }
  });

  // For browsers that don't support native lazy loading, use Intersection Observer
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;

          // If image has a data-src, swap it
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }

          observer.unobserve(img);
        }
      });
    });

    lazyImages.forEach(img => {
      imageObserver.observe(img);
    });
  }
}

/**
 * Generate breadcrumb navigation automatically
 * Creates breadcrumbs based on current URL path
 */
function generateBreadcrumbs() {
  // Skip on homepage
  const path = window.location.pathname;
  if (path === '/' || path === '/index.html' || path.endsWith('/makerlab/') || path.endsWith('/makerlab/index.html')) {
    return;
  }

  // Find the main element to insert breadcrumbs before it
  const main = document.querySelector('main');
  if (!main) return;

  // Create breadcrumb container
  const breadcrumbNav = document.createElement('nav');
  breadcrumbNav.className = 'breadcrumb';
  breadcrumbNav.setAttribute('aria-label', 'Breadcrumb');

  const container = document.createElement('div');
  container.className = 'container';

  const breadcrumbList = document.createElement('ol');
  breadcrumbList.className = 'breadcrumb-list';

  // Always start with Home
  const homeItem = document.createElement('li');
  homeItem.className = 'breadcrumb-item';
  const homeLink = document.createElement('a');
  homeLink.href = path.includes('/blog/') ? '../index.html' : 'index.html';
  homeLink.textContent = 'Home';
  homeItem.appendChild(homeLink);
  breadcrumbList.appendChild(homeItem);

  // Parse path segments
  const pathSegments = path.split('/').filter(segment => segment && segment !== 'makerlab');

  pathSegments.forEach((segment, index) => {
    // Add separator
    const separator = document.createElement('span');
    separator.className = 'breadcrumb-separator';
    separator.textContent = '›';
    separator.setAttribute('aria-hidden', 'true');
    breadcrumbList.appendChild(separator);

    // Create breadcrumb item
    const item = document.createElement('li');
    item.className = 'breadcrumb-item';

    // Format the segment name
    let displayName = segment
      .replace('.html', '')
      .replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());

    // Special cases
    if (displayName === 'Pricingservices') displayName = 'What We Offer';
    if (displayName === 'About Us') displayName = 'About';

    // If this is the last segment, make it active (no link)
    if (index === pathSegments.length - 1) {
      item.className = 'breadcrumb-item active';
      item.textContent = displayName;
      item.setAttribute('aria-current', 'page');
    } else {
      // Create link for intermediate segments
      const link = document.createElement('a');
      // Calculate relative path
      const depth = pathSegments.length - index - 1;
      const prefix = depth > 0 ? '../'.repeat(depth) : '';
      link.href = prefix + segment + (segment.includes('.html') ? '' : '/index.html');
      link.textContent = displayName;
      item.appendChild(link);
    }

    breadcrumbList.appendChild(item);
  });

  container.appendChild(breadcrumbList);
  breadcrumbNav.appendChild(container);

  // Insert breadcrumb before main content
  main.parentNode.insertBefore(breadcrumbNav, main);
}

/**
 * Initialize blog search functionality
 * Filters blog posts in real-time as user types
 */
function initBlogSearch() {
  const searchInput = document.getElementById('blog-search');
  const resultsCount = document.getElementById('search-results-count');
  const postsContainer = document.getElementById('blog-posts-container');

  if (!searchInput || !postsContainer) return;

  const blogPosts = postsContainer.querySelectorAll('.blog-post');
  const totalPosts = blogPosts.length;

  // Show initial count
  if (resultsCount) {
    resultsCount.textContent = `Showing ${totalPosts} posts`;
  }

  // Add search functionality
  searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    let visibleCount = 0;

    blogPosts.forEach(post => {
      const title = post.querySelector('.blog-post-title')?.textContent.toLowerCase() || '';
      const excerpt = post.querySelector('.blog-post-excerpt')?.textContent.toLowerCase() || '';
      const meta = post.querySelector('.blog-post-meta')?.textContent.toLowerCase() || '';

      const matches = title.includes(searchTerm) ||
                     excerpt.includes(searchTerm) ||
                     meta.includes(searchTerm);

      if (matches) {
        post.classList.remove('hidden');
        visibleCount++;
      } else {
        post.classList.add('hidden');
      }
    });

    // Update results count
    if (resultsCount) {
      if (searchTerm === '') {
        resultsCount.textContent = `Showing ${totalPosts} posts`;
      } else {
        resultsCount.textContent = `Found ${visibleCount} of ${totalPosts} posts`;
      }
    }

    // Show no results message if needed
    let noResultsMsg = postsContainer.querySelector('.no-results-message');
    if (visibleCount === 0 && searchTerm !== '') {
      if (!noResultsMsg) {
        noResultsMsg = document.createElement('div');
        noResultsMsg.className = 'no-results-message';
        noResultsMsg.textContent = `No posts found matching "${searchTerm}". Try different keywords.`;
        postsContainer.appendChild(noResultsMsg);
      }
    } else if (noResultsMsg) {
      noResultsMsg.remove();
    }
  });

  // Clear search with Escape key
  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      e.target.value = '';
      e.target.dispatchEvent(new Event('input'));
    }
  });
}

/**
 * Initialize blog pagination
 * Paginates blog posts with configurable items per page
 */
function initBlogPagination() {
  const postsContainer = document.getElementById('blog-posts-container');
  const paginationControls = document.getElementById('pagination-controls');
  const postsPerPageSelect = document.getElementById('posts-per-page');

  if (!postsContainer || !paginationControls) return;

  let currentPage = 1;
  let postsPerPage = parseInt(postsPerPageSelect?.value || 20);
  let allPosts = Array.from(postsContainer.querySelectorAll('.blog-post'));
  let filteredPosts = [...allPosts]; // For search integration

  // Function to get visible posts (considering search filter)
  function getVisiblePosts() {
    return allPosts.filter(post => !post.classList.contains('hidden'));
  }

  // Function to render pagination
  function renderPagination() {
    filteredPosts = getVisiblePosts();
    const totalPages = Math.ceil(filteredPosts.length / postsPerPage);

    // Hide pagination if not needed
    if (totalPages <= 1) {
      paginationControls.style.display = 'none';
      showPage(1);
      return;
    }

    paginationControls.style.display = 'flex';

    // Update prev/next buttons
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');

    if (prevBtn) {
      prevBtn.disabled = currentPage === 1;
    }
    if (nextBtn) {
      nextBtn.disabled = currentPage === totalPages;
    }

    // Render page numbers
    const pageNumbersContainer = document.getElementById('page-numbers');
    if (!pageNumbersContainer) return;

    pageNumbersContainer.innerHTML = '';

    // Calculate which page numbers to show
    const maxButtons = 7;
    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > maxButtons) {
      if (currentPage <= 4) {
        endPage = maxButtons - 1;
      } else if (currentPage >= totalPages - 3) {
        startPage = totalPages - (maxButtons - 2);
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    // Add first page and ellipsis if needed
    if (startPage > 1) {
      addPageButton(1);
      if (startPage > 2) {
        addEllipsis();
      }
    }

    // Add page buttons
    for (let i = startPage; i <= endPage; i++) {
      addPageButton(i);
    }

    // Add ellipsis and last page if needed
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        addEllipsis();
      }
      addPageButton(totalPages);
    }
  }

  // Function to add a page button
  function addPageButton(pageNum) {
    const pageNumbersContainer = document.getElementById('page-numbers');
    const button = document.createElement('button');
    button.className = 'page-number' + (pageNum === currentPage ? ' active' : '');
    button.textContent = pageNum;
    button.addEventListener('click', () => {
      currentPage = pageNum;
      showPage(currentPage);
      renderPagination();
      scrollToTop();
    });
    pageNumbersContainer.appendChild(button);
  }

  // Function to add ellipsis
  function addEllipsis() {
    const pageNumbersContainer = document.getElementById('page-numbers');
    const ellipsis = document.createElement('span');
    ellipsis.className = 'page-number ellipsis';
    ellipsis.textContent = '...';
    pageNumbersContainer.appendChild(ellipsis);
  }

  // Function to show specific page
  function showPage(page) {
    filteredPosts = getVisiblePosts();
    const startIndex = (page - 1) * postsPerPage;
    const endIndex = startIndex + postsPerPage;

    // Hide all posts first
    allPosts.forEach(post => {
      post.style.display = 'none';
    });

    // Show only posts for current page (that aren't filtered out by search)
    filteredPosts.forEach((post, index) => {
      if (index >= startIndex && index < endIndex) {
        post.style.display = 'block';
      }
    });
  }

  // Function to scroll to top of blog posts
  function scrollToTop() {
    const searchSection = document.querySelector('.blog-search-section');
    if (searchSection) {
      searchSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  // Event listeners for prev/next buttons
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
        renderPagination();
        scrollToTop();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      const totalPages = Math.ceil(filteredPosts.length / postsPerPage);
      if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
        renderPagination();
        scrollToTop();
      }
    });
  }

  // Event listener for posts per page change
  if (postsPerPageSelect) {
    postsPerPageSelect.addEventListener('change', (e) => {
      postsPerPage = parseInt(e.target.value);
      currentPage = 1;
      renderPagination();
      showPage(currentPage);
    });
  }

  // Listen for search changes to update pagination
  const searchInput = document.getElementById('blog-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      currentPage = 1;
      renderPagination();
      showPage(currentPage);
    });
  }

  // Initial render
  renderPagination();
  showPage(currentPage);
}
