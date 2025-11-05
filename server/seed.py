from django.contrib.auth import get_user_model
from catalog.models import Book, Category

User = get_user_model()


def ensure_user(username: str, password: str, role: str, email: str, is_staff: bool = False, is_superuser: bool = False):
    if not User.objects.filter(username=username).exists():
        u = User(username=username, role=role, email=email)
        u.set_password(password)
        u.is_staff = is_staff or is_superuser
        u.is_superuser = is_superuser
        u.save()


def ensure_book(title: str, author: str, isbn: str, category_name: str, copies: int):
    category, _ = Category.objects.get_or_create(name=category_name)
    if not Book.objects.filter(isbn=isbn).exists():
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            copies_total=copies,
            copies_available=copies,
        )


def run():
    # Staff and members
    ensure_user("admin", "Admin#123", "ADMIN", "admin@uniben.edu", is_staff=True, is_superuser=True)
    ensure_user("harris.librarian", "Lib#12345", "LIBRARIAN", "harris.librarian@uniben.edu", is_staff=True)
    ensure_user("ade.librarian", "Lib#23456", "LIBRARIAN", "ade.owo@uniben.edu", is_staff=True)

    ensure_user("ug-student1", "Student#123", "MEMBER", "ug.student1@uniben.edu")
    ensure_user("ug-student2", "Student#234", "MEMBER", "ug.student2@uniben.edu")
    ensure_user("pg-student1", "Student#345", "MEMBER", "pg.student1@uniben.edu")

    # Categories and representative university texts (realistic ISBNs)
    ensure_book(
        title="Introduction to Algorithms",
        author="Thomas H. Cormen; Charles E. Leiserson; Ronald L. Rivest; Clifford Stein",
        isbn="9780262046305",
        category_name="Computer Science",
        copies=4,
    )
    ensure_book(
        title="Clean Code: A Handbook of Agile Software Craftsmanship",
        author="Robert C. Martin",
        isbn="9780132350884",
        category_name="Computer Science",
        copies=3,
    )
    ensure_book(
        title="Artificial Intelligence: A Modern Approach (4th Edition)",
        author="Stuart Russell; Peter Norvig",
        isbn="9780134610993",
        category_name="Computer Science",
        copies=2,
    )
    ensure_book(
        title="Operating System Concepts (10th Edition)",
        author="Abraham Silberschatz; Peter B. Galvin; Greg Gagne",
        isbn="9781119456339",
        category_name="Computer Science",
        copies=3,
    )
    ensure_book(
        title="Database System Concepts (7th Edition)",
        author="Abraham Silberschatz; Henry F. Korth; S. Sudarshan",
        isbn="9780078022159",
        category_name="Computer Science",
        copies=3,
    )
    ensure_book(
        title="Modern Control Engineering (5th Edition)",
        author="Katsuhiko Ogata",
        isbn="9780136156734",
        category_name="Engineering",
        copies=2,
    )
    ensure_book(
        title="Campbell Biology (12th Edition)",
        author="Lisa A. Urry; Michael L. Cain; Steven A. Wasserman; Peter V. Minorsky; Jane B. Reece",
        isbn="9780134093413",
        category_name="Sciences",
        copies=4,
    )
    ensure_book(
        title="Guyton and Hall Textbook of Medical Physiology (14th Edition)",
        author="John E. Hall",
        isbn="9780323597128",
        category_name="Medicine",
        copies=2,
    )
    ensure_book(
        title="Organizational Behavior (18th Edition)",
        author="Stephen P. Robbins; Timothy A. Judge",
        isbn="9780134729329",
        category_name="Business",
        copies=3,
    )
    ensure_book(
        title="A History of Nigeria",
        author="Toyin Falola; Matthew M. Heaton",
        isbn="9780521681575",
        category_name="Humanities",
        copies=2,
    )

    print("Seeding complete.")


if __name__ == "__main__":
    run()


