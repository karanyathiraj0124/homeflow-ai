# HomeFlow AI

HomeFlow AI is a hackathon prototype for the Alexa+ track: a conversational household/productivity assistant with a real Model Context Protocol (MCP) server using Streamable HTTP, plus a browser-based demonstration client.

## What works
- Task creation, listing, completion, and deletion through MCP tools.
- A browser UI that calls the MCP server over Streamable HTTP using JSON-RPC (`initialize`, `notifications/initialized`, `tools/list`, `tools/call`).
- Local JSON persistence in `data/tasks.json`.
- A deterministic plan preview for common requests; no paid AI API or fabricated model capability.
- Tests for task tool behavior.

## Requirements
- Python 3.11+
- Node.js 20+

## Windows setup (PowerShell)
```powershell
cd homeflow-ai
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
npm install
```

## Run
Terminal 1:
```powershell
.\.venv\Scripts\Activate.ps1
python server.py
```
Terminal 2:
```powershell
npm run dev
```
Open the local URL printed by Vite (normally http://localhost:5173).

The MCP endpoint is `http://127.0.0.1:8000/mcp`.

## Test
```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
```
Then verify in the browser:
1. Click **Connect MCP**; status should show connected and tools should load.
2. Add a task with the form.
3. Ask `Help me prepare for my project deadline` and inspect the suggested plan.
4. Use **Complete** on a task, then refresh; it should remain completed.
5. Disconnect/reconnect and confirm tools are discovered again.

## Important limits
- This is a prototype, not a production smart-home integration.
- It does not connect to a real Alexa+ device or restricted Alexa+ preview tools. It demonstrates an independently hosted MCP server and simulated assistant UI, consistent with the hackathon's documented alternative.
- Plan suggestions are deterministic templates, not LLM-generated responses.
- No cloud/AWS service is integrated in this version. Do not select the AWS Builder mini challenge unless an AWS service is added and documented.
- Test locally before recording. Do not claim tests passed unless you ran them.

## Demo video (under 3 minutes)
1. (0:00–0:20) Introduce HomeFlow AI and the problem: scattered tasks and routines.
2. (0:20–0:45) Show Connect MCP and the discovered tool list.
3. (0:45–1:20) Add a task and show the server response.
4. (1:20–1:50) Ask for a plan and show the generated checklist.
5. (1:50–2:15) Complete a task and refresh to show persistence.
6. (2:15–2:40) Explain the real MCP Streamable HTTP integration and current limitations.

## Submission checklist
- Register/join at https://amazonappdev2026.devpost.com/
- Publish this repository publicly with the MIT license (or use the required private-reviewer process).
- Record and upload a public English video under 3 minutes.
- Provide accurate feedback for every tool/API used.
- Submit before the official deadline shown on Devpost.
