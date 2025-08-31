from src import calculator

# Previene que el codigo se ejecute al importar el modulo
if __name__ == "__main__":
    num = float(input("Enter a number: "))
    other_num = float(input("Enter another number: "))
    operation = input("Enter an operation (+, -, *, /): ")
    result = calculator.calculate(operation, num, other_num)
    print(result)
