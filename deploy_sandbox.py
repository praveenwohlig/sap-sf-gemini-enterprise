"""
deploy_sandbox.py
══════════════════════════════════════════════════════════════
Deploy sap_agent (sandbox mode) to Vertex AI Agent Engine.
- First run: creates a new Agent Engine, saves resource name to .agent_resource
- Subsequent runs: updates the existing Agent Engine in place

Run:
  python deploy_sandbox.py

Output:
  Agent resource path printed to stdout.
══════════════════════════════════════════════════════════════
"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # must run before sap_agent is imported (tools_sandbox reads env at module level)

import vertexai
from vertexai import agent_engines
from sap_agent.agent import root_agent

AGENT_DISPLAY_NAME   = "sap-sf-sandbox-agent"
RESOURCE_NAME_FILE   = Path(__file__).parent / ".agent_resource"

REQUIREMENTS = [
    "google-cloud-aiplatform[adk,agent_engines]",
    "google-adk==1.30.0",
    "requests",
]
EXTRA_PACKAGES = ["./sap_agent"]


def _resolve_project() -> str:
    project = os.environ.get("GCP_PROJECT_ID", "").strip()
    if project:
        return project
    result = subprocess.run(
        ["gcloud", "config", "get-value", "project"],
        capture_output=True, text=True, check=True,
    )
    project = result.stdout.strip()
    if not project:
        raise ValueError("GCP_PROJECT_ID not set in .env and no gcloud default project configured.")
    return project


def _resolve_bucket(raw: str) -> str:
    """Return gs://<bucket-name> — strips any path suffix (Vertex AI needs the bucket root)."""
    raw = raw.strip()
    if not raw:
        raise ValueError("GCS_BUCKET is not set in .env")
    raw = raw.removeprefix("gs://")
    bucket_name = raw.split("/")[0]
    return f"gs://{bucket_name}"


# ── GCP config ────────────────────────────────────────────────
PROJECT_ID     = _resolve_project()
LOCATION       = "us-central1"
STAGING_BUCKET = _resolve_bucket(os.environ.get("GCS_BUCKET", ""))

# ── Sandbox credentials (read from .env) ──────────────────────
SF_SANDBOX_HOST    = os.environ["SF_SANDBOX_HOST"]
SF_SANDBOX_API_KEY = os.environ["SF_SANDBOX_API_KEY"]
SF_SANDBOX_USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")

ENV_VARS = {
    "SF_SANDBOX_HOST":    SF_SANDBOX_HOST,
    "SF_SANDBOX_API_KEY": SF_SANDBOX_API_KEY,
    "SF_SANDBOX_USER_ID": SF_SANDBOX_USER_ID,
}


def main():
    print(f"Project:        {PROJECT_ID}")
    print(f"Staging bucket: {STAGING_BUCKET}")
    print(f"Location:       {LOCATION}")
    print()

    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    existing_resource = RESOURCE_NAME_FILE.read_text().strip() if RESOURCE_NAME_FILE.exists() else None

    if existing_resource:
        print(f"Updating existing agent: {existing_resource}")
        remote_app = agent_engines.get(existing_resource)
        remote_app.update(
            agent_engine=root_agent,
            display_name=AGENT_DISPLAY_NAME,
            requirements=REQUIREMENTS,
            extra_packages=EXTRA_PACKAGES,
            env_vars=ENV_VARS,
        )
    else:
        print("Creating new agent...")
        remote_app = agent_engines.create(
            agent_engine=root_agent,
            display_name=AGENT_DISPLAY_NAME,
            requirements=REQUIREMENTS,
            extra_packages=EXTRA_PACKAGES,
            env_vars=ENV_VARS,
        )
        RESOURCE_NAME_FILE.write_text(remote_app.resource_name)

    print("\n" + "=" * 55)
    print("  Deployment complete!")
    print(f"  Resource path: {remote_app.resource_name}")
    print("=" * 55)
    print("\nCopy the resource path above into:")
    print("Gemini Enterprise → Agents → Add Agent → Agent Platform resource path")


if __name__ == "__main__":
    main()