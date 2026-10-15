import json

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from app.ai.llm import get_llm
from app.schemas.evidence_analysis import (
    EvidenceAssessmentResult,
)


SYSTEM_PROMPT = """
You are the evidence assessment component of ReqLens.

ReqLens verifies whether delivered software satisfies documented
software requirements.

You are NOT performing final verification.

Your task is to inspect retrieved candidate evidence and determine
whether each candidate is genuinely relevant to ONE specific
verifiable criterion.

Important rules:

1. Only use the supplied criterion and evidence.
2. Do not invent implementation behavior.
3. Do not assume that semantically similar text proves the criterion.
4. Source code is implementation evidence only when it actually
   implements or directly participates in the requested behavior.
5. Test code is test evidence only when it actually exercises the
   requested behavior.
6. Documentation describes claimed behavior but does not by itself
   prove implementation.
7. Story/acceptance-criteria evidence describes planned behavior but
   does not prove implementation.
8. Preserve concrete values such as minutes, limits, roles, states,
   sizes and allowed values.
9. A candidate may be relevant while NOT supporting the criterion.
10. Contradictory evidence should still be considered relevant.
11. Do not decide VERIFIED, MISSING, CONFLICT, PARTIAL, or any final
    verification status.
12. If evidence is only loosely related, mark it weak or irrelevant.

Strength meanings:

strong:
Directly demonstrates behavior relevant to the criterion.

moderate:
Meaningfully supports the criterion but is incomplete or indirect.

weak:
Related but insufficient to establish the criterion.

irrelevant:
Does not materially help evaluate the criterion.
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
REQUIREMENT:
{requirement}

VERIFIABLE CRITERION:
{criterion}

CANDIDATE EVIDENCE:

{candidates}

Assess every candidate.
""",
        ),
    ]
)


def build_evidence_assessment_chain():

    llm = get_llm()

    structured_llm = (
        llm.with_structured_output(
            EvidenceAssessmentResult
        )
    )

    return prompt | structured_llm


def serialize_candidates(
    candidates: list[dict],
) -> str:

    clean = []

    for candidate in candidates:

        clean.append(
            {
                "candidate_id":
                    candidate["vector_id"],

                "source_name":
                    candidate["source_name"],

                "evidence_type":
                    candidate["evidence_type"],

                "content":
                    candidate["content"],
            }
        )

    return json.dumps(
        clean,
        indent=2,
    )