# Update Policy

- Installed version: read `VERSION`.
- Public version record: `https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/feishu-doc-beautifier.json`.
- On the first use in a new session, check the public record when network access is available. A failed check must not block the user's document task.
- If a newer version exists, explain the version number and release notes, then ask for confirmation before replacing files.
- Never silently overwrite an installed Skill, user knowledge base, document, account configuration, or another Skill.
- After an approved update, start a new task/session so the Agent reloads the newest files.
