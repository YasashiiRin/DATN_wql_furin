![icon_logo](https://dim.mcusercontent.com/cs/83e448ffef2b662c110cebf77/images/4040f7dc-d924-76d6-700c-5cb1664c61bd.jpg?w=564&dpr=2)

# FURIN: ĐỒ ÁN TỐT NGHIỆP WEBSITE QUẢN  LÝ ĐẶT XE DU LỊCH.

Website quản lý đặt xe du lịch là một website được thiết kế để tối ưu hóa
quy trình đặt xe của những người  muốn di chuyến qua những địa điểm , và nhắm 
tới việc tối ưu khả năng quản lý của chủ nhà xe , đối với các phương tiện của mình
cũng như tài xế và các lịch trình của họ

Ứng dụng được xây dựng và phát triển trên trung Django
#### Project Video: [Watch on Youtube](https://www.youtube.com)

### Cấu trúc thư mục dự án

- Django-Furin:
- ├── CarownerApp
- ├── DriverApp
- ├── HomeApp
- ├── LoginApp
- ├── media
- └── webApp

### Cấu trúc ứng dụng
Trong dự án website quản lý đặt xe du lịch này đã sắp xếp chức năng thành các ứng dụng riêng biệt để duy trì mô-đun cơ sở mã và có thể duy trì được nhưng vì còn chưa thể xác định cấu trúc từ đầu nên tên mỗi ứng dụng không hoàn toàn đại diện cho toàn bộ chức năng bên trong 🥲

##### LoginApp ( ứng dụng đăng ký đăng nhập)
##### HomeApp  ( ứng dụng trang chủ và đối tượng người đặt xe)
##### DriverApp  ( ứng dụng tài xế)
##### CarownerApp  ( ứng dụng chủ nhà xe)
### Bắt đầu:
Để thiết lập dự án bắt đầu bằng các bước sau:
Sao chép kho lưu trữ.
- 1. Tạo một môi trường ảo và kích hoạt nó.
- 2. Cài đặt các phần phụ thuộc của dự án bằng cách sử dụng pip install -r requirements.txt.
- 3. Tạo một tài khoản siêu người dùng bằng cách sử dụng python manage.py createsuperuser , và từ tài khoản này bạn tạo ra các tài khoản Nhà xe , còn với các tài khoản còn lại bạn có thể đăng ký như bình thường hoặc thêm từ admin
- 4. Khởi động máy chủ phát triển với python manage.py runserver.

Chúc bạn viết mã vui vẻ và xây dựng được website của mình
### Đặc trưng
- Giao diện chú trọng vào cảm nhận tương tác của người dùng , nên sẻ sử dụng rất dễ dàng và thuận tiện 
- Giao diện quản lý chi tiết giúp các người quản lý nắm bắt đầy đủ các thông tin cần thiết một cách nhanh nhất 
- Có thể mở rộng và tùy chỉnh: Được thiết kế chú trọng đến khả năng mở rộng, kiến ​​trúc mô-đun của hệ thống cho phép mở rộng và tùy chỉnh dễ dàng.

### Cài đặt đối với thư mục chưa có kho lưu trữ
- Sao chép kho lưu trữ
 git init
 git remote add dev https://gitlab.minds.vn/yasashiirin/datn_wql_furin.git
 git branch -M main
 git pull dev main
- Tạo môi trường ảo:
-py -m venv <tên môi trường ảo>
- Kích hoạt môi trường ảo
<tên môi trường ảo>/Scripts/activate
- run 
Vào thư mục gốc ( thư mục có tệp manage.py ) chạy lệnh py manage.py runserver
### Cách sử dụng
- Nhận tài khoản từ admin với tư các là chủ nhà xe
 Đăng nhập 
Các chủ nhà xe có thể quản lý các đối tượng liên quan như , tài xế , lịch trình , đơn đặt , và phương tiện của họ
- Đăng ký tài khoản với tư cách là người đặt xe
 Đăng ký và thực hiện xác thực email , người đặt xe có thể xem mọi thông tin của các chuyển đi
Tìm kiếm các chuyến đi , theo địa điểm đi, điểm đến ,thời gian đi , ngày đi ...thông tin tìm kiếm càng nhiều thì kết quả tìm kiếm sẻ được rút gọn
Người đặt xe có thể dễ dàng đặt một chuyến đi cho mình , và từ lịch sử đặt xe có thể xem lại cụ thể thời gian cũng như số chỗ đã đặt
Nếu vì lý do nào đó bạn có thể hủy đơn đặt của mình trước giờ xe xuất phát là 3 tiếng
Người đặt xe , cũng có thông tin hồ sơ của mình , bạn có thể đổi mọi thứ trừ email , số điện thoại nếu bạn muốn đổi thì phải thực hiện xác thực bằng mã OTP để đảm bảo số đó là số của chính bạn
- Nhận tài khoản với tư cách là tài xế 
Tài xế sẻ nhận tài khoản của mình từ chủ nhà xe, tài khoản này chủ nhà xe có thể xác thực cho họ , hoặc họ phải tự mình xác thực để đảm bảo email của họ còn hoạt động
Tài xế có thể xem các thông tin về các chuyến đi của họ , cũng như thông tin các đơn đặt tới họ , và thông tin liên hệ tới người đã đặt những đơn ấy
Tìm kiếm , tài xế dễ dàng tìm kiếm thông tin các người đặt tới họ bằng form tìm kiếm

##### ----------------------------------Chúc bạn một ngày tốt lành---------------------------------------
