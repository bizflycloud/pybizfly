<h1 align="center">PyBizfly</h1>
<p align="center">Hỗ trợ truy cập BizFly Cloud Cloud Server API để tạo cloud server, cấu hình tường lửa và nhiều hơn nữa.</p>

## Cài đặt
Cài đặt sử dụng thông qua**pip**

    pip install pybizfly
hoặc thông quan mã nguồn
    
    python setup.py install 
## Yêu cầu

## Cấu hình
```python  
import pybizfly
client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
```
<h2 id="tính-năng">Tính năng</h2>
PyBizfly hỗ trợ tất cả các tính năng được cung cấp bởi [BizFly Cloud Cloud Server API](https://support.bizflycloud.vn/api/cloudserver/)

- [Truy vấn thông tin và quản lý hoạt động cloud server](#cloud-server)
- [Thiết lập đặt lịch sao lưu cloud server](#backup)
- [Thiết lập, chỉnh sửa, truy vấn thông tin và xóa tường lửa cho cloud server](#firewall)
- [Truy vấn thông tin image tạo cloud server](#image)
- [Truy vấn thông tin flavor](#flavor)
- [Đặt SSH key cho tài khoản](#ssh-key)
- [Tạo snapshot cho cloud server](#snapshot)
- [Thiết lập và quản lý hoạt động các volume của cloud server](#volume)

## Sử dụng
<h3 id="cloud-server">Cloud server</h3>
PyBizfly hỗ trợ truy vấn thông tin và quản lý hoạt động các cloud server của tài khoản.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách liệt kê các server của một tài khoản.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
servers = client.cloud_server().list()

print(servers)
```
Ví dụ này biểu diễn cách lấy thông tin chi tiết của một server của tài khoản
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
servers = client.cloud_server().get('07e17db4-6794-4af1-b33g-6fb78c2bf165')

print(servers)
```
Ví dụ này biểu diễn cách tạo một cloud server. Cloud server có thể được tạo từ image, snapshot và volume.
```python   
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().create(name='cloud-server', os_type='image',
                                  os_id='07e17db4-6794-4af1-b33g-6fb78c2bf165', flavor_name='2c_2g',
                                  ssh_key_name='ssh-key-name', server_type='premium',
                                  root_disk_size=40, root_disk_type='SSD',
                                  addition_data_disks=[
                                  {'type': 'HDD', 'size': 40},
                                  {'type': 'HDD', 'size': 30}
                                  ],
                                  password=True, availability_zone='HN1')
print(server)
``` 
Ví dụ này biểu diễn cách xóa một cloud server.
```python   
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().delete('65as88as5d6as8dd2asd')

print(server)
```
Ví dụ này biểu diễn cách rebuild một server từ một image.
```python  
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
servers = client.cloud_server().rebuild(server_id='12as25asc74asd6asd', image_id='65as88as5d6as8dd2asd')

print(servers)
```
Ví dụ này biểu diễn cách resize cloud server theo một flavor.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().resize(server_id='12as25asc74asd6asd', flavor_name='2c_2g')

print(server)
```
    
Ví dụ này biểu diễn cách lấy vnc của một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().get_vnc(server_id='12as25asc74asd6asd', vnc_type='2c_2g')

print(server)
```  
Ví dụ này biểu diễn cách thêm tường lửa cho một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().add_firewall(server_id='12as25asc74asd6asd', firewall_id='65as88as5d6as8dd2asd')

print(server)
``` 
Ví dụ này biểu diễn cách thay kiểu (basic, premium, enterprise) cho một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().change_type(server_id='12as25asc74asd6asd', new_type='premium')

print(server)
```
Ví dụ này biểu diễn cách đổi mật khẩu cho một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().reset_password(server_id='12as25asc74asd6asd')

print(server)
```
Ví dụ này biểu diễn cách reboot cứng cho một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().hard_reboot(server_id='12as25asc74asd6asd')

print(server)
```   
Ví dụ này biểu diễn cách reboot mềm cho một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().soft_reboot(server_id='12as25asc74asd6asd')
    
print(server)
```
Ví dụ này biểu diễn cách bật một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().start(server_id='12as25asc74asd6asd')

print(server)
```
Ví dụ này biểu diễn cách tăt một cloud server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
server = client.cloud_server().stop(server_id='12as25asc74asd6asd')

print(server)
```
<h3 id="backup">Backup</h3>
PyBizfly hỗ trợ truy vấn danh sách, tạo, xóa và chỉnh sửa lịch sao lưu cloud server.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách in thông tin một bản sao lưu.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
backup = client.backup().get(backup_id='65as88as5d6as8dd2asd')

print(backup)
```   
Ví dụ này biểu diễn cách lên lịch tạo 3 bản sao lưu vào lúc 16h hàng ngày theo chu kỳ 1440 giây.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
backup = client.backup().create(resource_id='65as88as5d6as8dd2asd', backup_at_time=16,
                                backup_frequency=1440, backup_quantity=3)

print(backup)
```
Ví dụ này biểu diễn cách xóa một bản sao lưu.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
backup = client.backup().delete(backup_id='65as88as5d6as8dd2asd')

print(backup)
```
Ví dụ này biểu diễn cách sửa một lịch sao lưu.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
backup = client.backup().put(backup_id='65as88as5d6as8dd2asd', backup_at_time=16,
                                backup_frequency=1440, backup_quantity=3)

print(backup)
```

<h3 id="firewall">Firewall</h3>
PyBizfly hỗ trợ cấu hình tường lửa và cài đặt tường lửa cho cloud server.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách in thông tin một tường lửa.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
firewall = client.firewall().get(firewall_id='65as88as5d6as8dd2asd')

print(firewall)
```
Ví dụ này biểu diễn cách cấu hình thông tin một tường lửa và cài trên hai server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
firewall = client.firewall().create(name='firewall', inbound_rules=[
    {'type': 'SSH', 'protocol': 'TCP', "port_range": '22', 'cidr': '0.0.0.0/0'},
    {'type': 'HTTP', 'protocol': 'TCP', "port_range": '80', 'cidr': '192.168.17.5'},
    {'type': 'SSH', 'protocol': 'TCP', "port_range": '22', 'cidr': '2001:0db8:85a3:0000:0000:8a2e:0370:7334/128'}
    ], 
        outbound_rules=[
    {'type': 'PING', 'protocol': 'ICMP', 'cidr': '::/0'},
    {'type': 'CUSTOM', 'protocol': 'TCP', "port_range": '1-255', 'cidr': '192.168.0.0/28'},
    ], 
        on_servers=[
        '26b5cb61-95bb-417e-a1a3-2ea51f40d6ee',
        '5326pi96-16ab-4c7e-e12a-2da53f51d6ae'
    ])

print(firewall)
``` 
Ví dụ này biểu diễn cách cập nhật thông tin cấu hình thông tin một tường lửa
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
firewall = client.firewall().update(firewall_id='65as88as5d6as8dd2asd', inbound_rules=[
    {'type': 'SSH', 'protocol': 'TCP', "port_range": '22', 'cidr': '0.0.0.0/0'},
    {'type': 'HTTP', 'protocol': 'TCP', "port_range": '80', 'cidr': '192.168.17.5'},
    {'type': 'SSH', 'protocol': 'TCP', "port_range": '22', 'cidr': '2001:0db8:85a3:0000:0000:8a2e:0370:7334/128'}
    ], 
        outbound_rules=[
    {'type': 'PING', 'protocol': 'ICMP', 'cidr': '::/0'},
    {'type': 'CUSTOM', 'protocol': 'TCP', "port_range": '1-255', 'cidr': '192.168.0.0/28'},
    ], 
        on_servers=[
        '26b5cb61-95bb-417e-a1a3-2ea51f40d6ee',
        '5326pi96-16ab-4c7e-e12a-2da53f51d6ae'
    ])

print(firewall)
```  
Ví dụ này biểu diễn cách xóa tường lửa trên nhiều server
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
firewall = client.firewall().delete_across_servers(firewall_id='65as88as5d6as8dd2asd',
    servers=[
        '26b5cb61-95bb-417e-a1a3-2ea51f40d6ee',
        '5326pi96-16ab-4c7e-e12a-2da53f51d6ae'
    ])

print(firewall)
```  
<h3 id="image">Image</h3>
PyBizfly hỗ trợ truy vấn danh sách các image dùng để tạo server.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách lấy danh sách các image dùng để tạo server.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
images = client.image().list()

print(images)
```  
<h3 id="flavor">Flavor</h3>
PyBizfly hỗ trợ truy vấn danh sách các flavor

Ví dụ này biểu diễn cách lấy danh sách các flavor.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
flavors = client.flavor().list()

print(flavors)
``` 
<h3 id="ssh-key">SSH key</h3>
PyBizfly hỗ trợ đặt SSH key để cấu hình server

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách lấy danh sách các SSH key.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
keys = client.key_pair().list()

print(keys)
```
Ví dụ này biểu diễn cách lấy thêm một SSH key mới.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
keys = client.key_pair().create(name='sshkey', key_value='<key-value>')

print(keys)
```
Ví dụ này biểu diễn cách lấy xóa một SSH key theo tên.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
keys = client.key_pair().delete(name='sshkey')

print(keys)
``` 
<h3 id="snapshot">Snapshot</h3>
PyBizfly hỗ trợ tạo snapshot cho server.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách lấy danh sách các snapshot có thể dùng để tạo server (bootable=ue). 
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
snapshots = client.snapshot().list(bootable=True)

print(snapshots)
```
Ví dụ này biểu diễn cách tạo một snapshot.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
snapshot = client.snapshot().create(resource_name='', volume_id='', force=False)

print(snapshot)
```
Ví dụ này biểu diễn cách xóa một snapshot.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
snapshot = client.snapshot().delete(snapshot_id='65as88as5d6as8dd2asd')

print(snapshot)
```   
<h3 id="volume">Volume</h3>
PyBizfly truy vấn và quản lý các volume.

[⬆  Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách lấy các một volume có thể dùng để tạo server (bootable=True).
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volumes = client.volume().list(bootable=True)

print(volumes)
```
Ví dụ này biểu diễn cách tạo một volume mới.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().create(name='volume', volume_size=20, volume_type='SSD', availability_zone='HN1')

print(volume)
```
Ví dụ này biểu diễn cách xóa một volume.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().delete(volume_id='65as88as5d6as8dd2asd')

print(volume)
```
Ví dụ này biểu diễn lấy lại một volume từ một snapshot.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().restore_volume(volume_id='65as88as5d6as8dd2asd', snapshot_id='34as58as2egwe7fg3sda')

print(volume)
```
    
Ví dụ này biểu diễn tách một volume.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().detach(volume_id='65as88as5d6as8dd2asd')

print(volume)
```
    
Ví dụ này biểu diễn nối một volume với một instance.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().attach(volume_id='65as88as5d6as8dd2asd', instance_uuid='<instance>')

print(volume)
```
    
Ví dụ này biểu diễn mở rộng một volume theo block 10.
```python
import pybizfly

client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
volume = client.volume().extend(volume_id='65as88as5d6as8dd2asd', new_size=20)

print(volume)
```
