# ADMIN DASHBOARD REQUIREMENTS - RADHIRRA DESIGNS

## DATABASE CONNECTION
```
DATABASE_URL=postgresql://postgres.satzaiimlnpjhhmgbcez:vectratechhs17@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?sslmode=require
```

## CLOUDINARY (For Image Storage)
```
CLOUDINARY_CLOUD_NAME=ddlx2h9hr
CLOUDINARY_API_KEY=999271691163949
CLOUDINARY_API_SECRET=KNWUBus3MXZo5DWaOL5bcjczep0
```

---

## DATABASE TABLES & MODELS

### 1. USERS & AUTHENTICATION

#### Table: `users_customuser`
- id (Primary Key)
- email (Unique, used for login)
- username
- password (hashed)
- first_name
- last_name
- is_staff (Boolean - admin access)
- is_superuser (Boolean - full access)
- is_active (Boolean)
- date_joined
- last_login

#### Table: `users_userprofile`
- id (Primary Key)
- user_id (Foreign Key → users_customuser)
- phone
- gender (Male/Female/Other)
- profile_pic (Cloudinary URL)
- address
- city
- state
- zipcode

---

### 2. PRODUCTS MANAGEMENT

#### Table: `Radhirra_category`
- id (Primary Key)
- name (Unique)
- slug (Unique, auto-generated)
- created_at

#### Table: `Radhirra_product`
- id (Primary Key)
- category_id (Foreign Key → Radhirra_category)
- name
- sku (Unique)
- regular_price (Decimal)
- sale_price (Decimal, nullable)
- description (Text)
- size (XS/S/M/L/XL/XXL)
- sleeve (sleeveless/short/3/4)
- material
- specifications (Text)
- seller_information (Text)
- is_featured (Boolean) - Show on homepage
- is_new_arrival (Boolean) - Tag as new
- is_best_seller (Boolean) - Tag as bestseller

#### Table: `Radhirra_productimage`
- id (Primary Key)
- product_id (Foreign Key → Radhirra_product)
- image (Cloudinary URL)
- is_main (Boolean) - Main product image

---

### 3. ORDERS MANAGEMENT

#### Table: `Radhirra_order`
- id (Primary Key)
- user_id (Foreign Key → users_customuser)
- date_ordered
- complete (Boolean)
- transaction_id

#### Table: `Radhirra_orderitem`
- id (Primary Key)
- order_id (Foreign Key → Radhirra_order)
- product_id (Foreign Key → Radhirra_product)
- quantity
- date_added

#### Table: `Radhirra_shippingaddress`
- id (Primary Key)
- user_id (Foreign Key → users_customuser)
- order_id (Foreign Key → Radhirra_order)
- address
- city
- state
- zipcode
- date_added

---

### 4. CART MANAGEMENT

#### Table: `Radhirra_cart`
- id (Primary Key)
- user_id (Foreign Key → users_customuser, nullable)
- session_key (For guest users)
- created_at

#### Table: `Radhirra_cartitem`
- id (Primary Key)
- cart_id (Foreign Key → Radhirra_cart)
- product_id (Foreign Key → Radhirra_product)
- quantity
- size (XS/S/M/L/XL/XXL)
- sleeve (sleeveless/short/3/4)

---

### 5. REVIEWS MANAGEMENT

#### Table: `Radhirra_review`
- id (Primary Key)
- product_id (Foreign Key → Radhirra_product)
- user_id (Foreign Key → users_customuser)
- rating (1-5)
- comment (Text)
- created_at
- Unique constraint: (product_id, user_id)

---

## ADMIN DASHBOARD FEATURES

### 1. DASHBOARD HOME
- Total Sales (₹)
- Total Orders
- Total Products
- Total Customers
- Recent Orders (Last 10)
- Low Stock Alerts
- Revenue Chart (Monthly)

### 2. PRODUCT MANAGEMENT
**CRUD Operations:**
- Create Product
  - Name, SKU, Category
  - Regular Price, Sale Price
  - Description, Specifications
  - Size, Sleeve, Material
  - Upload Multiple Images (mark one as main)
  - Toggle: is_featured, is_new_arrival, is_best_seller
  
- List Products
  - Search by name/SKU
  - Filter by category
  - Sort by price/date
  - Bulk actions (delete, feature, unfeatured)
  
- Edit Product
- Delete Product
- Manage Product Images

### 3. CATEGORY MANAGEMENT
- Create Category
- List Categories
- Edit Category
- Delete Category (if no products)

### 4. ORDER MANAGEMENT
- List All Orders
  - Filter by status (complete/pending)
  - Filter by date range
  - Search by transaction_id/user
  
