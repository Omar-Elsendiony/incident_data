import json
import re
import random
from datetime import datetime, timedelta, date
from faker import Faker
import uuid

# Initialize Faker
fake = Faker()

# Global data storage
data = {}

# Email domains for realistic email generation
email_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'company.com', 'business.net', 'corp.org']

# Phone number area codes
area_codes = ['202', '212', '213', '214', '305', '312', '404', '415', '503', '617', '718', '832']

def generate_phone():
    """Generate realistic phone number"""
    area = random.choice(area_codes)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1{area}{exchange}{number}"

def generate_email(first_name, last_name, domain=None):
    """Generate realistic email"""
    if domain is None:
        domain = random.choice(email_domains)
    
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name.lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}{random.randint(1, 999)}@{domain}",
        f"{last_name.lower()}{random.randint(1, 999)}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}"
    ]
    return random.choice(patterns)

def generate_timestamps(base_date=None, days_range=365):
    """Generate created_at and updated_at timestamps"""
    if base_date is None:
        base_date = fake.date_time_between(start_date='-2y', end_date='now')
    
    created_at = base_date
    updated_at = fake.date_time_between(start_date=created_at, end_date='now')
    
    return created_at.isoformat(), updated_at.isoformat()

def slugify(name):
    """Helper to convert company name into domain-friendly slug"""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def generate_clients():
    """Generate clients data - at least 100 entries with uniqueness and alignment"""
    clients = {}
    used_names = set()
    used_emails = set()
    used_phones = set()
    used_registration_numbers = set()
    
    industries_by_type = {
        'enterprise': ['Aerospace', 'Automotive', 'Government', 'Energy', 'Telecommunications', 'Financial Services'],
        'mid_market': ['Manufacturing', 'Insurance', 'Healthcare', 'Real Estate', 'Technology'],
        'small_business': ['Retail', 'Food & Beverage', 'Construction', 'Hospitality'],
        'startup': ['Technology', 'Biotechnology', 'Media', 'Education', 'Fintech']
    }

    email_prefixes = ["contact", "support", "info", "hello", "admin"]

    countries = [
        'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
        'Australia', 'Japan', 'Brazil', 'India', 'Mexico'
    ]
    
    for i in range(1, 121):  # 120 clients
        # Ensure unique company name
        while True:
            client_name = fake.company()
            if client_name not in used_names:
                used_names.add(client_name)
                break
        
        # Choose client_type and aligned industry
        client_type = random.choice(list(industries_by_type.keys()))
        industry = random.choice(industries_by_type[client_type])
        
        # Build domain from company name
        domain = f"{slugify(client_name)}.com"
        
        # Email aligned with company name
        email_prefix = random.choice(email_prefixes)
        email = f"{email_prefix}@{domain}"
        
        # Ensure unique email
        while email in used_emails:
            email = f"{email_prefix}{random.randint(1, 999)}@{domain}"
        used_emails.add(email)
        
        # Unique phone number
        phone = generate_phone()
        while phone in used_phones:
            phone = generate_phone()
        used_phones.add(phone)

        registration_number = f"REG{random.randint(100000, 999999)}"
        while registration_number in used_registration_numbers:
            registration_number = f"REG{random.randint(100000, 999999)}"
        used_registration_numbers.add(registration_number)
        
        # Status distribution
        status = random.choices(
            ['active', 'inactive', 'suspended'], weights=[85, 10, 5]
        )[0]
        
        created_at, updated_at = generate_timestamps()
        
        clients[str(i)] = {
            'client_id': str(i),
            'client_name': client_name,
            'registration_number': registration_number,
            'contact_email': email,
            'contact_phone': phone,
            'client_type': client_type,
            'industry': industry,
            'country': random.choice(countries),
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    data['clients'] = clients
    return clients

def generate_vendors():
    """Generate vendors data - at least 100 entries with realistic uniqueness"""
    vendors = {}
    used_names = set()
    used_emails = set()
    used_phones = set()
    
    vendor_types_names = {
        'cloud_provider': [
            'AOS Cloud', 'Azurian Cloud Services', 'Goggle Cloud Platform',
            'IBM Nimbus', 'Orcale Cloud', 'DigitalOceanic', 'LinodeX', 'Vulturis'
        ],
        'payment_processor': [
            'Stripee', 'PayPole', 'Squarix Payments', 'Adyant',
            'Worldpayz', 'Authorize.NetX', 'Braintreee', 'Klarno'
        ],
        'software_vendor': [
            'Microcraft', 'Orcale Systems', 'SAPhia Solutions',
            'SalesForza', 'Adobix', 'Atlasian', 'ServiceNowo', 'Workdaze'
        ],
        'infrastructure_provider': [
            'Cysco Systems', 'VMwere', 'Red Hatchet', 'Dockar Inc',
            'HashyCorp', 'Kubernetix', 'Terrafirm', 'Ansiblee'
        ],
        'security_vendor': [
            'CrowdStrik3', 'Palo Alto Netwerks', 'Symantix',
            'McAfree', 'Fortanett', 'CheckPoynt', 'Splonq', 'Oktra'
        ]
    }

    suffixes = ["Technologies", "Solutions", "Systems", "Services", "Networks"]

    email_prefixes = ["support", "info", "sales", "contact", "admin"]

    for i in range(1, 101):  # 100 vendors
        # Ensure unique vendor name
        while True:
            vendor_type = random.choice(list(vendor_types_names.keys()))
            base_name = random.choice(vendor_types_names[vendor_type])
            vendor_name = base_name if random.random() < 0.7 else f"{base_name} {random.choice(suffixes)}"
            if vendor_name not in used_names:
                used_names.add(vendor_name)
                break
        
        # Domain derived from vendor name
        domain = f"{slugify(base_name)}.com"
        email_prefix = random.choice(email_prefixes)
        email = f"{email_prefix}@{domain}"
        
        # Ensure unique email
        while email in used_emails:
            email = f"{email_prefix}{random.randint(1,999)}@{domain}"
        used_emails.add(email)
        
        # Ensure unique phone
        phone = generate_phone()
        while phone in used_phones:
            phone = generate_phone()
        used_phones.add(phone)
        
        status = random.choices(['active', 'inactive', 'suspended'], weights=[90, 7, 3])[0]
        created_at, _ = generate_timestamps()
        
        vendors[str(i)] = {
            'vendor_id': str(i),
            'vendor_name': vendor_name,
            'vendor_type': vendor_type,
            'contact_email': email,
            'contact_phone': phone,
            'status': status,
            'created_at': created_at
        }
    
    data['vendors'] = vendors
    return vendors

def generate_users():
    """Generate users data - with realistic status distributions"""
    users = {}
    clients = data['clients']
    vendors = data['vendors']
    
    departments_by_role = {
        'incident_manager': ['Operations', 'IT Support', 'Technical Operations'],
        'technical_support': ['Technical Support', 'Engineering', 'IT Operations'],
        'account_manager': ['Account Management', 'Customer Success', 'Business Development'],
        'executive': ['Executive', 'Management', 'Leadership'],
        'system_administrator': ['IT Administration', 'System Operations', 'Infrastructure'],
        'client_contact': lambda industry: [
            f"{industry} Operations", f"{industry} IT", "Business Operations"
        ],
        'vendor_contact': lambda vendor_type: [
            f"{vendor_type.replace('_', ' ').title()} Support",
            "Technical Account Management", "Customer Success"
        ]
    }
    
    user_id = 1
    
    # --------------------
    # Internal employees
    # --------------------
    for i in range(120):  # 120 internal employees
        first_name = fake.first_name()
        last_name = fake.last_name()
        role = random.choice(['incident_manager', 'technical_support', 'account_manager', 'executive', 'system_administrator'])
        department = random.choice(departments_by_role[role])
        created_at, updated_at = generate_timestamps()
        
        # 75% active, 15% inactive, 10% on_leave
        status = random.choices(
            ['active', 'inactive', 'on_leave'],
            weights=[75, 15, 10]
        )[0]
        
        users[str(user_id)] = {
            'user_id': str(user_id),
            'client_id': None,
            'vendor_id': None,
            'first_name': first_name,
            'last_name': last_name,
            'email': generate_email(first_name, last_name),
            'phone': generate_phone(),
            'role': role,
            'department': department,
            'timezone': random.choice(['EST', 'PST', 'CST', 'MST', 'UTC']),
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
        user_id += 1
    
    # --------------------
    # Client users
    # --------------------
    for client_id, client in clients.items():
        num_client_users = random.randint(2, 3)
        for i in range(num_client_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            department_name = departments_by_role['client_contact'](client['industry'])[0]
            created_at, updated_at = generate_timestamps()
            
            if client['status'] in ['inactive', 'suspended']:
                status = 'inactive'
            else:
                # Add some variation, with a few on_leave
                status = random.choices(
                    ['active', 'inactive', 'on_leave'],
                    weights=[80, 10, 10]
                )[0]
            
            users[str(user_id)] = {
                'user_id': str(user_id),
                'client_id': client_id,
                'vendor_id': None,
                'first_name': first_name,
                'last_name': last_name,
                'email': generate_email(first_name, last_name),
                'phone': generate_phone(),
                'role': 'client_contact',
                'department': department_name,
                'timezone': random.choice(['EST', 'PST', 'CST', 'MST', 'UTC']),
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
            user_id += 1
    
    # --------------------
    # Vendor users
    # --------------------
    for vendor_id, vendor in vendors.items():
        num_vendor_users = random.randint(1, 2)
        for i in range(num_vendor_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            department_name = departments_by_role['vendor_contact'](vendor['vendor_type'])[0]
            created_at, updated_at = generate_timestamps()
            
            if vendor['status'] in ['inactive', 'suspended']:
                status = 'inactive'
            else:
                # 80% active, 15% inactive, 5% on_leave
                status = random.choices(
                    ['active', 'inactive', 'on_leave'],
                    weights=[80, 15, 5]
                )[0]
            
            users[str(user_id)] = {
                'user_id': str(user_id),
                'client_id': None,
                'vendor_id': vendor_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': generate_email(first_name, last_name),
                'phone': generate_phone(),
                'role': 'vendor_contact',
                'department': department_name,
                'timezone': random.choice(['EST', 'PST', 'CST', 'MST', 'UTC']),
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
            user_id += 1
    
    data['users'] = users
    return users

def generate_products():
    """Generate products data - at least 100 entries"""
    products = {}
    vendors = data['vendors']

    used_product_names = set()

    def generate_unique_product_name(vendor_name, tech_terms, buzzwords):
        while True:
            name = f"{vendor_name.split()[0]} {random.choice(tech_terms)} {random.choice(buzzwords)}"
            if name not in used_product_names:
                used_product_names.add(name)
                return name

    product_types_by_vendor = {
        'cloud_provider': ['api_gateway', 'data_integration', 'monitoring_tool', 'backup_service'],
        'payment_processor': ['payment_processing', 'api_gateway'],
        'software_vendor': ['banking_system', 'reporting_platform', 'data_integration'],
        'infrastructure_provider': ['monitoring_tool', 'security_service', 'backup_service'],
        'security_vendor': ['security_service', 'monitoring_tool']
    }

    tech_terms = [
        "Nova", "Orion", "Zenith", "Apex", "Nimbus", "Pulse", "Quantum",
        "Vertex", "Horizon", "Stratus", "Vector", "Helix", "Axis",
        "Catalyst", "Core", "Stream", "Fusion", "Lumen", "Echo", "Forge"
    ]

    buzzwords = ["Suite", "Engine", "Service", "Cloud", "Matrix", "Portal", "Hub", "Edge", "Flow", "Core", "Stream", "Fabric"]
    
    product_id = 1
    
    # Generate products for active vendors
    for vendor_id, vendor in vendors.items():
        if vendor['status'] == 'active':
            num_products = random.randint(1, 2)  # 1-2 products per active vendor
            for i in range(num_products):
                product_type = random.choice(product_types_by_vendor[vendor['vendor_type']])
                created_at, updated_at = generate_timestamps()
                
                # Decide if product is in maintenance
                status = random.choices(
                    ['active', 'maintenance', 'deprecated'],
                    weights=[85, 10, 5]  # small fraction maintenance
                )[0]
                
                products[str(product_id)] = {
                    'product_id': str(product_id),
                    'product_name': generate_unique_product_name(vendor['vendor_name'], tech_terms, buzzwords),
                    'product_type': product_type,
                    'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    'vendor_support_id': vendor_id,
                    'status': status,
                    'created_at': created_at,
                    'updated_at': updated_at
                }
                product_id += 1
    
    # Generate additional products to reach at least 100
    while product_id <= 100:
        vendor = random.choice([v for v in vendors.values() if v['status'] == 'active'])
        product_type = random.choice(product_types_by_vendor[vendor['vendor_type']])
        created_at, updated_at = generate_timestamps()
        
        product_name = generate_unique_product_name(vendor['vendor_name'], tech_terms, buzzwords)
        
        status = random.choices(
            ['active', 'maintenance', 'deprecated'],
            weights=[85, 10, 5]
        )[0]
        
        products[str(product_id)] = {
            'product_id': str(product_id),
            'product_name': product_name,
            'product_type': product_type,
            'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            'vendor_support_id': vendor['vendor_id'],
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
        product_id += 1
    
    # Add some deprecated products for inactive vendors
    inactive_vendors = [v for v in vendors.values() if v['status'] in ['inactive', 'suspended']]
    for vendor in inactive_vendors[:10]:  # First 10 inactive vendors
        product_type = random.choice(product_types_by_vendor[vendor['vendor_type']])
        created_at, updated_at = generate_timestamps()
        
        product_name = generate_unique_product_name(vendor['vendor_name'], tech_terms, buzzwords)
        
        products[str(product_id)] = {
            'product_id': str(product_id),
            'product_name': product_name,
            'product_type': product_type,
            'version': f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            'vendor_support_id': vendor['vendor_id'],
            'status': 'deprecated',
            'created_at': created_at,
            'updated_at': updated_at
        }
        product_id += 1
    
    data['products'] = products
    return products

def generate_infrastructure_components():
    """Generate infrastructure components data - at least 100 entries"""
    components = {}
    products = data['products']
    
    component_types_by_product = {
        'payment_processing': ['payment_gateway', 'api_endpoint', 'database'],
        'banking_system': ['database', 'api_endpoint', 'authentication_service'],
        'api_gateway': ['api_endpoint', 'load_balancer', 'firewall'],
        'data_integration': ['sftp_server', 'api_endpoint', 'database'],
        'reporting_platform': ['database', 'api_endpoint', 'file_storage'],
        'security_service': ['firewall', 'authentication_service', 'monitoring_system'],
        'backup_service': ['file_storage', 'sftp_server', 'monitoring_system'],
        'monitoring_tool': ['monitoring_system', 'api_endpoint', 'database']
    }

    cloud_regions = [
        "aws-us-east-1", "aws-us-west-2", "gcp-europe-west3", 
        "azure-centralus", "aws-ap-southeast-1"
    ]
    datacenters = [
        "NYC-DC1", "SFO-DC2", "LON-DC3", "FRA-DC4", "SGP-DC5"
    ]
    
    component_id = 1
    for product_id, product in products.items():
        possible_components = component_types_by_product[product['product_type']]
        num_components = min(len(possible_components), random.randint(2, 4))
        
        # Ensure unique component types for this product
        chosen_components = random.sample(possible_components, num_components)
        
        for component_type in chosen_components:
            environment = random.choice(['production', 'staging', 'development', 'test'])
            
            # Status should align with product status
            if product['status'] == 'deprecated':
                status = 'offline'
            elif product['status'] == 'maintenance':
                status = 'maintenance'
            else:
                status = random.choices(
                    ['online', 'offline', 'maintenance', 'degraded'],
                    weights=[80, 5, 10, 5]
                )[0]
            
            # Location logic
            if component_type in ['api_endpoint', 'payment_gateway', 'load_balancer']:
                location = random.choice(cloud_regions)
            elif component_type in ['database', 'file_storage', 'sftp_server']:
                location = random.choice(datacenters)
            else:  # mixed
                location = random.choice(cloud_regions + datacenters)
            
            created_at, updated_at = generate_timestamps()
            
            # Structured unique name
            component_name = f"{product['product_name'].split()[0]}-{component_type.replace('_','').title()}-{environment.title()}"
            
            components[str(component_id)] = {
                'component_id': str(component_id),
                'product_id': product_id,
                'component_name': component_name,
                'component_type': component_type,
                'environment': environment,
                'location': location,
                'port_number': random.randint(8000, 9999) if component_type in ['api_endpoint', 'sftp_server'] else None,
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
            component_id += 1
    
    data['infrastructure_components'] = components
    return components

def generate_client_subscriptions():
    """Generate client subscriptions data - at least 100 entries"""
    subscriptions = {}
    clients = data['clients']
    products = data['products']
    
    subscription_id = 1
    all_clients = list(clients.values())
    all_products = list(products.values())

    TODAY = date(2025, 8, 29)

    def generate_subscription_dates(status):
        """Generate start and end dates depending on subscription status"""
        if status == 'active':
            start_date = fake.date_between(start_date='-2y', end_date='-1y')
            end_date = fake.date_between(start_date=TODAY + timedelta(days=30),
                                        end_date=TODAY + timedelta(days=365))
        elif status in ['expired', 'cancelled']:
            start_date = fake.date_between(start_date='-3y', end_date='-2y')
            end_date = fake.date_between(start_date=start_date + timedelta(days=180),
                                        end_date=TODAY - timedelta(days=30))  # strictly in past
        elif status == 'suspended':
            start_date = fake.date_between(start_date='-2y', end_date='-6m')
            # bias towards still having time left
            end_date = fake.date_between(start_date=TODAY - timedelta(days=30),
                                        end_date=TODAY + timedelta(days=365))
        else:
            # fallback
            start_date = fake.date_between(start_date='-2y', end_date='-6m')
            end_date = fake.date_between(start_date=start_date + timedelta(days=365),
                                        end_date=TODAY + timedelta(days=365))
        return start_date, end_date

    def choose_subscription_status(client_status, product_status):
        if client_status == 'active' and product_status == 'active':
            return random.choices(['active', 'expired', 'cancelled'], weights=[75, 15, 10])[0]
        elif client_status == 'active' and product_status == 'deprecated':
            return random.choice(['cancelled', 'suspended'])
        elif client_status == 'suspended':
            return 'suspended'
        elif client_status == 'inactive':
            return random.choice(['expired', 'cancelled', 'suspended'])
        else:
            return 'cancelled'
    
    # Ensure each client has 1–3 subscriptions
    for client in all_clients:
        num_subscriptions = random.randint(1, 3)
        selected_products = random.sample(all_products, min(num_subscriptions, len(all_products)))
        
        for product in selected_products:
            created_at, updated_at = generate_timestamps()
            status = choose_subscription_status(client['status'], product['status'])
            start_date, end_date = generate_subscription_dates(status)
            
            subscriptions[str(subscription_id)] = {
                'subscription_id': str(subscription_id),
                'client_id': client['client_id'],
                'product_id': product['product_id'],
                'subscription_type': random.choice(['full_service', 'limited_service', 'trial', 'custom']),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'sla_tier': random.choice(['premium', 'standard', 'basic']),
                'rto_hours': random.choice([1, 2, 4, 8, 24]),
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
            subscription_id += 1
    
    # Ensure at least 100
    while subscription_id <= 100:
        client = random.choice(all_clients)
        product = random.choice(all_products)
        created_at, updated_at = generate_timestamps()
        
        status = choose_subscription_status(client['status'], product['status'])
        start_date, end_date = generate_subscription_dates(status)

        subscriptions[str(subscription_id)] = {
            'subscription_id': str(subscription_id),
            'client_id': client['client_id'],
            'product_id': product['product_id'],
            'subscription_type': random.choice(['full_service', 'limited_service', 'trial', 'custom']),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'sla_tier': random.choice(['premium', 'standard', 'basic']),
            'rto_hours': random.choice([1, 2, 4, 8, 24]),
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
        subscription_id += 1
    
    data['client_subscriptions'] = subscriptions
    return subscriptions

def generate_sla_agreements():
    """Generate SLA agreements data with correct tier specifications"""
    sla_agreements = {}
    subscriptions = data['client_subscriptions']
    
    sla_id = 1
    for subscription_id, subscription in subscriptions.items():
        # Generate SLA for each severity level
        severities = ['P1', 'P2', 'P3', 'P4']
        tier = subscription['sla_tier']
        
        # Updated response times by tier (in minutes) - matching your specifications
        response_times = {
            'premium': {'P1': 15, 'P2': 60, 'P3': 240, 'P4': 1440},      # 15min, 1hr, 4hr, 24hr
            'standard': {'P1': 60, 'P2': 240, 'P3': 1440, 'P4': 2880},   # 1hr, 4hr, 24hr, 48hr
            'basic': {'P1': 240, 'P2': 1440, 'P3': 2880, 'P4': 7200}     # 4hr, 24hr, 48hr, 120hr
        }
        
        # Updated resolution times by tier (in hours) - matching your specifications
        resolution_times = {
            'premium': {'P1': 2, 'P2': 8, 'P3': 48, 'P4': None},         # 2hr, 8hr, 48hr, no target
            'standard': {'P1': 8, 'P2': 24, 'P3': 72, 'P4': None},       # 8hr, 24hr, 72hr, no target
            'basic': {'P1': 24, 'P2': 72, 'P3': 240, 'P4': None}         # 24hr, 72hr, 240hr, no target
        }
        
        # Availability percentages by tier
        availability_percentages = {
            'premium': 99.9,
            'standard': 99.5,
            'basic': 99.0
        }
        
        for severity in severities:
            created_at, _ = generate_timestamps()
            
            sla_agreements[str(sla_id)] = {
                'sla_id': str(sla_id),
                'subscription_id': subscription_id,
                'severity_level': severity,
                'response_time_minutes': response_times[tier][severity],
                'resolution_time_hours': resolution_times[tier][severity],
                'availability_percentage': availability_percentages[tier],
                'created_at': created_at
            }
            sla_id += 1
    
    data['sla_agreements'] = sla_agreements
    return sla_agreements

def ensure_diverse_incident_distribution():
    """Ensure we have good distribution across tiers, products, and severities"""
    components = data['infrastructure_components']
    subscriptions = data['client_subscriptions']
    
    # Create component groups by subscription tier
    components_by_tier = {'premium': [], 'standard': [], 'basic': []}
    
    for comp_id, comp in components.items():
        # Find subscription for this component's product
        for sub_id, sub in subscriptions.items():
            if sub['product_id'] == comp['product_id']:
                tier = sub['sla_tier']
                components_by_tier[tier].append(comp_id)
                break
    
    return components_by_tier

def generate_incidents():
    """Generate incidents with realistic SLA-aligned timing and many recent incidents around Aug 31, 2025"""
    incidents = {}
    users = data['users']
    clients = data['clients']
    components = data['infrastructure_components']
    products = data['products']
    subscriptions = data['client_subscriptions']
    sla_agreements = data['sla_agreements']

    # Create lookup maps
    reporters = [u for u in users.values() if u['status'] == 'active']
    managers = [u for u in users.values() if u['status'] == 'active' and u['role'] == 'incident_manager']
    
    active_clients = [c for c in clients.values() if c['status'] == 'active']
    inactive_clients = [c for c in clients.values() if c['status'] == 'inactive']
    suspended_clients = [c for c in clients.values() if c['status'] == 'suspended']

    product_by_id = {p['product_id']: p for p in products.values()}
    
    # Create subscription lookup by component
    subscription_by_component = {}
    for sub_id, sub in subscriptions.items():
        product_id = sub['product_id']
        # Find components for this product
        for comp_id, comp in components.items():
            if comp['product_id'] == product_id:
                subscription_by_component[comp_id] = sub
    
    # Create SLA lookup by subscription and severity
    sla_by_subscription = {}
    for sla_id, sla in sla_agreements.items():
        sub_id = sla['subscription_id']
        severity = sla['severity_level']
        if sub_id not in sla_by_subscription:
            sla_by_subscription[sub_id] = {}
        sla_by_subscription[sub_id][severity] = sla

    # Title catalog
    titles_by_component = {
        'api_endpoint': {
            'performance_issue': [
                'High API Latency Detected', '5xx Error Spike on API', 'Rate Limit Saturation'
            ],
            'integration_failure': [
                'API Connection Failed', 'Webhook Delivery Failures', 'OAuth Token Rejected'
            ],
            'system_outage': [
                'API Unavailable', 'Routing Failure to API', 'DNS Resolution Failure for API'
            ],
        },
        'payment_gateway': {
            'vendor_issue': [
                'Payment Authorization Failures', 'High Decline Rates from Processor', 'Settlement Delay from Vendor'
            ],
            'performance_issue': [
                'Gateway Timeout Errors', 'Increased Transaction Latency', 'Intermittent Capture Failures'
            ],
            'system_outage': [
                'Gateway Unreachable', 'Processor Endpoint Down', 'Critical Gateway Connectivity Loss'
            ],
        },
        'database': {
            'data_update': [
                'Schema Migration Error', 'Record Corruption Detected', 'Write Conflicts Observed'
            ],
            'performance_issue': [
                'Replication Lag High', 'Connection Pool Exhausted', 'Deadlocks Detected'
            ],
            'system_outage': [
                'Primary Database Unavailable', 'Failover Did Not Trigger', 'Storage Volume Not Mounted'
            ],
        },
        'load_balancer': {
            'system_outage': [
                'LB Health Checks Failing', 'VIP Not Reachable', 'Listener Crash on LB'
            ],
            'performance_issue': [
                'Uneven Traffic Distribution', 'SSL Termination Failures', 'Session Stickiness Broken'
            ],
        },
        'firewall': {
            'security_breach': [
                'Unusual Port Scans Detected', 'Unauthorized Access Attempt Blocked', 'Inbound Traffic Spike'
            ],
            'integration_failure': [
                'Firewall Blocking Legitimate Traffic', 'Rule Misconfiguration', 'Outbound Port Blocked'
            ],
        },
        'authentication_service': {
            'security_breach': [
                'Multiple Failed Login Attempts', 'Suspicious SSO Activity', 'Brute Force Attempt Detected'
            ],
            'client_support': [
                'SSO Login Failures', 'Token Expiry Mismatch', 'MFA Provider Timeout'
            ],
        },
        'sftp_server': {
            'data_update': [
                'SFTP Upload Permission Denied', 'Key Exchange Failure', 'Partial Transfers Detected'
            ],
            'integration_failure': [
                'SFTP Connection Timeout', 'Host Key Mismatch', 'Batch Job Could Not Connect to SFTP'
            ],
        },
        'file_storage': {
            'data_update': [
                'File Corruption Detected', 'Checksum Mismatch on Object', 'Stale Snapshot Restored'
            ],
            'performance_issue': [
                'Object Store Latency', 'Slow Reads from Storage', 'Write Throughput Degradation'
            ],
        },
        'monitoring_system': {
            'performance_issue': [
                'Dashboard Query Latency', 'Timeseries Backfill Lag', 'Indexing Queue Backlog', 
                'Alert Flood from Multiple Sources', 'Agent Offline Across Nodes', 'Metrics Ingestion Delay'
            ],
        },
    }

    fallback_titles = {
        'performance_issue': ['Slow Response Times', 'High Latency Detected', 'Resource Exhaustion'],
        'system_outage': ['Service Unavailable', 'Network Connectivity Lost', 'Complete System Down'],
        'integration_failure': ['Third-party Service Down', 'Data Flow Interrupted', 'API Connection Failed'],
        'security_breach': ['Unauthorized Access Detected', 'Suspicious Activity', 'Data Breach Alert'],
        'data_update': ['Data Sync Failed', 'Database Update Error', 'Record Corruption'],
        'client_support': ['Login Issues', 'Access Configuration Issue', 'User Provisioning Error'],
        'vendor_issue': ['Vendor Service Outage', 'Third-party Performance Issues', 'Vendor Communication Error'],
    }

    def pick_category_and_title(component_type):
        buckets = titles_by_component.get(component_type, {})
        if not buckets:
            cat = random.choice(list(fallback_titles.keys()))
            title = random.choice(fallback_titles[cat])
            return cat, title
        cat = random.choice(list(buckets.keys()))
        title = random.choice(buckets[cat])
        return cat, title

    def severity_to_impact_urgency(sev):
        mapping = {
            'P1': ('critical', 'critical'),
            'P2': ('high', 'high'),
            'P3': ('medium', 'medium'),
            'P4': ('low', 'low')
        }
        return mapping[sev]

    def choose_severity():
        return random.choices(['P1', 'P2', 'P3', 'P4'], weights=[10, 20, 40, 30])[0]

    def calculate_sla_compliant_resolution(detected_at, severity, subscription_id):
        """Calculate resolution time based on SLA requirements"""
        if subscription_id not in sla_by_subscription:
            return None, False
        
        sla = sla_by_subscription[subscription_id].get(severity)
        if not sla or not sla['resolution_time_hours']:
            return None, False
        
        # Calculate SLA deadline
        sla_deadline = detected_at + timedelta(hours=sla['resolution_time_hours'])
        
        # For incidents around Aug 31, 2025 - 80% chance of meeting SLA for recent ones
        # Historical incidents have normal 70% chance
        target_date = datetime(2025, 8, 31)
        days_from_target = abs((detected_at.date() - target_date.date()).days)
        
        if days_from_target <= 7:  # Recent incidents around Aug 31
            meets_sla = random.random() < 0.8  # Higher success rate
        else:  # Historical incidents
            meets_sla = random.random() < 0.7  # Normal rate
        
        if meets_sla:
            resolution_factor = random.uniform(0.1, 0.95)
            resolution_time = detected_at + timedelta(hours=sla['resolution_time_hours'] * resolution_factor)
        else:
            breach_factor = random.uniform(1.05, 2.0)
            resolution_time = detected_at + timedelta(hours=sla['resolution_time_hours'] * breach_factor)
        
        return resolution_time, not meets_sla

    def choose_latest_status(component_status, product_status):
        if component_status == 'offline':
            if product_status == 'active':
                return random.choice(['open', 'in_progress'])
            else:
                return 'closed'
        if component_status == 'maintenance':
            return 'in_progress'
        if component_status == 'degraded':
            return random.choice(['resolved', 'closed'])
        return random.choices(['open', 'in_progress', 'resolved', 'closed'], weights=[20, 30, 30, 20])[0]

    def choose_historical_status(component_status, product_status):
        if product_status == 'deprecated' and component_status == 'offline':
            return 'closed'
        return random.choices(['resolved', 'closed'], weights=[60, 40])[0]

    def client_for_status(status):
        if status == 'closed':
            pool_choice = random.choices(['active', 'inactive', 'suspended'], weights=[70, 15, 15])[0]
            if pool_choice == 'active' and active_clients:
                return random.choice(active_clients)
            if pool_choice == 'inactive' and inactive_clients:
                return random.choice(inactive_clients)
            if pool_choice == 'suspended' and suspended_clients:
                return random.choice(suspended_clients)
            return random.choice(active_clients) if active_clients else random.choice(list(clients.values()))
        else:
            return random.choice(active_clients) if active_clients else random.choice(list(clients.values()))

    incident_id = 1
    
    # Set target date to August 31, 2025
    target_date = datetime(2025, 8, 31, 23, 59, 59)

    # Define time periods around August 31, 2025
    recent_period_start = target_date - timedelta(days=7)    # Aug 24-31, 2025
    recent_period_end = target_date + timedelta(days=1)      # Until Sep 1, 2025
    historical_start = target_date - timedelta(days=540)     # 18 months before Aug 31
    historical_end = target_date - timedelta(days=30)        # 30 days before Aug 31

    # Get diverse component distribution
    components_by_tier = ensure_diverse_incident_distribution()

    previous_titles_by_component = {}

    for comp in components.values():
        comp_id = comp['component_id']
        comp_type = comp['component_type']
        prod = product_by_id.get(comp['product_id'])
        prod_status = prod['status'] if prod else 'active'
        
        # Get subscription for this component
        subscription = subscription_by_component.get(comp_id)
        tier = subscription['sla_tier'] if subscription else 'standard'

        # Decide number of incidents - more for premium tier around Aug 31
        if comp['status'] == 'online' and prod_status == 'active':
            if tier == 'premium':
                n_historical = random.randint(3, 5)
                n_recent = random.randint(3, 6)  # More incidents for premium
            elif tier == 'standard':
                n_historical = random.randint(2, 4)
                n_recent = random.randint(2, 4)
            else:  # basic
                n_historical = random.randint(1, 3)
                n_recent = random.randint(1, 3)
        else:
            n_historical = random.randint(1, 2)
            n_recent = random.randint(0, 1)

        # Generate historical incidents
        historical_timestamps = []
        for i in range(n_historical):
            dt = fake.date_time_between(start_date=historical_start, end_date=historical_end)
            historical_timestamps.append(dt)
        historical_timestamps.sort()

        # Generate recent incidents (around Aug 31, 2025)
        recent_timestamps = []
        for i in range(n_recent):
            dt = fake.date_time_between(start_date=recent_period_start, end_date=recent_period_end)
            recent_timestamps.append(dt)
        recent_timestamps.sort()

        all_timestamps = historical_timestamps + recent_timestamps
        n_total = len(all_timestamps)

        # Determine statuses
        statuses = []
        for i in range(n_total):
            if i == n_total - 1:  # Latest incident
                statuses.append(choose_latest_status(comp['status'], prod_status))
            elif i >= n_historical:  # Recent incidents
                # Recent incidents more likely to be open/in_progress
                statuses.append(random.choices(['open', 'in_progress', 'resolved'], weights=[30, 40, 30])[0])
            else:  # Historical incidents
                statuses.append(choose_historical_status(comp['status'], prod_status))

        # Handle special cases
        if prod_status == 'deprecated' and comp['status'] == 'offline':
            statuses = ['closed'] * n_total
        if comp['status'] == 'degraded':
            statuses = [s if s in ['resolved', 'closed'] else random.choice(['resolved', 'closed']) for s in statuses]

        # Generate incidents
        prev_titles = previous_titles_by_component.setdefault(comp_id, [])

        for idx in range(n_total):
            status = statuses[idx]
            detected_at = all_timestamps[idx]
            created_at = detected_at + timedelta(minutes=random.randint(1, 30))

            # Choose title
            if prev_titles and random.random() < 0.25:
                category, title = random.choice(prev_titles)
                is_recurring = True
            else:
                category, title = pick_category_and_title(comp_type)
                is_recurring = False

            # Ensure severity distribution varies by tier and time period
            if idx >= n_historical:  # Recent incidents
                if tier == 'premium':
                    severity = random.choices(['P1', 'P2', 'P3', 'P4'], weights=[20, 30, 35, 15])[0]
                elif tier == 'standard':
                    severity = random.choices(['P1', 'P2', 'P3', 'P4'], weights=[10, 25, 45, 20])[0]
                else:  # basic
                    severity = random.choices(['P1', 'P2', 'P3', 'P4'], weights=[5, 15, 40, 40])[0]
            else:  # Historical incidents
                severity = choose_severity()  # Use original distribution

            impact, urgency = severity_to_impact_urgency(severity)

            # Calculate resolution timing based on SLA
            resolved_at = None
            closed_at = None
            sla_breach = False
            rto_breach = False

            if status in ['resolved', 'closed']:
                if subscription:
                    calculated_resolution, is_sla_breach = calculate_sla_compliant_resolution(
                        detected_at, severity, subscription['subscription_id']
                    )
                    if calculated_resolution:
                        resolved_at = calculated_resolution
                        sla_breach = is_sla_breach
                        rto_breach = is_sla_breach and severity in ['P1', 'P2']
                    else:
                        # Fallback if no SLA
                        resolved_at = detected_at + timedelta(hours=random.randint(1, 48))
                else:
                    # No subscription - use random timing
                    resolved_at = detected_at + timedelta(hours=random.randint(1, 48))
                
                if status == 'closed':
                    closed_at = resolved_at + timedelta(hours=random.randint(1, 24))

            # Manager assignment
            assigned_manager = None
            if status != 'open' and managers:
                assigned_manager = random.choice(managers)

            # Client selection
            client = client_for_status(status)

            # Reporter
            reporter = random.choice(reporters) if reporters else random.choice(list(users.values()))

            # Downtime calculation
            downtime_minutes = 0
            if severity in ['P1', 'P2'] and resolved_at:
                downtime_duration = resolved_at - detected_at
                downtime_minutes = min(int(downtime_duration.total_seconds() / 60), 480)  # Cap at 8 hours

            # Track titles for recurrence
            if not any(t == title for (_, t) in prev_titles):
                prev_titles.append((category, title))

            # Build incident record
            incidents[str(incident_id)] = {
                'incident_id': str(incident_id),
                'title': title,
                'reporter_id': reporter['user_id'],
                'assigned_manager_id': assigned_manager['user_id'] if assigned_manager else None,
                'client_id': client['client_id'],
                'component_id': comp_id,
                'severity': severity,
                'status': status,
                'impact': impact,
                'urgency': urgency,
                'category': category,
                'detected_at': detected_at.isoformat(),
                'resolved_at': resolved_at.isoformat() if resolved_at else None,
                'closed_at': closed_at.isoformat() if closed_at else None,
                'rto_breach': rto_breach,
                'sla_breach': sla_breach,
                'is_recurring': is_recurring,
                'downtime_minutes': downtime_minutes,
                'created_at': created_at.isoformat(),
                'updated_at': (closed_at or resolved_at or created_at + timedelta(hours=random.randint(1, 24))).isoformat()
            }

            incident_id += 1

    data['incidents'] = incidents
    return incidents

def generate_incident_updates():
    """Generate incident updates data with proper alignment to incidents, workarounds, communications"""
    updates = {}
    incidents = data['incidents']
    users = data['users']
    workarounds = data.get('workarounds', {})
    communications = data.get('communications', {})
    
    eligible_updaters = [
        u for u in users.values()
        if u['status'] == 'active' and u['role'] in ['incident_manager', 'technical_support', 'executive']
    ]
    managers = [u for u in users.values() if u['status'] == 'active' and u['role'] == 'incident_manager']
    
    update_id = 1
    for incident_id, incident in incidents.items():
        incident_created = datetime.fromisoformat(incident['created_at'].replace('Z', ''))
        incident_updated = datetime.fromisoformat(incident['updated_at'].replace('Z', ''))

        # Keep track of applied updates so we can ensure final state matches
        current_severity = incident['severity']
        current_manager = incident['assigned_manager_id']
        current_status = incident['status']

        incident_updates = []

        # Status / Resolution updates
        if current_status in ['resolved', 'closed']:
            # Generate past status changes before resolution
            if random.random() < 0.6:
                incident_updates.append({
                    'update_type': 'status_change',
                    'field_name': 'status',
                    'old_value': 'open',
                    'new_value': 'in_progress'
                })
            incident_updates.append({
                'update_type': 'resolution',
                'field_name': 'status',
                'old_value': 'in_progress',
                'new_value': 'resolved'
            })
            if current_status == 'closed':
                incident_updates.append({
                    'update_type': 'status_change',
                    'field_name': 'status',
                    'old_value': 'resolved',
                    'new_value': 'closed'
                })
        elif current_status in ['in_progress', 'open']:
            # At least one status change if in_progress
            if current_status == 'in_progress':
                incident_updates.append({
                    'update_type': 'status_change',
                    'field_name': 'status',
                    'old_value': 'open',
                    'new_value': 'in_progress'
                })

        # Severity changes
        if random.random() < 0.4:  # 40% of incidents had a severity change
            old_severity = random.choice(['P1', 'P2', 'P3', 'P4'])
            if old_severity != current_severity:
                incident_updates.append({
                    'update_type': 'severity_change',
                    'field_name': 'severity',
                    'old_value': old_severity,
                    'new_value': current_severity
                })

        # Assignments
        if current_manager:
            prev_manager = random.choice(managers)['user_id']
            if prev_manager != current_manager and random.random() < 0.5:
                incident_updates.append({
                    'update_type': 'assignment',
                    'field_name': 'assigned_manager_id',
                    'old_value': prev_manager,
                    'new_value': current_manager
                })
            else:
                incident_updates.append({
                    'update_type': 'assignment',
                    'field_name': 'assigned_manager_id',
                    'old_value': None,
                    'new_value': current_manager
                })

        # Workaround updates (if exists for this incident)
        incident_workarounds = [w for w in workarounds.values() if w['incident_id'] == incident_id]
        for w in incident_workarounds:
            incident_updates.append({
                'update_type': 'workaround',
                'field_name': 'workaround_id',
                'old_value': None,
                'new_value': w['workaround_id']
            })

        # Communication updates (if exists for this incident)
        incident_comms = [c for c in communications.values() if c['incident_id'] == incident_id]
        for c in incident_comms:
            incident_updates.append({
                'update_type': 'communication',
                'field_name': 'communication_id',
                'old_value': None,
                'new_value': c['communication_id']
            })

        # Assign timestamps and updater
        for upd in incident_updates:
            updater = random.choice(eligible_updaters)
            created_at = fake.date_time_between(start_date=incident_created, end_date=incident_updated)

            updates[str(update_id)] = {
                'update_id': str(update_id),
                'incident_id': incident_id,
                'updated_by_id': updater['user_id'],
                'update_type': upd['update_type'],
                'field_name': upd['field_name'],
                'old_value': upd['old_value'],
                'new_value': upd['new_value'],
                'created_at': created_at.isoformat()
            }
            update_id += 1

    data['incident_updates'] = updates
    return updates

def generate_workarounds():
    """Generate workarounds data - at least 100 entries"""
    workarounds = {}
    incidents = data['incidents']
    users = data['users']
    
    # Only incidents with P1, P2 severity might have workarounds
    critical_incidents = {k: v for k, v in incidents.items() if v['severity'] in ['P1', 'P2']}
    
    # Users who can implement workarounds (incident managers, technical support, account managers)
    implementers = [u for u in users.values() if u['status'] == 'active' and 
                   u['role'] in ['incident_manager', 'technical_support', 'system_administrator']]
    
    workaround_id = 1
    for incident_id, incident in critical_incidents.items():
        if random.choice([True, False]):  # 50% chance of having a workaround
            implementer = random.choice(implementers)
            
            # Status should align with incident status
            if incident['status'] == 'in_progress':
                status = 'active'
            elif incident['status'] in ['resolved', 'closed']:
                status = random.choice(['inactive', 'replaced'])
            else:
                continue  # Skip open incidents
            
            implemented_at = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
                end_date=datetime.fromisoformat(incident['updated_at'].replace('Z', ''))
            )
            created_at, _ = generate_timestamps(base_date=implemented_at)
            
            workarounds[str(workaround_id)] = {
                'workaround_id': str(workaround_id),
                'incident_id': incident_id,
                'implemented_by_id': implementer['user_id'],
                'effectiveness': random.choice(['complete', 'partial', 'minimal']),
                'status': status,
                'implemented_at': implemented_at.isoformat(),
                'created_at': created_at
            }
            workaround_id += 1
    
    # Generate additional workarounds to reach at least 100
    while workaround_id <= 100:
        incident = random.choice(list(critical_incidents.values()))
        implementer = random.choice(implementers)
        
        if incident['status'] == 'in_progress':
            status = 'active'
        elif incident['status'] in ['resolved', 'closed']:
            status = random.choice(['inactive', 'replaced'])
        else:
            continue
        
        implemented_at = fake.date_time_between(
            start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
            end_date=datetime.fromisoformat(incident['updated_at'].replace('Z', ''))
        )
        created_at, _ = generate_timestamps(base_date=implemented_at)
        
        workarounds[str(workaround_id)] = {
            'workaround_id': str(workaround_id),
            'incident_id': incident['incident_id'],
            'implemented_by_id': implementer['user_id'],
            'effectiveness': random.choice(['complete', 'partial', 'minimal']),
            'status': status,
            'implemented_at': implemented_at.isoformat(),
            'created_at': created_at
        }
        workaround_id += 1
    
    data['workarounds'] = workarounds
    return workarounds

def generate_root_cause_analysis():
    """Generate root cause analysis data - at least 100 entries"""
    rca_data = {}
    incidents = data['incidents']
    users = data['users']
    
    # RCA for in_progress and resolved incidents
    eligible_incidents = {k: v for k, v in incidents.items() if v['status'] in ['in_progress', 'resolved']}
    
    # Users who can conduct RCA
    conductors = [u for u in users.values() if u['status'] == 'active' and 
                 u['role'] in ['incident_manager', 'technical_support', 'system_administrator']]
    
    rca_id = 1
    for incident_id, incident in eligible_incidents.items():
        conductor = random.choice(conductors)
        
        # Status should align with incident status
        if incident['status'] == 'in_progress':
            rca_status = random.choice(['in_progress', 'completed'])
        else:  # resolved
            rca_status = random.choice(['completed', 'approved'])
        
        completed_at = None
        if rca_status in ['completed', 'approved']:
            completed_at = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
                end_date=datetime.fromisoformat(incident['updated_at'].replace('Z', ''))
            ).isoformat()
        
        created_at, _ = generate_timestamps()
        
        rca_data[str(rca_id)] = {
            'rca_id': str(rca_id),
            'incident_id': incident_id,
            'analysis_method': random.choice(['five_whys', 'fishbone', 'timeline_analysis', 'fault_tree']),
            'conducted_by_id': conductor['user_id'],
            'completed_at': completed_at,
            'status': rca_status,
            'created_at': created_at
        }
        rca_id += 1
    
    data['root_cause_analysis'] = rca_data
    return rca_data

def generate_communications():
    """Generate communications data - at least 100 entries"""
    communications = {}
    incidents = data['incidents']
    users = data['users']
    
    # Users who can send communications
    senders = [u for u in users.values() if u['status'] == 'active' and 
              u['role'] in ['incident_manager', 'technical_support']]
    
    # Users who can receive communications
    recipients = [u for u in users.values() if u['status'] == 'active']
    
    recipient_type_by_role = {
        'client_contact': 'client',
        'incident_manager': 'internal_team',
        'technical_support': 'internal_team',
        'account_manager': 'internal_team',
        'executive': 'executive',
        'system_administrator': 'internal_team',
        'vendor_contact': 'vendor'
    }
    
    comm_id = 1
    for incident_id, incident in incidents.items():
        num_communications = random.randint(1, 3)
        
        for i in range(num_communications):
            sender = random.choice(senders)
            recipient = random.choice(recipients)
            
            recipient_type = recipient_type_by_role.get(recipient['role'], 'internal_team')
            
            sent_at = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
                end_date=datetime.fromisoformat(incident['updated_at'].replace('Z', ''))
            )
            
            created_at, _ = generate_timestamps(base_date=sent_at)
            
            communications[str(comm_id)] = {
                'communication_id': str(comm_id),
                'incident_id': incident_id,
                'sender_id': sender['user_id'],
                'recipient_id': recipient['user_id'],
                'recipient_type': recipient_type,
                'communication_type': random.choice(['email', 'sms', 'phone_call', 'status_page', 'portal_update']),
                'sent_at': sent_at.isoformat(),
                'delivery_status': random.choices(['sent', 'delivered', 'failed', 'pending'], 
                                                weights=[20, 70, 5, 5])[0],
                'created_at': created_at
            }
            comm_id += 1
    
    data['communications'] = communications
    return communications

def generate_escalations():
    """Generate realistic escalations data - at least 100 entries"""
    escalations = {}
    incidents = data['incidents']
    users = data['users']
    workarounds = data.get('workarounds', {})

    # eligible incidents: only in_progress / resolved
    eligible_incidents = {
        k: v for k, v in incidents.items()
        if v['status'] in ['in_progress', 'resolved']
    }

    # users allowed to escalate
    escalation_to_users = [
        u for u in users.values()
        if u['status'] == 'active' and u['role'] in [
            'incident_manager', 'technical_support', 'account_manager', 'executive', 'vendor_contact'
        ]
    ]
    escalation_by_users = [
        u for u in users.values()
        if u['status'] == 'active' and u['role'] in [
            'incident_manager', 'technical_support', 'account_manager', 'executive'
        ]
    ]

    escalation_level_by_role = {
        'technical_support': 'technical',
        'incident_manager': 'management',
        'account_manager': 'management',
        'executive': 'executive',
        'vendor_contact': 'vendor'
    }

    escalation_id = 1
    for incident_id, incident in list(eligible_incidents.items()):
        if random.random() < 0.5:  # ~50% chance of escalation
            escalated_by = random.choice(escalation_by_users)
            possible_targets = [u for u in escalation_to_users if u['user_id'] != escalated_by['user_id']]
            escalated_to = random.choice(possible_targets)

            # ---- Reason determination ----
            reasons = []
            if incident.get('sla_breach'):
                reasons.append('sla_breach')
            if incident['severity'] in ['P1','P2','P3']:
                reasons.append('severity_increase')
            if incident['status'] == 'in_progress':
                # unresolved but workaround exists → resource issue
                if any(w['incident_id'] == incident_id for w in workarounds.values()):
                    reasons.append('resource_unavailable')
            # fallback reasons if none matched
            if not reasons:
                reasons = ['executive_request','client_demand']
            escalation_reason = random.choice(reasons)

            escalation_level = escalation_level_by_role[escalated_to['role']]

            escalated_at = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z','')),
                end_date=datetime.fromisoformat(incident['updated_at'].replace('Z',''))
            )

            acknowledged_at = None
            resolved_at = None
            status = random.choice(['open','acknowledged','resolved'])
            if status in ['acknowledged','resolved']:
                acknowledged_at = escalated_at + timedelta(hours=random.randint(1,4))
                if status == 'resolved':
                    resolved_at = acknowledged_at + timedelta(hours=random.randint(1,8))

            created_at, _ = generate_timestamps(base_date=escalated_at)

            escalations[str(escalation_id)] = {
                'escalation_id': str(escalation_id),
                'incident_id': incident_id,
                'escalated_by_id': escalated_by['user_id'],
                'escalated_to_id': escalated_to['user_id'],
                'escalation_reason': escalation_reason,
                'escalation_level': escalation_level,
                'escalated_at': escalated_at.isoformat(),
                'acknowledged_at': acknowledged_at.isoformat() if acknowledged_at else None,
                'resolved_at': resolved_at.isoformat() if resolved_at else None,
                'status': status,
                'created_at': created_at
            }
            escalation_id += 1

    data['escalations'] = escalations
    return escalations

def generate_change_requests():
    """Generate change requests data - at least 100 entries"""
    change_requests = {}
    incidents = data['incidents']
    users = data['users']
    
    # Change requests for in_progress and resolved incidents
    eligible_incidents = {k: v for k, v in incidents.items() if v['status'] in ['in_progress', 'resolved']}
    
    # Users who can request and approve changes
    requesters = [u for u in users.values() if u['status'] == 'active' and 
                 u['role'] in ['incident_manager', 'technical_support', 'system_administrator', 'executive']]
    approvers = [u for u in users.values() if u['status'] == 'active' and 
                u['role'] in ['incident_manager', 'technical_support', 'executive']]
    
    change_id = 1
    for incident_id, incident in list(eligible_incidents.items())[:120]:  # Limit to 120
        requester = random.choice(requesters)
        approver = random.choice(approvers)
        while approver == requester:
            approver = random.choice(approvers)
        
        change_type = random.choice(['emergency', 'standard', 'normal'])
        risk_level = random.choice(['high', 'medium', 'low'])
        status = random.choice(['requested', 'approved', 'scheduled', 'in_progress', 'completed', 'failed', 'rolled_back'])
        
        scheduled_start = None
        scheduled_end = None
        actual_start = None
        actual_end = None
        
        if status in ['scheduled', 'in_progress', 'completed', 'failed', 'rolled_back']:
            base_time = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
                end_date='now'
            )
            scheduled_start = base_time
            scheduled_end = base_time + timedelta(hours=random.randint(1, 8))
            
            if status in ['in_progress', 'completed', 'failed', 'rolled_back']:
                actual_start = scheduled_start + timedelta(minutes=random.randint(-30, 30))
                if status in ['completed', 'failed', 'rolled_back']:
                    actual_end = actual_start + timedelta(hours=random.randint(1, 12))
        
        created_at, updated_at = generate_timestamps()
        
        change_requests[str(change_id)] = {
            'change_id': str(change_id),
            'incident_id': incident_id,
            'title': f"Emergency Fix for {incident['title']}",
            'change_type': change_type,
            'requested_by_id': requester['user_id'],
            'approved_by_id': approver['user_id'] if status != 'requested' else None,
            'risk_level': risk_level,
            'scheduled_start': scheduled_start.isoformat() if scheduled_start else None,
            'scheduled_end': scheduled_end.isoformat() if scheduled_end else None,
            'actual_start': actual_start.isoformat() if actual_start else None,
            'actual_end': actual_end.isoformat() if actual_end else None,
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
        change_id += 1
    
    data['change_requests'] = change_requests
    return change_requests

def generate_rollback_requests():
    """Generate rollback requests data - at least 100 entries"""
    rollback_requests = {}
    change_requests = data['change_requests']
    incidents = data['incidents']
    users = data['users']
    
    # Rollbacks for failed or problematic change requests
    failed_changes = {k: v for k, v in change_requests.items() if v['status'] in ['failed', 'rolled_back']}
    
    requesters = [u for u in users.values() if u['status'] == 'active' and 
                 u['role'] in ['incident_manager', 'technical_support', 'executive']]
    approvers = [u for u in users.values() if u['status'] == 'active' and 
                u['role'] in ['incident_manager', 'executive', 'technical_support']]
    
    rollback_id = 1
    for change_id, change in failed_changes.items():
        requester = random.choice(requesters)
        approver = random.choice(approvers)

        while approver == requester:
            approver = random.choice(approvers)
        
        status = random.choice(['requested', 'approved', 'in_progress', 'completed', 'failed'])
        
        executed_at = None
        if status in ['in_progress', 'completed', 'failed']:
            executed_at = fake.date_time_between(
                start_date=datetime.fromisoformat(change['created_at'].replace('Z', '')),
                end_date='now'
            ).isoformat()
        
        created_at, _ = generate_timestamps()
        
        rollback_requests[str(rollback_id)] = {
            'rollback_id': str(rollback_id),
            'change_id': change_id,
            'incident_id': change['incident_id'],
            'requested_by_id': requester['user_id'],
            'approved_by_id': approver['user_id'] if status != 'requested' else None,
            'executed_at': executed_at,
            'validation_completed': random.choice([True, False]) if status == 'completed' else False,
            'status': status,
            'created_at': created_at
        }
        rollback_id += 1
    
    data['rollback_requests'] = rollback_requests
    return rollback_requests

def generate_metrics():
    """Generate metrics data - at least 100 entries"""
    metrics = {}
    incidents = data['incidents']
    
    metric_id = 1
    for incident_id, incident in incidents.items():
        # Generate 1-2 metrics per incident
        num_metrics = random.randint(1, 2)
        
        for i in range(num_metrics):
            metric_type = random.choice(['MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'])
            
            # Value based on incident severity
            if incident['severity'] == 'P1':
                value_minutes = random.randint(15, 120)
                target_minutes = random.randint(30, 60)
            elif incident['severity'] == 'P2':
                value_minutes = random.randint(30, 240)
                target_minutes = random.randint(60, 120)
            elif incident['severity'] == 'P3':
                value_minutes = random.randint(60, 480)
                target_minutes = random.randint(120, 240)
            else:  # P4
                value_minutes = random.randint(120, 1440)
                target_minutes = random.randint(240, 480)
            
            recorded_at = fake.date_time_between(
                start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
                end_date=datetime.fromisoformat(incident['updated_at'].replace('Z', ''))
            )
            created_at, _ = generate_timestamps(base_date=recorded_at)
            
            metrics[str(metric_id)] = {
                'metric_id': str(metric_id),
                'incident_id': incident_id,
                'metric_type': metric_type,
                'value_minutes': value_minutes,
                'target_minutes': target_minutes,
                'recorded_at': recorded_at.isoformat(),
                'created_at': created_at
            }
            metric_id += 1
    
    data['metrics'] = metrics
    return metrics

def generate_incident_reports():
    """Generate incident reports data - at least 100 entries"""
    incident_reports = {}
    incidents = data['incidents']
    users = data['users']
    
    # Users who can generate reports
    generators = [u for u in users.values() if u['status'] == 'active' and 
                 u['role'] in ['incident_manager', 'account_manager', 'executive']]
    
    report_id = 1
    for incident_id, incident in incidents.items():
        generator = random.choice(generators)
        report_type = random.choice(['executive_summary', 'technical_details', 'business_impact', 
                                    'compliance_report', 'post_mortem'])
        status = random.choice(['draft', 'completed', 'distributed'])
        
        generated_at = fake.date_time_between(
            start_date=datetime.fromisoformat(incident['created_at'].replace('Z', '')),
            end_date='now'
        )
        created_at, _ = generate_timestamps(base_date=generated_at)
        
        incident_reports[str(report_id)] = {
            'report_id': str(report_id),
            'incident_id': incident_id,
            'report_type': report_type,
            'generated_by_id': generator['user_id'],
            'generated_at': generated_at.isoformat(),
            'status': status,
            'created_at': created_at
        }
        report_id += 1
    
    data['incident_reports'] = incident_reports
    return incident_reports

def generate_knowledge_base_articles():
    """Generate knowledge base articles data - at least 100 entries"""
    kb_articles = {}
    incidents = data['incidents']
    users = data['users']
    
    # Incident category -> KB baseline category
    incident_category_map = {
        'client_onboarding': 'client_onboarding',
        'client_support': 'incident_response',
        'client_escalation': 'sla_management',
        'data_update': 'data_synchronization',
        'system_outage': 'system_outages',
        'security_breach': 'security_incidents',
        'performance_issue': 'performance_degradation',
        'integration_failure': 'third_party_integrations',
        'vendor_issue': 'vendor_escalations'
    }

    # Component type -> More specific KB category
    component_category_map = {
        'sftp_server': 'file_transfer_problems',
        'api_endpoint': 'api_integration',
        'database': 'database_issues',
        'load_balancer': 'network_connectivity',
        'firewall': 'network_connectivity',
        'authentication_service': 'authentication_issues',
        'payment_gateway': 'payment_processing',
        'file_storage': 'backup_recovery',
        'monitoring_system': 'monitoring_alerts'
    }

    def determine_kb_category(incident, components):
        """
        Pick KB category based on incident category + component type.
        """
        base_category = incident_category_map.get(incident['category'], 'incident_response')
        if incident.get('component_id') and incident['component_id'] in components:
            comp_type = components[incident['component_id']]['component_type']
            return component_category_map.get(comp_type, base_category)
        return base_category

    def determine_article_type(incident):
        """
        Choose article type based on severity/status/flags.
        """
        if incident['status'] == 'resolved':
            return 'resolution_steps'
        if incident['severity'] in ['P1', 'P2']:
            return 'troubleshooting'
        if incident.get('is_recurring') or incident.get('sla_breach') or incident.get('rto_breach'):
            return 'prevention_guide'
        return 'faq'
    
    # Users who can create and review articles
    creators = [u for u in users.values() if u['status'] == 'active' and 
               u['role'] in ['incident_manager', 'technical_support']]
    reviewers = [u for u in users.values() if u['status'] == 'active' and 
                u['role'] in ['incident_manager', 'technical_support', 'executive']]
    
    categories = [
        'authentication_issues', 'payment_processing', 'api_integration',
        'data_synchronization', 'system_outages', 'performance_degradation',
        'security_incidents', 'backup_recovery', 'user_management',
        'billing_issues', 'compliance_procedures', 'vendor_escalations'
    ]
    
    article_id = 1
    
    # Generate articles based on incidents
    for incident_id, incident in list(incidents.items())[:150]:  # Limit to 150
        if random.choice([True, False]):  # 50% chance
            creator = random.choice(creators)
            reviewer = random.choice(reviewers) if random.choice([True, False]) else None
            
            article_type = determine_article_type(incident)
            category = determine_kb_category(incident, data['infrastructure_components'])
            status = random.choice(['draft', 'published', 'archived'])
            
            created_at, updated_at = generate_timestamps()
            
            kb_articles[str(article_id)] = {
                'article_id': str(article_id),
                'incident_id': incident_id,
                'title': f"How to Handle {incident['title']}",
                'article_type': article_type,
                'created_by_id': creator['user_id'],
                'reviewed_by_id': reviewer['user_id'] if reviewer else None,
                'category': category,
                'view_count': random.randint(1, 500),
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
            article_id += 1
    
    # Generate additional standalone articles
    while article_id <= 100:
        creator = random.choice(creators)
        reviewer = random.choice(reviewers) if random.choice([True, False]) else None
        
        article_type = random.choice(['troubleshooting', 'resolution_steps', 'prevention_guide', 'faq'])
        category = random.choice(categories)
        status = random.choice(['draft', 'published', 'archived'])
        
        created_at, updated_at = generate_timestamps()
        
        kb_articles[str(article_id)] = {
            'article_id': str(article_id),
            'incident_id': None,
            'title': f"General Guide: {fake.catch_phrase()}",
            'article_type': article_type,
            'created_by_id': creator['user_id'],
            'reviewed_by_id': reviewer['user_id'] if reviewer else None,
            'category': category,
            'view_count': random.randint(0, 500),
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        }
        article_id += 1
    
    data['knowledge_base_articles'] = kb_articles
    return kb_articles

def generate_post_incident_reviews():
    """Generate post incident reviews data - at least 100 entries"""
    pir_data = {}
    incidents = data['incidents']
    users = data['users']
    
    # PIRs for resolved and closed incidents
    eligible_incidents = {k: v for k, v in incidents.items() if v['status'] in ['resolved', 'closed']}
    
    # Users who can facilitate PIRs
    facilitators = [u for u in users.values() if u['status'] == 'active' and 
                   u['role'] in ['incident_manager', 'executive']]
    
    pir_id = 1
    for incident_id, incident in eligible_incidents.items():
        facilitator = random.choice(facilitators)
        
        # Schedule PIR after incident closure
        incident_end = datetime.fromisoformat((incident['closed_at'] or incident['resolved_at']).replace('Z', ''))
        scheduled_date = incident_end + timedelta(days=random.randint(1, 7))
        
        status = random.choice(['scheduled', 'completed', 'cancelled'])
        
        created_at, _ = generate_timestamps()
        
        pir_data[str(pir_id)] = {
            'pir_id': str(pir_id),
            'incident_id': incident_id,
            'scheduled_date': scheduled_date.isoformat(),
            'facilitator_id': facilitator['user_id'],
            'timeline_accuracy_rating': random.randint(1, 5) if status == 'completed' else None,
            'communication_effectiveness_rating': random.randint(1, 5) if status == 'completed' else None,
            'technical_response_rating': random.randint(1, 5) if status == 'completed' else None,
            'status': status,
            'created_at': created_at
        }
        pir_id += 1
    
    data['post_incident_reviews'] = pir_data
    return pir_data

def save_all_data():
    """Save all generated data to JSON files"""
    # Generate all data in order (respecting dependencies)
    print("Generating clients...")
    generate_clients()
    
    print("Generating vendors...")
    generate_vendors()
    
    print("Generating users...")
    generate_users()
    
    print("Generating products...")
    generate_products()
    
    print("Generating infrastructure components...")
    generate_infrastructure_components()
    
    print("Generating client subscriptions...")
    generate_client_subscriptions()
    
    print("Generating SLA agreements...")
    generate_sla_agreements()
    
    print("Generating incidents...")
    generate_incidents()
    
    print("Generating workarounds...")
    generate_workarounds()
    
    print("Generating root cause analysis...")
    generate_root_cause_analysis()
    
    print("Generating communications...")
    generate_communications()

    print("Generating incident updates...")
    generate_incident_updates()
    
    print("Generating escalations...")
    generate_escalations()
    
    print("Generating change requests...")
    generate_change_requests()
    
    print("Generating rollback requests...")
    generate_rollback_requests()
    
    print("Generating metrics...")
    generate_metrics()
    
    print("Generating incident reports...")
    generate_incident_reports()
    
    print("Generating knowledge base articles...")
    generate_knowledge_base_articles()
    
    print("Generating post incident reviews...")
    generate_post_incident_reviews()
    
    # Save to individual JSON files
    for table_name, table_data in data.items():
        filename = f"incident_management_data/{table_name}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(table_data, f, indent=2, ensure_ascii=False)
        print(f"Generated {filename} with {len(table_data)} records")
    
    print("\nData generation complete!")
    print(f"Total tables generated: {len(data)}")
    for table_name, table_data in data.items():
        print(f"  {table_name}: {len(table_data)} records")

if __name__ == "__main__":
    save_all_data()