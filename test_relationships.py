from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.task import Task


db = SessionLocal()

try:
    # 1️⃣ Create User
    user = User(
        email="rohit@example.com",
        hashed_password="fakehashed",
        system_role="SUPERADMIN"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print("User created:", user.id, user.email)

    # 2️⃣ Create Project
    project = Project(
        name="SaaS Backend",
        description="Testing relationships"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    print("Project created:", project.id, project.name)

    # 3️⃣ Add Membership
    membership = ProjectMember(
        user_id=user.id,
        project_id=project.id,
        role="OWNER"
    )
    db.add(membership)
    db.commit()

    print("Membership created")

    # 4️⃣ Create Tasks
    task1 = Task(
        title="Design Models",
        description="Create ORM models",
        project_id=project.id,
        creator_id=user.id
    )

    task2 = Task(
        title="Test Relationships",
        description="Verify ORM navigation",
        project_id=project.id,
        creator_id=user.id
    )

    db.add_all([task1, task2])
    db.commit()

    print("Tasks created")

    # 5️⃣ Test Relationships

    print("\n--- Relationship Tests ---")

    db.refresh(project)

    print("Project Tasks:")
    for task in project.tasks:
        print("-", task.title)

    print("\nUser Memberships:")
    for m in user.memberships:
        print("-", m.project_id, m.role)

finally:
    db.close()
