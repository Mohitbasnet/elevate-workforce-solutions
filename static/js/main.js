// Corporate Professional JavaScript for Elevate Workforce Solutions
// Enhanced interactions for professional user experience

document.addEventListener('DOMContentLoaded', function() {
    // === CORPORATE NAVBAR ENHANCEMENTS === //
    initializeNavbar();
    
    // === PROFESSIONAL ANIMATIONS === //
    initializeAnimations();
    
    // === CORPORATE FORM ENHANCEMENTS === //
    enhanceForms();
    
    // === PROFESSIONAL LOADING STATES === //
    initializeLoadingStates();
    
    // === CORPORATE TOOLTIPS & POPOVERS === //
    initializeTooltips();
    
    // === PROFESSIONAL SEARCH ENHANCEMENTS === //
    enhanceSearchFunctionality();
    
    // === CORPORATE CARD INTERACTIONS === //
    enhanceCardInteractions();
    
    // === PROFESSIONAL PAGE TRANSITIONS === //
    initializePageTransitions();
});

// === CORPORATE NAVBAR FUNCTIONALITY === //
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Professional scroll behavior
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scroll shadow effect
        if (scrollTop > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    }, { passive: true });
    
    // Enhanced nav link interactions
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// === PROFESSIONAL ANIMATIONS === //
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-up');
            }
        });
    }, observerOptions);
    
    // Observe corporate elements
    const elementsToAnimate = document.querySelectorAll(
        '.job-card, .dashboard-card, .stat-item, .card'
    );
    
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
    
    // Professional counter animations
    animateCounters();
}

// === CORPORATE COUNTER ANIMATIONS === //
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number, .dashboard-stat-number');
    
    const countUp = (element, target) => {
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.floor(current);
            
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 20);
    };
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                const target = parseInt(entry.target.textContent);
                entry.target.classList.add('counted');
                countUp(entry.target, target);
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// === CORPORATE FORM ENHANCEMENTS === //
function enhanceForms() {
    const formControls = document.querySelectorAll('.form-control, .form-select');
    const forms = document.querySelectorAll('form');
    
    // Professional input interactions
    formControls.forEach(input => {
        // Enhanced focus states
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            this.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            this.style.transform = 'scale(1)';
        });
        
        // Professional validation feedback
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
    
    // Professional form submission
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });
}

// === PROFESSIONAL LOADING STATES === //
function initializeLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Store original content
        const originalContent = button.innerHTML;
        
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.classList.contains('loading-btn')) {
                // Add professional loading state
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                
                // Create loading overlay
                const loadingOverlay = document.createElement('div');
                loadingOverlay.style.cssText = `
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(255, 255, 255, 0.9);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1;
                `;
                loadingOverlay.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                
                this.appendChild(loadingOverlay);
                
                // Remove loading state after delay (if not a real form submission)
                if (!this.type === 'submit') {
                    setTimeout(() => {
                        this.removeChild(loadingOverlay);
                    }, 1500);
                }
            }
        });
    });
}

// === CORPORATE TOOLTIPS & POPOVERS === //
function initializeTooltips() {
    // Initialize Bootstrap tooltips with corporate styling
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            container: 'body',
            delay: { show: 300, hide: 100 }
        });
    });
    
    // Professional hover cards
    const cards = document.querySelectorAll('.job-card, .dashboard-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.zIndex = '1';
        });
    });
}

// === PROFESSIONAL SEARCH ENHANCEMENTS === //
function enhanceSearchFunctionality() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name*="search"]');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        // Professional search with debouncing
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchIcon = this.parentElement.querySelector('i');
            
            if (searchIcon) {
                searchIcon.className = 'fas fa-spinner fa-spin';
            }
            
            searchTimeout = setTimeout(() => {
                if (searchIcon) {
                    searchIcon.className = 'fas fa-search';
                }
                // Add your search logic here
                console.log('Searching for:', this.value);
            }, 500);
        });
        
        // Professional search suggestions (placeholder for future enhancement)
        input.addEventListener('focus', function() {
            // Could add dropdown suggestions here
        });
    });
}

