from langchain_core.prompts import ChatPromptTemplate

from app.ai.llm import get_llm
from app.schemas.requirement_extraction import (
    RequirementExtractionResult,
)


SYSTEM_PROMPT = """
You are the requirement extraction component of ReqLens.

ReqLens verifies whether delivered software matches documented
software requirements.

Your task is ONLY to extract requirements from the supplied
document.

Rules:

1. Do not evaluate implementation.
2. Do not invent requirements.
3. Preserve explicit requirement identifiers when available.
4. Preserve important numeric and behavioral constraints.
5. Break each requirement into atomic independently verifiable
   criteria.
6. Every criterion must be supported by the source document.
7. Do not add best practices that are not stated in the source.
8. Preserve the meaning of the original requirement.
9. Distinguish expected behavior from explicit constraints.
10. If the document does not contain requirements, return an
    empty requirements list.

For requirement_type use one of:

functional
non_functional
business_rule
security
performance
other
"""


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Extract the software requirements from the following document.

DOCUMENT:

{document}
""",
        ),
    ]
)


def build_requirement_extraction_chain():

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        RequirementExtractionResult
    )

    return prompt | structured_llm