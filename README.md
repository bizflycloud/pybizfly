<h1 align="center">PyBizfly</h1>
<p align="center">Hỗ trợ sử dụng BizFly Cloud Cloud Server API.</p>

## Cài đặt
Cài đặt sử dụng **pip**

    pip install pybizfly
## Yêu cầu
## Cấu hình
## Tính năng
pybizfly hỗ trợ tất cả các tính năng được cung cấp bởi [BizFly Cloud Cloud Server API](https://support.bizflycloud.vn/api/cloudserver/#introduction) cung cấp, bao gồm:
* Liệt kê toàn bộ image có thể tạo thành server.
* ...
## Sử dụng
###Cloud server

Ví dụ này biểu diễn cách liệt kê các server của một tài khoản.

    import pybizfly

    client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
    servers = client.cloud_server().list()
    
    print(servers)

Ví dụ này biểu diễn cách rebuild một server từ một image.
    
    import pybizfly

    client = pybizfly.BizFlyClient(email='dungpq@vccloud.vn', password='123456')
    servers = client.cloud_server().rebuild(server_id='12as25asc74asd6asd', image_id='65as88as5d6as8dd2asd')
    
    print(servers)
