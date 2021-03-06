# CLOUD SERVER CONSTANTS
REBUILD = "rebuild"
RESIZE = "resize"
GET_VNC = "get_vnc"
ADD_FIREWALL = "add_firewall"
CHANGE_TYPE = "change_type"
RESET_PASSWORD = "reset_password"
HARD_REBOOT = "hard_reboot"
SOFT_REBOOT = "soft_reboot"
START = "start"
STOP = "stop"
CLOUD_SERVER_ACTIONS = [REBUILD, RESIZE, GET_VNC, ADD_FIREWALL, CHANGE_TYPE,
                        RESET_PASSWORD, HARD_REBOOT, SOFT_REBOOT, STOP, START]

# os types
OS_IMAGE_TYPE = 'image'
OS_SNAPSHOT_TYPE = 'snapshot'
OS_VOLUME_TYPE = 'volume'
CLOUD_SERVER_OS_TYPES = [OS_IMAGE_TYPE, OS_SNAPSHOT_TYPE, OS_VOLUME_TYPE]

# disk types
HDD = 'HDD'
SSD = 'SSD'
CLOUD_SERVER_DISK_TYPES = [SSD, HDD]

# server types
PREMIUM = 'premium'
ENTERPRISE = 'enterprise'
BASIC = 'basic'
CLOUD_SERVER_SERVER_TYPES = [PREMIUM, ENTERPRISE, BASIC]

# availability zone
HN1 = 'HN1'
HN2 = 'HN2'
AVAILABILITY_ZONES = [HN1, HN2]

# flavor
DEFAULT_FLAVOR = '2c_2g'

# VOLUME_CONSTANTS
RESTORE_VOLUME = 'restore_volume'
DETACH = 'detach'
ATTACH = 'attach'
EXTEND = 'extend'
VOLUME_ACTIONS = [RESTORE_VOLUME, DETACH, ATTACH, EXTEND]
