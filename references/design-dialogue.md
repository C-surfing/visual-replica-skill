# Design dialogue: keep the user in charge

## When starting with mixed inspirations

The user might say: "I like A's layout, B's restrained type, C's sidebar, but I don't want the result to look like a dashboard."

Do not treat these links as three identical target screenshots. Extract **transferable decisions**. For each reference identify (a) what the user pointed at, (b) why that quality matters for this product, (c) what not to copy, and (d) whether the user explicitly said it or the agent inferred it.

Then phrase one short agreement in non-technical language:

> We're aiming for a quiet working environment. The content should dominate. From A, we'll borrow the generous layout; from B, the clear headings; from C, the simple navigation. We'll avoid A's branding and C's busy color. Is the navigation meant to be nearly invisible, or should it remain easy to spot?

Ask only questions that affect the direction. Multiple-choice questionnaires and formulaic "choose a style" rituals are not required.

## During implementation

The first generated screen is a hypothesis, not confirmation. Recheck confirmed constraints before major changes. Revisit them after meaningful visual or interaction changes. Do not repeat the entire discovery process for a small tweak.

After inspecting the actual interface (using whatever visual tools the host already has), write:

> **Closer:** The main text now has more breathing room. **Still off:** The sidebar competes too much with the content. **Next:** Reduce its visual weight and check whether navigation remains discoverable.

Observations must describe real inspected results, not inferred code behavior. If you lack a view of the actual UI, say what is unverified and request one relevant input. Do not frame CSS or HTML tests as a substitute for taste judgment.

## When feedback contradicts the agreement

Do not automatically obey either the old contract or the agent's default aesthetic. Surface the conflict:

> Earlier we decided the navigation should be quiet. Your latest feedback suggests it needs to be more noticeable. Should that earlier choice change, or should we improve discoverability without increasing visual weight?

Only mark a changed constraint as user-confirmed with explicit user acceptance. Retain the old version so the difference is visible. Use `intent guard` if the project relies on the optional contract.

## When it should stop

Stop when the person has accepted the direction and remaining important problems are either resolved or honestly disclosed. An automated screenshot score is not an aesthetic stopping condition. A redesign may intentionally diverge from any single reference while satisfying the user's chosen mix.

## What should persist

Keep the few high-value choices, their rationale and source, recent meaningful feedback, and unresolved conflicts. Do not keep lengthy every-turn transcripts, incidental CSS values, dozens of generic design principles, or artificial aesthetic scores.

The purpose is **continuity of human judgment**, not a second visual design engine.
