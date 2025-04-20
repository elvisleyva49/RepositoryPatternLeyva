from abc import ABC, abstractmethod
from typing import List

# 1. Entidad de Dominio
class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def apply_discount(self, discount: float):
        self.price *= (1 - discount)
        return self

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"

# 2. Interfaz del Repositorio
class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Product:
        pass

    @abstractmethod
    def find_expensive_products(self, min_price: float) -> List[Product]:
        pass

# 3. Implementación en Memoria (para simplificar)
class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products = {
            1: Product(1, "Laptop", 999.99),
            2: Product(2, "Phone", 699.99),
            3: Product(3, "Tablet", 299.99),
            4: Product(4, "Monitor", 499.99),
        }

    def save(self, product: Product) -> None:
        self.products[product.id] = product

    def find_by_id(self, id: int) -> Product:
        return self.products.get(id)

    def find_expensive_products(self, min_price: float) -> List[Product]:
        return [p for p in self.products.values() if p.price > min_price]

# 4. Servicio de Negocio
class PricingService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def apply_discount_to_expensive_products(self, discount: float):
        expensive_products = self.product_repo.find_expensive_products(500.0)
        for product in expensive_products:
            product.apply_discount(discount)
            self.product_repo.save(product)

# 5. Ejemplo de Uso
if __name__ == "__main__":
    # Configuración
    repo = InMemoryProductRepository()
    pricing_service = PricingService(repo)

    # Estado inicial
    print("Productos antes del descuento:")
    for product in repo.products.values():
        print(product)

    # Aplicar descuento
    pricing_service.apply_discount_to_expensive_products(0.1)  # 10% de descuento

    # Estado final
    print("\nProductos después del descuento (solo caros):")
    for product in repo.find_expensive_products(500.0):
        print(product)