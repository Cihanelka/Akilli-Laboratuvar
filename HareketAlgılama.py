import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Pin Tanımlamaları
LDR_PIN = 17  # Işık sensörü pin numarası
PIR_PIN = 27  # Hareket sensörü pin numarası
LED_PIN = 18  # LED pin numarası

# DHT11 (Sıcaklık ve Nem) Sensörü
sensor = Adafruit_DHT.DHT11  # DHT11 sensörü kullanılıyor
DHT_PIN = 4  # DHT11'in bağlı olduğu GPIO pini

# GPIO Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)  # LDR sensörü pini
GPIO.setup(PIR_PIN, GPIO.IN)  # PIR sensörü pini
GPIO.setup(LED_PIN, GPIO.OUT)  # LED pini


# Sıcaklık ve Nem Okuma Fonksiyonu
def get_temperature_and_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    return temperature, humidity


# Işık Kontrol Fonksiyonu
def control_lights():
    if GPIO.input(LDR_PIN) == GPIO.LOW:  # Işık seviyeleri düşükse
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED'i aç
        print("Işık seviyesi düşük, LED açıldı.")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # LED'i kapat
        print("Işık seviyesi yüksek, LED kapatıldı.")


# Sıcaklık ve Nem Kontrol Fonksiyonu
def control_temperature():
    temperature, humidity = get_temperature_and_humidity()
    if temperature is not None and humidity is not None:
        print(f"Sıcaklık: {temperature:.1f} °C, Nem: {humidity:.1f} %")
        if temperature < 20:  # Sıcaklık 20°C'nin Altına Düştü
            print("Sıcaklık düşük, ısıtıcıyı açabilirsiniz.")
        else:
            print("Sıcaklık normal.")
    else:
        print("Sıcaklık ve nem verisi alınamadı.")


# Hareket Algılama Fonksiyonu
def motion_detection():
    if GPIO.input(PIR_PIN):
        print("Hareket Algılandı!")
        GPIO.output(LED_PIN, GPIO.HIGH)  # Hareket Varsa LED'i Aç
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # Hareket Yoksa LED'i Kapat
        print("Hareket Yok")


# Ana Döngü
try:
    while True:
        # Işık Kontrolü
        control_lights()

        # Sıcaklık ve Nem Kontrolü
        control_temperature()

        # Hareket Algılama
        motion_detection()

        time.sleep(3)  # 1 saniye bekle

except KeyboardInterrupt:
    print("Program Durduruluyor...")
    GPIO.cleanup()  # GPIO Pinlerini Temizle