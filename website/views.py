import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Service, PortfolioProject, TeamMember,
    WhyChooseUs, ProcessStep, ContactInquiry,
    EstimatorSolution, EstimatorFeature, EstimatorTier
)
from .forms import ContactForm

logger = logging.getLogger(__name__)


def home(request):
    """Homepage — hero, trust, services, portfolio, why-us, process, CTA, estimator."""
    context = {
        'services': Service.objects.all(),
        'featured_projects': PortfolioProject.objects.filter(featured=True)[:3],
        'reasons': WhyChooseUs.objects.all(),
        'process_steps': ProcessStep.objects.all(),
        'estimator_solutions': EstimatorSolution.objects.filter(is_active=True),
        'estimator_features': EstimatorFeature.objects.filter(is_active=True),
        'estimator_tiers': EstimatorTier.objects.filter(is_active=True),
        'page_title': 'IntelliSoft Innovations — Technology Built Around Your Business',
        'meta_description': (
            'IntelliSoft Innovations creates professional websites, e-commerce platforms, '
            'custom software, and modern digital solutions designed around your business.'
        ),
    }
    return render(request, 'website/home.html', context)


def services(request):
    """Full services listing page."""
    context = {
        'services': Service.objects.all(),
        'page_title': 'Our Services — IntelliSoft Innovations',
        'meta_description': (
            'Explore our services: website development, e-commerce, custom software, '
            'web applications, UI/UX design, business automation, AI solutions, and support.'
        ),
    }
    return render(request, 'website/services.html', context)


def service_detail(request, slug):
    """Individual service detail page."""
    service = get_object_or_404(Service, slug=slug)
    context = {
        'service': service,
        'page_title': f'{service.title} — IntelliSoft Innovations',
        'meta_description': service.short_description[:160],
    }
    return render(request, 'website/service_detail.html', context)


def portfolio(request):
    """Portfolio grid with category filtering."""
    context = {
        'projects': PortfolioProject.objects.all(),
        'categories': PortfolioProject.CATEGORY_CHOICES,
        'page_title': 'Our Work — IntelliSoft Innovations',
        'meta_description': (
            'Selected work from IntelliSoft Innovations — websites, e-commerce platforms, '
            'web applications, and custom business systems.'
        ),
    }
    return render(request, 'website/portfolio.html', context)


def about(request):
    """About page — company story, team, values."""
    context = {
        'team_members': TeamMember.objects.all(),
        'reasons': WhyChooseUs.objects.all(),
        'page_title': 'About Us — IntelliSoft Innovations',
        'meta_description': (
            'IntelliSoft Innovations is a software-focused technology company dedicated '
            'to creating useful, modern, and reliable digital solutions.'
        ),
    }
    return render(request, 'website/about.html', context)


def process(request):
    """Development process page — 7-step process."""
    context = {
        'process_steps': ProcessStep.objects.all(),
        'page_title': 'Our Process — IntelliSoft Innovations',
        'meta_description': (
            'Our development process: Discover, Plan, Design, Build, Test, Launch, Grow. '
            'We build digital solutions with a structured, transparent approach.'
        ),
    }
    return render(request, 'website/process.html', context)


def contact(request):
    """Contact form page — GET shows form (pre-filled from estimator if provided), POST validates and saves."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            # Send email notification
            try:
                send_mail(
                    subject=f'New Project Inquiry from {inquiry.name}',
                    message=(
                        f'Name: {inquiry.name}\n'
                        f'Email: {inquiry.email}\n'
                        f'Phone: {inquiry.phone}\n'
                        f'Company: {inquiry.company}\n'
                        f'Service: {inquiry.service}\n'
                        f'Budget: {inquiry.get_budget_range_display()}\n\n'
                        f'Project Details:\n{inquiry.project_details}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Failed to send contact inquiry email notification for inquiry #%s', inquiry.pk)
            return redirect('contact_success')
    else:
        initial = {}
        service_slug = request.GET.get('service', '').strip()
        budget_code = request.GET.get('budget', '').strip()
        details_text = request.GET.get('details', '').strip()

        if service_slug:
            matched_service = Service.objects.filter(slug__iexact=service_slug).first()
            if matched_service:
                initial['service'] = matched_service.pk

        valid_budgets = {code for code, _ in ContactInquiry.BUDGET_CHOICES if code}
        if budget_code in valid_budgets:
            initial['budget_range'] = budget_code

        if details_text:
            initial['project_details'] = details_text

        form = ContactForm(initial=initial)

    context = {
        'form': form,
        'page_title': "Let's Build Something Great — IntelliSoft Innovations",
        'meta_description': (
            'Have an idea or a project in mind? Contact IntelliSoft Innovations '
            "and let's discuss the best way forward."
        ),
    }
    return render(request, 'website/contact.html', context)


def contact_success(request):
    """Thank-you page after successful form submission."""
    context = {
        'page_title': 'Thank You — IntelliSoft Innovations',
        'meta_description': 'Your project inquiry has been received. We will get back to you shortly.',
    }
    return render(request, 'website/contact_success.html', context)


# =========================================================================
# CUSTOM HTTP ERROR HANDLERS (404, 500, 403, 400)
# =========================================================================

def error_404(request, exception=None):
    """Custom 404 — Page Not Found handler."""
    context = {
        'page_title': '404 — Route Not Found | IntelliSoft Innovations',
        'meta_description': 'The page or resource you requested could not be found.',
        'error_code': '404',
        'error_title': 'Route Not Found',
        'error_message': 'The endpoint, resource, or page you are attempting to reach does not exist or has been relocated.',
    }
    return render(request, 'website/404.html', context, status=404)


def error_500(request):
    """Custom 500 — Internal Server Error handler."""
    context = {
        'page_title': '500 — System Error | IntelliSoft Innovations',
        'meta_description': 'An unexpected condition occurred on the server.',
        'error_code': '500',
        'error_title': 'Internal System Error',
        'error_message': 'The cluster encountered an unhandled server condition. Our automated telemetry has flagged this incident.',
    }
    return render(request, 'website/500.html', context, status=500)


def error_403(request, exception=None):
    """Custom 403 — Access Forbidden handler."""
    context = {
        'page_title': '403 — Access Restricted | IntelliSoft Innovations',
        'meta_description': 'Access to this system endpoint is restricted.',
        'error_code': '403',
        'error_title': 'Access Restricted',
        'error_message': 'You do not have administrative clearance or token credentials to access this system route.',
    }
    return render(request, 'website/403.html', context, status=403)


def error_400(request, exception=None):
    """Custom 400 — Bad Request handler."""
    context = {
        'page_title': '400 — Malformed Request | IntelliSoft Innovations',
        'meta_description': 'The server could not understand the request.',
        'error_code': '400',
        'error_title': 'Malformed Request',
        'error_message': 'The server was unable to parse or process the payload due to invalid syntax or parameters.',
    }
    return render(request, 'website/400.html', context, status=400)

