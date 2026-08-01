import os

try:
    from langchain_community.utilities import SQLDatabase
except Exception:  # pragma: no cover - optional dependency
    SQLDatabase = None

try:
    from langchain_experimental.agents import create_sql_agent
except Exception:  # pragma: no cover - compatibility fallback
    create_sql_agent = None

try:
    from langchain_ollama import ChatOllama
except Exception:  # pragma: no cover - optional dependency
    ChatOllama = None

try:
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - optional dependency
    ChatOpenAI = None


def _build_llm():
    use_ollama = os.getenv("USE_OLLAMA", "1").lower() in {"1", "true", "yes", "on"}

    if use_ollama:
        if ChatOllama is None:
            raise RuntimeError(
                "Ollama support is not installed. Install Ollama and run 'pip install langchain-ollama'."
            )

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
            temperature=0,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if ChatOpenAI is None:
        raise RuntimeError("OpenAI support is not installed. Install langchain-openai or use Ollama.")

    return ChatOpenAI(temperature=0, model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


def _fallback_message(exc=None):
    base = (
        "The local AI assistant is not ready yet. Please install Ollama or make sure the LangChain "
        "dependencies are available."
    )
    if exc:
        return f"{base} Details: {exc}"
    return base


def ask_hospital_ai(user_question):
    if SQLDatabase is None:
        return _fallback_message("langchain-community is unavailable")

    try:
        db = SQLDatabase.from_uri("sqlite:///data/hospital_local_cache.db")
        llm = _build_llm()

        if create_sql_agent is None:
            raise RuntimeError("The installed LangChain version does not expose create_sql_agent")

        agent_executor = create_sql_agent(llm, db=db, verbose=False)
        response = agent_executor.invoke({"input": user_question})
        return response["output"]
    except Exception as exc:
        message = str(exc).lower()
        if "connection refused" in message or "connect" in message or "ollama" in message:
            return (
                "Local Ollama is not reachable. Please install Ollama, start it, and pull a model like "
                "'ollama pull llama3.2:latest'."
            )
        return _fallback_message(exc)
