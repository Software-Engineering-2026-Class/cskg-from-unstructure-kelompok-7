from fastapi import FastAPI, HTTPException, Body
from pydantic import (
    BaseModel,
    Field,
)
import uvicorn
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Any

# --- Configuration ---
SPARQL_ENDPOINT = "http://virtuoso:8890/sparql"
CSKG_GRAPH_URI = "http://group2.org/cskg"
STIX_NS = "http://docs.oasis-open.org/cti/ns/stix#"
SEPSES_CVE_NS = "https://w3id.org/sepses/resource/cve/"

# --- Initialize FastAPI ---
app = FastAPI(
    title="Cybersecurity Knowledge Graph API",
    description="Query a LIVE CSKG running on Virtuoso.",
)


# --- API Models ---
class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        json_schema_extra={"example": "SELECT ?s ?p ?o WHERE { ?s ?p ?o . } LIMIT 10"},
    )


def get_sparql_connection():
    """Configures the SPARQLWrapper for Virtuoso."""
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setReturnFormat(JSON)
    return sparql


def run_select_query(query: str):
    sparql = get_sparql_connection()
    sparql.setQuery(query)
    return sparql.query().convert()


def first_int_result(results: Any, variable: str) -> int:
    bindings = results.get("results", {}).get("bindings", [])
    if not bindings:
        return 0
    value = bindings[0].get(variable, {}).get("value", 0)
    return int(value)


@app.get("/", summary="Check API and graph status")
def get_status():
    """Checks if the API is running and pings the Virtuoso DB."""
    try:
        global_results = run_select_query(
            "SELECT (COUNT(*) as ?triples) WHERE { ?s ?p ?o }"
        )
        cskg_results = run_select_query(
            f"""
            SELECT (COUNT(*) as ?triples)
            WHERE {{
              GRAPH <{CSKG_GRAPH_URI}> {{ ?s ?p ?o }}
            }}
            """
        )

        return {
            "status": "online",
            "graph_db_backend": "Virtuoso",
            "sparql_endpoint": SPARQL_ENDPOINT,
            "named_graph": CSKG_GRAPH_URI,
            "global_triples": first_int_result(global_results, "triples"),
            "cskg_named_graph_triples": first_int_result(cskg_results, "triples"),
        }
    except Exception as e:
        return {"status": "error", "db_connection_error": str(e)}


@app.get("/stats", summary="Get CSKG named graph statistics")
def get_stats():
    """Returns statistics scoped only to the CSKG named graph."""
    try:
        total_query = f"""
        SELECT (COUNT(*) as ?total)
        WHERE {{ GRAPH <{CSKG_GRAPH_URI}> {{ ?s ?p ?o }} }}
        """
        type_query = f"""
        SELECT ?type (COUNT(DISTINCT ?s) as ?count)
        WHERE {{ GRAPH <{CSKG_GRAPH_URI}> {{ ?s a ?type }} }}
        GROUP BY ?type
        ORDER BY DESC(?count)
        """
        predicate_query = f"""
        SELECT ?predicate (COUNT(*) as ?count)
        WHERE {{ GRAPH <{CSKG_GRAPH_URI}> {{ ?s ?predicate ?o }} }}
        GROUP BY ?predicate
        ORDER BY DESC(?count)
        """
        sepses_query = f"""
        SELECT (COUNT(DISTINCT ?s) as ?total)
        WHERE {{
          GRAPH <{CSKG_GRAPH_URI}> {{
            ?s a <{STIX_NS}Vulnerability> .
            FILTER(STRSTARTS(STR(?s), "{SEPSES_CVE_NS}"))
          }}
        }}
        """

        total_results = run_select_query(total_query)
        type_results = run_select_query(type_query)
        predicate_results = run_select_query(predicate_query)
        sepses_results = run_select_query(sepses_query)

        type_counts = {
            row["type"]["value"]: int(row["count"]["value"])
            for row in type_results.get("results", {}).get("bindings", [])
        }
        predicate_counts = {
            row["predicate"]["value"]: int(row["count"]["value"])
            for row in predicate_results.get("results", {}).get("bindings", [])
        }

        return {
            "named_graph": CSKG_GRAPH_URI,
            "total_triples": first_int_result(total_results, "total"),
            "count_by_type": type_counts,
            "count_by_predicate": predicate_counts,
            "total_reports": type_counts.get(f"{STIX_NS}Report", 0),
            "total_vulnerabilities": type_counts.get(f"{STIX_NS}Vulnerability", 0),
            "total_malware": type_counts.get(f"{STIX_NS}Malware", 0),
            "total_indicators": type_counts.get(f"{STIX_NS}Indicator", 0),
            "total_attack_patterns": type_counts.get(f"{STIX_NS}AttackPattern", 0),
            "total_threat_actors": type_counts.get(f"{STIX_NS}ThreatActor", 0),
            "total_sepses_cve_uri": first_int_result(sepses_results, "total"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stats query failed: {e}")


@app.post("/query", summary="Execute a SPARQL query")
def query_graph(request: QueryRequest = Body(...)):
    """Executes a raw SPARQL query against the Virtuoso database."""
    try:
        results: Any = run_select_query(request.query)

        # These lines will now pass type-checking
        variables = results.get("head", {}).get("vars", [])
        output = []
        for binding in results.get("results", {}).get("bindings", []):
            row_dict = {}
            for var in variables:
                row_dict[var] = binding.get(var, {}).get("value")
            output.append(row_dict)

        return {"variables": variables, "results": output}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
