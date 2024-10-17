This is the start of a framework where MVC would be followed, separating different concerns, such as the frontend, database, and business logic.

Each concern would be a separate image/service allowing better scaling up and extending. For local development, the move from plain docker to compose is used. It allows easy migration to cloud services and K8s

The idea being all services are small, self-container, immutable, a part from the database. This has many advantages over big fat applications.


