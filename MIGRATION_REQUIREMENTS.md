# Database Migration Requirements - WhatsApp/Email Checkout System

## Overview
Transform your e-commerce system to support WhatsApp/Email checkout with proper order management and admin controls.

## Required Database Changes

### 1. Order Table Enhancements (`Radhirra_order`)

```sql
-- Add new columns for order management
ALTER TABLE Radhirra_order ADD COLUMN order_type VARCHAR(10) DEFAULT 'whatsapp';
ALTER TABLE Radhirra_order ADD COLUMN order_status VARCHAR(10) DEFAULT 'pending';
ALTER TABLE Radhirra_order ADD COLUMN total_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE Radhirra_order ADD COLUMN contact_value VARCHAR(255);
ALTER TABLE Radhirra_order ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add constraints for data integrity
ALTER TABLE Radhirra_order ADD CONSTRAINT chk_order_type CHECK (order_type IN ('whatsapp', 'email'));
ALTER TABLE Radhirra_order ADD CONSTRAINT chk_order_status CHECK (order_status IN ('pending', 'confirmed', 'completed', 'cancelled'));
```

### 2. OrderItem Table Enhancements (`Radhirra_orderitem`)

```sql
-- Add price snapshot and variant information
ALTER TABLE Radhirra_orderitem ADD COLUMN price_at_order DECIMAL(10,2) DEFAULT 0;
ALTER TABLE Radhirra_orderitem ADD COLUMN variant_info VARCHAR(255);
```

### 3. ShippingAddress Table Modifications (`Radhirra_shippingaddress`)

```sql
-- Make address fields optional for admin updates
ALTER TABLE Radhirra_shippingaddress ALTER COLUMN address DROP NOT NULL;
ALTER TABLE Radhirra_shippingaddress ALTER COLUMN city DROP NOT NULL;
ALTER TABLE Radhirra_shippingaddress ALTER COLUMN state DROP NOT NULL;
ALTER TABLE Radhirra_shippingaddress ALTER COLUMN zipcode DROP NOT NULL;

-- Add phone number field
ALTER TABLE Radhirra_shippingaddress ADD COLUMN phone_number VARCHAR(20);
```

### 4. Performance Indexes (Optional)

```sql
-- Add indexes for better query performance
CREATE INDEX idx_order_status ON Radhirra_order(order_status);
CREATE INDEX idx_order_type ON Radhirra_order(order_type);
CREATE INDEX idx_order_date ON Radhirra_order(date_ordered);
```

## New Field Descriptions

| Table | Field | Type | Purpose |
|-------|-------|------|---------|
| `Radhirra_order` | `order_type` | VARCHAR(10) | Track order source (whatsapp/email) |
| `Radhirra_order` | `order_status` | VARCHAR(10) | Order lifecycle (pending/confirmed/completed/cancelled) |
| `Radhirra_order` | `total_amount` | DECIMAL(10,2) | Price snapshot at order time |
| `Radhirra_order` | `contact_value` | VARCHAR(255) | Phone number or email address |
| `Radhirra_order` | `updated_at` | TIMESTAMP | Track order modifications |
| `Radhirra_orderitem` | `price_at_order` | DECIMAL(10,2) | Product price when ordered |
| `Radhirra_orderitem` | `variant_info` | VARCHAR(255) | Size/color/customization details |
| `Radhirra_shippingaddress` | `phone_number` | VARCHAR(20) | Customer phone number |

## System Features After Migration

✅ **Order Creation**: Automatic order creation on WhatsApp/Email button click  
✅ **Status Tracking**: pending → confirmed → completed/cancelled workflow  
✅ **Price Protection**: Snapshot prices at order time  
✅ **Variant Storage**: Size/sleeve/customization information  
✅ **Contact Tracking**: Phone/email for each order  
✅ **Admin Management**: Enhanced admin interface for order processing  
✅ **Analytics Ready**: Filter by order source and status  

## Testing Steps

1. Add items to cart
2. Select items and proceed to checkout
3. Fill shipping information
4. Click "Order via WhatsApp" or "Order via Email"
5. Verify order created with `pending` status in admin
6. Test admin order status updates
7. Verify cart items removed after successful order

## Admin Dashboard Features

- View orders by type (WhatsApp/Email)
- Filter by status (Pending/Confirmed/Completed/Cancelled)
- Update order status manually
- View price snapshots and variant information
- Track order modifications with timestamps