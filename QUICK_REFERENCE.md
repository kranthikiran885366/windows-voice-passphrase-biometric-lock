# Sivaji Security System - Quick Reference Card

## Quick Start (5 Minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Setup fail-safe
python main.py --mode setup-developer-secret

# 3. Enroll
python main.py --mode enroll --username "authorized_user"

# 4. Authenticate
python main.py

# Done!
```

## Emergency Fail-Safe (In Crisis)

```bash
# 1. Request OTK
python main.py --mode request-otk --failure-type MICROPHONE_FAILURE

# 2. When prompted:
# - Enter developer secret
# - Press Ctrl+Alt+F12+D
# - Enter OTK
```

## Common Commands

| Task | Command |
|------|---------|
| Start auth | `python main.py` |
| Enroll user | `python main.py --mode enroll` |
| Setup fail-safe | `python main.py --mode setup-developer-secret` |
| Request OTK | `python main.py --mode request-otk --failure-type MICROPHONE_FAILURE` |
| Check status | `python main.py --mode check-failsafe-status` |
| Disable fail-safe | `python main.py --mode disable-failsafe` |
| Run tests | `python main.py --mode test` |
| Configure | `python main.py --mode config` |

## Fail-Safe Specs

| Property | Value |
|----------|-------|
| Activation | 3 factors (secret + OTK + physical) |
| Secret | PBKDF2-SHA256, 100k iterations |
| OTK Validity | 15 minutes, single-use |
| Physical | Ctrl+Alt+F12+D sequence |
| Max Uses | 3 per session |
| Duration | 30 minutes max |
| Encryption | AES-256-GCM + HMAC |

## File Locations

```
/security/developer_failsafe.py     → Fail-safe implementation
/data/failsafe_state.enc            → Encrypted fail-safe state
/logs/failsafe_events.enc           → Encrypted audit log
/docs/DEVELOPER_OVERRIDE.md         → Complete guide
/docs/INTEGRATION_GUIDE.md          → Deployment procedures
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Microphone error | Run: `python main.py --mode test` |
| OTK expired | Request new: `--mode request-otk` |
| Secret wrong | Verify in password manager |
| Physical confirm fails | Press: Ctrl→Alt→F12→D |
| Max uses exceeded | Restart system to reset |
| Fail-safe corrupted | Restore from backup |

## Key Policies

- **Secret Storage**: Use password manager, NEVER plaintext
- **OTK Handling**: Fresh OTK per activation
- **Audit Review**: Monthly review recommended
- **Backups**: Weekly encrypted backups
- **Testing**: Quarterly fail-safe tests

## Performance Targets

- Authentication: <2 seconds
- Accuracy: ≥98%
- False Acceptance: <0.5%
- False Rejection: <2%

## Security Checklist

- ✓ Developer secret: 16+ chars, mixed case/numbers/symbols
- ✓ OTK stored separately from secret
- ✓ Audit logs reviewed monthly
- ✓ System tested quarterly
- ✓ Backups encrypted and stored securely
- ✓ Fail-safe never activated for normal use
- ✓ Physical confirmation sequence confirmed
- ✓ System clock synchronized

## Documentation Map

| Document | Purpose |
|----------|---------|
| README.md | Overview & quick start |
| DEVELOPER_OVERRIDE.md | Complete fail-safe guide |
| SYSTEM_ARCHITECTURE.md | Technical design |
| ALGORITHMS_USED.md | Math & algorithms |
| SECURITY_MODEL.md | Threat analysis |
| INTEGRATION_GUIDE.md | Deployment procedures |
| QUICK_REFERENCE.md | This cheat sheet |

## Support Resources

- **Technical Issues**: Check INTEGRATION_GUIDE.md
- **Fail-Safe Help**: See DEVELOPER_OVERRIDE.md
- **Security Questions**: Review SECURITY_MODEL.md
- **Deployment**: Follow INTEGRATION_GUIDE.md
- **Architecture**: Read SYSTEM_ARCHITECTURE.md

---

**Bookmark this page for quick access!**
