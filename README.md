# SaaS API Backend System

A production-structured backend system built with FastAPI.

This project demonstrates:

- Layered architecture (Router → Service → Permission → Model)
- RBAC + Attribute-based access control
- Structured error handling
- Audit logging
- Soft deletes
- JWT authentication
- Git discipline workflow

---

## 🏗 Architecture

app/
├── routes/          # API layer  
├── services/        # Business logic layer  
├── core/            # Security, permissions, config  
├── db/models/       # SQLAlchemy models  
├── schema/          # Pydantic schemas  
├── main.py          # App entry  

---

## 🔐 Permission System

- Project membership required
- Role-based validation
- Attribute validation
- Centralized `enforce_policy()` guard

---

## 📜 Audit Logging

Every critical action:
- create_project
- update_project
- delete_project

Is recorded in `audit_logs` table.

---

## ❗ Structured Errors

All API errors return:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "status": 400
  }
}
```

---

## 🚀 How to Run

```bash
uvicorn app.main:app --reload
```

---

## 🔧 Tech
