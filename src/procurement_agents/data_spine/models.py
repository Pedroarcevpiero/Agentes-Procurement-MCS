"""Modelos SQLAlchemy 2.0 del data spine de procurement.

Ocho tablas: `suppliers`, `categories`, `spend_transactions`, `contracts`,
`invoices`, `market_benchmarks`, `savings_opportunities` (auditoria de
salidas del agente), `demand_scenarios`. Usa el estilo declarativo 2.0
(`Mapped`/`mapped_column`) con tipos explicitos, FKs e indices sobre las
columnas de filtrado mas comunes (category_id, supplier_id,
transaction_date).
"""
from __future__ import annotations

import datetime
import enum
import uuid

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarativa comun a todo el data spine."""


class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    DRAFT = "draft"


class InvoiceMatchStatus(str, enum.Enum):
    MATCHED = "matched"
    DISCREPANCY = "discrepancy"
    UNMATCHED = "unmatched"


class OpportunityStatus(str, enum.Enum):
    PROPOSED = "proposed"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class DemandScenarioType(str, enum.Enum):
    LOW = "low"
    BASE = "base"
    HIGH = "high"


class Supplier(Base):
    """Proveedor sobre el que se registra gasto, contratos y facturas."""

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    legal_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, doc="Tax ID / DUNS sintetico."
    )
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    primary_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    risk_score: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=0, doc="0 (bajo riesgo) - 100 (alto riesgo)."
    )
    on_time_delivery_rate: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    quality_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    diversity_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    primary_category: Mapped["Category | None"] = relationship(
        foreign_keys=[primary_category_id]
    )

    __table_args__ = (Index("ix_suppliers_primary_category_id", "primary_category_id"),)


class Category(Base):
    """Categoria de compra (taxonomia estilo procurement, ej. IT Hardware)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    taxonomy_code: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, doc="Codigo estilo UNSPSC sintetico."
    )
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_direct_spend: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent_category: Mapped["Category | None"] = relationship(
        remote_side=[id], foreign_keys=[parent_category_id]
    )


class Contract(Base):
    """Contrato negociado que ampara transacciones y facturas de un proveedor."""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_number: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    negotiated_unit_price: Mapped[float] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    payment_terms_days: Mapped[int] = mapped_column(nullable=False, default=30)
    auto_renew: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[ContractStatus] = mapped_column(
        Enum(ContractStatus, name="contract_status"), nullable=False, default=ContractStatus.ACTIVE
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    supplier: Mapped["Supplier"] = relationship()
    category: Mapped["Category"] = relationship()

    __table_args__ = (
        Index("ix_contracts_supplier_id", "supplier_id"),
        Index("ix_contracts_category_id", "category_id"),
        Index("ix_contracts_status", "status"),
    )


class SpendTransaction(Base):
    """Transaccion de gasto individual (linea de PO / gasto ejecutado)."""

    __tablename__ = "spend_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    contract_id: Mapped[int | None] = mapped_column(
        ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True
    )
    po_number: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    quantity: Mapped[float] = mapped_column(Numeric(14, 4), nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(14, 4), nullable=False)
    business_unit: Mapped[str] = mapped_column(String(64), nullable=False)
    cost_center: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    supplier: Mapped["Supplier"] = relationship()
    category: Mapped["Category"] = relationship()
    contract: Mapped["Contract | None"] = relationship()

    __table_args__ = (
        Index("ix_spend_transactions_category_id", "category_id"),
        Index("ix_spend_transactions_supplier_id", "supplier_id"),
        Index("ix_spend_transactions_transaction_date", "transaction_date"),
        Index(
            "ix_spend_transactions_category_date",
            "category_id",
            "transaction_date",
        ),
    )


class Invoice(Base):
    """Factura de proveedor, parcialmente emparejada contra contrato/transaccion."""

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    contract_id: Mapped[int | None] = mapped_column(
        ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True
    )
    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("spend_transactions.id", ondelete="SET NULL"), nullable=True
    )
    invoice_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    match_status: Mapped[InvoiceMatchStatus] = mapped_column(
        Enum(InvoiceMatchStatus, name="invoice_match_status"),
        nullable=False,
        default=InvoiceMatchStatus.UNMATCHED,
    )
    discrepancy_amount: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    discrepancy_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    supplier: Mapped["Supplier"] = relationship()
    contract: Mapped["Contract | None"] = relationship()
    transaction: Mapped["SpendTransaction | None"] = relationship()

    __table_args__ = (
        Index("ix_invoices_supplier_id", "supplier_id"),
        Index("ix_invoices_contract_id", "contract_id"),
        Index("ix_invoices_match_status", "match_status"),
    )


class MarketBenchmark(Base):
    """Indice/precio de referencia de mercado por categoria y periodo mensual."""

    __tablename__ = "market_benchmarks"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    period_month: Mapped[datetime.date] = mapped_column(
        Date, nullable=False, doc="Primer dia del mes del benchmark."
    )
    price_index: Mapped[float] = mapped_column(
        Numeric(10, 4), nullable=False, doc="Indice de precio normalizado (base 100)."
    )
    yoy_price_change_pct: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    region: Mapped[str] = mapped_column(String(32), nullable=False, default="GLOBAL")
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="synthetic_market_feed")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    category: Mapped["Category"] = relationship()

    __table_args__ = (
        UniqueConstraint(
            "category_id", "period_month", "region", name="uq_market_benchmarks_category_month_region"
        ),
        Index("ix_market_benchmarks_category_id", "category_id"),
        Index("ix_market_benchmarks_period_month", "period_month"),
    )


class SavingsOpportunity(Base):
    """Auditoria de oportunidades de ahorro reportadas por el agente.

    `source_transaction_ids` / `source_benchmark_ids` guardan los IDs
    citados como evidencia; el guardrail `require_citation_hook` verifica
    que existan en `spend_transactions` / `market_benchmarks` antes de
    permitir el registro.
    """

    __tablename__ = "savings_opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, unique=True, nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )
    opportunity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    estimated_savings_usd: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(OpportunityStatus, name="opportunity_status"),
        nullable=False,
        default=OpportunityStatus.PROPOSED,
    )
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    source_transaction_ids: Mapped[list[int]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    source_benchmark_ids: Mapped[list[int]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    created_by_agent: Mapped[str] = mapped_column(String(64), nullable=False)
    session_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    category: Mapped["Category"] = relationship()
    supplier: Mapped["Supplier | None"] = relationship()

    __table_args__ = (
        Index("ix_savings_opportunities_category_id", "category_id"),
        Index("ix_savings_opportunities_supplier_id", "supplier_id"),
        Index("ix_savings_opportunities_status", "status"),
    )


class DemandScenario(Base):
    """Escenario de volatilidad de demanda (bajo/base/alto) por categoria."""

    __tablename__ = "demand_scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, unique=True, nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    scenario_type: Mapped[DemandScenarioType] = mapped_column(
        Enum(DemandScenarioType, name="demand_scenario_type"), nullable=False
    )
    horizon_months: Mapped[int] = mapped_column(nullable=False, default=12)
    projected_volume_change_pct: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    projected_spend_usd: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    volatility_index: Mapped[float] = mapped_column(Numeric(6, 4), nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_by_agent: Mapped[str] = mapped_column(String(64), nullable=False)
    session_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    category: Mapped["Category"] = relationship()

    __table_args__ = (
        Index("ix_demand_scenarios_category_id", "category_id"),
        Index("ix_demand_scenarios_scenario_type", "scenario_type"),
    )
