"""
Management command to seed the database with initial data from the design spec.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from website.models import (
    Service, WhyChooseUs, ProcessStep, TeamMember, PortfolioProject,
    EstimatorSolution, EstimatorFeature, EstimatorTier
)


class Command(BaseCommand):
    help = 'Seed the database with initial IntelliSoft Innovations data from the design spec.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        self._seed_services()
        self._seed_why_choose_us()
        self._seed_process_steps()
        self._seed_team()
        self._seed_portfolio()
        self._seed_estimator()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _seed_services(self):
        services = [
            {
                'title': 'Website Development',
                'slug': 'website-development',
                'icon_class': 'icon-web',
                'short_description': 'Build modern, responsive websites for businesses, organizations, and personal brands.',
                'features': 'Responsive design, Mobile-first layouts, Professional UI, SEO-friendly structure, Fast-loading pages, Contact forms, Social media integration, Google Maps integration, Custom sections, Business information pages, Maintenance and future improvements',
                'order': 1,
            },
            {
                'title': 'E-Commerce Development',
                'slug': 'ecommerce-development',
                'icon_class': 'icon-ecommerce',
                'short_description': 'Create complete online stores that allow businesses to sell products online — available 24/7.',
                'features': 'Product management, Product categories, Product variants, Product images and galleries, Search and filtering, Shopping cart, Checkout, Order management, Stock management, Discount pricing, Featured products, Best-seller sections, Customer-friendly product pages, Responsive mobile experience',
                'order': 2,
            },
            {
                'title': 'Custom Software Development',
                'slug': 'custom-software',
                'icon_class': 'icon-software',
                'short_description': 'Develop software around your actual business workflow instead of forcing your business into a generic template.',
                'features': 'Business management systems, Inventory systems, Order management, Customer management, Admin dashboards, Internal tools, Booking systems, Workflow systems, Custom web applications, API-based applications',
                'order': 3,
            },
            {
                'title': 'Web Application Development',
                'slug': 'web-applications',
                'icon_class': 'icon-webapp',
                'short_description': 'Build interactive browser-based applications for businesses and organizations.',
                'features': 'Dashboards, Admin panels, Customer portals, Booking platforms, Management systems, SaaS interfaces, Internal business tools, Data-driven applications',
                'order': 4,
            },
            {
                'title': 'UI/UX Design',
                'slug': 'ui-ux-design',
                'icon_class': 'icon-uiux',
                'short_description': 'Design interfaces that are visually professional, easy to use, and conversion-focused.',
                'features': 'Business understanding, User identification, Information architecture, Wireframes, Visual direction, Responsive interfaces, Feedback-based refinement, Clear hierarchy, Strong typography, Consistent spacing, Simple navigation, Accessible contrast',
                'order': 5,
            },
            {
                'title': 'Business Automation',
                'slug': 'business-automation',
                'icon_class': 'icon-automation',
                'short_description': 'Help businesses reduce repetitive manual work through software and automation.',
                'features': 'Order workflows, Notifications, Data processing, Customer communication, Admin workflows, Reporting, Integrations, Automated business processes',
                'order': 6,
            },
            {
                'title': 'AI-Powered Solutions',
                'slug': 'ai-solutions',
                'icon_class': 'icon-ai',
                'short_description': 'AI services that provide measurable business benefit — not buzzwords.',
                'features': 'AI chat assistants, Customer-support automation, Content assistance, Business data analysis, Intelligent search, Workflow automation, AI API integration',
                'order': 7,
            },
            {
                'title': 'Maintenance & Support',
                'slug': 'maintenance-support',
                'icon_class': 'icon-maintenance',
                'short_description': 'Long-term support for websites and software — the relationship continues beyond launch.',
                'features': 'Bug fixing, Content updates, Feature improvements, Performance optimization, Security updates, Product updates, Technical support, Continuous development',
                'order': 8,
            },
        ]

        for data in services:
            Service.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
        self.stdout.write(f'  [OK] {len(services)} services created')

    def _seed_why_choose_us(self):
        reasons = [
            {
                'title': 'Business Understanding',
                'description': 'We focus on the actual business problem before choosing the technology.',
                'icon_class': 'icon-business',
                'order': 1,
            },
            {
                'title': 'Custom Solutions',
                'description': "We don't believe every business should use the same template.",
                'icon_class': 'icon-custom',
                'order': 2,
            },
            {
                'title': 'Modern Design',
                'description': "Clean, professional interfaces designed for today's users.",
                'icon_class': 'icon-design',
                'order': 3,
            },
            {
                'title': 'Scalable Development',
                'description': 'Solutions should be capable of growing with the business.',
                'icon_class': 'icon-scale',
                'order': 4,
            },
            {
                'title': 'Clear Communication',
                'description': 'Clients should understand what is being built and why.',
                'icon_class': 'icon-communication',
                'order': 5,
            },
            {
                'title': 'Long-Term Support',
                'description': 'The relationship should continue beyond launch.',
                'icon_class': 'icon-support',
                'order': 6,
            },
        ]

        for data in reasons:
            WhyChooseUs.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
        self.stdout.write(f'  [OK] {len(reasons)} reasons created')

    def _seed_process_steps(self):
        steps = [
            {
                'step_number': 1,
                'title': 'Discovery',
                'description': 'Understand the business, users, requirements, and goals.',
                'order': 1,
            },
            {
                'step_number': 2,
                'title': 'Planning',
                'description': 'Define features, structure, technology, scope, and timeline.',
                'order': 2,
            },
            {
                'step_number': 3,
                'title': 'UI/UX Design',
                'description': 'Create the visual and interaction system.',
                'order': 3,
            },
            {
                'step_number': 4,
                'title': 'Development',
                'description': 'Build the website, application, or software solution.',
                'order': 4,
            },
            {
                'step_number': 5,
                'title': 'Testing',
                'description': 'Test usability, responsiveness, functionality, and performance.',
                'order': 5,
            },
            {
                'step_number': 6,
                'title': 'Launch',
                'description': 'Deploy the finished solution.',
                'order': 6,
            },
            {
                'step_number': 7,
                'title': 'Support',
                'description': 'Continue improving and maintaining the product.',
                'order': 7,
            },
        ]

        for data in steps:
            ProcessStep.objects.update_or_create(
                step_number=data['step_number'],
                defaults=data
            )
        self.stdout.write(f'  [OK] {len(steps)} process steps created')

    def _seed_team(self):
        members = [
            {
                'name': 'MD Santunu Kaysar Mahin',
                'role': 'Founder & Chief Executive Officer',
                'bio': 'Leading IntelliSoft Innovations with a focus on architecting scalable digital platforms, modern cloud software, and AI automation that solve real business problems.',
                'image': 'team/mahin_ceo_studio.png',
                'order': 1,
            },
            {
                'name': 'Tanvir Ahmed',
                'role': 'Lead Software Architect',
                'bio': 'Specializes in high-throughput distributed systems, event-driven microservices with Go and FastAPI, and resilient PostgreSQL architectures.',
                'image': '',
                'order': 2,
            },
            {
                'name': 'Farhana Yasmin',
                'role': 'Head of UI/UX & Design Systems',
                'bio': 'Designs modern neumorphic and glassmorphic interfaces, interactive prototypes, and accessible customer-focused SaaS experiences.',
                'image': '',
                'order': 3,
            },
            {
                'name': 'Rafiqul Islam',
                'role': 'Cloud Infrastructure & DevOps Lead',
                'bio': 'Automates enterprise CI/CD pipelines, Docker containerization, Kubernetes clusters, and zero-downtime production deployments.',
                'image': '',
                'order': 4,
            },
        ]

        for data in members:
            TeamMember.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
        self.stdout.write(f'  [OK] {len(members)} team members created')

    def _seed_portfolio(self):
        projects = [
            {
                'title': 'Modern E-Commerce Platform',
                'slug': 'modern-ecommerce-platform',
                'category': 'ecommerce',
                'short_description': 'A full-featured online store with product management, cart, checkout, and order tracking.',
                'technologies': 'Django, PostgreSQL, Stripe, HTML/CSS, JavaScript',
                'key_features': 'Product catalog, Shopping cart, Secure checkout, Order management, Admin dashboard',
                'outcome': 'Enabled the client to sell products online with a professional, mobile-friendly store.',
                'featured': True,
                'order': 1,
            },
            {
                'title': 'Business Management Dashboard',
                'slug': 'business-management-dashboard',
                'category': 'webapps',
                'short_description': 'A custom admin dashboard for managing orders, customers, and inventory in one place.',
                'technologies': 'Python, Django, REST API, Chart.js, Bootstrap',
                'key_features': 'Real-time analytics, Order tracking, Customer management, Inventory control, Reports',
                'outcome': 'Reduced manual admin work by automating key business workflows.',
                'featured': True,
                'order': 2,
            },
            {
                'title': 'Professional Service Website',
                'slug': 'professional-service-website',
                'category': 'websites',
                'short_description': 'A clean, responsive website for a professional services firm with contact forms and SEO.',
                'technologies': 'Django, HTML5, CSS3, JavaScript, SEO',
                'key_features': 'Responsive design, Contact forms, SEO optimization, Google Maps, Social integration',
                'outcome': 'Established a strong online presence and increased client inquiries.',
                'featured': True,
                'order': 3,
            },
        ]

        for data in projects:
            PortfolioProject.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
        self.stdout.write(f'  [OK] {len(projects)} portfolio projects created')

    def _seed_estimator(self):
        # 1. Solutions
        solutions = [
            {
                'name': 'Enterprise Web App / SaaS',
                'slug': 'webapps',
                'short_description': 'Full-stack platform, portals & dashboards',
                'base_price': 4500,
                'base_weeks': 4.0,
                'recommended_stack': 'Django 5.1 • React 19 • Postgres • Redis',
                'dedicated_team': '1 Lead Architect, 2 Senior Devs, 1 UI/UX',
                'order': 1,
            },
            {
                'name': 'Cloud Microservices & APIs',
                'slug': 'software',
                'short_description': 'High-throughput REST & GraphQL backends',
                'base_price': 3800,
                'base_weeks': 3.0,
                'recommended_stack': 'FastAPI • Go Microservices • Kafka • K8s',
                'dedicated_team': '1 Cloud Architect, 2 Backend Devs, 1 DevOps',
                'order': 2,
            },
            {
                'name': 'AI Automation & LLM Agents',
                'slug': 'ai',
                'short_description': 'Autonomous pipelines & custom fine-tuning',
                'base_price': 5200,
                'base_weeks': 4.0,
                'recommended_stack': 'Python • LangChain • PyTorch • Vector DB',
                'dedicated_team': '1 AI Researcher, 2 Full-Stack Devs, 1 MLOps',
                'order': 3,
            },
            {
                'name': 'Bespoke CRM / Business System',
                'slug': 'business',
                'short_description': 'Internal workflows, inventory & operations',
                'base_price': 4200,
                'base_weeks': 3.5,
                'recommended_stack': 'Django 5.1 • Next.js • Postgres • Celery',
                'dedicated_team': '1 Tech Lead, 2 Engineers, 1 QA Specialist',
                'order': 4,
            },
        ]
        for data in solutions:
            EstimatorSolution.objects.update_or_create(slug=data['slug'], defaults=data)
        self.stdout.write(f'  [OK] {len(solutions)} estimator solutions created')

        # 2. Features
        features = [
            {
                'name': 'Bank-Grade Auth & RBAC',
                'description': 'OAuth, 2FA, Role permissions',
                'price': 900,
                'weeks': 1.0,
                'is_default': True,
                'order': 1,
            },
            {
                'name': 'Real-time WebSockets & Push',
                'description': 'Live chat, notifications, live data sync',
                'price': 1200,
                'weeks': 1.5,
                'is_default': True,
                'order': 2,
            },
            {
                'name': 'Custom AI Agent / LLM Integration',
                'description': 'Intelligent assistants, RAG, automated workflows',
                'price': 2200,
                'weeks': 2.0,
                'is_default': False,
                'order': 3,
            },
            {
                'name': 'Stripe Payments & Subscriptions',
                'description': 'Checkout, recurring billing, invoices',
                'price': 950,
                'weeks': 1.0,
                'is_default': True,
                'order': 4,
            },
            {
                'name': 'Advanced Analytics & Reporting',
                'description': 'Interactive KPI charts, CSV/PDF exports',
                'price': 1100,
                'weeks': 1.5,
                'is_default': False,
                'order': 5,
            },
            {
                'name': 'Automated CI/CD & Docker Cloud',
                'description': 'GitHub Actions, automated tests, container deployment',
                'price': 950,
                'weeks': 1.0,
                'is_default': False,
                'order': 6,
            },
        ]
        for data in features:
            EstimatorFeature.objects.update_or_create(name=data['name'], defaults=data)
        self.stdout.write(f'  [OK] {len(features)} estimator features created')

        # 3. Tiers
        tiers = [
            {
                'name': 'Startup MVP',
                'description': 'Lean, rapid release, up to 10k users',
                'multiplier': 1.00,
                'is_default': True,
                'order': 1,
            },
            {
                'name': 'Growth Scale',
                'description': 'Clustered, 100k+ concurrent users',
                'multiplier': 1.25,
                'is_default': False,
                'order': 2,
            },
            {
                'name': 'Mission-Critical Enterprise',
                'description': 'High concurrency & 99.99% SLA uptime',
                'multiplier': 1.55,
                'is_default': False,
                'order': 3,
            },
        ]
        for data in tiers:
            EstimatorTier.objects.update_or_create(name=data['name'], defaults=data)
        self.stdout.write(f'  [OK] {len(tiers)} estimator tiers created')
