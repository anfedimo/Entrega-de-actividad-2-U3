import random
from bson.objectid import ObjectId

print("Generando 1000 documentos de productos con esquema flexible...")

categorias = ["Electronics", "Clothing", "Home"]
productos = []

for i in range(1000):
    categoria = random.choice(categorias)

    # 1. Atributos base (comunes a todos los documentos)
    producto = {
        "name": f"Producto Ecommify {i+1}",
        "category": categoria,
        "price": round(random.uniform(15.0, 1200.0), 2),

        # 2. Patrón Computed (Métricas precalculadas para lecturas rápidas)
        "computed_metrics": {
            "total_units_sold": random.randint(0, 5000),
            "average_rating": round(random.uniform(1.0, 5.0), 1)
        },

        # 3. Patrón Referencing (Simulamos referencias a una colección externa de 'reviews')
        "reviews": [ObjectId() for _ in range(random.randint(0, 3))]
    }

    # 4. Esquema Flexible (El subdocumento 'specifications' muta según la categoría)
    if categoria == "Electronics":
        producto["specifications"] = {
            "processor": random.choice(["Intel Core i5", "Intel Core i7", "AMD Ryzen 5"]),
            "ram": random.choice(["8GB", "16GB", "32GB"]),
            "warranty_years": random.randint(1, 3)
        }
    elif categoria == "Clothing":
        producto["specifications"] = {
            "size": random.choice(["S", "M", "L", "XL"]),
            "material": random.choice(["Cotton", "Polyester", "Wool"]),
            "gender": random.choice(["Unisex", "Male", "Female"])
        }
    else: # Home
        producto["specifications"] = {
            "weight_kg": round(random.uniform(1.0, 20.0), 1),
            "color": random.choice(["Red", "Blue", "Black", "White", "Wood"])
        }

    productos.append(producto)

# Limpiamos la colección primero por si ejecutas la celda varias veces (Idempotencia)
db.products.drop()

# Inserción masiva en Atlas (Bulk insert)
db.products.insert_many(productos)
cantidad = db.products.count_documents({})

print(f"✅ ¡Completado! Se han insertado {cantidad} documentos en la colección 'products'.")