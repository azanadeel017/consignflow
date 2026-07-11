-- ConsignFlow Relational Database Schema
-- Optimized for PostgreSQL (Scales to millions of transactions)
-- Enforces referential integrity, indexes for performance, and constraints for financial accuracy.

-- Enable UUID extension for secure, non-sequential, and scalable primary keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------
-- Table: platforms
-- Description: Stores supported marketplaces and their corresponding fee structures.
-- -----------------------------------------------------
CREATE TABLE platforms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, -- e.g., 'WHATNOT', 'EBAY', 'POSHMARK', 'TIKTOK_SHOP'
    commission_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.0000, -- e.g., 0.0800 for 8%
    transaction_fee_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.0000, -- e.g., 0.0290 for 2.9%
    flat_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- e.g., 0.30 for $0.30
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: sellers
-- Description: Stores consignor accounts, contact information, and default splits.
-- -----------------------------------------------------
CREATE TABLE sellers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    status VARCHAR(50) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Suspended')),
    default_split_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.6000, -- Default split rate paid to seller (e.g. 60% split)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: inventory_items
-- Description: Tracks physical inventory items received for consignment.
-- -----------------------------------------------------
CREATE TABLE inventory_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_id UUID NOT NULL REFERENCES sellers(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0.00),
    status VARCHAR(50) NOT NULL DEFAULT 'Draft' CHECK (status IN ('Draft', 'Active', 'Sold', 'Returned', 'Expired')),
    custom_split_rate DECIMAL(5, 4), -- Optional split rate override specifically for this item
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: transactions
-- Description: Records sales transactions, platform fees, and financial breakdowns.
-- -----------------------------------------------------
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id UUID UNIQUE NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    platform_id UUID NOT NULL REFERENCES platforms(id) ON DELETE RESTRICT,
    gross_price DECIMAL(10, 2) NOT NULL CHECK (gross_price >= 0.00),
    
    -- Calculated Platform Fees (Stored for audit and reporting history)
    platform_commission DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (platform_commission >= 0.00),
    platform_transaction_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (platform_transaction_fee >= 0.00),
    platform_flat_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (platform_flat_fee >= 0.00),
    total_platform_fees DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (total_platform_fees >= 0.00),
    
    -- Payout Split Breakdowns
    seller_payout DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (seller_payout >= 0.00),
    store_revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (store_revenue >= 0.00),
    
    -- Status and Metadata
    status VARCHAR(50) NOT NULL DEFAULT 'Completed' CHECK (status IN ('Completed', 'Pending_Payout', 'Payout_Cleared', 'Refunded')),
    external_transaction_id VARCHAR(255), -- Reference ID from Whatnot, eBay, etc.
    sold_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Database Indexes for Scalability (Millions of Rows)
-- -----------------------------------------------------
CREATE INDEX idx_inventory_items_seller ON inventory_items(seller_id);
CREATE INDEX idx_inventory_items_status ON inventory_items(status);
CREATE INDEX idx_transactions_platform ON transactions(platform_id);
CREATE INDEX idx_transactions_sold_at ON transactions(sold_at);
CREATE INDEX idx_transactions_status ON transactions(status);