// === CORPORATE CARD INTERACTIONS === //
function enhanceCardInteractions() {
    const jobCards = document.querySelectorAll('.job-card');
    
    jobCards.forEach(card => {
        // Professional card click behavior
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a, button')) {
                const jobLink = this.querySelector('.job-title a');
                if (jobLink) {
                    // Add professional transition effect
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        window.location.href = jobLink.href;
                    }, 150);
                }
            }
        });
        
        // Professional bookmark functionality (placeholder)
        const bookmarkBtn = card.querySelector('.bookmark-btn');
        if (bookmarkBtn) {
            bookmarkBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                
                const icon = this.querySelector('i');
                if (icon.classList.contains('far')) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    this.classList.add('bookmarked');
                    showNotification('Job bookmarked successfully!', 'success');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                    this.classList.remove('bookmarked');
                    showNotification('Bookmark removed', 'info');
                }
            });
        }
    });
}

// === PROFESSIONAL PAGE TRANSITIONS === //
function initializePageTransitions() {
    const links = document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.target !== '_blank' && !this.classList.contains('no-transition')) {
                // Add professional page transition effect
                document.body.style.opacity = '0.95';
                document.body.style.transform = 'scale(0.99)';
                document.body.style.transition = 'all 0.2s ease-out';
            }
        });
    });
}

// === PROFESSIONAL NOTIFICATION SYSTEM === //
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: var(--shadow-lg);
        border: none;
    `;
    
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 4000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// === CORPORATE PERFORMANCE OPTIMIZATIONS === //
// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// === CORPORATE ACCESSIBILITY ENHANCEMENTS === //
document.addEventListener('keydown', function(e) {
    // Professional keyboard navigation
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// === CORPORATE LOCAL STORAGE ENHANCEMENTS === //
const CorporateStorage = {
    setItem: function(key, value) {
        try {
            localStorage.setItem(`elevate_${key}`, JSON.stringify(value));
        } catch (e) {
            console.warn('Corporate Storage: Unable to save to localStorage');
        }
    },
    
    getItem: function(key) {
        try {
            const item = localStorage.getItem(`elevate_${key}`);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.warn('Corporate Storage: Unable to read from localStorage');
            return null;
        }
    },
    
    removeItem: function(key) {
        try {
            localStorage.removeItem(`elevate_${key}`);
        } catch (e) {
            console.warn('Corporate Storage: Unable to remove from localStorage');
        }
    }
};

// === CORPORATE FORM AUTO-SAVE === //
function initializeAutoSave() {
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    
    autoSaveForms.forEach(form => {
        const formId = form.getAttribute('data-auto-save');
        const inputs = form.querySelectorAll('input, textarea, select');
        
        // Load saved data
        const savedData = CorporateStorage.getItem(`form_${formId}`);
        if (savedData) {
            inputs.forEach(input => {
                if (savedData[input.name]) {
                    input.value = savedData[input.name];
                }
            });
        }
        
        // Save on input
        const saveData = debounce(() => {
            const formData = {};
            inputs.forEach(input => {
                formData[input.name] = input.value;
            });
            CorporateStorage.setItem(`form_${formId}`, formData);
        }, 1000);
        
        inputs.forEach(input => {
            input.addEventListener('input', saveData);
        });
        
        // Clear on successful submit
        form.addEventListener('submit', () => {
            CorporateStorage.removeItem(`form_${formId}`);
        });
    });
}

// Initialize auto-save after DOM is loaded
document.addEventListener('DOMContentLoaded', initializeAutoSave);

// === CORPORATE ANALYTICS TRACKING === //
function trackCorporateEvent(category, action, label = null) {
    // Placeholder for corporate analytics tracking
    console.log('Corporate Event:', { category, action, label });
    
    // Integration point for Google Analytics, Adobe Analytics, etc.
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            event_category: category,
            event_label: label
        });
    }
}

// === CORPORATE ERROR HANDLING === //
window.addEventListener('error', function(e) {
    console.error('Corporate Error:', e.error);
    // Could send to error tracking service here
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Corporate Unhandled Promise Rejection:', e.reason);
    // Could send to error tracking service here
});

// === CORPORATE FEATURE FLAGS === //
const CorporateFeatures = {
    enableAdvancedSearch: true,
    enableNotifications: true,
    enableAutoSave: true,
    enableAnalytics: false
};

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CorporateStorage,
        trackCorporateEvent,
        showNotification,
        CorporateFeatures
    };
} 