"""Tests for Product and ProductPrice models."""
import pytest
from decimal import Decimal
from app.db.models import Product, ProductPrice, News


def test_product_model_has_required_fields():
    """Product model has all required columns."""
    cols = {c.name for c in Product.__table__.columns}
    assert "id" in cols
    assert "name" in cols
    assert "brand" in cols
    assert "description" in cols
    assert "photo_url" in cols
    assert "updated_at" in cols


def test_product_price_model_has_required_fields():
    """ProductPrice model has all required columns."""
    cols = {c.name for c in ProductPrice.__table__.columns}
    assert "product_id" in cols
    assert "branch_id" in cols
    assert "branch_name" in cols
    assert "price" in cols
    assert "qty" in cols


def test_product_price_composite_primary_key():
    """ProductPrice has composite primary key (product_id, branch_id)."""
    pk_cols = {c.name for c in ProductPrice.__table__.primary_key.columns}
    assert pk_cols == {"product_id", "branch_id"}


def test_news_model_has_required_fields():
    """News model has all required columns."""
    cols = {c.name for c in News.__table__.columns}
    assert "id" in cols
    assert "title" in cols
    assert "content" in cols
    assert "published_at" in cols
