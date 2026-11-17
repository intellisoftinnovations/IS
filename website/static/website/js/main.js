/* ==========================================================================
   IntelliSoft Innovations — Main JavaScript (Enhanced)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // 1. DARK MODE TOGGLE
    // =========================================================================
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Load saved theme or respect system preference
    const savedTheme = localStorage.getItem('intellisoft-theme');
    if (savedTheme) {
        html.setAttribute('data-theme', savedTheme);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        html.setAttribute('data-theme', 'dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('intellisoft-theme', next);
        });
    }


    // =========================================================================
    // 2. MOBILE NAVIGATION — Fixed fullscreen overlay approach
    // =========================================================================
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = navMenu.classList.contains('open');
            
            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        function openMenu() {
            navToggle.classList.add('active');
            navMenu.classList.add('open');
            navToggle.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            navToggle.classList.remove('active');
            navMenu.classList.remove('open');
            navToggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }

        // Close mobile menu when a link is clicked
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', closeMenu);
        });

        // Close mobile menu when CTA button is clicked
        navMenu.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', closeMenu);
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('open')) {
                closeMenu();
            }
        });

        // Ensure menu closes if resized to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && navMenu.classList.contains('open')) {
                closeMenu();
            }
        });
    }


    // =========================================================================
    // 3. NAVBAR SCROLL EFFECTS
    // =========================================================================
    const navbar = document.getElementById('navbar');

    if (navbar) {
        let ticking = false;
        const onScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    if (window.scrollY > 10) {
                        navbar.classList.add('scrolled');
                    } else {
                        navbar.classList.remove('scrolled');
                    }
                    ticking = false;
                });
                ticking = true;
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }


    // =========================================================================
    // 4. SCROLL-TRIGGERED FADE-IN ANIMATIONS — Enhanced stagger
    // =========================================================================
    const fadeElements = document.querySelectorAll('.fade-in');

    if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -30px 0px'
        });

        fadeElements.forEach(el => observer.observe(el));
    } else {
        // Fallback: show all elements immediately
        fadeElements.forEach(el => el.classList.add('visible'));
    }


    // =========================================================================
    // 5. PORTFOLIO CATEGORY FILTERING — Enhanced with animation
    // =========================================================================
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioCards = document.querySelectorAll('.portfolio-card[data-category]');

    if (filterButtons.length > 0 && portfolioCards.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;

                // Update active button
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Filter cards with staggered animation
                let visibleIndex = 0;
                portfolioCards.forEach(card => {
                    const category = card.dataset.category;
                    const shouldShow = filter === 'all' || category === filter;

                    if (shouldShow) {
                        card.style.display = '';
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        
                        // Stagger the re-entry
                        const delay = visibleIndex * 80;
                        setTimeout(() => {
                            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, delay);
                        visibleIndex++;
                    } else {
                        card.style.transition = 'opacity 0.2s ease';
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 200);
                    }
                });
            });
        });
    }


    // =========================================================================
    // 6. ACTIVE NAV LINK HIGHLIGHTING
    // =========================================================================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath === href) {
            link.classList.add('active');
        } else if (href && href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });


    // =========================================================================
    // 7. SMOOTH SCROLL FOR ANCHOR LINKS
    // =========================================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                const navHeight = navbar ? navbar.offsetHeight : 0;
                const targetPos = targetEl.getBoundingClientRect().top + window.scrollY - navHeight - 20;
                window.scrollTo({ top: targetPos, behavior: 'smooth' });
            }
        });
    });


    // =========================================================================
    // 8. FORM ENHANCEMENT — Real-time field validation
    // =========================================================================
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        const requiredFields = contactForm.querySelectorAll('[required], #contact-name, #contact-email, #contact-details');
        
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => {
                if (field.value.trim()) {
                    field.style.borderColor = '';
                } else if (field.hasAttribute('required') || ['contact-name', 'contact-email', 'contact-details'].includes(field.id)) {
                    // Don't add error on blur for optional fields
                }
            });

            field.addEventListener('input', () => {
                // Remove error state on input
                const errorEl = field.parentElement.querySelector('.form-error');
                if (errorEl && field.value.trim()) {
                    errorEl.style.display = 'none';
                    field.style.borderColor = '';
                }
            });
        });
    }


    // =========================================================================
    // 9. LIVE UI DESIGN STUDIO — Interactive Style Switcher in Hero
    // =========================================================================
    const styleTabs = document.querySelectorAll('.style-tab-btn');
    const demoCard = document.getElementById('style-demo-card');
    const demoBadge = document.getElementById('demo-badge-text');
    const demoDeployBtn = document.getElementById('hero-demo-deploy-btn');
    const demoDeployText = document.getElementById('demo-deploy-text');
    const demoSwitch = document.getElementById('hero-demo-switch');
    const demoSlider = document.getElementById('hero-demo-slider');
    const demoPodText = document.getElementById('demo-pod-text');
    const demoMetricVal = document.getElementById('demo-metric-val');

    const styleMeta = {
        'glassmorphism': {
            badge: 'Glassmorphic UI',
            deployText: 'Deploy Glassmorphic Build',
            metric: '2,400 req/s'
        },
        'neumorphism': {
            badge: 'Neumorphic Soft UI',
            deployText: 'Engage Tactile System',
            metric: '2,850 req/s'
        },
        'minimalist': {
            badge: 'Minimalist SaaS',
            deployText: 'Ship Clean Production',
            metric: '3,200 req/s'
        },
        'cyber': {
            badge: 'Cyber Matrix Console',
            deployText: 'EXECUTE DEPLOY --PROD',
            metric: '4,150 req/s'
        }
    };

    if (styleTabs.length > 0 && demoCard) {
        styleTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetStyle = tab.dataset.style;

                // Update active tab button
                styleTabs.forEach(t => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                });
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');

                // Morph demo card classes
                demoCard.classList.remove(
                    'style-glassmorphism',
                    'style-neumorphism',
                    'style-minimalist',
                    'style-cyber'
                );
                demoCard.classList.add(`style-${targetStyle}`);

                // Update text elements with subtle animation
                const meta = styleMeta[targetStyle];
                if (meta) {
                    if (demoBadge) demoBadge.textContent = meta.badge;
                    if (demoDeployText) demoDeployText.textContent = meta.deployText;
                    if (demoMetricVal) demoMetricVal.textContent = meta.metric;
                }
            });
        });

        // Hero demo switch toggle (mouse + keyboard)
        if (demoSwitch) {
            const toggleDemoSwitch = () => {
                const isActive = demoSwitch.classList.toggle('active');
                demoSwitch.setAttribute('aria-checked', isActive ? 'true' : 'false');
            };
            demoSwitch.addEventListener('click', toggleDemoSwitch);
            demoSwitch.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleDemoSwitch();
                }
            });
        }

        // Hero demo slider concurrency
        if (demoSlider && demoPodText) {
            demoSlider.addEventListener('input', (e) => {
                const pods = e.target.value;
                demoPodText.textContent = `${pods} Pods Active`;
                if (demoMetricVal) {
                    const rps = Math.round(Number(pods) * 52);
                    demoMetricVal.textContent = `${rps.toLocaleString()} req/s`;
                }
            });
        }

        // Hero demo deploy button feedback
        if (demoDeployBtn) {
            demoDeployBtn.addEventListener('click', () => {
                const originalText = demoDeployText ? demoDeployText.textContent : 'Deploy';
                if (demoDeployText) demoDeployText.textContent = '✓ Build Deployed to Cluster!';
                demoDeployBtn.style.opacity = '0.9';
                setTimeout(() => {
                    if (demoDeployText) demoDeployText.textContent = originalText;
                    demoDeployBtn.style.opacity = '';
                }, 1600);
            });
        }
    }


    // =========================================================================
    // 9.1 DESIGN SYSTEMS MINI SANDBOX INTERACTIONS
    // =========================================================================
    document.querySelectorAll('[data-sandbox-action]').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.sandboxAction;
            if (action === 'neu') {
                btn.style.transform = 'scale(0.95)';
                setTimeout(() => { btn.style.transform = ''; }, 150);
            } else if (action === 'glass') {
                btn.style.transform = 'translateY(-2px)';
                setTimeout(() => { btn.style.transform = ''; }, 200);
            } else if (action === 'minimal') {
                btn.style.background = '#2563EB';
                btn.style.color = '#FFFFFF';
                setTimeout(() => { btn.style.background = ''; btn.style.color = ''; }, 300);
            } else if (action === 'cyber') {
                const original = btn.textContent;
                btn.textContent = 'ONLINE (12ms)';
                setTimeout(() => { btn.textContent = original; }, 1200);
            }
        });
    });


    // =========================================================================
    // 10. INTERACTIVE PROJECT SCOPE & COST ESTIMATOR (Business Logic)
    // =========================================================================
    const solutionBtns = document.querySelectorAll('#estimator-solution-group .estimator-option-btn');
    const styleBtns = document.querySelectorAll('#estimator-style-group .estimator-option-btn');
    const moduleChecks = document.querySelectorAll('#estimator-modules-group .estimator-check-card');
    const tierBtns = document.querySelectorAll('#estimator-tier-group .estimator-option-btn');

    // Blueprint output DOM targets
    const calcPriceDisplay = document.getElementById('calc-price-display');
    const calcTimelineDisplay = document.getElementById('calc-timeline-display');
    const calcSolutionName = document.getElementById('calc-solution-name');
    const calcStyleName = document.getElementById('calc-style-name');
    const calcTierName = document.getElementById('calc-tier-name');
    const calcStackName = document.getElementById('calc-stack-name');
    const calcTeamName = document.getElementById('calc-team-name');
    const estimatorInquireBtn = document.getElementById('estimator-inquire-btn');

    // Math breakdown DOM targets
    const calcBaseSubtotal = document.getElementById('calc-base-subtotal');
    const calcFeatCount = document.getElementById('calc-feat-count');
    const calcFeatSubtotal = document.getElementById('calc-feat-subtotal');
    const calcTierMultiplier = document.getElementById('calc-tier-multiplier');
    const calcCombinedSubtotal = document.getElementById('calc-combined-subtotal');

    // Architecture fallback mappings if not provided in data attributes
    const architectureStacks = {
        'webapps': {
            stack: 'Django 5.1 • React 19 • Postgres • Redis',
            team: '1 Lead Architect, 2 Senior Devs, 1 UI/UX'
        },
        'software': {
            stack: 'FastAPI • Go Microservices • Kafka • K8s',
            team: '1 Cloud Architect, 2 Backend Devs, 1 DevOps'
        },
        'ai': {
            stack: 'Python • LangChain • PyTorch • Vector DB',
            team: '1 AI Researcher, 2 Full-Stack Devs, 1 MLOps'
        },
        'business': {
            stack: 'Django 5.1 • Next.js • Postgres • Celery',
            team: '1 Tech Lead, 2 Engineers, 1 QA Specialist'
        }
    };

    function updateStepTracker(stepNum) {
        const trackerItems = document.querySelectorAll('.estimator-steps-tracker .step-tracker-item');
        trackerItems.forEach((item, index) => {
            if (index + 1 === stepNum) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    function recalculateEstimate() {
        if (!calcPriceDisplay) return;

        // 1. Solution Base (from dynamic Django data-attributes or fallback)
        const activeSolution = document.querySelector('#estimator-solution-group .estimator-option-btn.active') || solutionBtns[0];
        const solutionType = activeSolution ? (activeSolution.dataset.type || 'webapps') : 'webapps';
        const solutionTitle = activeSolution ? (activeSolution.dataset.title || activeSolution.querySelector('.estimator-opt-title')?.textContent?.trim() || 'Enterprise Web App / SaaS') : 'Enterprise Web App / SaaS';
        const basePrice = activeSolution ? parseFloat(activeSolution.dataset.basePrice || 4500) : 4500;
        const baseWeeks = activeSolution ? parseFloat(activeSolution.dataset.baseWeeks || 4) : 4;
        const archFallback = architectureStacks[solutionType] || architectureStacks['webapps'];
        const solStack = activeSolution && activeSolution.dataset.stack ? activeSolution.dataset.stack : archFallback.stack;
        const solTeam = activeSolution && activeSolution.dataset.team ? activeSolution.dataset.team : archFallback.team;

        // 2. UI Style
        const activeStyle = document.querySelector('#estimator-style-group .estimator-option-btn.active') || styleBtns[0];
        const styleTitle = activeStyle ? (activeStyle.dataset.style || activeStyle.querySelector('.estimator-opt-title')?.textContent?.trim() || 'Glassmorphism & Aurora Gradients') : 'Glassmorphism & Aurora Gradients';

        // 3. Modules (from dynamic Django data-attributes)
        let modulePriceSum = 0;
        let moduleWeeksSum = 0;
        let moduleCount = 0;
        const selectedModuleNames = [];

        document.querySelectorAll('#estimator-modules-group input[type="checkbox"]:checked').forEach(input => {
            modulePriceSum += parseFloat(input.dataset.price || 0);
            moduleWeeksSum += parseFloat(input.dataset.weeks || 0);
            moduleCount++;
            if (input.dataset.name) {
                selectedModuleNames.push(input.dataset.name);
            }
        });

        // 4. Scale Tier (from dynamic Django data-attributes)
        const activeTier = document.querySelector('#estimator-tier-group .estimator-option-btn.active') || tierBtns[0];
        const tierMultiplier = activeTier ? parseFloat(activeTier.dataset.multiplier || 1.0) : 1.0;
        const tierTitle = activeTier ? (activeTier.dataset.tier || activeTier.querySelector('.estimator-opt-title')?.textContent?.trim() || 'Startup MVP') : 'Startup MVP';

        // Calculate Transparent Math Totals
        const rawBasePlusModules = basePrice + modulePriceSum;
        const combinedSubtotal = rawBasePlusModules * tierMultiplier;
        const lowPrice = Math.round(combinedSubtotal / 50) * 50;
        const highPrice = Math.round((combinedSubtotal * 1.28) / 50) * 50;

        const rawWeeks = (baseWeeks + moduleWeeksSum) * (tierMultiplier > 1 ? 1.15 : 1.0);
        const lowWeeks = Math.max(3, Math.round(rawWeeks * 10) / 10);
        const highWeeks = Math.round((lowWeeks * 1.25) * 10) / 10;

        // Update Math Breakdown Card (Clear & Simple to Understand)
        if (calcBaseSubtotal) calcBaseSubtotal.textContent = `$${Math.round(basePrice).toLocaleString()}`;
        if (calcFeatCount) calcFeatCount.textContent = moduleCount;
        if (calcFeatSubtotal) calcFeatSubtotal.textContent = `+$${Math.round(modulePriceSum).toLocaleString()}`;
        if (calcTierMultiplier) calcTierMultiplier.textContent = `× ${tierMultiplier.toFixed(2)} (${tierTitle})`;
        if (calcCombinedSubtotal) calcCombinedSubtotal.textContent = `$${Math.round(combinedSubtotal).toLocaleString()}`;

        // Update Prominent Highlight Totals
        const priceRangeText = `$${lowPrice.toLocaleString()} – $${highPrice.toLocaleString()}`;
        calcPriceDisplay.textContent = priceRangeText;
        calcTimelineDisplay.textContent = `Estimated Delivery: ${lowWeeks} – ${highWeeks} Weeks`;

        const mobileCalcPrice = document.getElementById('mobile-calc-price');
        if (mobileCalcPrice) {
            mobileCalcPrice.textContent = priceRangeText;
        }

        // Update Blueprint Specs
        if (calcSolutionName) calcSolutionName.textContent = solutionTitle;
        if (calcStyleName) calcStyleName.textContent = styleTitle;
        if (calcTierName) calcTierName.textContent = `${tierTitle} Tier`;
        if (calcStackName) calcStackName.textContent = solStack;
        if (calcTeamName) calcTeamName.textContent = solTeam;

        // Map calculated price to Contact Form budget choices:
        let budgetChoice = '5000_10000';
        if (lowPrice < 2500) {
            budgetChoice = '1000_2500';
        } else if (lowPrice < 5000) {
            budgetChoice = '2500_5000';
        } else if (lowPrice < 10000) {
            budgetChoice = '5000_10000';
        } else {
            budgetChoice = 'above_10000';
        }

        // Map to contact form Service.slug values
        const serviceSlugMap = {
            'webapps': 'web-applications',
            'web-applications': 'web-applications',
            'software': 'custom-software',
            'custom-software': 'custom-software',
            'ai': 'ai-solutions',
            'ai-solutions': 'ai-solutions',
            'business': 'business-automation',
            'business-automation': 'business-automation',
            'ecommerce': 'ecommerce-development',
            'website': 'website-development',
        };
        const serviceChoice = serviceSlugMap[solutionType] || 'web-applications';

        // Prepare Scope Details for Inquire CTA
        const detailsSummary = `Project Scope Estimate:
• Solution: ${solutionTitle}
• UI Design Paradigm: ${styleTitle}
• Scale & SLA Tier: ${tierTitle} (Multiplier: ${tierMultiplier.toFixed(2)}x)
• Selected Features (${moduleCount}): ${selectedModuleNames.length > 0 ? selectedModuleNames.join(', ') : 'Core platform only'}
• Estimated Investment: $${lowPrice.toLocaleString()} – $${highPrice.toLocaleString()}
• Estimated Delivery: ${lowWeeks} – ${highWeeks} Weeks
• Recommended Stack: ${solStack}`;

        if (estimatorInquireBtn) {
            const params = new URLSearchParams({
                service: serviceChoice,
                budget: budgetChoice,
                details: detailsSummary
            });
            estimatorInquireBtn.setAttribute('href', `/contact/?${params.toString()}`);
        }
    }

    // Step Tracker Click-to-Scroll navigation
    const trackerStepItems = document.querySelectorAll('.estimator-steps-tracker .step-tracker-item');
    trackerStepItems.forEach((item, index) => {
        item.style.cursor = 'pointer';
        item.addEventListener('click', () => {
            const targetGroupId = `step-group-${index + 1}`;
            const targetGroup = document.getElementById(targetGroupId);
            if (targetGroup) {
                targetGroup.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            updateStepTracker(index + 1);
        });
    });

    // Bind Solution Pills (Step 1)
    if (solutionBtns.length > 0) {
        solutionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                solutionBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                updateStepTracker(1);
                recalculateEstimate();
            });
        });
    }

    // Bind Style Pills (Step 2)
    if (styleBtns.length > 0) {
        styleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                styleBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                updateStepTracker(2);
                recalculateEstimate();
            });
        });
    }

    // Bind Module Checkboxes (Step 3)
    if (moduleChecks.length > 0) {
        moduleChecks.forEach(card => {
            const checkbox = card.querySelector('input[type="checkbox"]');
            if (checkbox) {
                // Synchronize checked card style
                if (checkbox.checked) {
                    card.classList.add('checked');
                } else {
                    card.classList.remove('checked');
                }

                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        card.classList.add('checked');
                    } else {
                        card.classList.remove('checked');
                    }
                    updateStepTracker(3);
                    recalculateEstimate();
                });
            }
        });
    }

    // Bind Scale Tier Buttons (Step 4)
    if (tierBtns.length > 0) {
        tierBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tierBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                updateStepTracker(4);
                recalculateEstimate();
            });
        });
    }

    // Initial Calculation on Load
    if (calcPriceDisplay) {
        recalculateEstimate();
    }

    // Mobile Sticky Estimator Summary Bar visibility (< 960px)
    const mobileEstimatorBar = document.getElementById('mobile-estimator-bar');
    const estimatorSection = document.getElementById('project-estimator');
    const estimatorResults = document.getElementById('estimator-results');

    if (mobileEstimatorBar && estimatorSection && 'IntersectionObserver' in window) {
        let inEstimatorSection = false;
        let resultsVisible = false;

        const syncMobileBar = () => {
            if (inEstimatorSection && !resultsVisible && window.innerWidth <= 960) {
                mobileEstimatorBar.classList.add('visible');
            } else {
                mobileEstimatorBar.classList.remove('visible');
            }
        };

        const sectionObserver = new IntersectionObserver((entries) => {
            inEstimatorSection = entries[0].isIntersecting;
            syncMobileBar();
        }, { threshold: 0.05 });
        sectionObserver.observe(estimatorSection);

        if (estimatorResults) {
            const resultsObserver = new IntersectionObserver((entries) => {
                resultsVisible = entries[0].isIntersecting;
                syncMobileBar();
            }, { threshold: 0.15 });
            resultsObserver.observe(estimatorResults);
        }

        window.addEventListener('resize', syncMobileBar, { passive: true });
    }


    // =========================================================================
    // 11. CONTACT FORM AUTO-FILL FROM ESTIMATOR PARAMETERS
    // =========================================================================
    const urlParams = new URLSearchParams(window.location.search);
    const serviceParam = urlParams.get('service');
    const budgetParam = urlParams.get('budget');
    const detailsParam = urlParams.get('details');

    if (serviceParam || budgetParam || detailsParam) {
        const serviceSelect = document.getElementById('contact-service');
        const budgetSelect = document.getElementById('contact-budget');
        const detailsTextarea = document.getElementById('contact-details');
        const loadedBanner = document.getElementById('estimator-loaded-banner');

        if (serviceSelect && serviceParam && !serviceSelect.value) {
            const normalized = serviceParam.toLowerCase().replace(/-/g, ' ');
            Array.from(serviceSelect.options).forEach(opt => {
                const text = opt.text.toLowerCase();
                if (opt.value.toLowerCase() === serviceParam.toLowerCase() ||
                    text.includes(normalized) ||
                    text.includes(serviceParam.toLowerCase())) {
                    opt.selected = true;
                }
            });
        }

        if (budgetSelect && budgetParam) {
            Array.from(budgetSelect.options).forEach(opt => {
                if (opt.value === budgetParam) {
                    opt.selected = true;
                }
            });
        }

        if (detailsTextarea && detailsParam) {
            detailsTextarea.value = detailsParam;
            // Expand height to show the estimate nicely
            detailsTextarea.style.minHeight = '180px';
        }

        if (loadedBanner) {
            loadedBanner.classList.add('show');
        }
    }

});

