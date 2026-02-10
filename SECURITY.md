# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by:

1. **DO NOT** create a public GitHub issue
2. Email the repository owner at: starkarthikr@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Response Time**: You will receive an initial response within 48 hours
- **Investigation**: We will investigate and validate the report
- **Fix Timeline**: Critical issues will be fixed within 7 days
- **Disclosure**: We follow coordinated disclosure practices

## Security Best Practices

### For Users

1. **Never commit secrets**: Always use environment variables or GitHub Secrets
2. **Keep dependencies updated**: Regularly update Python packages
3. **Review permissions**: Only grant necessary GitHub Actions permissions
4. **Use branch protection**: Enable branch protection rules on main branch

### API Key Security

- Store all API keys in GitHub Secrets (Settings → Secrets and variables → Actions)
- Never hardcode API keys in source code or workflow files
- Rotate API keys regularly
- Revoke exposed keys immediately

## Security Features Enabled

- [x] Dependabot security updates
- [x] GitHub Actions permissions restricted
- [x] Secret scanning
- [x] Security policy published

## Known Security Considerations

### Third-Party APIs

This project uses OpenRouter API for AI analysis:
- API keys must be stored securely in GitHub Secrets
- Rate limiting is implemented
- No sensitive data is sent to external services

### Automated Workflows

- Workflows run with minimal permissions
- Only necessary secrets are exposed to workflows
- All dependencies are pinned to specific versions

## Security Updates

Security updates will be published as:
- GitHub Security Advisories
- Release notes with `[SECURITY]` prefix
- Commits with security fixes

Last Updated: February 10, 2026
