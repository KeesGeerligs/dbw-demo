# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Domain_create_agent: for suggesting meanigful DNS domain"""

from google.adk import Agent
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm

from marketing_agency.config import API_BASE_URL, MODEL_NAME_AT_ENDPOINT, API_KEY
from . import prompt

domain_create_agent = Agent(
    model=LiteLlm(
        model=MODEL_NAME_AT_ENDPOINT,
        api_base=API_BASE_URL,
        api_key=API_KEY
    ),
    name="domain_create_agent",
    instruction=prompt.DOMAIN_CREATE_PROMPT,
    output_key="domain_create_output",
    # tools=[google_search],
)
