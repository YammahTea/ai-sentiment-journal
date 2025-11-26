import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from Back.app import app, get_async_session
from Back.db import Base

# fake in-memory database for speed & safety
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create the test engine
engine = create_async_engine(
  TEST_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


""" --- The Database Session --- """
@pytest.fixture
async def session():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with TestingSessionLocal() as session:
    yield session

"""  --- The Client --- """
@pytest.fixture
async def client(session):
  # Overrides the dependency: "so it doesn't use the real DB, use the fake session"
  def override_get_db():
    yield session

  app.dependency_overrides[get_async_session] = override_get_db

  # Create the AsyncClient (The "Browser")
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


""" TEST cases """

@pytest.mark.asyncio
async def test_read_home(client): # check if the homepage is loaded
  response = await client.get("/")
  assert response.status_code == 200


@pytest.mark.asyncio
async def test_analyze_sentiment(client): # check if the ai sentiment works
  response = await client.post(
    "/journal",
    json={"text": "I am so happy today!"}
  )

  assert response.status_code == 200
  data = response.json()

  # Check that we got a Dictionary (Object), not a List
  assert "mood" in data
  assert "score" in data
  assert data["mood"] in ["Positive", "Very Positive"]


@pytest.mark.asyncio
async def test_database_persistence(client): # check if the message was saved in the db
  await client.post("/journal", json={"text": "Test message in the database"})

  response = await client.get("/messages")
  data = response.json()

  journals = data["Journals"]
  assert len(journals) > 0
  assert journals[-1]["message"] == "Test message in the database"
