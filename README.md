# Take-Home Technical Assessment

## Overview
Build a multi-tenant task management API with Django. This assessment evaluates your Django expertise, database design skills, and ability to implement basic multi-tenancy patterns.

- Time Allocation: 4-6 hours over 2-3 days
- Compensation: TBD

## Technical Requirements

### Core Django Application

Build a Django REST API with multi-tenant task management:

#### Multi-tenancy Requirements:
    • Support multiple organizations (tenants) in a single database
    • Each user belongs to exactly one organization
    • Users can only see their organization's data
    • Organization context determined by authenticated user
    • Proper data isolation between organizations

#### API Endpoints:
    • POST /api/v1/auth/login - User authentication
    • GET /api/v1/tasks/ - List current user's organization tasks, considering their deadline and priority, with cursor-based pagination
    • POST /api/v1/tasks/ - Create task in user's organization
    • PUT /api/v1/tasks/{id}/ - Update task (if belongs to user's org)
    • DELETE /api/v1/tasks/{id}/ - Delete task (if belongs to user's org)
    • GET /api/v1/users/ - List users in current user's organization
    • POST /api/v1/users/ - Add user to current user's organization

Questions:
    
    * what with first user in organization? only admin can create organization and first user?
    * maybe better is use task_id instead of id in task endpoints?
    * may we use default url: /api/v1/token/pair instead of /api/v1/auth/login ?

#### Data Models:
    • Organization: name, created_at
    • User: Standard Django user + organization foreign key (many-to-one relationship)
    • Task: title, description, completed, assigned_to, organization, created_at,deadline_datetime_with_tz,priority
    • Users are assigned to exactly one organization. One organization can have multiple users.

#### Authentication & Authorization:
    • JWT-based authentication
    • Organization context automatically determined from authenticated user
    • Users can only access their own organization's data
    • Middleware to set current organization context based on authenticated user
    • Proper permission classes for organization-level access control

### Testing Requirements

#### Comprehensive unit tests required:
    • Model tests (validation, relationships, constraints)
    • API endpoint tests using Django Ninja's testing patterns
    • Multi-tenancy tests (data isolation between organizations)
    • Authentication tests (JWT token validation, unauthorized access)
    • Schema validation tests (request/response schemas)
    • Edge case testing (invalid data, unauthorized access attempts)

#### Test coverage expectations:
    • Minimum 80% code coverage
    • Test all API endpoints with different user contexts
    • Test Django Ninja schema validation
    • Include negative test cases (unauthorized access, invalid data)

#### Database & Performance
    • Database: SQLite for assessment (simpler deployment, no external dependencies)
    • Data isolation: Ensure queries are automatically filtered by organization
    • Migrations: Proper Django migrations for all model changes

__Production Readiness Note__: Be prepared to discuss how you would adapt this SQLite implementation for production PostgreSQL, including scaling considerations, indexing strategies, and performance optimizations.

### Deployment
    • Deploy to any platform that supports SQLite (AWS FreeTier, Heroku, Railway, DigitalOcean, etc.)
    • Include environment configuration
    • Database migrations should work automatically with SQLite
    • Provide working API URL for testing

__Follow-up Discussion__: Be prepared to explain how you would deploy this to production with PostgreSQL, including infrastructure considerations, scaling strategies, and DevOps practices.

### Multi-Tenancy Implementation Details

#### Required Patterns

Implement __one__ of these multi-tenancy approaches:

##### Option A: Row-Level Security (Preferred)
    • Filter all queries by the authenticated user's organization automatically

##### Option B: Schema-per-Tenant
    • Dynamic database routing based on user's organization

#### Data Isolation Requirements
    • Users in Organization A cannot see Organization B's tasks
    • API endpoints must automatically filter data by authenticated user's organization
    • Database queries must include organization filters automatically
    • Admin interface should respect multi-tenancy 

#### Performance Considerations
    • Efficient database indexes for multi-tenant queries
    • Minimize database round trips
    • Proper use of Django ORM optimization techniques
    • Consider query performance with 1000+ organizations and 100k+ tasks

## Deliverables

### 1. Working API
    • Deployed API with all endpoints functional
    • Provide base URL for API testing
    • Include test credentials for multiple organizations
    • API should return proper JSON responses with appropriate HTTP status codes

### 2. Source Code
    • GitHub repository with clear commit history
    • Clean Django project structure
    • Environment configuration files (.env.example)
    • Dependencies documented
    • README.md  with local development setup instructions
### 3. Test Suite
    • Comprehensive unit tests using Django's TestCase
    • Test runner should pass all tests: python manage.py test or pytest
    • Include test coverage report
    • Tests should demonstrate multi-tenancy works correctly

## Evaluation Criteria

### Must-Haves (Automatic rejection if missing)
- [ ] API is deployed and all endpoints return proper responses
- [ ] Multi-tenancy works correctly (complete data isolation between organizations)
- [ ] Unit tests pass and demonstrate multi-tenancy functionality
- [ ] JWT authentication works properly with Django Ninja
- [ ] Users cannot access other organizations' data
- [ ] Code follows Django and Ninja best practices
- [ ] Proper use of Ninja schemas for request/response validation

### Django/Ninja Expertise Indicators
    • Proper use of Django Ninja schemas for request/response validation
    • Efficient database queries and Django ORM usage
    • Custom authentication and permission handling with Ninja
    • Appropriate use of Django's authentication system
    • Clean model design with proper foreign key relationships
    • Understanding of Django Ninja's automatic OpenAPI documentation
    • Proper HTTP status codes and error responses

### Testing Excellence
    • Comprehensive test coverage (80%+ required)
    • Tests for all API endpoints and edge cases
    • Multi-tenancy isolation tests
    • Proper use of Django's testing framework with Ninja endpoints
    • Schema validation testing
    • Meaningful test assertions and scenarios

### Bonus Points
    • Advanced Django Ninja features (pagination, filtering, custom schemas)
    • Custom Django management commands
    • Database query optimization and analysis
    • API documentation customization
    • Advanced authentication/permission patterns
    • Performance testing or benchmarking

## Submission Guidelines
  1. __Repository:__ Send GitHub repository link with public access
  2. __Live Demo:__ Include application URL and test credentials for multiple organizations
  3. __Multi-Tenancy Explanation:__ Brief description of your approach and key implementation decisions
  4. __Test Organizations:__ Provide credentials for at least 2 test organizations with sample data

## Important Notes
  • Django Focus: 80% of evaluation is on Django backend implementation
  • Multi-Tenancy is Critical: This is the core challenge - must be implemented correctly
  • Working Solution Required: Partially working applications will not be considered
  • Data Isolation: Any cross-organization data leaks result in automatic rejection
  • Ask Questions: If any requirements are unclear, reach out immediately
  • Time Tracking: Please note actual time spent in your README

## Testing & Validation

### API Testing

We will test your API using curl/Postman with these scenarios:

#### Basic functionality:

```bash
# Register users in different organizations
POST /api/v1/auth/register
# Login and get JWT tokens
POST /api/v1/auth/login
# Create tasks for each user
POST /api/v1/tasks/
# Verify data isolation and prioritization implementation
GET /api/v1/tasks/ (with different user tokens)
```
##### Multi-tenancy validation:
    1. Create tasks as User A (Organization A)
    2. Login as User B (Organization B)
    3. Verify User B cannot see Organization A's tasks
    4. Test all CRUD operations with cross-organization access attempts
    5. Verify proper HTTP status codes (403 Forbidden for unauthorized access)

##### Unit Test Validation
    • Your test suite must pass: python manage.py test
    • Tests must demonstrate multi-tenancy works correctly
    • Include test coverage report
    • Tests should cover both positive and negative scenarios

__Your API must pass all validation tests to qualify for payment.__

## Technical Support

For questions about multi-tenancy requirements or technical issues, contact: 

    * Marcin Galczynski
    * Tomasz Mackowski

Deadline: [X] days from receipt



# local setup

```bash
git clone git@github.com:arturro/django-ninja-prv.git
# or
gh repo clone arturro/django-ninja-prv
cd django-ninja-prv
```

### docker compose setup

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
```

### local setup without docker
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install --upgrade pip
pip install -r requirements/requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py test
./manage.py runserver 0.0.0.0:8000
```
   * open http://127.0.0.1:8000/admin/tenant/user/ create user with organization
   * open http://127.0.0.1:8000/api/v1/docs#/ Ninja automatic docs
    


http://13.60.68.249:8000/api/v1/docs#/token/token_obtain_pair


## private

```bash
cd app
coverage run manage.py test
coverage report
coverage html
```

## TODO

- [ ] fix all TODOs in the code
- [ ] add deployment instructions to README
- [ ] add user registration endpoint?
- [ ] add pagination to GET /api/v1/tasks/
- [ ] add filtering to GET /api/v1/tasks/ (by deadline and priority)
- [ ] add sorting to GET /api/v1/tasks/ (by deadline and priority)
- [ ] add tests for pagination, filtering and sorting
- [ ] add more tests for edge cases
- [ ] add multi stage Dockerfile
- 
- [ ] add CI/CD pipeline (GitHub Actions)
- [ ] add linting (flake8, black)
- [ ] add pre-commit hooks
- [ ] add logging
- [ ] add monitoring (Sentry)
- [ ] add rate limiting
- [ ] add caching (Redis)
- [ ] add Swagger/OpenAPI documentation
- [ ] add Postman collection
- [ ] add environment variables management (django-environ)
- [ ] add user roles (admin, user)
- [ ] add password reset functionality
- [ ] add more documentation
- [ ] add uv installation to requirements.txt
- [ ] add .env.example file
- [ ] add database indexing for better performance
- [ ] local deployment from uv installation

