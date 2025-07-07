# __manifest__.py

{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage hospital operations including patients, doctors, appointments, admissions, labs, pharmacy, and billing.',
    'description': """
        Odoo Hospital Management System (HMS)
        ======================================
        Features:
        - Patient Registration & Management
        - Doctor Profiles & Scheduling
        - Appointment Booking System
        - OPD & IPD Management
        - Ward & Bed Management
        - Lab Test Requests & Results
        - Prescription & Pharmacy Management
        - Invoice and Billing
        - Dashboard & Reporting
    """,
    'author': 'Your Name or Company',
    'website': 'https://yourcompanywebsite.com',
    'category': 'Healthcare',
    'depends': ['base', 'mail', 'hr', 'stock', 'account', 'web'],
    'data': [
        # # Security
        'security/ir.model.access.csv',
        'data/data.xml',
        # 'security/hms_security.xml',
        #
        # # Views
        'views/patients_view.xml',
        'views/appointment.xml',
        'views/doctors.xml',
        'views/menus.xml',
        # 'views/doctor_view.xml',
        # 'views/ipd_view.xml',
        # 'views/ward_view.xml',
        # 'views/bed_view.xml',
        # 'views/prescription_view.xml',
        # 'views/lab_test_view.xml',
        # 'views/invoice_view.xml',
        #
        # # Menus
        # 'views/hms_menus.xml',
        #
        # # Dashboard (optional)
        # 'views/hms_dashboard_view.xml',
        #
        # # Reports (optional)
        # 'reports/hms_reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hospital_management_odoo/static/description/icon.png',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
