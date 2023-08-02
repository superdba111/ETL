Designing a class in Python involves several key considerations. Here are some steps you can follow:
(good video https://www.youtube.com/watch?v=lX9UQp2NwTk -0:54 Keep your classes small
8:43 Make your classes easy to use 
14:18 Use dependency injection
17:46 Make sure a class is actually needed
22:45 Use encapsulation)

### 1. Define the Class:
Every class should have a specific purpose within your program. You start by using the class keyword followed by the name of the class.

class Car:

### 2. Initialize the Class (Constructor):
You usually define an __init__() method in your class. This is a special method that is automatically called when an object of the class is created. It is used to initialize the attributes of the class.

class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

### 3. Define Class Methods:
Methods are functions that are defined inside a class. They represent the behaviors of the class objects
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start_engine(self):
        print(f"The {self.brand} {self.model}'s engine is starting.")

### 4. Define Class Attributes:
Class attributes are variables that are defined in the class. They represent the properties or characteristics of the class objects.
class Car:
    wheels = 4  # This is a class attribute

    def __init__(self, brand, model, year):
        self.brand = brand  # These are instance attributes
        self.model = model
        self.year = year

### 5. Error Handling:
It's also crucial to handle errors that may occur in your class methods. This can be done using try/except blocks.

### 6. Inheritance:
If your class shares methods or attributes with another class, you might consider using inheritance, which allows you to inherit methods and attributes from a parent class.

### 7. Documentation:
Each class should have a docstring at the beginning that provides a brief description of the class.

Remember that the main goal of using classes is to create more organized and modular code that is easy to read and debug. It's also important to follow good coding practices such as using clear and descriptive names for your classes, methods, and attributes.
