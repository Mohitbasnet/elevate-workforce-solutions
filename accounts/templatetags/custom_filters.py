from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]

@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def range_filter(value):
    """Convert integer to range for template loops"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

@register.filter
def status_badge_class(status):
    """Return CSS class for application status badges"""
    status_classes = {
        'pending': 'warning',
        'reviewed': 'info',
        'shortlisted': 'primary',
        'interview': 'success',
        'rejected': 'danger',
        'hired': 'success'
    }
    return status_classes.get(status, 'secondary')

@register.filter
def phone_format(phone):
    """Format phone number for display"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, str(phone)))
    
    # Format based on length
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        return phone

@register.filter
def currency_format(amount):
    """Format currency amount"""
    try:
        amount = float(amount)
        return f"NPR {amount:,.0f}"
    except (ValueError, TypeError):
        return amount

@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        value = float(value)
        total = float(total)
        if total == 0:
            return 0
        return round((value / total) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def truncate_skills(skills_text, max_skills=5):
    """Truncate skills list to show only first few skills"""
    if not skills_text:
        return ""
    
    skills = [skill.strip() for skill in str(skills_text).split(',') if skill.strip()]
    
    if len(skills) <= max_skills:
        return ', '.join(skills)
    else:
        displayed_skills = skills[:max_skills]
        remaining = len(skills) - max_skills
        return f"{', '.join(displayed_skills)} and {remaining} more"

@register.filter
def file_size(file_field):
    """Get human readable file size"""
    if not file_field:
        return ""
    
    try:
        size = file_field.size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return ""

@register.filter
def days_since(date_field):
    """Calculate days since a date"""
    if not date_field:
        return ""
    
    from django.utils import timezone
    from datetime import datetime
    
    if isinstance(date_field, str):
        return date_field
    
    now = timezone.now() if timezone.is_aware(date_field) else datetime.now()
    diff = now - date_field
    
    days = diff.days
    if days == 0:
        return "Today"
    elif days == 1:
        return "Yesterday"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = days // 365
        return f"{years} year{'s' if years > 1 else ''} ago" 