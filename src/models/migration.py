import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, DECIMAL, Enum, ForeignKey, VARBINARY, Text, Index
from models.connection import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


# class MigrateVersion(Base, TimestampMixin):
#     """版本迁移信息"""
#     __tablename__ = 'MigrateVersion'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     operator_name = Column(String(60), nullable=False)
#     describe = Column(String(255), nullable=False)
#     remarks = Column(Text)


class Project(Base, TimestampMixin):
    __tablename__ = 'Project'

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(255), nullable=False, primary_key=True)
    parent_id = Column(Integer, nullable=False, default=0)
    outsource_id = Column(VARBINARY(255), nullable=True)
    supplier_company_id = Column(Integer, ForeignKey('SupplierCompany.supplier_company_id'), nullable=True, index=True)
    source_code = Column(Integer, nullable=True)
    project_owner_id = Column(Integer, nullable=True, index=True)
    project_owner_name = Column(String(255), ForeignKey('ProjectOwner.project_owner_name'), nullable=True, index=True)
    project_model = Column(String(255), nullable=True)
    project_location = Column(String(255), nullable=True)
    project_kick_off_date = Column(DateTime, nullable=True)


class ProjectOwner(Base, TimestampMixin):
    """项目负责人信息"""
    __tablename__ = 'ProjectOwner'

    project_owner_id = Column(Integer, primary_key=True, autoincrement=True)
    project_owner_name = Column(String(255), nullable=True, index=True)
    project_owner_alias = Column(String(255), nullable=True)
    project_owner_email = Column(String(255), nullable=True)
    created_time = Column(DateTime, nullable=True)

    # 定义联合索引
    __table_args__ = (
        Index('project_owner_id', 'project_owner_id', 'project_owner_name'),
    )


class Contract(Base, TimestampMixin):
    """合同"""
    __tablename__ = 'Contract'

    c_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_type = Column(String(100), nullable=True)
    effective_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    contract_id = Column(String(100), nullable=True, index=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=True, index=True)


