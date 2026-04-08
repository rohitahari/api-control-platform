# 🔐 SaaS API Key & Rate Limiting Platform

A production-style backend system built with FastAPI that provides:

* API key authentication
* Redis-based rate limiting
* Usage tracking
* Plan-based access control (Free / Pro / Enterprise)

---

## 🚀 Features

* 🔑 API Key Generation & Validation
* ⚡ Rate Limiting using Redis
* 📊 Usage Tracking (requests count, last used)
* 🧠 Plan-based limits (Free / Pro / Enterprise)
* 🔐 JWT Authentication system
* 🧩 Plug-and-play dependency for any API

---

## 🛠 Tech Stack

* FastAPI
* PostgreSQL
* Redis
* SQLAlchemy

---

## 📦 Project Structure

```
app/
  core/
  db/
  models/
  routes/
  services/
```

---

## ⚙️ Setup

### 1. Clone repo

```
git clone https://github.com/your-username/saas-api-platform.git
cd saas-api-platform
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Setup environment variables

Create `.env` from `.env.example`

### 5. Run server

```
uvicorn app.main:app --reload --port 8001
```

---

## 🔑 Example Usage

### Generate API Key (after login)

### Test API Key

```
curl -H "X-API-Key: YOUR_API_KEY" \
http://127.0.0.1:8001/api/v1/api-keys/test-api-key
```

---

## 📊 Rate Limiting

* Free → 10 requests/min
* Pro → 100 requests/min
* Enterprise → 1000 requests/min

---

## 🧠 Use Cases

* Protect your API from abuse
* Add API key authentication to your SaaS
* Track usage per client
* Build paid API services

---

## 🚀 Future Improvements

* Dashboard UI
* Billing integration
* Analytics
* Multi-project support

---

## 🤝 Contributing

Pull requests welcome.

---

# 🔐 SaaS API Key & Rate Limiting Platform

A production-style backend system built with FastAPI that provides:

* API key authentication
* Redis-based rate limiting
* Usage tracking
* Plan-based access control (Free / Pro / Enterprise)

---

## 🚀 Features

* 🔑 API Key Generation & Validation
* ⚡ Rate Limiting using Redis
* 📊 Usage Tracking (requests count, last used)
* 🧠 Plan-based limits (Free / Pro / Enterprise)
* 🔐 JWT Authentication system
* 🧩 Plug-and-play dependency for any API

---

## 🛠 Tech Stack

* FastAPI
* PostgreSQL
* Redis
* SQLAlchemy

---

## 📦 Project Structure

```
app/
  core/
  db/
  models/
  routes/
  services/
```

---

## ⚙️ Setup

### 1. Clone repo

```
git clone https://github.com/your-username/saas-api-platform.git
cd saas-api-platform
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Setup environment variables

Create `.env` from `.env.example`

### 5. Run server

```
uvicorn app.main:app --reload --port 8001
```

---

## 🔑 Example Usage

### Generate API Key (after login)

### Test API Key

```
curl -H "X-API-Key: YOUR_API_KEY" \
http://127.0.0.1:8001/api/v1/api-keys/test-api-key
```

---

## 📊 Rate Limiting

* Free → 10 requests/min
* Pro → 100 requests/min
* Enterprise → 1000 requests/min

---

## 🧠 Use Cases

* Protect your API from abuse
* Add API key authentication to your SaaS
* Track usage per client
* Build paid API services

---

## 🚀 Future Improvements

* Dashboard UI
* Billing integration
* Analytics
* Multi-project support

---

## 🤝 Contributing

Pull requests welcome.

---

## 📜 License

MIT

