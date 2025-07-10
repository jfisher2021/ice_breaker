from langchain.agents.output_parsers import ReActSingleInputOutputParser

# Crear el parser
parser = ReActSingleInputOutputParser()

# Ejemplo 1: Texto con SOLO una acción (FUNCIONA)
response_with_action = """I need to find the length of "DOG".
Action: get_length
Action Input: DOG"""

print("=== EJEMPLO 1: Solo Acción ===")
try:
    result = parser.parse(response_with_action)
    print(f"Tipo: {type(result)}")
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error: {e}")

# Ejemplo 2: Texto con SOLO respuesta final (FUNCIONA)  
response_with_final = """I know the answer now.
Final Answer: 3"""

print("\n=== EJEMPLO 2: Solo Respuesta Final ===")
try:
    result = parser.parse(response_with_final)
    print(f"Tipo: {type(result)}")
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error: {e}")

# Ejemplo 3: Texto con AMBOS (FALLA)
response_with_both = """I need to find the length of "DOG".
Action: get_length
Action Input: DOG
Observation: 3
Thought: I now know the answer.
Final Answer: 3"""

print("\n=== EJEMPLO 3: Acción Y Respuesta Final (FALLA) ===")
try:
    result = parser.parse(response_with_both)
    print(f"Tipo: {type(result)}")
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error: {e}")
