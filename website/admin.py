from django.contrib import admin
from .models import (
    Service, PortfolioProject, TeamMember,
    WhyChooseUs, ProcessStep, ContactInquiry,
    EstimatorSolution, EstimatorFeature, EstimatorTier
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title',)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order')
    list_filter = ('category', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'order')
    search_fields = ('title', 'short_description')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')
    list_editable = ('order',)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'service', 'status', 'created_at', 'is_read')
    list_filter = ('status', 'is_read', 'service', 'budget_range', 'created_at')
    search_fields = ('name', 'email', 'company', 'project_details')
    readonly_fields = ('created_at',)
    list_editable = ('status', 'is_read')
    date_hierarchy = 'created_at'


@admin.register(EstimatorSolution)
class EstimatorSolutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'base_weeks', 'slug', 'order', 'is_active')
    list_editable = ('base_price', 'base_weeks', 'order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'recommended_stack')


@admin.register(EstimatorFeature)
class EstimatorFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weeks', 'is_default', 'order', 'is_active')
    list_editable = ('price', 'weeks', 'is_default', 'order', 'is_active')
    search_fields = ('name', 'description')


@admin.register(EstimatorTier)
class EstimatorTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'multiplier', 'is_default', 'order', 'is_active')
    list_editable = ('multiplier', 'is_default', 'order', 'is_active')
    search_fields = ('name', 'description')

