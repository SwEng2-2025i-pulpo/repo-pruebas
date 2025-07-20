import json
import os
import glob

def merge_mochawesome_jsons(input_pattern):
    """Une todos los archivos mochawesome JSON en uno solo (results concatenados)."""
    files = glob.glob(input_pattern)
    merged = {"results": []}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'results' in data:
                merged['results'].extend(data['results'])
    return merged

def convertir_mochawesome_a_simple(data, output_path):
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
    # Cambia el patrón según tu estructura
    input_pattern = "cypress/results/*.json"
    output_path = "resultados/resultados_frontend.json"
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    # 1. Merge
    merged = merge_mochawesome_jsons(input_pattern)
    # 2. Convertir a formato simple
    convertir_mochawesome_a_simple(merged, output_path)