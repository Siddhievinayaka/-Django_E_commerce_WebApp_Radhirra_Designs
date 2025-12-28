-- SQL commands to add WhatsApp/Email checkout system fields
-- Run these commands directly in your database

-- Add new fields to Radhirra_order table
ALTER TABLE Radhirra_order ADD COLUMN order_type VARCHAR(10) DEFAULT 'whatsapp';
ALTER TABLE Radhirra_order ADD COLUMN order_status VARCHAR(10) DEFAULT 'pending';
ALTER TABLE Radhirra_order ADD COLUMN total_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE Radhirra_order ADD COLUMN contact_value VARCHAR(255);
ALTER TABLE Radhirra_order ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Add new fields to Radhirra_orderitem table
ALTER TABLE Radhirra_orderitem ADD COLUMN price_at_order DECIMAL(10,2) DEFAULT 0;
ALTER TABLE Radhirra_orderitem ADD COLUMN variant_info VARCHAR(255);

-- Modify Radhirra_shippingaddress table to allow null values
ALTER TABLE Radhirra_shippingaddress MODIFY COLUMN address VARCHAR(200) NULL;
ALTER TABLE Radhirra_shippingaddress MODIFY COLUMN city VARCHAR(200) NULL;
ALTER TABLE Radhirra_shippingaddress MODIFY COLUMN state VARCHAR(200) NULL;
ALTER TABLE Radhirra_shippingaddress MODIFY COLUMN zipcode VARCHAR(200) NULL;

-- Add phone_number field to Radhirra_shippingaddress table
ALTER TABLE Radhirra_shippingaddress ADD COLUMN phone_number VARCHAR(20);

-- Add constraints for enum-like behavior (optional)
ALTER TABLE Radhirra_order ADD CONSTRAINT chk_order_type CHECK (order_type IN ('whatsapp', 'email'));
ALTER TABLE Radhirra_order ADD CONSTRAINT chk_order_status CHECK (order_status IN ('pending', 'confirmed', 'completed', 'cancelled'));