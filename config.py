"""
config.py - Simple Configuration for Ticket Summary App
Contains only essential settings and mappings.
"""

# Essential columns we need (12 columns)
SELECTED_COLUMNS = [
    'ORDER_NUMBER', 'ACCEPTANCE_TIME', 'COMPLETION_TIME', 'CUSTOMER_COMPLETION_TIME',
    'CUSTOMER_NUMBER', 'ORDER_TYPE', 'PROCESSING_STATUS', 'SERVICE_CATEGORY',
    'ORDER_DESCRIPTION_1', 'ORDER_DESCRIPTION_2', 'COMPLETION_RESULT_KB', 'NOTE_MAXIMUM'
]

# Valid categories to keep
VALID_CATEGORIES = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']

# Category to Product mapping
CATEGORY_MAPPING = {
    'KAI': 'Broadband',
    'NET': 'Broadband', 
    'KAV': 'Voice',
    'KAD': 'TV',
    'GIGA': 'GIGA',
    'VOD': 'VOD',
    'HDW': 'Hardware'
}

# Date format in the data
DATE_FORMAT = '%m/%d/%Y %H:%M'

# Story sections
STORY_SECTIONS = ['Initial Issue', 'Follow-ups', 'Developments', 'Later Incidents', 'Recent Events']