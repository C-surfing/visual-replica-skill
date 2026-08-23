---
name: visual-replica-skill-pro
description: Expert workflow for high fidelity UI reconstruction from screenshots, designs, and references. Guides coding agents to analyze, implement, verify, diagnose, and improve visual replicas.
---

# Visual Replica Skill Pro

## Role

Act as a senior frontend engineer specialized in visual reconstruction.

Your objective is not to create a beautiful new design.

Your objective is to reproduce the existing visual target faithfully while keeping production quality code.

---

# Fundamental Principle

Reference image = visual specification.

Rendered application = only reliable evidence.

Never claim success from code inspection alone.

---

# Workflow

## Step 0: Task Planning

Identify task type:

A. Existing project + reference image
- modify current implementation

B. Screenshot only
- create component architecture first

C. Multiple references
- extract shared design language

D. Responsive recreation
- infer layout rules, not fixed pixels only


---

# Step 1: Visual Analysis

Before coding, extract:

## Structure

- page regions
- hierarchy
- repeated components
- alignment relationships


## Geometry

Estimate:

- viewport
- container size
- margins
- padding
- gaps
- proportions


## Typography

Analyze:

- font size
- weight
- line height
- wrapping
- hierarchy


## Assets

Identify:

- images
- icons
- illustrations
- logos


Create:

visual-spec.json


---

# Step 2: Implementation

Order matters.

Always implement:

1. viewport and global container
2. macro layout
3. repeated components
4. asset placement
5. typography
6. colors
7. shadows and micro details


Do not tune shadows while layout is incorrect.

---

# Step 3: Verification Loop

Mandatory:

Implement
↓
Run application
↓
Capture screenshot
↓
Compare with reference
↓
Diagnose differences
↓
Apply minimal fix
↓
Repeat


---

# Step 4: Visual Diagnosis

Classify before editing.

## Global offset

Symptoms:
Everything shifted.

Check:

- viewport
- root container
- body margin
- safe area


## Vertical drift

Symptoms:
Top matches but bottom diverges.

Check:

- repeated spacing
- line height
- component height


## Typography mismatch

Symptoms:
Only text regions differ.

Check:

- font
- weight
- letter spacing


## Component mismatch

Symptoms:
Repeated elements all wrong.

Check:

- shared component
- tokens
- abstraction


---

# Step 5: Iteration Learning

Every significant iteration records:

Problem:
What differs?

Hypothesis:
Why?

Change:
What changed?

Result:
Did fidelity improve?


Only keep improvements.

Rollback regressions.

---

# Quality Gates

Before completion verify:

## Visual

- structure matches
- spacing matches
- typography is close
- assets are correct

## Engineering

- reusable components
- maintainable styles
- no screenshot hacks
- no excessive absolute positioning

## Validation

- real rendered screenshot checked
- differences documented


---

# Continuous Improvement

After completion:

Record:

- failure patterns
- successful fixes
- reusable UI patterns

Future tasks should benefit from previous experience.
