import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()


class MedGemmaClient:

    def __init__(self):
        self.endpoint = os.getenv("MEDGEMMA_API_URL")
        self.model    = os.getenv("MEDGEMMA_MODEL")
        self.token    = os.getenv("MEDGEMMA_API_TOKEN")

    def summarize(self, transcript, system_prompt):

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": json.dumps(transcript, ensure_ascii=False)}
            ]
        }

        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        raw_response = response.json()

        # ── Extract the model's text content from the API envelope ──────────
        try:
            content = raw_response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise ValueError(
                f"Unexpected API response structure: {e}\nFull response: {raw_response}"
            )

        # ── Strip markdown fences if the model wrapped output in ```json ─────
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())

        # ── Parse the JSON string into a Python dict ─────────────────────────
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Model returned invalid JSON: {e}\nRaw content:\n{content[:500]}"
            )