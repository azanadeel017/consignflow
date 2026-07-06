# ConsignFlow Project Checklist

This checklist tracks the implementation of **ConsignFlow**, a modern consignment management system designed to streamline inventory ingestion, consignor agreements, sales tracking, and payouts.

## Phase 1: Project Setup & Database Design
- [ ] Initialize repository & project structure (Next.js / TypeScript / Tailwind CSS)
- [ ] Set up database schema & ORM (e.g., PostgreSQL with Prisma)
  - [ ] **Consignors**: ID, Name, Contact, Commission Rate (default 60/40), Status
  - [ ] **Inventory Items**: ID, Consignor ID, Title, Description, Category, Price, Status (`Draft`, `Active`, `Sold`, `Returned`), Payout Rate
  - [ ] **Payouts**: ID, Consignor ID, Amount, Payment Method, Status (`Pending`, `Paid`), Reference ID
- [ ] Configure ESLint, Prettier, and Husky Git hooks

## Phase 2: Core Backend Services & APIs
- [ ] Implement authentication & role-based access control (Admin vs. Consignor)
- [ ] Create CRUD endpoints for **Consignors**
- [ ] Create CRUD endpoints for **Inventory Items**
  - [ ] Implement pricing logic & auto-markdown rules (e.g., 20% off after 30 days)
- [ ] Implement **Sales & Intake processing** REST endpoints
- [ ] Implement payout calculation and ledger generation

## Phase 3: Administrative Dashboard (Frontend)
- [ ] Design administrative layout with a cohesive color scheme (deep indigo/slate dark-mode theme)
- [ ] Build **Consignor Management** panel (add/edit consignors, view agreements)
- [ ] Build **Inventory Intake** interface (fast barcode/SKU generation, photo upload placeholder, bulk entry)
- [ ] Build **Point of Sale (POS) / Sale Logger** screen to process purchases and record payouts
- [ ] Build **Payout Processing** console (generate ledger reports, mark payouts as cleared)

## Phase 4: Consignor Portal (Frontend)
- [ ] Design custom consignor dashboard layout
- [ ] Implement item tracking view (allow consignors to see which of their items are active, sold, or expired)
- [ ] Implement payout history & balance ledger interface

## Phase 5: Testing, Polish & Deployment
- [ ] Write unit tests for core accounting/commission logic
- [ ] Perform end-to-end user flow verification (Intake -> Sale -> Payout)
- [ ] Polish UI with micro-interactions, loading skeletons, and smooth page transitions
- [ ] Deploy to staging environment
