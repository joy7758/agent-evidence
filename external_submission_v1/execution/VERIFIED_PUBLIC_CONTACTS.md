# Verified Public Contacts

These contacts were classified from public-source context supplied by the user.
They are not default outreach targets. Do not guess additional addresses, scrape
personal emails, or use security and privacy contacts for generic protocol
promotion.

| Target | Email / channel | Source context | Allowed use | Not allowed use | Recommended priority | send_allowed_by_default |
| --- | --- | --- | --- | --- | --- | --- |
| Cursor / Anysphere | `security@cursor.com` | Cursor Security page says other security-related questions can contact this address. | Narrow agent security, audit, replay, and evidence architecture feedback. | Generic marketing, endorsement request, Origin integration claim, vulnerability report. | Optional after public release and public-channel posting. | false |
| Cursor / Anysphere | `security-reports@cursor.com` | Cursor Security page says potential vulnerabilities should be reported there. | Real vulnerability disclosure only. | Project outreach, protocol pitch, Origin pitch, general feedback. | Do not use for this package unless a real vulnerability exists. | false |
| Cursor / Anysphere | `hi@cursor.com` | Cursor privacy/security pages use it for privacy rights, privacy policy questions, support, or account deletion. | Account, support, or privacy context only. | Technical protocol outreach or research pitch. | Not recommended. | false |
| Cursor Origin | Origin waitlist, Cursor Forum, Help, Contact Sales | Origin page is a waitlist and Cursor site provides public support/contact surfaces. | Public technical feedback request through official channels. | Claiming official Origin support or integration. | High. | false |
| Graphite | `security@graphite.dev` | Graphite privacy/security page says this address can be used for SOC2 audit report requests. | Security/audit report context only. | Generic protocol pitch or partnership outreach. | Not recommended for this package. | false |
| Graphite | `security@graphite.com` | Graphite privacy policy contact email. | Privacy/security policy contact context only. | Generic protocol pitch or partnership outreach. | Not recommended. | false |
| Graphite | Community Slack, GitHub/public channels, Cursor contact/demo route | Graphite public site lists community and public contact routes. | Public technical feedback about stacked PR and agent PR evidence. | Claiming Graphite endorsement or integration. | High. | false |
| MCP | GitHub Discussions, GitHub Issues, Discord, Working Groups, SEP sponsor route | MCP contributor communication and contribution paths. | Discussions first; Issues for actionable implementation problems; SEP for protocol-level changes. | Email outreach, protocol replacement claim, official MCP endorsement claim. | High. | false |

Sending to `security@cursor.com` requires both
`AEP_ALLOW_CURSOR_SECURITY_RESEARCH_EMAIL=YES` and `I_APPROVE_EMAIL_SEND=YES`.
Sending to `security-reports@cursor.com` requires both
`AEP_REAL_VULNERABILITY_REPORT=YES` and `I_APPROVE_EMAIL_SEND=YES`.
Sending to Graphite security contacts requires both
`AEP_ALLOW_GRAPHITE_SECURITY_AUDIT_EMAIL=YES` and `I_APPROVE_EMAIL_SEND=YES`.
Sending to `hi@cursor.com` requires both `AEP_ALLOW_CURSOR_SUPPORT_EMAIL=YES`
and `I_APPROVE_EMAIL_SEND=YES`.
