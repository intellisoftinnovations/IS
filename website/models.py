from django.db import models


class Service(models.Model):
    """A service offered by IntelliSoft Innovations."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(
        max_length=100,
        help_text="CSS class name for the service icon (e.g., 'icon-web', 'icon-ecommerce')"
    )
    short_description = models.TextField()
    features = models.TextField(
        help_text="Comma-separated list of features"
    )
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]


class PortfolioProject(models.Model):
    CATEGORY_CHOICES = [
        ('websites', 'Websites'),
        ('ecommerce', 'E-Commerce'),
        ('webapps', 'Web Applications'),
        ('business', 'Business Systems'),
        ('uiux', 'UI/UX'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    short_description = models.TextField()
    technologies = models.CharField(
        max_length=500,
        help_text="Comma-separated list of technologies used"
    )
    key_features = models.TextField(
        help_text="Comma-separated list of key features"
    )
    outcome = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def get_features_list(self):
        return [f.strip() for f in self.key_features.split(',') if f.strip()]


class TeamMember(models.Model):
    """A team member of IntelliSoft Innovations."""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.role}"


class WhyChooseUs(models.Model):
    """Reasons why clients should choose IntelliSoft."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Why Choose Us'
        verbose_name_plural = 'Why Choose Us'

    def __str__(self):
        return self.title


class ProcessStep(models.Model):
    """A step in the development process."""
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.step_number:02d} — {self.title}"


class ContactInquiry(models.Model):
    """A project inquiry submitted through the contact form."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    BUDGET_CHOICES = [
        ('', 'Select a range'),
        ('under_500', 'Under $500'),
        ('500_1000', '$500 – $1,000'),
        ('1000_2500', '$1,000 – $2,500'),
        ('2500_5000', '$2,500 – $5,000'),
        ('5000_10000', '$5,000 – $10,000'),
        ('above_10000', '$10,000+'),
        ('not_sure', 'Not sure yet'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=200, blank=True, verbose_name='Company / Business')
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries'
    )
    budget_range = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES,
        blank=True
    )
    project_details = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f"{self.name} — {self.email} ({self.created_at:%Y-%m-%d})"


class EstimatorSolution(models.Model):
    """Platform solution options for the Project Estimator, editable in Django admin."""
    name = models.CharField(max_length=200, help_text="e.g., Enterprise Web App / SaaS")
    slug = models.SlugField(unique=True, help_text="Maps to contact service, e.g., webapps, software, ai")
    short_description = models.CharField(max_length=255, help_text="e.g., Full-stack platforms, client portals & dashboards")
    base_price = models.PositiveIntegerField(default=4500, help_text="Base cost in USD (e.g., 4500)")
    base_weeks = models.DecimalField(max_digits=4, decimal_places=1, default=4.0, help_text="Base delivery time in weeks (e.g., 4.0)")
    recommended_stack = models.CharField(max_length=255, default="Django 5.1 • React 19 • Postgres • Redis", help_text="Tech stack recommended for this solution")
    dedicated_team = models.CharField(max_length=255, default="1 Lead Architect, 2 Senior Devs, 1 UI/UX", help_text="Team composition")
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Estimator Solution'
        verbose_name_plural = 'Estimator Solutions'

    def __str__(self):
        return f"{self.name} (${self.base_price:,})"


class EstimatorFeature(models.Model):
    """Add-on features and modules for the Project Estimator, editable in Django admin."""
    name = models.CharField(max_length=200, help_text="e.g., Bank-Grade Auth & RBAC")
    description = models.CharField(max_length=255, blank=True, help_text="e.g., OAuth, 2FA, Role permissions")
    price = models.PositiveIntegerField(default=900, help_text="Feature price in USD (e.g., 900)")
    weeks = models.DecimalField(max_digits=4, decimal_places=1, default=1.0, help_text="Additional delivery weeks (e.g., 1.0)")
    is_default = models.BooleanField(default=False, help_text="Check if pre-selected by default")
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Estimator Feature'
        verbose_name_plural = 'Estimator Features'

    def __str__(self):
        return f"{self.name} (+${self.price:,}, +{self.weeks}w)"


class EstimatorTier(models.Model):
    """Scale and SLA tiers for the Project Estimator, editable in Django admin."""
    name = models.CharField(max_length=150, help_text="e.g., Startup MVP, Growth Scale, Enterprise 99.99%")
    description = models.CharField(max_length=255, help_text="e.g., Rapid release, up to 10k users")
    multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.00, help_text="Cost multiplier (e.g., 1.00, 1.25, 1.55)")
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Estimator Scale Tier'
        verbose_name_plural = 'Estimator Scale Tiers'

    def __str__(self):
        return f"{self.name} ({self.multiplier}x)"

