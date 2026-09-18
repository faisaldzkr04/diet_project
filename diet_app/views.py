from django.shortcuts import render, redirect, get_object_or_404
from .models import Food
from .forms import FoodForm
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.conf import settings

def main_page(request):
    return render(request, "main.html")

# Halaman Login Admin
def login_page(request):
    if request.session.get('admin_logged_in'):
        return redirect('admin_page')  # Jika sudah login, langsung ke halaman admin

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Cek username dan password (gantilah dengan database jika diperlukan)
        if username == "admin" and password == "admin123":
            request.session["admin_logged_in"] = True  # Simpan status login di session
            return redirect("admin_page")  # Pindah ke halaman admin setelah login
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, "admin/dietadmin_login.html")

# Halaman Logout Admin
def logout_page(request):
    request.session.flush()  # Hapus semua session
    return redirect("login_page")  # Pindah ke halaman login setelah logout

# Halaman Admin dengan Proteksi Login
def admin_page(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login_page')  # Jika belum login, arahkan ke halaman login

    from .models import Food  # Import model Food jika diperlukan
    foods = Food.objects.all()
    return render(request, "admin/admin_page.html", {"foods": foods})

def generate_multiple_tfn(name, tfn_list, save_path):
    plt.figure(figsize=(6, 4))
    
    for i, (low, mid, up) in enumerate(tfn_list):
        x = [low, mid, up]
        y = [0, 1, 0]
        plt.plot(x, y, marker='o', label=f'{name} {i+1}')

    plt.title(f"TFN - {name}")
    plt.xlabel("Nilai")
    plt.ylabel("Keanggotaan")
    plt.ylim(-0.1, 1.2)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Fungsi AHP (bobot kriteria: fiber, protein, carbs)
def calculate_ahp_weights():
    ahp_matrix = [
        [1.000, 2.377, 2.446],
        [0.421, 1.000, 2.820],
        [0.409, 0.355, 1.000]
    ]
    total = [sum(col) for col in zip(*ahp_matrix)]
    normalized = [[val / total[i] for i, val in enumerate(row)] for row in ahp_matrix]
    weights = [sum(row) / len(row) for row in normalized]

    return {
        "ahp_matrix": ahp_matrix,
        "normalized_matrix": normalized,
        "ahp_weights": weights,
    }

# Fungsi Fuzzy
def calculate_fuzzy_defuzz(food, jenis):
    value = food[jenis]

    if jenis == "carbs":
        l = (0, 14.83, 29.65)
        m = (14.83, 29.65, 44.48)
        u = (29.65, 44.48, 59.3)
        b = 29.65
    elif jenis == "protein":
        l = (0, 11.73, 23.45)
        m = (11.73, 23.45, 35.18)
        u = (23.45, 35.18, 46.9)
        b = 23.45
    elif jenis == "fiber":
        l = (0, 2.3, 4.6)
        m = (2.3, 4.6, 6.9)
        u = (4.6, 6.9, 9.2)
        b = 4.6

    # Derajat L
    der_l = 1 if value <= l[1] else (l[2] - value) / (l[2] - l[1]) if value <= l[2] else 0
    # Derajat M
    if value <= m[0]:
        der_m = 0
    elif value <= m[1]:
        der_m = (value - m[0]) / (m[1] - m[0])
    elif value <= m[2]:
        der_m = (m[2] - value) / (m[2] - m[1])
    else:
        der_m = 0
    # Derajat U
    if value <= u[0]:
        der_u = 0
    elif value <= u[1]:
        der_u = (value - u[0]) / (u[1] - u[0])
    elif value <= u[2]:
        der_u = 1
    else:
        der_u = 1

    total_derajat = der_l + der_m + der_u
    if total_derajat == 0:
        defuzz = 0
    else:
        defuzz = ((der_l * l[1]) + (der_m * m[1]) + (der_u * u[1])) / total_derajat

    return round(defuzz, 4)

# Fungsi utama
def user_page(request):
    foods = []
    fuzzy_foods = []

    ahp_data = calculate_ahp_weights()
    ahp_weights = ahp_data["ahp_weights"]

    akg = carbs_need = protein_need = fat_need = fiber_need = sodium_need = None
    bmi = ideal_weight = None
    bmi_category = weight_suggestion = ""

    # Menggunakan .first() agar aman jika makanan tertentu belum/tidak ada di database
    gado = Food.objects.filter(name__iexact="Gado-Gado").first()
    gudeg = Food.objects.filter(name__iexact="Gudeg").first()
    nasi = Food.objects.filter(name__iexact="Nasi").first()
    ubi = Food.objects.filter(name__iexact="Ubi Rebus").first()
    abon = Food.objects.filter(name__iexact="Abon Sapi").first()
    buncis = Food.objects.filter(name__iexact="Buncis Rebus").first()
    usus = Food.objects.filter(name__iexact="Usus Ayam Goreng").first()
    bayam = Food.objects.filter(name__iexact="Bayam Rebus").first()
    ayam_sayap = Food.objects.filter(name__iexact="Ayam Goreng Sayap").first()

    if request.method == "POST":
        age = float(request.POST.get("age", 0))
        weight = float(request.POST.get("weight", 0))
        height = float(request.POST.get("height", 0)) / 100
        gender = request.POST.get("gender")
        activity = float(request.POST.get("activity", 1.2))

        adjusted_weight = weight
        if height > 0 and weight > 0:
            bmi = weight / (height ** 2)
            if bmi < 18.5:
                bmi_category = "Kurus"
            elif 18.5 <= bmi < 24.9:
                bmi_category = "Normal"
            elif 25 <= bmi < 29.9:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obesitas"

            ideal_min_weight = 18.5 * (height ** 2)
            ideal_max_weight = 24.9 * (height ** 2)
            ideal_weight = (ideal_min_weight + ideal_max_weight) / 2

            if weight < ideal_min_weight:
                weight_suggestion = f"Anda disarankan menaikkan berat badan sekitar {ideal_min_weight - weight:.1f} kg."
            elif weight > ideal_max_weight:
                weight_suggestion = f"Anda disarankan menurunkan berat badan sekitar {weight - ideal_max_weight:.1f} kg."
            else:
                weight_suggestion = "Berat badan Anda sudah dalam kisaran ideal."

            adjusted_weight = ideal_weight if (weight < ideal_min_weight or weight > ideal_max_weight) else weight

        # AKG
        if gender == "male":
            bmr = 66.5 + (13.75 * adjusted_weight) + (5.003 * height * 100) - (6.75 * age)
        elif gender == "female":
            bmr = 655.1 + (9.563 * adjusted_weight) + (1.85 * height * 100) - (4.676 * age)
        else:
            bmr = 0

        akg = round(bmr * activity)
        carbs_need = round(((0.75 * akg) + (0.60 * akg)) / 8)
        protein_need = round(((0.15 * akg) + (0.10 * akg)) / 8)
        fat_need = round(((0.25 * akg) + (0.10 * akg)) / 18)
        fiber_need = 15 if age <= 5 else 20 if age <= 11 else 25 if age <= 16 else 30
        sodium_need = round(30 * weight)

        foods = Food.objects.all()

        # ID kategori
        fruit_ids = list(Food.objects.filter(id__range=(44, 60)).values_list("id", flat=True))
        carbs_ids = list(Food.objects.filter(id__range=(8, 25)).values_list("id", flat=True))
        fiber_ids = list(Food.objects.filter(id__range=(29, 43)).values_list("id", flat=True))
        protein_ids = list(Food.objects.filter(id__range=(61, 85)).values_list("id", flat=True))

        for food in foods:
            defuzz_carbs = calculate_fuzzy_defuzz(food.__dict__, "carbs")
            defuzz_protein = calculate_fuzzy_defuzz(food.__dict__, "protein")
            defuzz_fiber = calculate_fuzzy_defuzz(food.__dict__, "fiber")

            final_score = (
                defuzz_carbs * ahp_weights[2] +
                defuzz_protein * ahp_weights[1] +
                defuzz_fiber * ahp_weights[0]
            )

            # Tentukan kategori berbasis ID atau fallback ke nutrisi tertinggi
            category = None
            if food.id in carbs_ids:
                category = "carbs"
            elif food.id in protein_ids:
                category = "protein"
            elif food.id in fiber_ids:
                category = "fiber"
            elif food.id in fruit_ids:
                category = "fruit"
            else:
                # Fallback untuk makanan baru yang ID-nya di luar range hardcoded
                c, p, fib = food.carbs or 0, food.protein or 0, food.fiber or 0
                if c >= p and c >= fib:
                    category = "carbs"
                elif p >= c and p >= fib:
                    category = "protein"
                else:
                    category = "fiber"

            fuzzy_foods.append({
                "name": food.name,
                "carbs": food.carbs,
                "protein": food.protein,
                "fat": food.fat,
                "fiber": food.fiber,
                "sodium": food.sodium,
                "defuzz_carbs": defuzz_carbs,
                "defuzz_protein": defuzz_protein,
                "defuzz_fiber": defuzz_fiber,
                "final_score": round(final_score, 4),
                "category": category
            })

    # Filter & ranking berdasarkan kategori
    carbs_foods = sorted(
        [f for f in fuzzy_foods if f["category"] == "carbs"],
        key=lambda x: -x["final_score"]
    )
    protein_foods = sorted(
        [f for f in fuzzy_foods if f["category"] == "protein"],
        key=lambda x: -x["final_score"]
    )
    fiber_foods = sorted(
        [f for f in fuzzy_foods if f["category"] == "fiber"],
        key=lambda x: -x["final_score"]
    )
    fruit_foods = sorted(
        [f for f in fuzzy_foods if f["category"] == "fruit"],
        key=lambda x: (x["sodium"], x["fat"])
    )

    return render(request, "user_page.html", {
        "fuzzy_foods": fuzzy_foods,
        "carbs_foods": carbs_foods,
        "protein_foods": protein_foods,
        "fiber_foods": fiber_foods,
        "fruit_foods": fruit_foods,
        "akg": akg,
        "carbs_need": carbs_need,
        "protein_need": protein_need,
        "fat_need": fat_need,
        "fiber_need": fiber_need,
        "sodium_need": sodium_need,
        "bmi": bmi,
        "bmi_category": bmi_category,
        "weight_suggestion": weight_suggestion,
        "ideal_weight": round(ideal_weight, 1) if ideal_weight else None,
        "gado": gado,
        "gudeg": gudeg,
        "nasi": nasi,
        "ubi": ubi,
        "abon": abon,
        "buncis": buncis,
        "usus": usus,
        "bayam": bayam,
        "ayam_sayap": ayam_sayap,
        "ahp_matrix": ahp_data["ahp_matrix"],
        "normalized_matrix": ahp_data["normalized_matrix"],
        "ahp_weights": ahp_data["ahp_weights"],
    })

def add_food_page(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = FoodForm()
    return render(request, 'admin/add_food_page.html', {'form': form})

def update_food_page(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = FoodForm(instance=food)
    return render(request, 'admin/update_food_page.html', {'form': form})

def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    food.delete()
    return redirect('admin_page')