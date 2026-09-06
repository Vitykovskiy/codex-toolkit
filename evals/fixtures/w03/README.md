# Synthetic contact form
Requires Python 3.11+ and a browser with JavaScript modules. No npm dependencies.
Run `python3 server.py` from this directory; open `http://127.0.0.1:8765`.
The local API is synthetic; this is not production integration.

Implement the contact form in app.js using existing components and api.js.
Inputs: required name and email. Submit label: Send. Pending label: Sending….
Keep entered values on error, show the server message and focus the error region.
On success show Saved and focus the success region. Empty/invalid input uses native
validation. Prevent duplicate submissions while pending and permit retry after failure.

API: POST /api/contact, JSON {"name": string, "email": string}.
Success: 201 {"id": "contact-1"}. Email fail@example.test produces
422 {"message": "Email rejected"}. The API helper throws Error(message) on failure.
Test data: Ada / ada@example.test and Ada / fail@example.test.

Browser scenario: keyboard-fill name/email, submit valid data, observe Saved and
success focus; reload, submit failure email, observe Email rejected and error focus;
change to valid email and retry successfully. Check pending disabled state using the
browser's controlled network delay if supported; record that condition explicitly.
Record console/network failures and viewport. Static reading cannot prove focus.
