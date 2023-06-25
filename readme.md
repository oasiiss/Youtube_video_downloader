## Youtube video indirme sitesi

**demo :** https://www.osmanefekurt.site


**Kurulum;**

```
git clone https://github.com/oasiiss/Youtube_video_downloader.git
```
*Yukarıdaki komut ile projeyi indiriyoruz*

```
nano .env
```
*.env dosyasını oluşturup içine* ```SECRET_KEY = (Django projenizin secret key'i)``` *yazıyoruz*

```
pipenv install
```
*Sanal ortamımızı kuruyoruz*

```
pipenv shell
```
*Sanal ortamımızı aktif ediyoruz*

```
python manage.py migrate
```
*Veri tabanını migrate ediyoruz*

```
python manage.py collectstatic
```
*Static dosyalarını main_static dizininde topluyoruz*


*Video indirme işlemi sıkıntısız çalışabilmesi için sistemimize ffmpeg kütüphanesini kurmamız gerekiyor*

**Windows için**
```
choco install ffmpeg
```

**Mac için**
```
brew install ffmpeg
```

**Linux için**
```
sudo apt-get install ffmpeg
```

