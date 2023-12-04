from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime

# Kullanıcı Giriş Decoratorı
# Bu fonksiyon, giriş yapmış bir kullanıcı olup olmadığını kontrol eder
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:  
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için Giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Giriniz.")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message = "Lüfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message = "Parolanız Uyuşmuyor.")
        ])
    confirm = PasswordField("Parola Doğrula")

# Kullanıcı Giriş Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı ")
    password = PasswordField("Parola")

# Flask ile MySQL Konfigurasyonu 
app = Flask(__name__)
app.secret_key = "ABlock"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ABlock"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Anasayfa
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM articles"
    result = cursor.execute(sorgu)
    
    if result > 0:
        articles = cursor.fetchall()  
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%S")     
        return render_template("index.html", articles=articles, current_datetime=current_datetime)
    else:
        return render_template("index.html")

# Hakkımızda Bölümü
@app.route("/about")
def about():
    return render_template("about.html")

# Makale Sayfası
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles"
    result = cursor.execute(sorgu)

    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else:
        return render_template("articles.html")
    
    
# Kontrol Paneli
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles "
    result = cursor.execute(sorgu,)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)
    else:
        return render_template("dashboard.html")
    
# Kayıt İşlemi
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

# Post Bölümü (GÖNDERMEK)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt (form.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "Insert into users (name,email,username,password) VALUES (%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
# Flash mesaj bastırma  'mesaj' + 'kategori'
        flash("Başarıyla Kayıt oldunuz...", "success")
        return redirect(url_for("login"))
    
# GET Bölümü (ALMAK)
    else:
        return render_template ("register.html", form = form)

# Login İşlemi

@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Select * From users WHERE username = %s"

        result = cursor.execute(sorgu,(username,))
        
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Giriş Başarılı...","success")

                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Parola yanlış.","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...","danger")
            return redirect(url_for("login"))
            

    return render_template("login.html",form = form)

# Detay Sayfası
@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles WHERE id = %s"
    result = cursor.execute(sorgu,(id,))

    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")

# Logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# Makale Ekleme
@app.route("/addarticle", methods = ["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert into articles (title,author,content) VALUES (%s,%s,%s)"
        cursor.execute(sorgu,(title,session["username"],content))

        mysql.connection.commit()
        cursor.close()

        flash("Makale Başarıyla Eklendi","success")

        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)

# Makale Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu ="Select * From articles WHERE id = %s"
    result = cursor.execute(sorgu,(id,))

    if result > 0 :
        sorgu2 = "Delete From articles WHERE id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        
        return redirect(url_for("dashboard"))
    else:
        flash("Böyle bir makale yok veya bu işlem için yetkiniz yok.","danger")
        return redirect(url_for("index"))

# Makale Güncelle
@app.route("/edit/<string:id>", methods = ["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * From articles WHERE id = %s "
        result = cursor.execute(sorgu,(id,))

        if result == 0:
            flash("Böyle bir makale yok veya yetkiniz yok","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()

            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form = form )
    else:
        # POST request
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        
        sorgu2= "UPDATE articles SET title = %s, content = %s WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newTitle,newContent,id))
        mysql.connection.commit()

        flash("Makale Güncellendi","success")

        return redirect(url_for("dashboard"))


# Makale Form

class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators=[validators.Length(min = 5, max = 100)])
    content = TextAreaField("Makale içeriği",validators=[validators.Length(min = 10)])

# Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()
        sorgu = "Select * From articles WHERE title like '%" +keyword +"%' "

        result = cursor.execute(sorgu)
        if result == 0:
            flash("Makale yok...","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)


# Profil Sekmesi
@app.route("/profil")
@login_required
def profil():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT users.name, COUNT(articles.id) AS article_count FROM users LEFT JOIN articles ON users.username = articles.author GROUP BY users.username"
    cursor.execute(sorgu)
    kullanicilar = cursor.fetchall()

    return render_template("profil.html", kullanicilar=kullanicilar)



# if __name__ == "__main__": yapısı, bir modülün veya dosyanın doğrudan çalıştırılıp çalıştırılmadığını kontrol etmek için kullanılır. 
# Bu yapının içinde yer alan kodlar, yalnızca modül veya dosya doğrudan çalıştırıldığında çalışır.
if __name__ == "__main__":
    app.run(debug=True)