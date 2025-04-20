import pytest
from repository_pattern.main import (
    Product,
    ProductRepository,
    InMemoryProductRepository,
    PricingService
)
class TestProduct:
    def test_apply_discount(self):
        product = Product(1, "Test", 100.0)
        product.apply_discount(0.1)
        assert product.price == 90.0

class TestInMemoryProductRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryProductRepository()

    def test_find_by_id(self, repo):
        product = repo.find_by_id(1)
        assert product.name == "Laptop"
        assert product.price == 999.99

    def test_find_expensive_products(self, repo):
        expensive = repo.find_expensive_products(500.0)
        assert len(expensive) == 2  # Laptop and Phone

class TestPricingService:
    @pytest.fixture
    def service(self):
        repo = InMemoryProductRepository()
        return PricingService(repo)

    def test_apply_discount(self, service):
        service.apply_discount_to_expensive_products(0.1)
        expensive = service.product_repo.find_expensive_products(500.0)
        assert expensive[0].price == 999.99 * 0.9
        assert expensive[1].price == 699.99 * 0.9