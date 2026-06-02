import random

print("--- Completando el Modelo: Colección Externa de Reviews ---")

# [SOLUCIÓN] Limpiamos la colección para evitar el error E11000 de llave duplicada
db.reviews.drop()

# 1. Tomamos un producto aleatorio que tenga al menos 1 review en su arreglo
producto_con_reviews = db.products.find_one({"reviews.0": {"$exists": True}})

if producto_con_reviews:
    ids_resenas = producto_con_reviews["reviews"]
    documentos_resenas = []

    # 2. Creamos los documentos físicos en la nueva colección 'reviews'
    for review_id in ids_resenas:
        documentos_resenas.append({
            "_id": review_id,
            "user": f"Usuario_{random.randint(100, 999)}",
            "comment": random.choice([
                "Excelente producto, muy recomendado.",
                "Buena calidad pero el envío demoró.",
                "Cumple con las especificaciones."
            ]),
            "rating": random.randint(3, 5)
        })

    # Insertamos las reseñas en su propia colección
    db.reviews.insert_many(documentos_resenas)
    print(f"✅ Se crearon {len(documentos_resenas)} reseñas físicas en la colección 'reviews'.\n")

    # 3. Consulta C: Validando el Patrón de Referencia Extendida ($lookup)
    pipeline_lookup = [
        {"$match": {"_id": producto_con_reviews["_id"]}},
        {"$lookup": {
            "from": "reviews",          # Colección externa a consultar
            "localField": "reviews",    # Campo local (arreglo de ObjectIds)
            "foreignField": "_id",      # Campo foráneo en 'reviews'
            "as": "detalle_resenas"     # Nombre del nuevo campo con el resultado
        }},
        {"$project": {
            "_id": 0,
            "name": 1,
            "category": 1,
            "detalle_resenas.user": 1,
            "detalle_resenas.comment": 1
        }}
    ]

    print("--- RESULTADO C: Consulta de Producto haciendo JOIN ($lookup) con sus Reseñas ---")
    resultado_join = db.products.aggregate(pipeline_lookup)
    for doc in resultado_join:
        import json
        print(json.dumps(doc, indent=2, default=str))

else:
    print("No se encontró un producto. Vuelve a ejecutar la celda de inserción de productos.")