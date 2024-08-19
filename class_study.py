"""
関連: EmployeeクラスはDepartmentクラスと関連しています。
Departmentは複数のEmployeeを持ちます。

集約: DepartmentクラスがEmployeeクラスを集約しています。
EmployeeはDepartmentに追加されますが、Departmentが削除
されてもEmployeeは削除されません。

コンポジション: ProjectクラスがTaskをコンポジション
しています。TaskはProjectが削除されると共に削除されます。

汎化（継承）: TemporaryEmployeeクラスはEmployeeクラスを
継承しています。

依存: Companyクラスは一時的にPrinterクラスを使用しています。

実現: FreelancerクラスはPayableインターフェースを実装し、
支払いメソッドを実現しています。
Payableは共通の動詞な気がする。支払い可能なものは支払いできる。
"""

class Employee:
    """クラス: Employee（社員）"""
    def __init__(self, name):
        self.name = name

    def work(self):
        print(f"{self.name} is working.")

class Department:
    """クラス: Department（部署）
    集約関係: Department（全体）とEmployee（部分）
    """
    def __init__(self, name):
        self.name = name
        self.employees = []  # 集約（複数のEmployeeを保持）

    def add_employee(self, employee):
        self.employees.append(employee)

    def show_employees(self):
        for employee in self.employees:
            print(f"Employee: {employee.name}")

class Project:
    """クラス: Project（プロジェクト）
    コンポジション関係: Project（全体）とTask（部分）
    """
    class Task:
        """ネストされたクラス: Task（タスク）"""
        def __init__(self, description):
            self.description = description

    def __init__(self, name):
        self.name = name
        self.tasks = []  # コンポジション（複数のTaskを保持）

    def add_task(self, description):
        task = self.Task(description)
        self.tasks.append(task)

    def show_tasks(self):
        for task in self.tasks:
            print(f"Task: {task.description}")

class TemporaryEmployee(Employee):
    """クラス: TemporaryEmployee（派遣社員）
    汎化（継承）: Employeeを継承したクラス
    """
    def __init__(self, name, contract_end_date):
        super().__init__(name)
        self.contract_end_date = contract_end_date

    def work(self):
        print(f"{self.name} is working temporarily until {self.contract_end_date}.")

class Printer:
    """クラス: Printer（プリンター）"""
    def print_document(self):
        print("Printing document...")

class Company:
    """クラス: Company（会社）
    依存関係: CompanyはPrinterを一時的に利用
    """
    def __init__(self, name):
        self.name = name

    def print_annual_report(self, printer):
        printer.print_document()

class Payable:
    """インターフェース: Payable（支払い可能）
    実現関係: Payableインターフェースを実現するクラス
    """
    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement this method")

class Freelancer(Employee, Payable):
    """クラス: Freelancer（フリーランサー）
    実現: Payableインターフェースを実装
    """
    def __init__(self, name, hourly_rate):
        super().__init__(name)
        self.hourly_rate = hourly_rate

    def pay(self, hours):
        print(f"{self.name} has been paid {hours * self.hourly_rate} dollars.")

# サンプル実行
# 集約の例
dept = Department("IT Department")
emp1 = Employee("Alice")
emp2 = Employee("Bob")
dept.add_employee(emp1)
dept.add_employee(emp2)
dept.show_employees()

# コンポジションの例
proj = Project("New Website")
proj.add_task("Design homepage")
proj.add_task("Develop backend")
proj.show_tasks()

# 汎化（継承）の例
temp_emp = TemporaryEmployee("Charlie", "2024-12-31")
temp_emp.work()

# 依存の例
company = Company("TechCorp")
printer = Printer()
company.print_annual_report(printer)

# 実現の例
freelancer = Freelancer("Dave", 50)
freelancer.pay(10)
