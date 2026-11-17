from django.test import TestCase, Client
from django.urls import reverse
from .models import (
    Service, PortfolioProject, TeamMember,
    WhyChooseUs, ProcessStep, ContactInquiry,
    EstimatorSolution, EstimatorFeature, EstimatorTier
)
from .forms import ContactForm


class WebsiteModelTests(TestCase):
    def test_service_features_list_parsing(self):
        service = Service.objects.create(
            title='Web Applications',
            slug='web-applications',
            icon_class='icon-webapp',
            short_description='Interactive web apps',
            features='Dashboards, Admin panels, , Customer portals ',
            order=1,
        )
        self.assertEqual(
            service.get_features_list(),
            ['Dashboards', 'Admin panels', 'Customer portals']
        )

    def test_portfolio_project_lists_parsing(self):
        project = PortfolioProject.objects.create(
            title='Cloud Portal',
            slug='cloud-portal',
            category='webapps',
            short_description='Enterprise portal',
            technologies='Django, React, PostgreSQL',
            key_features='SSO, RBAC, Analytics',
            featured=True,
            order=1,
        )
        self.assertEqual(project.get_technologies_list(), ['Django', 'React', 'PostgreSQL'])
        self.assertEqual(project.get_features_list(), ['SSO', 'RBAC', 'Analytics'])


class WebsiteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            title='Web Application Development',
            slug='web-applications',
            icon_class='icon-webapp',
            short_description='Browser-based business applications.',
            features='Dashboards, Portals',
            order=1,
        )
        self.project = PortfolioProject.objects.create(
            title='FinTech Dashboard',
            slug='fintech-dashboard',
            category='webapps',
            short_description='Analytics dashboard',
            technologies='Django, TypeScript',
            key_features='Real-time charts',
            featured=True,
            order=1,
        )
        TeamMember.objects.create(name='Test Founder', role='Founder & CEO', bio='Lead architect', order=1)
        WhyChooseUs.objects.create(title='Custom Solutions', description='Tailored to business.', order=1)
        ProcessStep.objects.create(step_number=1, title='Discover', description='Understand goals.', order=1)
        EstimatorSolution.objects.create(
            name='Enterprise Web App / SaaS',
            slug='web-applications',
            short_description='Full-stack SaaS',
            base_price=4500,
            base_weeks=4.0,
            order=1,
        )
        EstimatorFeature.objects.create(name='Auth & RBAC', price=900, weeks=1.0, is_default=True, order=1)
        EstimatorTier.objects.create(name='Startup MVP', description='Rapid release', multiplier=1.00, is_default=True, order=1)

    def test_public_pages_return_200(self):
        urls = [
            reverse('home'),
            reverse('services'),
            reverse('service_detail', kwargs={'slug': self.service.slug}),
            reverse('portfolio'),
            reverse('about'),
            reverse('process'),
            reverse('contact'),
            reverse('contact_success'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_error_pages_and_catch_all_404(self):
        self.assertEqual(self.client.get(reverse('preview_400')).status_code, 400)
        self.assertEqual(self.client.get(reverse('preview_403')).status_code, 403)
        self.assertEqual(self.client.get(reverse('preview_404')).status_code, 404)
        self.assertEqual(self.client.get(reverse('preview_500')).status_code, 500)
        self.assertEqual(self.client.get('/non-existent-route/').status_code, 404)
        admin_no_slash = self.client.get('/admin')
        self.assertEqual(admin_no_slash.status_code, 301)
        self.assertTrue(admin_no_slash['Location'].endswith('/admin/'))

    def test_contact_prefill_from_estimator_params(self):
        response = self.client.get(
            reverse('contact'),
            {
                'service': 'web-applications',
                'budget': '5000_10000',
                'details': 'Estimated Scope: SaaS Platform',
            }
        )
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial.get('service'), self.service.pk)
        self.assertEqual(form.initial.get('budget_range'), '5000_10000')
        self.assertEqual(form.initial.get('project_details'), 'Estimated Scope: SaaS Platform')

    def test_contact_post_creates_inquiry(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': ' +880 1700 000000 ',
            'company': 'Acme Corp',
            'service': self.service.pk,
            'budget_range': '5000_10000',
            'project_details': 'Need a custom client portal.',
            'website': '',
        })
        self.assertRedirects(response, reverse('contact_success'))
        inquiry = ContactInquiry.objects.get(email='jane@example.com')
        self.assertEqual(inquiry.status, 'new')
        self.assertEqual(inquiry.phone, '+880 1700 000000')
        self.assertEqual(inquiry.service, self.service)

    def test_contact_honeypot_rejects_bot_submission(self):
        form = ContactForm(data={
            'name': 'Bot User',
            'email': 'bot@example.com',
            'project_details': 'Spam message',
            'website': 'http://spam.example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)
