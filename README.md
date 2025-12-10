# Warm Lead Sourcer

**Turn Social Engagement Into Warm Leads — Instantly**

Extract and enrich engagement data from LinkedIn posts to identify and qualify warm leads with proven interest in your content.

---

## 📖 Table of Contents

- [Overview](#overview)
- [How the Scraper Works](#how-the-scraper-works)
- [Quick Start](#quick-start)
- [Operating the Scraper](#operating-the-scraper)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Warm Lead Sourcer automates the process of:
1. **Extracting** comments and reactions from LinkedIn posts
2. **Enriching** user profiles with education, experience, and contact data
3. **Scoring** leads based on relevance and data completeness
4. **Exporting** qualified leads as CSV/XLSX files

---

## 🔄 How the Scraper Works

### **Step-by-Step Process:**

#### **1. Post Submission**
- User submits a LinkedIn post URL via frontend (`/input-url`)
- URL is validated and saved to MongoDB with status `pending`
- Post URN (activity ID) is extracted: `7402045266020794369`

#### **2. Post Processing**
```
POST /api/posts/:postId/process
```
- **Status**: `pending` → `processing`
- Calls LinkedIn RapidAPI to extract:
  - Post content and author info
  - Metrics (likes, comments, shares count)

#### **3. Engagement Extraction**
```
GET https://linkdapi-best-unofficial-linkedin-api.p.rapidapi.com/api/v1/posts/comments?urn={postUrn}
```
- Fetches all **commenters** from the post
- Each commenter provides:
  - Name, URN, profile URL, headline
- **Parallel processing**: All engagements processed simultaneously

#### **4. Profile Enrichment**
For each commenter/reactor:
```
GET /api/v1/profile/education?urn={userUrn}
GET /api/v1/profile/experience?urn={userUrn}
```
- Fetches detailed profile data:
  - **Education**: University, degree, field of study
  - **Experience**: Company, role, duration
  - **Location**: City, country

#### **5. Lead Scoring**
```typescript
calculateMatchScore(profile):
  Base: 10 points
  + 15 if headline exists
  + 30 if education exists
  + 10 if degree specified
  + 25 if experience exists
  + 10 if country exists
  + 10 if city exists
  = Max 100 points
```

#### **6. Email Generation**
```typescript
generateEmailGuess(profile):
  firstName.lastName@universityDomain
  Example: john.doe@stanford.edu
```
- Maps universities to email domains
- Only generates if university is in database

#### **7. Data Storage**
- Each lead saved to MongoDB `leads` collection
- Deduplicated by URN per post
- Status updated: `processing` → `completed`

#### **8. Export**
```
GET /api/leads/export?postId={postId}&format=csv
```
- Filters leads by criteria (score, location, etc.)
- Generates CSV/XLSX with all lead data
- Downloads instantly

---

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ and npm
- MongoDB running locally or connection URI
- RapidAPI account with LinkdAPI subscription
- LinkedIn post URLs to test

### **1. Clone Repository**

```bash
git clone https://github.com/DirectEd-Development/Warm-Lead-Sourcer.git
cd Warm-Lead-Sourcer
```

### **2. Install All Dependencies**

```bash
npm install
```

This installs dependencies for both frontend and backend.

### **3. Environment Setup**

Create `.env` file in `backend/` directory:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/warm-lead-sourcer

# RapidAPI LinkedIn
RAPIDAPI_KEY=your-rapidapi-key-here
RAPIDAPI_HOST=linkdapi-best-unofficial-linkedin-api.p.rapidapi.com

# JWT Authentication
JWT_SECRET=your-super-secret-jwt-key

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### **4. Start Development Servers**

**Option A: Start All Services**
```bash
npm run dev
```

**Option B: Start Individually**
```bash
# Terminal 1 - Backend
cd backend
npm run start:dev

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### **5. Access Applications**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **API Docs**: http://localhost:3001/api

---

## 🎮 Operating the Scraper

### **Method 1: Via Frontend UI**

1. **Navigate to Input Page**
   ```
   http://localhost:3000/input-url
   ```

2. **Paste LinkedIn Post URL**
   ```
   https://www.linkedin.com/posts/username_activity-.......
   ```

3. **Click "START EXTRACTION"**
   - Status will show: Validating → Reading interactions → Collecting profiles → Enriching data

4. **View Results**
   - Leads displayed in table
   - Filter by score, location, university
   - Export to CSV/XLSX

### **Method 2: Via API Directly**

#### **Step 1: Create Post Entry**
```bash
curl -X POST http://localhost:3001/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.linkedin.com/posts/username_activity-7402045266020794369-Hb47",
    "platform": "linkedin"
  }'
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "url": "https://www.linkedin.com/posts/...",
  "status": "pending"
}
```

#### **Step 2: Process the Post**
```bash
curl -X POST http://localhost:3001/api/posts/507f1f77bcf86cd799439011/process
```

**Response:**
```json
{
  "message": "Post processing started",
  "postId": "507f1f77bcf86cd799439011"
}
```

#### **Step 3: Check Processing Status**
```bash
curl http://localhost:3001/api/posts/507f1f77bcf86cd799439011
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "status": "completed",
  "totalEngagements": 45,
  "processedEngagements": 42,
  "processedAt": "2025-12-08T10:30:00Z"
}
```

#### **Step 4: Get Leads**
```bash
curl "http://localhost:3001/api/leads?postId=507f1f77bcf86cd799439011&minScore=50"
```

**Response:**
```json
{
  "leads": [
    {
      "name": "John Doe",
      "headline": "Data Scientist at Google",
      "education": [{
        "institution": "Stanford University",
        "degree": "MS Computer Science"
      }],
      "matchScore": 85,
      "guessedEmail": "john.doe@stanford.edu"
    }
  ],
  "total": 42
}
```

#### **Step 5: Export Leads**
```bash
curl "http://localhost:3001/api/leads/export?postId=507f1f77bcf86cd799439011&format=csv" \
  --output leads.csv
```

### **Method 3: Batch Processing**

Create `batch.json`:
```json
{
  "posts": [
    "https://www.linkedin.com/posts/user1_activity-123...",
    "https://www.linkedin.com/posts/user2_activity-456..."
  ]
}
```

Process multiple posts:
```bash
curl -X POST http://localhost:3001/api/posts/batch \
  -H "Content-Type: application/json" \
  -d @batch.json
```

---

---

## 🏗️ Architecture

### **System Flow**
```
User Input (LinkedIn URL)
    ↓
Frontend (Next.js)
    ↓
Backend API (NestJS)
    ↓
┌───────────────────────────────┐
│  Scraping Service             │
│  ├─ LinkedIn Provider         │
│  ├─ Post Extraction           │
│  ├─ Engagement Extraction     │
│  └─ Profile Enrichment        │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│  RapidAPI         │
│  ├─ /posts/comments           │
│  ├─ /profile/education        │
│  └─ /profile/experience       │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│  Lead Processing              │
│  ├─ Match Scoring             │
│  ├─ Email Guessing            │
│  └─ Deduplication             │
└───────────────────────────────┘
    ↓
MongoDB (leads collection)
    ↓
Export Service (CSV/XLSX)
```

### **Directory Structure**
```
├── backend/              # NestJS API server
│   ├── src/modules/
│   │   ├── auth/        # JWT + Google OAuth
│   │   ├── users/       # User management
│   │   ├── posts/       # Post CRUD operations
│   │   ├── scraping/    # LinkedIn scraping logic
│   │   │   ├── scraping.service.ts       # Main orchestration
│   │   │   └── providers/
│   │   │       └── linkedin.provider.ts  # RapidAPI integration
│   │   ├── leads/       # Lead filtering & management
│   │   └── export/      # CSV/XLSX generation
│   └── test/            # Unit & integration tests
├── frontend/            # Next.js web application
│   ├── app/
│   │   ├── page.tsx            # Landing page
│   │   ├── input-url/          # URL input page
│   │   ├── signup/             # User registration
│   │   └── login/              # User login
│   └── components/      # Reusable UI components
└── genai_service/       # Python AI service 
    |-api
    |-config/
    |-core
    
    ```

---

## ⚙️ Configuration

### **Required Environment Variables**

**Backend (`backend/.env`):**
```env
# Database
MONGODB_URI=mongodb://localhost:27017/warm-lead-sourcer

# RapidAPI Configuration
RAPIDAPI_KEY=your rapid api key
RAPIDAPI_HOST=your rapid api host

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-this

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret

# Server Configuration
PORT=3001
NODE_ENV=development
```

**Frontend (`frontend/.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### **Rate Limits & Quotas**

| Resource | Limit | Notes |
|----------|-------|-------|
| **RapidAPI Free Tier** | 100 requests/month | Upgrade to Pro for 10,000/month |
| **Comments per Post** | ~500 max | API limitation |
| **Parallel Requests** | 5 concurrent | To avoid rate limiting |
| **Profile Enrichment** | 2 sec/profile | Average response time |
| **Processing Speed** | 3-5 profiles/min | With free tier limits |
| **MongoDB Storage** | Unlimited | Local database |

---

## 📡 API Endpoints

### **Posts**
```
POST   /api/posts                    Create new post entry
GET    /api/posts/:id                Get post details
POST   /api/posts/:id/process        Start processing
DELETE /api/posts/:id                Delete post
POST   /api/posts/batch              Batch create posts
```

### **Leads**
```
GET    /api/leads                    Get all leads (with filters)
GET    /api/leads/:id                Get lead by ID
GET    /api/leads/export             Export leads to CSV/XLSX
DELETE /api/leads/:id                Delete lead
```

**Query Parameters for `/api/leads`:**
- `postId` - Filter by post ID
- `minScore` - Minimum match score (0-100)
- `maxScore` - Maximum match score
- `country` - Filter by country
- `city` - Filter by city
- `university` - Filter by university name
- `company` - Filter by current company

### **Authentication**
```
POST   /api/auth/register            Create new user account
POST   /api/auth/login               Login with email/password
POST   /api/auth/google              Google OAuth login
GET    /api/auth/me                  Get current user info
```

---

## 🧪 Testing

### **Unit Tests**
```bash
cd backend
npm run test
```

### **Test Coverage**
```bash
npm run test:cov
```

### **Integration Tests**
```bash
npm run test:e2e
```

### **Manual API Testing**

Use the example LinkedIn post:
```
https://www.linkedin.com/posts/munashe-masomeke-803475217_dataabrscience-dataabranalytics-activity-7402045266020794369-Hb47
```

Test with Postman or curl following the [Operating the Scraper](#operating-the-scraper) section.

---

## 🐛 Troubleshooting

### **Problem: RapidAPI returns "URN not found"**
**Solution:** 
- Verify the post URL is public and accessible
- Extract the activity ID correctly (e.g., `7402045266020794369`)
- Check your RapidAPI subscription is active

### **Problem: No leads created after processing**
**Solution:**
- Check if the post has any comments
- Verify RapidAPI key has remaining quota
- Check backend logs for API errors: `npm run start:dev`

### **Problem: "Profile data not found"**
**Solution:**
- Some profiles may be private or restricted
- The scraper continues with available data
- Check `matchScore` - leads with lower scores have less data

### **Problem: MongoDB connection failed**
**Solution:**


# Or use MongoDB Atlas cloud connection:
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/warm-lead-sourcer
```

### **Problem: Email guessing not working**
**Solution:**
- Add university domains to the mapping in `scraping.service.ts`:
```typescript
const domains: Record<string, string> = {
  'your university': 'youruniversity.edu',
  // Add more mappings
};
```

### **Problem: Rate limit exceeded**
**Solution:**
- Upgrade RapidAPI plan
- Process posts in smaller batches
- Add delays between requests

---

### Full Test Suite
```bash
npm run test:all         
npm run test:coverage    
```

### Manual Testing
```bash
npm run test:backend      
```

## 📋 Features Implemented

### ✅ Core Functionality
- **LinkedIn Post Processing** - Extract post content and metrics
- **Engagement Extraction** - Get comments and reactions from posts
- **Profile Enrichment** - Fetch education, experience, and skills data
- **Lead Generation** - Create qualified leads with match scoring
- **Email Guessing** - Generate university-based email addresses
- **Filtering System** - Filter leads by location, university, role
- **User Authentication** - JWT-based auth with Google OAuth

### ✅ Technical Implementation
- **Modular Architecture** - Clean separation of concerns
- **TypeScript** - Full type safety throughout
- **Test Coverage** - 40%+ unit test coverage
- **Error Handling** - Comprehensive error management
- **Rate Limiting** - API request throttling
- **Data Validation** - Input validation with class-validator

## 🏗️ Architecture

```
├── backend/              # NestJS API server
│   ├── src/modules/
│   │   ├── auth/        # Authentication & authorization
│   │   ├── users/       # User management
│   │   ├── posts/       # Post processing
│   │   ├── scraping/    # LinkedIn API integration
│   │   ├── leads/       # Lead management & filtering
│   │   └── export/      # CSV/XLSX export (ready)
│   └── test/            # Unit & integration tests
├── frontend/            # Next.js web application
├── genai_service/       # Python AI service (future)
└── docs/               # Documentation
```

## 🔧 Configuration

### Required Environment Variables

**Backend (.env):**
```env
MONGODB_URI=mongodb://localhost:27017/warm-lead-sourcer
RAPIDAPI_KEY=your-rapidapi-key
JWT_SECRET=your-jwt-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 📊 API Endpoints

### Authentication
- `POST /users/register` - User registration
- `POST /users/login` - User login
- `GET /auth/google` - Google OAuth login

### Core Features
- `POST /posts` - Submit LinkedIn URL for processing
- `GET /posts` - List user's posts
- `GET /posts/:id` - Get post details
- `GET /leads/post/:postId` - Get generated leads
- `GET /leads/post/:postId/stats` - Get lead statistics

### Filtering
- `GET /leads/post/:postId?country=US&university=Stanford&role=Engineer`

## 🧪 Testing Guide

### 1. Unit Test
```bash
cd backend
npm test               
npm run test:cov        
```

**Expected Results:**
- ✅ 20+ tests passing
- ✅ 40%+ code coverage
- ✅ All core services tested

### 2. Integration Test 
```bash
npm run test:integration
```

**Tests:**
- ✅ LinkedIn API connectivity
- ✅ Post data extraction
- ✅ Profile enrichment
- ✅ Lead generation pipeline
- ✅ Email generation

### 3. Manual API Testing

**Sample Request:**
```bash
curl -X POST http://localhost:5000/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"url": "https://www.linkedin.com/feed/update/urn:li:activity:......"}'
```

## 📈 Performance

### Benchmarks
- **Post Processing**: 2-5 seconds
- **Profile Enrichment**: 2 seconds per profile
- **Lead Generation**: 20-30 seconds for 5 leads
- **API Response**: <500ms average

### Rate Limits
- **RapidAPI Free**: 100 requests/month
- **Processing Speed**: 3-5 profiles/minute
- **Recommended Batch**: 5-10 leads per test

## 🔍 Troubleshooting

### Common Issues

**Database Connection Failed:**
```bash

npm run test:integration
```

**RapidAPI Rate Limit:**
```bash

npm run test:backend
```

**Environment Variables Missing:**
```bash

cp backend/.env.example backend/.env
```

## 📝 Development Workflow

### Adding New Features
1. Write unit tests first
2. Implement feature
3. Run integration tests
4. Update documentation

### Code Quality
- TypeScript strict mode
- ESLint + Prettier
- 40%+ test coverage required
- All tests must pass

## 🚀 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] All tests passing
- [ ] Build successful
- [ ] Rate limits configured

### Build Commands
```bash
npm run build:all     
npm run test:all        
```


## 🎯 Success Criteria

### Minimum Viable Product
- [x] LinkedIn URL processing
- [x] Engagement extraction
- [x] Profile enrichment
- [x] Lead generation with scoring
- [x] Basic filtering
- [x] User authentication
- [x] 40%+ test coverage