class ContractorVendor(Base, TimestampMixin):
    """员工合同"""
    __tablename__ = 'ContractorVendor'

    purchase_order_vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_order_bill_flow_id = Column(Integer, ForeignKey('PurchaseOrderBillFlow.purchase_order_bill_flow_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True, index=True)
    vendor_id = Column(Integer, ForeignKey('Vendor.vendor_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True, index=True)
    sub_project_name = Column(String(255), nullable=True)
    main_project_name = Column(String(255), nullable=True)
    project_id = Column(Integer, nullable=True)
    vendor_rate = Column(String(255), nullable=True)
    standard_working_hours = Column(Float, nullable=True)
    vacation_hours = Column(Float, nullable=True)
    overtime_hours = Column(Float, nullable=True)
    vacation_amount = Column(DECIMAL(10, 2), nullable=True)
    overtime_amount = Column(DECIMAL(10, 2), nullable=True)
    actual_working_hours = Column(Float, nullable=True)
    monthly_cost = Column(DECIMAL(10, 2), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    actual_amount = Column(DECIMAL(10, 2), nullable=True)
    payment_adjustment = Column(DECIMAL(10, 2), nullable=True)
    justification = Column(String(255), nullable=True)


class ProjectContract(Base, TimestampMixin):
    """项目合同关联表"""
    __tablename__ = 'ProjectContract'

    project_contract_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(String(255), ForeignKey('Contract.contract_id'), nullable=True, index=True)
    c_id = Column(Integer, nullable=True)
    project_name = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=True, index=True)


class Vendor(Base, TimestampMixin):
    """员工表"""
    __tablename__ = 'Vendor'

    vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_english_name = Column(String(255), nullable=True)
    vendor_chinese_name = Column(String(255), nullable=True)
    vendor_alias = Column(String(255), nullable=True)
    site_status = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    vendor_type = Column(String(255), nullable=True)
    assignment_end_date = Column(DateTime, nullable=True, comment='alias_expiration_date')
    maximum_end_date = Column(DateTime, nullable=True, comment='alias_max_expiration_date')
    vendor_onboarding_date = Column(DateTime, nullable=True)
    vendor_hourly_rate = Column(DECIMAL(10, 2), nullable=True)
    vendor_rate_currency_information = Column(String(255), nullable=True, comment='Vendor Rate')
    supplier_company_id = Column(Integer, nullable=True)


class VendorLeaveOvertime(Base, TimestampMixin):
    """员工出勤表"""
    __tablename__ = 'VendorLeaveOvertime'

    vendor_leave_overtime_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey('Vendor.vendor_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True, index=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    hours = Column(Float, nullable=True)
    type = Column(String(255), nullable=True, comment='leave/overtime')
    created_time = Column(DateTime, nullable=True)
    sub_project_name = Column(String(255), nullable=True, index=True)
    main_project_name = Column(String(255), nullable=True)
    project_id = Column(Integer, nullable=True)


class ProjectVendor(Base, TimestampMixin):
    """项目内员工信息"""
    __tablename__ = 'ProjectVendor'

    project_vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey('Vendor.vendor_id'), nullable=True, index=True)
    sub_project_name = Column(String(255), ForeignKey('Project.project_name'), nullable=True, index=True)
    sub_project_id = Column(Integer, nullable=True)
    main_project_name = Column(String(255), nullable=True)
    main_project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=True)


class ProjectCostForecast(Base, TimestampMixin):
    """项目支出预算"""
    __tablename__ = 'ProjectCostForecast'

    project_cost_forecast = Column(Integer, primary_key=True, autoincrement=True)
    po_number = Column(String(255), nullable=True)
    cost_forecasting_month = Column(DateTime, nullable=True)
    cost_amount = Column(DECIMAL(10, 2), nullable=True)
    project_name = Column(String(255), ForeignKey('Project.project_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=True, index=True)
    vendor_rate = Column(DECIMAL(10, 2), nullable=True)
    payment_model = Column(String(255), nullable=True)
    currency_unit = Column(String(255), nullable=True)


class CurrencyExchangeRate(Base, TimestampMixin):
    """汇率表"""
    __tablename__ = 'CurrencyExchangeRate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_exchange_rate = Column(DECIMAL(10, 4), nullable=True)
    currency_exchange_applied_start_time = Column(DateTime, nullable=True)
    currency_exchange_applied_end_time = Column(DateTime, nullable=True)
    currecny_usage = Column(String(255), nullable=True)


class Roles(Base, TimestampMixin):
    """权限"""
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alias = Column(String(60), nullable=False, index=True)
    name = Column(String(60), nullable=False, index=True)
    role_type = Column(Enum('admin', 'project_owner', 'ventor'), nullable=False)
    active = Column(Integer, nullable=False, default=1)


class SupplierCompany(Base, TimestampMixin):
    """供应商公司"""
    __tablename__ = 'SupplierCompany'

    supplier_company_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_company_name = Column(String(255), nullable=True)
    created_time = Column(DateTime, nullable=True)
    supplier_company_name_zh = Column(String(255), nullable=True)
    supplier_company_abbreviation = Column(String(255), nullable=True)


class SupplierNumber(Base, TimestampMixin):
    """供应商编号"""
    __tablename__ = 'SupplierNumber'

    supplier_number_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_company_id = Column(Integer, nullable=True)
    supplier_company_name = Column(String(255), nullable=True)
    microsoft_company_code = Column(String(255), nullable=True)
    supplier_number = Column(String(255), nullable=False, comment='Vendor Number')
    microsoft_company_code_description = Column(String(255), nullable=True)


class PurchaseOrder(Base, TimestampMixin):
    """采购单"""
    __tablename__ = 'PurchaseOrder'

    purchase_order_id = Column(Integer, primary_key=True, autoincrement=True)
    po_number = Column(String(100), nullable=True)
    original_amount = Column(DECIMAL(10, 2), nullable=True)
    payable_amount = Column(DECIMAL(10, 2), nullable=True)
    open_amount = Column(DECIMAL(10, 2), nullable=True)
    project_name = Column(String(255), ForeignKey('Project.project_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=True, index=True)
    payment_model = Column(String(255), nullable=True, comment='Milestone;Fixed price')
    po_status = Column(String(255), nullable=True, comment='Active Inactive')
    project_id = Column(Integer, nullable=True)
    total_invoiced_amount = Column(DECIMAL(10, 2), nullable=True)
    po_start_date = Column(DateTime, nullable=True)
    po_end_date = Column(DateTime, nullable=True)
    po_duration_months = Column(String(255), nullable=True)
    currency_unit = Column(String(255), nullable=True, comment='Currency unit')


class PurchaseOrderBillFlow(Base, TimestampMixin):
    """采购单票据流"""
    __tablename__ = 'PurchaseOrderBillFlow'

    purchase_order_bill_flow_id = Column(Integer, primary_key=True, autoincrement=True)
    po_monthly_amount = Column(DECIMAL(10, 2), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    total_vendors = Column(Integer, nullable=True)
    onsite_vendors = Column(Integer, nullable=True)
    offsite_vendors = Column(Integer, nullable=True)
    total_workdays = Column(Integer, nullable=True)
    total_vacations_hours = Column(Float, nullable=True)
    total_overtime_hours = Column(Float, nullable=True)
    overtime_amount = Column(DECIMAL(10, 2), nullable=True)
    vacations_amount = Column(DECIMAL(10, 2), nullable=True)
    sub_project_name = Column(String(255), index=True, nullable=True)
    main_project_name = Column(String(255), nullable=True)
    currency_unit = Column(String(255), nullable=True, comment='Currency unit')


class PurchaseOrder_IO_CC(Base, TimestampMixin):
    """采购单 io cc 信息"""
    __tablename__ = 'PurchaseOrder_IO_CC'

    project_io_cc_payment_id = Column(Integer, primary_key=True, autoincrement=True)
    io = Column(String(255), nullable=True)
    cc = Column(String(255), nullable=True)
    project_id = Column(Integer, nullable=True)
    purchase_order_id = Column(Integer, nullable=True)
    po_number = Column(String(255), nullable=True)
    project_name = Column(String(255), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=True)
    payment_data = Column(DateTime, nullable=True)
    currency_unit = Column(String(255), nullable=True, comment='Currency unit')


class PurchaseOrder_Invoice(Base, TimestampMixin):
    """采购单发票"""
    __tablename__ = 'PurchaseOrder_Invoice'

    purchase_order_invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_data = Column(DateTime, nullable=True)
    invoice_amount = Column(DECIMAL(10, 2), nullable=True)
    purchase_order_id = Column(Integer, nullable=True)
    po_number = Column(Integer, nullable=True)
    project_name = Column(String(255), nullable=True)
    currency_unit = Column(String(255), nullable=True, comment='Currency unit')

