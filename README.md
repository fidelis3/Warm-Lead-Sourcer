# Warm Lead Sourcer

Extract and enrich engagement data from public social posts to generate warm leads.

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd Warm-Lead-Sourcer
```

### 2. Install All Dependencies

```bash
npm run install:all
```

### 3. Environment Setup

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Update the `.env` files with your configuration values.

### 4. Start Development Servers

```bash
npm run dev
```

### 5. Test Applications

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## 🧪 Testing

### Quick Integration Test (No Database Required)
```bash
npm run test:integration
```

### Full Test Suite
```bash
npm run test:all          # All tests
npm run test:coverage     # With coverage report
```

### Manual Testing
```bash
npm run test:backend      # Unit tests only
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

### 1. Unit Tests (Recommended First)
```bash
cd backend
npm test                 # Run all unit tests
npm run test:cov        # With coverage report
```

**Expected Results:**
- ✅ 20+ tests passing
- ✅ 40%+ code coverage
- ✅ All core services tested

### 2. Integration Test (No Database)
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
  -d '{"url": "https://www.linkedin.com/feed/update/urn:li:activity:7353638537595932672"}'
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
# Use integration test instead
npm run test:integration
```

**RapidAPI Rate Limit:**
```bash
# Check quota at rapidapi.com
# Use unit tests for development
npm run test:backend
```

**Environment Variables Missing:**
```bash
# Copy and update example files
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
npm run build:all       # Build both frontend and backend
npm run test:all        # Run all tests
```

## 📞 Support

### Getting Help
1. Check TESTING.md for detailed testing guide
2. Run unit tests to verify core functionality
3. Use integration test for API validation
4. Review error logs for specific issues

### Reporting Issues
Include:
- Test results output
- Environment configuration
- Error messages
- Steps to reproduce

## 🎯 Success Criteria

### Minimum Viable Product
- [x] LinkedIn URL processing
- [x] Engagement extraction
- [x] Profile enrichment
- [x] Lead generation with scoring
- [x] Basic filtering
- [x] User authentication
- [x] 40%+ test coverage

### Future Enhancements
- [ ] CSV/XLSX export
- [ ] Instagram integration
- [ ] Twitter integration
- [ ] Advanced filtering
- [ ] Email verification
- [ ] Bulk processing