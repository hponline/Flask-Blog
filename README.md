# Proje Adı - Python Flask Web-Blog

Projenin Amacı: Kullanıcıların makale oluşturmasına, okumasına, güncellemesine ve silmesine olanak tanıyan bir web uygulamasıdır. 
Ayrıca kullanıcı kayıt, giriş, kimlik doğrulama de içerir. Web sitesi yanıt verir ve tüm cihazlarda iyi görünür.

<h4>Teknik Detaylar:</h4>

Frontend:
HTML5
CSS3
JavaScript
Bootstrap

BackEnd:
Flask
MySQL

Diğer:
CKEditor

<h3> Öne Çıkan Özellikler </h3>

1 -  Kullanıcı Giriş Decorator'ı
  
'login_required' fonksiyonu ile giriş yapmış kullanıcıların belirli sayfalara erişim kontrolü sağlar.

2 -  Kullanıcı Profil Sayfası:

'profil' fonksiyonu, kullanıcıların isimleri ve yazdıkları makale sayıları ile birlikte profil sayfasını oluşturur ve anasayfa da gösterilmesini sağlar.

3 - Makale Güncelleme Sayfası:

'update' fonksiyonu, bir makalenin güncellenebilmesi için formun doldurulabileceği bir sayfa sağlar.

4 - Flash Mesajları:

'flash' fonksiyonu, kullanıcıya çeşitli durumlar hakkında bilgi veren mesajlar göstermek için kullanıldı.

5 - Veritabanı İlişkileri:

Kullanıcılar ('users') ve makaleler ('articles') arasındaki ilişki sağlandı. Her makale, bir kullanıcıya ait olacak şekilde tasarlandı.

6 - Anasayfa Gönderileri:

'index' fonksiyonu, veritabanından çekilen makaleleri anasayfada gösterir. Her makale başlığına tıklandığında detay sayfasına yönlendirme yapıldı.


## Teknolojiler ve Kütüphaneler


- **Flask:** Web uygulaması çatısı olarak kullanıldı.
- **Flask-MySQLdb:** MySQL veritabanıyla etkileşim sağlamak için kullanıldı.
- **WTForms:** Form işlemleri için kullanıldı.
- **Passlib:** Parola güvenliği sağlamak için kullanıldı.

...

## Udemy Flask Dersi

Bu proje, Mustafa Murat Coşkun'un Udemy üzerindeki (Python | Sıfırdan İleri Seviye Programlama) Flask derslerine dayanmaktadır. Yaptığım ilk projeyi sizlerle paylaşmak istedim.


