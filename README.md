# Warm Lead Sourcer

Extract and enrich engagement data from public social posts to generate warm leads.

## Getting Started

### 1. Clone Repository

```bash
git clone <repository-url>
cd Warm-Lead-Sourcer
```

### 2. Install All Dependencies

```bash
npm run install:all
```

### 3. Start Development Servers

```bash
npm run dev
```

### 4. Test Both Applications

- Frontend: http://localhost:3000
- Backend: http://localhost:3001

## Manual Setup (Alternative)

If you prefer to set up each service individually:

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### Backend (NestJS)

```bash
cd backend
npm install
npm run start:dev
```

## Architecture

- **Frontend**: Next.js + Tailwind CSS → Vercel
- **Backend**: NestJS → Render

## Environment Setup

Copy environment examples:
```bash
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env
```
