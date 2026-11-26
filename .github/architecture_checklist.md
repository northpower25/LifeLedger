# LifeLedger Architecture Checklist

Version: 1.0

Status: Mandatory

This checklist must be completed before:

- Architecture changes
- New features
- Pull Requests
- Major refactorings
- New integrations
- New AI providers
- New storage providers
- New connectors

---

# Purpose

LifeLedger is expected to evolve over many years.

This checklist exists to prevent architectural drift.

Any unchecked item must be explained.

---

# 1. LifeLedger Architecture

## Responsibility Validation

Does this change belong inside LifeLedger?

LifeLedger responsibilities:

- Personal Health Record
- Health Timeline
- Family Health
- Medication Management
- Medical Documents
- Emergency Profiles
- User Experience

Questions:

[ ] Is this a user-facing feature?

[ ] Does it belong to the health record?

[ ] Does it belong to document management?

[ ] Does it belong to medication management?

[ ] Does it belong to health timeline management?

If NO:

Do not implement inside LifeLedger.

---

# 2. VitaFabric Validation

All health data must enter through VitaFabric.

Questions:

[ ] Does the feature interact with health data?

[ ] Is health data mapped through VitaFabric?

[ ] Is FHIR used as canonical model?

[ ] Is provenance captured?

[ ] Is data quality considered?

[ ] Is synchronization handled correctly?

Reject if any answer is NO.

---

# 3. LifeWeaver Validation

LifeWeaver owns:

- AI
- MCP
- Agents
- RAG
- Knowledge Graph
- Health Twin

Questions:

[ ] Does the feature use AI?

[ ] Is AI logic located inside LifeWeaver?

[ ] Is MCP compatibility preserved?

[ ] Is provider abstraction maintained?

Reject if AI logic is placed elsewhere.

---

# 4. FHIR Compliance

FHIR is the canonical health model.

Questions:

[ ] Are FHIR resources used?

[ ] Is the FHIR model unchanged?

[ ] Is mapping documented?

[ ] Is terminology documented?

[ ] Is FHIR R4 compatibility maintained?

Reject if custom health models are introduced.

---

# 5. Consent Validation

User consent is mandatory.

Questions:

[ ] Does this feature access personal health data?

[ ] Is user consent required?

[ ] Is consent checked?

[ ] Is consent auditable?

[ ] Is consent revocable?

Reject if consent is bypassed.

---

# 6. Provenance Validation

Every health record must be traceable.

Questions:

[ ] Is source recorded?

[ ] Is connector recorded?

[ ] Is import time recorded?

[ ] Is identifier retained?

[ ] Is provenance available for auditing?

Reject if provenance is missing.

---

# 7. Privacy First Validation

Questions:

[ ] Does this feature expose health data externally?

[ ] Is data minimization applied?

[ ] Is data sharing explicit?

[ ] Is user control preserved?

[ ] Can the feature run locally?

Reject if privacy is reduced.

---

# 8. Local First Validation

Questions:

[ ] Can the feature operate locally?

[ ] Is cloud usage optional?

[ ] Can the user self-host?

[ ] Is offline operation possible?

Reject if cloud becomes mandatory.

---

# 9. Security Validation

Questions:

[ ] Is data encrypted at rest?

[ ] Is data encrypted in transit?

[ ] Are secrets stored securely?

[ ] Are audit logs preserved?

[ ] Are permissions enforced?

Required technologies:

- AES-256-GCM
- Argon2
- RBAC
- MFA support

Reject if security weakens.

---

# 10. Internationalization Validation

LifeLedger must never become English-only.

Questions:

[ ] Are all UI strings translatable?

[ ] Are translation keys used?

[ ] Are date formats locale aware?

[ ] Are number formats locale aware?

[ ] Are notifications localizable?

[ ] Are AI prompts language aware?

Reject if hardcoded language appears.

---

# 11. Vendor Neutrality Validation

Questions:

[ ] Is implementation provider agnostic?

[ ] Can provider be replaced?

[ ] Is there lock-in?

[ ] Are open standards preferred?

Reject if vendor lock-in increases.

---

# 12. AI Agnostic Validation

Questions:

[ ] Can the feature work with OpenAI?

[ ] Anthropic?

[ ] Gemini?

[ ] Grok?

[ ] Ollama?

[ ] Future providers?

Reject if implementation depends on a single provider.

---

# 13. MCP Validation

Questions:

[ ] MCP compatibility preserved?

[ ] MCP resources documented?

[ ] Agent interoperability maintained?

Reject if MCP support is reduced.

---

# 14. Companion App Validation

Questions:

[ ] Flutter compatibility maintained?

[ ] Offline support preserved?

[ ] Sync architecture respected?

[ ] OCR architecture respected?

Reject if mobile architecture diverges.

---

# 15. Home Assistant Validation

Questions:

[ ] Integration remains optional?

[ ] No Home Assistant dependency introduced?

[ ] APIs remain platform-neutral?

Reject if Home Assistant becomes required.

---

# 16. Documentation Validation

Questions:

[ ] Documentation updated?

[ ] ADR required?

[ ] RFC required?

[ ] Architecture diagrams impacted?

[ ] Specifications impacted?

Reject if implementation changes documentation but documentation is not updated.

---

# 17. Repository Structure Validation

Questions:

[ ] Correct location selected?

[ ] No duplicate functionality introduced?

[ ] No architectural boundary violated?

Verify:

platform/
specifications/
plugins/
integrations/
docs/

Reject if boundaries are crossed.

---

# 18. Future Maintainability

Questions:

[ ] Is the solution understandable?

[ ] Is it testable?

[ ] Is it replaceable?

[ ] Is it extensible?

[ ] Is it observable?

Reject if technical debt exceeds benefit.

---

# Final Architecture Decision

If any answer results in:

- FHIR bypass
- Consent bypass
- Provenance bypass
- Privacy reduction
- Local First violation
- Security regression
- Vendor lock-in
- Hardcoded localization

the change shall not be approved.

Create ADR or RFC instead.

---

# Architecture Review Result

Architecture Review Completed:

[ ] PASS

[ ] PASS WITH ADR

[ ] PASS WITH RFC

[ ] REJECTED

Reviewer:

____________________

Date:

____________________
