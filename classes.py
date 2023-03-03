class Student:
    def __init__(self, id: int, name: str = "default", email: str = "default@gmail.com", phone: str = "050-1112222") -> None:
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self) -> str:
        return f'{self.name}, {self.email}, {self.phone}'


class Teacher:
    def __init__(self, id: int, name: str = "default", email: str = "default@gmail.com") -> None:
        self.id = id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f'{self.name}, {self.email}'


class Course:
    def __init__(self, id: int, name: str = "default", description: str = "default", teacher_id: int = 0) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.teacher_id = teacher_id

    def __str__(self) -> str:
        return f'{self.name},{self.description}'


class User:
    def __init__(self, id: int, email: str = "default", password: str = "12345678", role: str = "default") -> None:
        self.id = id
        self.email = email
        self.password = password
        self.role = role

    def __str__(self) -> str:
        return f'{self.email},{self.password},{self.role}'


class Grade:
    def __init__(self, name: str = "default", grade: int = 0) -> None:
        self.name = name
        self.grade = grade
        if self.grade is None:
            self.grade = 0

    def __repr__(self) -> str:
        return f'{self.name},{self.grade}'
