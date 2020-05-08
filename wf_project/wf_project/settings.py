"""
Django settings for wf_project project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fh33gjx$+5lu0u7r^j%6(bv1#n@#r!*+z9qd%g@bgud^dv*n)x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # HY workflow modules
    'administration.apps.AdministrationConfig',
    'approval.apps.ApprovalConfig',
    'dashboard.apps.DashboardConfig',
    #'contract_service.apps.ContractServiceConfig',
    #'drawer_reimbursement.apps.DrawerReimbursementConfig',
    'drawer_disbursement.apps.DrawerDisbursementConfig',
    'fixed_asset.apps.FixedAssetConfig',
    'human_resource.apps.HumanResourceConfig',
    'Inventory.apps.InventoryConfig',
    'memo.apps.MemoConfig',
    'payment.apps.PaymentConfig',
    'purchasing.apps.PurchasingConfig',
    'staff_overtime.apps.StaffOvertimeConfig',
    'PDFreport.apps.PdfreportConfig',
    'drawer_reimbursement.apps.DrawerReimbursementConfig',
    'utility_dashboard.apps.UtilityDashboardConfig',
    'audit_trail.apps.AuditTrailConfig',
    'accounts_task.apps.AccountsTaskConfig',
    'stock.apps.StockConfig',
    #'sales.apps.SalesConfig',
    #'vendor.apps.VendorConfig',

    # Any apps which need to have their templates overridden by adminlte
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
    'django_extensions',
    'ckeditor',
    'django_select2',
    'ckeditor_uploader',
    'rest_framework_datatables',
    'widget_tweaks',
    'report_builder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wf_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates','accounts_task'),
            os.path.join(BASE_DIR, 'templates','approval'),
            os.path.join(BASE_DIR, 'templates','drawer_disbursement'),
            os.path.join(BASE_DIR, 'templates','fixed_asset'),
            os.path.join(BASE_DIR, 'templates','human_resource'),
            os.path.join(BASE_DIR, 'templates','memo'),
            os.path.join(BASE_DIR, 'templates','payment'),
            os.path.join(BASE_DIR, 'templates','purchasing'),  
            os.path.join(BASE_DIR, 'templates','staff_overtime'),     
            os.path.join(BASE_DIR, 'templates','report'),
            os.path.join(BASE_DIR, 'templates','reimbursement_request'), 
            os.path.join(BASE_DIR, 'templates','stock'),            
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'purchasing.context_processors.po_trans_type',
                'purchasing.context_processors.grn_trans_type',
                'purchasing.context_processors.pi_trans_type',
                'purchasing.context_processors.pcn_trans_type',
                'purchasing.context_processors.pdn_trans_type',
                'payment.context_processors.py_trans_type',
                'staff_overtime.context_processors.staff_ot_trans_type',
                'drawer_reimbursement.context_processors.reimbursement_trans_type',
                'dashboard.context_processors.dashboard_drawer',
            ],
        },
    },
]

WSGI_APPLICATION = 'wf_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

####################################
    ##  CKEDITOR CONFIGURATION ##
####################################
 
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
 
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
    'remarks_po': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Table','BulletedList', 'NumberedList']
        ],
        'height':174,
    },
    'del_ins_po': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Table','BulletedList', 'NumberedList']
        ],
        'height':100,
    },
    'details_memo': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Table','BulletedList', 'NumberedList', 'Source']
        ],
    },
    'remarks_py': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Table','BulletedList', 'NumberedList']
        ],
    },
}
 
###################################