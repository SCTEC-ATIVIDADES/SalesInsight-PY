# Research: RF08 Pipeline Entry Point

## Existing pipeline modules

- Decision: Keep dataset generation in `gerador_dados.py` and all reusable sales operations in `modulo_vendas.py`; `main.py` coordinates only.
- Rationale: Constitution Principle I requires this separation; both modules and required operations already exist.
- Alternatives considered: Reimplement logic in `main.py` or add a new pipeline module. Rejected as duplicative and contrary to constitution.

## Entry-point execution and import safety

- Decision: Preserve the `if __name__ == "__main__"` guard; invoke stages in sequence when run directly.
- Rationale: Prevent import side effects and fulfill RF08 acceptance scenarios. Current `main.py` already has the guard.
- Alternatives considered: Run stages at import time. Rejected because it creates unexpected file/console side effects and makes testing harder.

## Dataset behavior

- Decision: Use `vendas.csv`; generate 150 base records only if the file is absent.
- Rationale: Matches user-provided example, existing repository default, and generator API. Generator creates a deliberate duplicate, so output contains 151 data rows.
- Alternatives considered: Regenerate every run or change dataset size. Rejected because existing input should be reused and example specifies 150.

## Existing pipeline API and gap

- Decision: Reuse `carregar_csv`, `inspecionar_dados`, `limpar_dados`, `criar_campos_derivados`, `calcular_metricas`, `segmentar_clientes_por_gasto`, and `exportar_resultados`; select up to five highest-spend customers for display.
- Rationale: These APIs are implemented and tested. `processar_transformacao`, `segmentar_clientes`, and `obter_top_clientes` named in the example do not exist in `modulo_vendas.py`. The spec does not require a generic higher-order transform; top-five selection is presentation and can use Python’s built-in sorting.
- Alternatives considered: Add alias APIs solely to match the example or add a generic higher-order transform. Rejected as unnecessary abstraction. Keep any ranking/extraction in `main.py` limited to presentation/orchestration; if ranking becomes domain logic, existing module is the correct home.

## Output and failure behavior

- Decision: Preserve `outputs/estatisticas.json`, `outputs/metricas_resumo.csv`, and RF07 schemas. Report export failure without success indication; report read/generation/processing failures clearly and avoid unhandled tracebacks for expected I/O errors.
- Rationale: RF07 exporter already guarantees file names/schema and emits `[OK]` only after both writes; constitution Principles IV/V govern resilient errors and output traceability.
- Alternatives considered: Change output format or add atomic two-file rollback. Rejected: out of RF08 scope and not required by current contract.
