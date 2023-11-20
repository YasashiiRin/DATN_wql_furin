![icon_logo](https://dim.mcusercontent.com/cs/83e448ffef2b662c110cebf77/images/4040f7dc-d924-76d6-700c-5cb1664c61bd.jpg?w=564&dpr=2)

# FURIN: ĐỒ ÁN TỐT NGHIỆP WEBSITE QUẢN  LÝ ĐẶT XE DU LỊCH.

Website quản lý đặt xe du lịch là một website được thiết kế để tối ưu hóa
quy trình đặt xe của những người  muốn di chuyến qua những địa điểm , và nhắm 
tới việc tối ưu khả năng quản lý của chủ nhà xe , đối với các phương tiện của mình
cũng như tài xế và các lịch trình của họ

Ứng dụng được xây dựng và phát triển trên trung Django
#### Project Video: [Watch on Youtube](https://www.youtube.com)

### Cấu trúc thư mục dự án
Django-Furin:.
│   db.sqlite3
│   django_furin_travel
│   manage.py
│   README.md
│   requirements.txt
│   structure.txt
│
├───CarownerApp
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           0001_initial.cpython-39.pyc
│   │           __init__.cpython-39.pyc
│   │
│   ├───static
│   │   ├───CSS
│   │   │       custom_admin.css
│   │   │       Login.css
│   │   │       toast.css
│   │   │
│   │   ├───images
│   │   │       bg1.jpg
│   │   │       bg2.jpg
│   │   │       bg3.jpg
│   │   │       bg4.jpg
│   │   │       bg5.jpg
│   │   │       bg6.jpg
│   │   │       logo5.ico
│   │   │
│   │   └───JS
│   │           custom_admin.js
│   │           style.js
│   │           toast.js
│   │           validator.js
│   │
│   ├───templates
│   │   ├───admin
│   │   │   └───CarownerApp
│   │   │       └───schedules
│   │   │               change_list_results.html.html
│   │   │
│   │   └───CarownerApp
│   └───__pycache__
│           admin.cpython-39.pyc
│           apps.cpython-39.pyc
│           models.cpython-39.pyc
│           __init__.cpython-39.pyc
│
├───DriverApp
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───backends
│   │   │   custom_auth.py
│   │   │
│   │   └───__pycache__
│   │           custom_auth.cpython-39.pyc
│   │
│   ├───middleware
│   │   │   custom_auth_middleware.py
│   │   │
│   │   └───__pycache__
│   │           custom_auth_middleware.cpython-39.pyc
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-39.pyc
│   │
│   ├───static
│   │   ├───CSS
│   │   │       bootstrap.min.css
│   │   │       fontawesome.min.css
│   │   │       styleDriver.css
│   │   │       templatemo_driver.css
│   │   │       toast_driver.css
│   │   │
│   │   ├───images
│   │   │       arrow-down.png
│   │   │       avatar.png
│   │   │       check-mark.png
│   │   │       img1.png
│   │   │       logo5.ico
│   │   │       notification-01.jpg
│   │   │       notification-02.jpg
│   │   │       notification-03.jpg
│   │   │       product-image.jpg
│   │   │
│   │   └───JS
│   │           book.js
│   │           bootstrap.min.js
│   │           Chart.min.js
│   │           jquery-3.3.1.min.js
│   │           moment.min.js
│   │           style.js
│   │           toast_driver_form.js
│   │           tooplate-scripts.js
│   │
│   ├───templates
│   │   └───DriverApp
│   │           driver.html
│   │           driver_login.html
│   │           profile_driver.html
│   │
│   └───__pycache__
│           admin.cpython-39.pyc
│           apps.cpython-39.pyc
│           models.cpython-39.pyc
│           urls.cpython-39.pyc
│           views.cpython-39.pyc
│           __init__.cpython-39.pyc
│
├───HomeApp
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-39.pyc
│   │
│   ├───static
│   │   ├───CSS
│   │   │       bootstrap.min.css
│   │   │       bootstrap_editpf.css
│   │   │       profile.css
│   │   │       style.css
│   │   │       style_home_customer.css
│   │   │       templatemo-style.css
│   │   │       toast_customer_form.css
│   │   │       toast_home.css
│   │   │       toast_profile_customer.css
│   │   │       UI_customer.css
│   │   │
│   │   ├───images
│   │   │       bg10.jpg
│   │   │       bg11.jpg
│   │   │       bg12.jpg
│   │   │       bg13.jpg
│   │   │       bg14.jpg
│   │   │       bg15.jpg
│   │   │       bg16.jpg
│   │   │       bg17.jpg
│   │   │       bg18.jpg
│   │   │       bg19.jpg
│   │   │       bg20.jpg
│   │   │       bg21.jpg
│   │   │       bg22.jpg
│   │   │       bg23.jpg
│   │   │       bg24.jpg
│   │   │       bg25.jpg
│   │   │       bg26.jpg
│   │   │       bg27.jpg
│   │   │       bg7.webp
│   │   │       bg8.ico
│   │   │       bg9.jpg
│   │   │       bgw2_1.jpg
│   │   │       bgw2_2.jpg
│   │   │       ico1.png
│   │   │       icon_delete.png
│   │   │       logo1.ico
│   │   │       logo2.ico
│   │   │       logo3.ico
│   │   │       logo4.ico
│   │   │       logo5.ico
│   │   │       logo_light.ico
│   │   │       logo_light.png
│   │   │       search_policy.png
│   │   │
│   │   └───JS
│   │           book.js
│   │           style.js
│   │           toast_customer_form.js
│   │           toast_profile_customer.js
│   │
│   ├───templates
│   │   └───HomeApp
│   │           edit_profile.html
│   │           home.html
│   │           home_customer.html
│   │           profile_customer.html
│   │
│   └───__pycache__
│           admin.cpython-39.pyc
│           apps.cpython-39.pyc
│           forms.cpython-39.pyc
│           models.cpython-39.pyc
│           urls.cpython-39.pyc
│           views.cpython-39.pyc
│           __init__.cpython-39.pyc
│
├───LoginApp
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───backends
│   │   │   custom_auth.py
│   │   │
│   │   └───__pycache__
│   │           custom_auth.cpython-39.pyc
│   │
│   ├───middleware
│   │   │   custom_auth_middleware.py
│   │   │   custom_logout_middleware.py
│   │   │
│   │   └───__pycache__
│   │           custom_auth_middleware.cpython-39.pyc
│   │           custom_logout_middleware.cpython-39.pyc
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           0001_initial.cpython-39.pyc
│   │           __init__.cpython-39.pyc
│   │
│   ├───static
│   │   ├───CSS
│   │   │       Login.css
│   │   │       toast.css
│   │   │
│   │   ├───images
│   │   │       bg1.jpg
│   │   │       bg2.jpg
│   │   │       bg3.jpg
│   │   │       bg4.jpg
│   │   │       bg5.jpg
│   │   │       bg6.jpg
│   │   │       icon_ss.png
│   │   │       logo5.ico
│   │   │
│   │   └───JS
│   │           style.js
│   │           toast.js
│   │           validator.js
│   │
│   ├───templates
│   │   └───LoginApp
│   │           login.html
│   │           LoginCustomer.html
│   │           notify_loading.html
│   │           verifyEmail.html
│   │           verifyEmail_success.html
│   │
│   └───__pycache__
│           admin.cpython-39.pyc
│           apps.cpython-39.pyc
│           backends.cpython-39.pyc
│           models.cpython-39.pyc
│           urls.cpython-39.pyc
│           views.cpython-39.pyc
│           __init__.cpython-39.pyc
│
├───media
│   │   avatar3.png
│   │   avatar4.png
│   │   avatar5.png
│   │   car2.jpg
│   │   car3.jpg
│   │   car4.jpg
│   │   Ha_Thu.jpg
│   │   Khuonghoa.jpg
│   │   Lantern_Alley_Anime_Style_Art.jpg
│   │   Lantern_Alley_Anime_Style_Art_dCamoi1.jpg
│   │   megumi.jpg
│   │   megumi_01CwyF2.jpg
│   │   megumi_5iBLMTc.jpg
│   │   megumi_HzfizIk.jpg
│   │   megumi_miGTLpZ.jpg
│   │   megumi_OY93rU3.jpg
│   │   megumi_TiXMaBw.jpg
│   │   tải_xuống_2.jpg
│   │   tải_xuống_2_0OQTV2w.jpg
│   │   x_x_x.jpg
│   │
│   └───vehicle_img
│           346301782_203904395824400_7498300072183089189_n.jpg
│           346301782_203904395824400_7498300072183089189_n_qHKWite.jpg
│           352810567_835179214878560_1203354482723881292_n.jpg
│           364647082_156755347439198_8501760530931465881_n.jpg
│           91816047_p0_master1200.jpg
│           98178458_p0_master1200.jpg
│           99895354_p0_master1200.jpg
│           Arknights_Worldwide_on_Twitter.png
│           avt_bg1.png
│           buri_on_Twitter.jpg
│           Inuyasha__Sesshoumaru_Welcome_to_Heian.jpg
│           Screenshot_2022-09-29_154542.jpg
│           thumb-1920-817218.jpg
│
└───webApp
    │   asgi.py
    │   settings.py
    │   urls.py
    │   views.py
    │   wsgi.py
    │   __init__.py
    │
    ├───static
    │   └───JS
    └───__pycache__
            settings.cpython-39.pyc
            urls.cpython-39.pyc
            views.cpython-39.pyc
            wsgi.cpython-39.pyc
            __init__.cpython-39.pyc

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
