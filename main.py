import requests
import sys

# Foydali funksiyalar (Helpers o‘rniga oddiy funksiya)
def get_machine_code():
    # Test uchun random kod — bu yerga haqiqiy kodni yozing
    import uuid
    return str(uuid.uuid4())  # Test uchun random UUID

# Rangli chop etish uchun funksiya
def color(text, color_name):
    colors = {
        "white": "\033[97m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color_name, '')}{text}{colors['reset']}"

# Aktivatsiya tekshiruvi
def check_activation():
    url = "https://raw.githubusercontent.com/astralkbr/env/refs/heads/main/universal.csv"
    try:
        response = requests.get(url)
        hash_values_list = [line.strip() for line in response.text.splitlines()]
    except Exception as e:
        print(f"❌ Aktivatsiya tekshiruvida xatolik: {e}")
        sys.exit()

    machine_code = get_machine_code()
    print(color(f"🔑 Machine Code: {machine_code}", "white"))

    if machine_code not in hash_values_list:
        print(color("🚫 Kod aktivlashtirilmagan! Aktivatsiya uchun: @astralkibr ga murojaat qiling!", "magenta"))
        sys.exit()

    print(color("✅ Aktivatsiya muvaffaqiyatli!", "white"))

# Salomlashish funksiyasi
def greet_user(name):
    """Foydalanuvchini salomlash funksiyasi"""
    print(f"Hello, {name}! Welcome to the Python world.")

# Dastur asosiy qismi
def main():
    check_activation()
    user_name = input("Ismingizni kiriting: ")
    greet_user(user_name)

if __name__ == "__main__":
    main()
