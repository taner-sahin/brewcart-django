# ☕ BrewCart

BrewCart is a backend-focused Django specialty coffee e-commerce project built to simulate real-world backend systems using a scalable and repeatable architecture.

The project focuses heavily on advanced product filtering, queryset logic, search systems, user-based cart architecture, and professional Django backend workflows rather than frontend complexity.

---

# 🖼️ Project Preview

## 🏠 Home Page
Minimal specialty coffee storefront with dynamic navbar and featured products.

## 🔎 Advanced Search & Filtering
Search products by:
- keyword
- category
- minimum price
- maximum price
- stock availability
- ordering options

## ⭐ Review & Rating System
Users can:
- write reviews
- give 1–5 star ratings
- view average rating per product

## 🛒 Database-Based Cart System
Dynamic cart system fully powered by database logic.

## 📦 Checkout & Order Flow
Real-world order workflow with user-based order management.

---

# 🧠 About

This project is part of a structured Django backend development journey.

Each project in this series follows the same architecture while introducing one major backend feature.

🎯 Focus of this project:

Building advanced queryset, filtering, search, and rating systems using Django ORM and database-driven architecture.

---

# ⚙️ Core Features

## 🔐 Authentication
- User registration
- Login / Logout
- Protected checkout system
- User-based cart logic
- User-based order history

---

## 🛍 Product System
- Product listing
- Slug-based product detail pages
- Category filtering
- Dynamic category navbar
- Featured products section

---

## 🔎 Advanced Search & Filtering (Main Feature)

### Query Features
- Search by product name
- Search using request.GET
- Multi-filter support
- Dynamic queryset filtering
- Q object search logic

### Filter Features
- Category filtering
- Price min / max filtering
- In-stock filtering
- Ordering system

### Ordering Options
- Price low → high
- Price high → low
- Newest products
- Product name ordering

---

## ⭐ Review & Rating System

### User Features
- Add review
- Give 1–5 star rating
- Product review listing

### Backend Logic
- ForeignKey relationships
- related_name usage
- Avg() aggregation
- Count() aggregation
- Dynamic rating calculation

---

## 🛒 Database-Based Cart System
- Add products to cart
- Increase / decrease quantity
- Remove cart items
- User-specific cart storage
- Dynamic navbar cart count
- Database-driven architecture
- NOT session-based

---

## 📦 Order System
- Checkout workflow
- Order creation
- OrderItem snapshot logic
- Automatic cart cleanup
- My Orders page
- Order detail page
- Admin order management

---

# 🚀 Backend Highlights

- Advanced queryset filtering
- Dynamic search system
- Q object implementation
- request.GET architecture
- Aggregate functions
- Avg() and Count() usage
- Database-driven cart system
- Snapshot order logic
- Slug-based clean URLs
- User-based data isolation
- Dynamic navbar architecture
- Backend-first project structure

---

# 🔄 Business Flow

User registers
→ Logs in
→ Searches products
→ Filters products dynamically
→ Opens product detail page
→ Adds products to cart
→ Cart stored in database
→ Checkout process starts
→ Order is created
→ OrderItems generated
→ Cart cleared automatically
→ User tracks orders from My Orders page

---

# 🛠 Tech Stack

- Python
- Django
- SQLite
- Bootstrap

---

# 🧩 Project Structure

accounts → authentication system  
products → products, filtering & reviews  
cart → database-based cart system  
orders → checkout & order management  
templates → global templates  
static → CSS, JS, images  
media → uploaded product images  

---

# 📚 What I Learned

- Building advanced queryset systems
- Implementing dynamic product filtering
- Using request.GET professionally
- Using Q objects for search logic
- Working with aggregate functions
- Building review & rating systems
- Structuring scalable Django backends
- Creating database-driven cart architecture
- Managing user-based order workflows
- Building reusable backend architecture

---

# 📊 Status

🚧 Backend Development In Progress

### Completed Systems
- Authentication System
- Hero Banner
- Static Homepage
- Dynamic Navbar Structure
- AI-Generated Product Images
- GitHub Showcase Design

### Active Development
- Product Models
- Category System
- Filtering System
- Query Logic
- Cart Architecture
- Review System

---

# 🗺 Backend Journey Roadmap

Project 1 → SnapCart ✅  
Project 2 → OrderCore ✅  
Project 3 → StockFlow ✅  
Project 4 → CouponCart ✅  
Project 5 → VariShop ✅  
Project 6 → BrewCart 🚧  

---

# 👤 Author

Taner Sahin

GitHub:
https://github.com/taner-sahin