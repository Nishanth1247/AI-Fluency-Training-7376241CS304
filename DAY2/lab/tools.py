import ast
import operator as op

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def get_course_fee(course_code):
    course_code = course_code.upper()

    if course_code not in COURSE_FEES:
        return f"Unknown course: {course_code}"

    return COURSE_FEES[course_code]


# Safe calculator
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg
}


def calculator(expression):
    def evaluate(node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            operator = OPERATORS[type(node.op)]
            return operator(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            operator = OPERATORS[type(node.op)]
            return operator(operand)

        raise ValueError("Unsupported expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]