- View Order Details
  - Customer info
  - Order items
  - Shipping address
  - Total amount
  
- Update Order Status
- Print Invoice

### 5. CUSTOMER MANAGEMENT
- List All Customers
  - Search by email/name
  - View customer details
  - View order history
  
- View Customer Profile
  - Personal info
  - Order history
  - Total spent
  
- Deactivate/Activate User

### 6. REVIEWS MANAGEMENT
- List All Reviews
  - Filter by rating
  - Filter by product
  - Search by user
  
- Approve/Reject Reviews
- Delete Reviews

### 7. REPORTS & ANALYTICS
- Sales Report
  - Daily/Weekly/Monthly/Yearly
  - Revenue trends
  
- Product Performance
  - Best selling products
  - Low performing products
  
- Customer Analytics
  - New customers
  - Repeat customers
  - Customer lifetime value

### 8. SETTINGS
- Site Settings
- Payment Gateway Config
- Shipping Settings
- Email Templates

---

## API ENDPOINTS NEEDED

### Authentication
- POST /api/admin/login
- POST /api/admin/logout

### Products
- GET /api/admin/products (list with pagination)
- POST /api/admin/products (create)
- GET /api/admin/products/{id} (detail)
- PUT /api/admin/products/{id} (update)
- DELETE /api/admin/products/{id}
- POST /api/admin/products/{id}/images (upload)

### Categories
- GET /api/admin/categories
- POST /api/admin/categories
- PUT /api/admin/categories/{id}
- DELETE /api/admin/categories/{id}

### Orders
- GET /api/admin/orders
- GET /api/admin/orders/{id}
- PUT /api/admin/orders/{id}/status

### Customers
- GET /api/admin/customers
- GET /api/admin/customers/{id}
- PUT /api/admin/customers/{id}/status

### Reviews
- GET /api/admin/reviews
- DELETE /api/admin/reviews/{id}

### Dashboard Stats
- GET /api/admin/stats/overview
- GET /api/admin/stats/sales
- GET /api/admin/stats/products

---

## CALCULATED FIELDS (Computed at Runtime)

### Product
- discount_percentage = ((regular_price - sale_price) / regular_price) * 100
- main_image = images.filter(is_main=True).first()

### Order
- get_cart_total = sum(orderitem.get_total for all items)
- get_cart_items = sum(orderitem.quantity for all items)

### OrderItem
- get_total = (sale_price or regular_price) * quantity

### CartItem
- get_total = (sale_price or regular_price) * quantity

---

## PERMISSIONS & ROLES

### Superuser (is_superuser=True)
- Full access to everything

### Staff (is_staff=True)
- Product management
- Order management
- Customer view only
- Cannot delete users

### Regular User (is_staff=False)
- No admin access

---

## IMPORTANT NOTES

1. **Authentication**: Use email for login (not username)
2. **Images**: All images stored in Cloudinary
3. **Currency**: Indian Rupees (₹)
4. **Timezone**: UTC
5. **Database**: PostgreSQL on Supabase
6. **Session**: Cache-based sessions

---

## SAMPLE QUERIES

### Get Featured Products
```sql
SELECT * FROM Radhirra_product WHERE is_featured = TRUE LIMIT 8;
```

### Get Order with Items
```sql
SELECT o.*, oi.*, p.name, p.regular_price, p.sale_price
FROM Radhirra_order o
JOIN Radhirra_orderitem oi ON o.id = oi.order_id
JOIN Radhirra_product p ON oi.product_id = p.id
WHERE o.id = ?;
```

### Get Customer Orders
```sql
SELECT * FROM Radhirra_order 
WHERE user_id = ? 
ORDER BY date_ordered DESC;
```

### Get Product Reviews
```sql
SELECT r.*, u.username, u.email
FROM Radhirra_review r
JOIN users_customuser u ON r.user_id = u.id
WHERE r.product_id = ?
ORDER BY r.created_at DESC;
```

### Sales Report (Monthly)
```sql
SELECT 
  DATE_TRUNC('month', date_ordered) as month,
  COUNT(*) as total_orders,
  SUM(
    (SELECT SUM(
      CASE 
        WHEN p.sale_price IS NOT NULL THEN p.sale_price * oi.quantity
        ELSE p.regular_price * oi.quantity
      END
    )
    FROM Radhirra_orderitem oi
    JOIN Radhirra_product p ON oi.product_id = p.id
    WHERE oi.order_id = o.id)
  ) as total_revenue
FROM Radhirra_order o
WHERE complete = TRUE
GROUP BY month
ORDER BY month DESC;
```
