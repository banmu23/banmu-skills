# Update Policy

## Public Version Source

Latest-version metadata:

```text
https://raw.githubusercontent.com/banmu23/banmu-skills/refs/heads/main/versions/feishu-doc-beautifier.json
```

Local version:

```text
VERSION
```

## Check Rule

On the first use in each new chat or session:

1. If internet access is available, read the public version metadata.
2. Compare its `version` with the local `VERSION` value using semantic-version order.
3. If the public version is not newer, continue without an update message.
4. If a newer version exists, do not silently replace local files. Tell the user the current and latest versions, summarize the release notes, and ask whether to update.
5. If the check fails, continue the user's document task. A failed update check must not block normal use.

## Approved Update Flow

After the user confirms an update, prefer the marketplace upgrade flow:

```text
codex plugin marketplace upgrade banmu-skills
codex plugin add feishu-doc-beautifier@banmu-skills
```

Then ask the user to start a new chat or session so the updated plugin is loaded.

If the current product surface cannot run these commands, give the user the fixed marketplace link and a short update prompt instead of pretending the update completed.

## Safety Boundaries

- Do not change permissions, accounts, or unrelated plugins.
- Do not delete the old installed copy without the user's confirmation.
- Do not expose local paths, credentials, private knowledge-base content, or customer data in update messages.
- Do not replace a working version when the public version metadata is invalid or cannot be verified.
