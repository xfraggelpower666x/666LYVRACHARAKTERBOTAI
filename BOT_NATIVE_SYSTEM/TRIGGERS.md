# Native bot trigger control — case insensitive, explicit prefix only

PREFIX: `666LYVRABOT`
Aliases: `666 LYVRA BOT` (not native LYVRA), `LYVRA CHARACTER BOT` only when explicitly addressing this bot system.
Never capture `LYVRA`, `LYVRA UPDATE`, `666PFS`, `666CLIC`, or other system command namespaces.

| Trigger | Action | Default effect |
|---|---|---|
| `666LYVRABOT SYSTEMSTART` | evidence-first read and rehydrate current bot system | read-only |
| `666LYVRABOT WEITER` | resume last verified Bot development stage | read-only until authorized |
| `666LYVRABOT NEXT CHAT` / `NEW CHAT` | produce pinned handoff and return anchor | read-only |
| `666LYVRABOT DASHBOARD` | show Whole-Bot and facet/sub-LifeCircle status | read-only |
| `666LYVRABOT AUDIT` | inspect repo/worker/branch/security compliance | read-only |
| `666LYVRABOT CODEFORGE` | inspect plan, tests, patches and recovery | no implicit production release |
| `666LYVRABOT UPDATE` | stage governed bot-repo-only updates | prechange+audit+readback required |
| `666LYVRABOT HANDOFF` | prepare or reconcile system-scoped exchange | no auto-approval |
| `666LYVRABOT RECOVERY` | validate preserved baseline and propose rollback | no auto-reset |
| `666LYVRABOT FACETS` / `CAPABILITIES` | show current registry and measured implementation | read-only |

Trigger handling is a repository-documented operating protocol; a chatbot/client still needs to be configured to interpret commands. It is NOT a daemon, running trigger listener, or automatic activation by itself.
