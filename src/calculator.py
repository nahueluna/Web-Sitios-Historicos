from src import operations

def calculate(operation, a, b):
    match operation:
        case "+":
            return operations.add(a, b)

        case "-":
            return operations.subtract(a, b)

        case "*":
            return operations.multiply(a, b)

        case "/":
            return operations.divide(a, b)

        case _:
            return "Invalid operation"
