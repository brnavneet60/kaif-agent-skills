---
name: licensing-analysis
description: >-
  Assess software licensing and supply-chain obligations for every component in
  the architecture — OSS license class, copyleft reach, commercial/dual
  licensing, compatibility, and compliance risk — and recommend a posture. Use
  when the design depends on third-party or open-source software. Ties to SBOM
  and supply-chain security.
---

# Licensing analysis

## Purpose

Prevent a legal/compliance surprise late in delivery. For a CTO audience,
translate license obligations into business risk and a clear posture per
component. Licensing is fact-sensitive and version-sensitive — verify, do not
recall.

## When to use

- The architecture uses any OSS, third-party library, managed service, or model
  with usage terms.
- Build-vs-buy or "can we embed/redistribute this?" questions arise.

## License classes (orientation, not legal advice)

| Class | Examples | Obligation shape | Typical risk for SaaS |
|---|---|---|---|
| Permissive | MIT, BSD, Apache-2.0 | Attribution; Apache adds patent grant | Low |
| Weak copyleft | MPL-2.0, LGPL, EPL | Share changes to the licensed files | Low–medium |
| Strong copyleft | GPLv3 | Derivative works must be GPL | Medium (linking) |
| Network copyleft | AGPLv3, SSPL | Triggers on network use / offering as a service | **High for SaaS** |
| Source-available / BSL | BSL 1.1, Elastic, Confluent | Time/again-use restrictions; not OSI-OSS | Medium–high |
| Commercial / dual | Vendor EULA, open-core | Per-seat/usage terms; feature gating | Contract-dependent |

> AGPL/SSPL and BSL are the usual traps for a hosted product. Confirm the exact
> license **and version** of each component before relying on this table.

## Instructions

1. **Inventory components** from `solution-architecture` and
   `technology-evaluation` — every OSS lib, service, database, and model.
2. **Identify the exact license and version** for each via
   `discovery-research` (repo `LICENSE` file, release notes). Date-stamp it;
   projects relicense (e.g. several DBs moved to BSL/SSPL).
3. **Classify obligations** and, critically, **how the component is used**:
   linked/embedded vs called over a network vs modified-and-distributed vs
   offered-as-a-service. The same license implies different obligations by usage.
4. **Flag conflicts:** strong/network copyleft in a proprietary/SaaS product;
   incompatible license combinations; source-available terms that restrict a
   hosted offering.
5. **Check the supply chain:** recommend an SBOM (CycloneDX/SPDX), signed images
   (cosign), and license-scanning in CI. Note this as a control, aligned with
   KAIF supply-chain practices.
6. **Recommend a posture per component:** adopt / adopt-with-conditions /
   replace / seek-commercial-license / legal-review-required. Escalate genuine
   legal questions to counsel — this skill informs, it is not legal sign-off.

## Output contract

A `## Licensing & Supply-Chain` section:

- Component license inventory: component → license (+version, as-of) → usage
  mode → obligation → risk (H/M/L) → posture.
- Conflicts & flags: any copyleft/source-available issues for this deployment
  model, called out plainly.
- Supply-chain controls: SBOM, image signing, CI license scan (recommended).
- Recommendation: overall licensing posture + any items needing legal review.

## Quality checks

- [ ] Every component has an exact license + version, date-stamped, with source.
- [ ] Usage mode (linked / network / distributed / SaaS) is stated per item —
      not just the license name.
- [ ] AGPL/SSPL/BSL components are explicitly flagged against the deployment
      model.
- [ ] SBOM + signing + CI scan are recommended as controls.
- [ ] Genuine legal questions are marked `legal-review-required`, not answered as
      fact. This is analysis, not legal advice.
