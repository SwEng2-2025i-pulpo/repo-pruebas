import json
import os

def convertir_mochawesome_a_simple(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tests = []
    for suite in data.get('results', []):
        for res in suite.get('suites', []):
            for test in res.get('tests', []):
                name = test.get('title', 'Sin nombre')
                status = test.get('state', 'failed')
                details = (
                    test.get('err', {}).get('message', '')
                    if status != "passed"
                    else test.get('displayError', '') or test.get('fullTitle', '')
                )
                tests.append({
                    "name": name,
                    "status": "passed" if status == "passed" else "failed",
                    "details": details or ("Pasó la prueba sin novedad" if status == "passed" else "Verifica el error en Cypress")
                })
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump({"tests": tests}, out, ensure_ascii=False, indent=2)
    print(f"Archivo convertido: {output_path}")

if __name__ == "__main__":
    input_path = "cypress/reports/mochawesome.json"
    output_path = "resultados/resultados_frontend.json"
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    convertir_mochawesome_a_simple(input_path, output_path)