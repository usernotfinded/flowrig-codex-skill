# Review Rubric

Use this for final self-review and code-review tasks.

## Severity scale

- **Blocker**: breaks core behavior, data safety, auth, build, or tests.
- **High**: likely production bug or security issue.
- **Medium**: edge case, maintainability issue, missing important test.
- **Low**: style, clarity, small documentation improvement.

## Checklist

### Correctness

- Does the change solve the actual user request?
- Are edge cases handled?
- Are defaults and error paths preserved?
- Does it handle empty, null, missing, duplicate, and malformed inputs where relevant?

### Integration

- Does it fit existing architecture?
- Are imports/exports updated?
- Are migrations, generated clients, schemas, and config files synced?

### Tests

- Is there a regression test for the changed behavior?
- Are tests meaningful or just snapshot churn?
- Did any baseline failures exist before the patch?

### Security / privacy

- Any auth, permission, token, secret, file path, browser, network, payment, or data-retention impact?
- Any new command execution, shell interpolation, SSRF, XSS, SQL injection, path traversal, unsafe deserialization, or dependency risk?

### Maintainability

- Is the diff smaller than the problem?
- Did it introduce duplicate logic?
- Are public APIs and backward compatibility preserved?
- Is naming consistent with the repo?

## Review output

```md
## Verdict

## Findings
| Severity | File/area | Issue | Suggested fix |
|---|---|---|---|

## Verification gaps

## Recommended next action
```
