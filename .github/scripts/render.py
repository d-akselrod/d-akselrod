#!/usr/bin/env python3
"""Render the profile README's SVG cards.

Every card is built from the configuration below, so this needs no network
access, no credentials and no third-party service. Stdlib only, so the
workflow needs no dependency install step either.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cards  # noqa: E402
from theme import THEMES  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "assets"

NAME = "Daniel Akselrod"
ROLE = "Full Stack & AI Software Engineer"
META = ("Toronto, Canada   ·   Software Engineer II @ Guidewire   ·   "
        "M.S. Computer Science @ Georgia Tech")

STACK = [
    ("Languages", ["TypeScript", "JavaScript", "Python", "Java", "Kotlin",
                   "C#", "SQL", "Bash"]),
    ("Agentic AI", ["RAG", "MCP", "Claude Agent SDK", "OpenAI Agents SDK",
                    "LangGraph", "LangChain", "Amazon Bedrock"]),
    ("Machine Learning", ["PyTorch", "TensorFlow", "scikit-learn", "NumPy",
                          "Pandas", "SciPy"]),
    ("Backend & Data", ["Spring Boot", "ASP.NET Core", "FastAPI",
                        "PostgreSQL", "MongoDB"]),
    ("Frontend", ["React", "HTML/CSS", "Tailwind", "Jest", "Electron"]),
    ("Cloud", ["AWS Lambda", "EC2", "EKS", "S3", "Aurora", "DynamoDB",
               "Azure App Service", "Key Vault", "Container Registry"]),
    ("DevOps", ["Docker", "Kubernetes", "GitHub Actions", "Azure Pipelines",
                "TeamCity", "Datadog"]),
]

EDUCATION = [
    ("M.S. Computer Science",
     "Georgia Tech  ·  Computing Systems  ·  4.0 GPA  ·  Dec 2026"),
    ("B.Eng. Software Engineering",
     "McMaster University  ·  2024"),
]

CERTIFICATIONS = [
    ("AWS Certified Cloud Practitioner", "Amazon Web Services"),
    ("AWS Certified AI Practitioner", "Amazon Web Services"),
]

def write(stem, theme_name, svg):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{stem}-{theme_name}.svg"
    previous = path.read_text() if path.exists() else None
    if previous != svg:
        path.write_text(svg)
        print(f"updated {path.relative_to(OUT.parent)}")
    return path


def main():
    for theme_name, t in THEMES.items():
        write("hero", theme_name, cards.hero(t, NAME, ROLE, META))
        write("stack", theme_name, cards.stack(t, STACK))
        write("credentials", theme_name,
              cards.credentials(t, EDUCATION, CERTIFICATIONS))

    print(f"rendered {len(THEMES) * 3} cards into {OUT}")


if __name__ == "__main__":
    main()
