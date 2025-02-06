# Basit Yüz Tanıma

Bu proje, OpenCV ve `face_recognition` kütüphanesini kullanarak basit bir yüz tanıma sistemi gösterir. Sistem, bir video akışından tanınan yüzleri algılar ve ekranda tanınan kişilerin adlarını görüntüler.

## Gereksinimler

Başlamadan önce, aşağıdaki Python kütüphanelerinin yüklü olduğundan emin olun:

- `opencv-python` (video yakalama ve görsel işleme için)
- `face_recognition` (yüz tespiti ve tanıma için)
- `numpy` (dizi işleme için)
- `glob` (dosya yolları ile çalışmak için)
- `pickle` (yüz verilerini kaydetmek ve yüklemek için)

Gerekli kütüphaneleri pip ile yükleyebilirsiniz:

```bash
pip install opencv-python face_recognition numpy
