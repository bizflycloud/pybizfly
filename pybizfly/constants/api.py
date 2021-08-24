DEFAULT_HOST_URI = "https://manage.bizflycloud.vn"

CATALOG_ENDPOINT = '/api/auth/service'
TOKEN_ENDPOINT = '/api/token'

RESOURCE_ENDPOINTS = {
    'OS_IMAGE': 'os-images',
    'FLAVOR': 'flavors',
    'CLOUD_SERVER': 'servers',
    'VOLUME': 'volumes',
    'SNAPSHOT': 'snapshots',
    'KEYPAIR': 'keypairs',
    'BACKUP_CALENDAR': 'backup',
    'FIREWALL': 'firewalls',
    'DNS': '',
}

RESOURCE_SERVICES = {
    'BUSINESS_EMAIL': 'Business Email',
    'CLOUD_SERVER': 'Cloud Server',
    'LOAD_BALANCER': 'Load Balancer',
    'VPN_SITE_TO_SITE': 'VPN Site to Site',
    'DNS': 'DNS',
    'AUTO_SCALING': 'Auto Scaling',
    'CONTAINER_REGISTRY': 'Container Registry',
    'SIMPLE_STORAGE': 'Simple Storage',
    'K8S': 'Kubernetes Engine',
    'ALERT': 'Alert',
    'AUTH': 'Auth',
}
