# Synthetic security review
Scope: app.py and its in-memory fixtures. Local execution only, no external systems.
The authenticated actor is passed by trusted middleware, not request parameters.
Documents must only be readable by actors in the same organization.
Review only; do not change the application. Use no real credentials or user data.
