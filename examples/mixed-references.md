# Mixed references: an example of design intent continuity

A user requests a reading product: "I like the spacious composition of website A, the typography of website B, and the unobtrusive navigation of website C. Don't make this look like an analytics dashboard."

The agent should **not** try to pixel-match A, B and C simultaneously. It records what each contributes and why. An appropriate short agreement:

> We're making a calm reading workspace. The reading area is the visual priority. We'll borrow A's whitespace, B's readable hierarchy and C's quiet navigation. We won't copy their branding or create an analytics dashboard. The specific font is not yet settled.

The contract begins as a draft. It contains a `direction`, separate `references` entries with `borrow`, `not_copy`, `why`, and one or two important `intent.preserve` choices marked `agent-inferred` until the user actually confirms them.

**Round 1.** The agent builds an interface. The user says: "Still too much like a dashboard; the cards are fighting for attention." The agent records that quote (rather than inventing feedback), proposes reducing side panels, and keeps the reading area's priority intact.

A helpful response:

> The reading area is still crowded by secondary cards. Next I'd remove the redundant panels and make the content easier to scan. Your earlier choice of quiet navigation will stay as it is.

**Round 2.** The user now asks for a stronger sidebar. That may conflict with the previously approved quiet navigation. The agent explains the conflict and asks whether the existing decision should change, or whether discoverability can improve without changing the visual hierarchy.

Before replacing a confirmed constraint, the agent compares the previous and proposed contract. `visual-replica intent guard` identifies the change; it does not decide on the user's behalf.

Use browser screenshots only when they answer a concrete question about the outcome. Neither an optional test PASS nor a high similarity score counts as design approval.
