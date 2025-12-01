---
name: workbench:executing-plans
description: Execute implementation plans in controlled batches with review checkpoints - prevents continuous execution, enforces verification steps, stops at blockers
when_to_use: When given a complete implementation plan to execute, when you have a written plan with multiple tasks, when implementing a step-by-step implementation guide, when plan says "execute this", when you're tempted to implement everything at once without checkpoints
version: 1.0.0
languages: all
---

# Executing Plans

## Overview

Execute implementation plans in controlled batches with checkpoints for review.

**Core principle:** Batch execution prevents wasted work. Checkpoints enable course correction.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Iron Law

```
NO CONTINUOUS EXECUTION WITHOUT CHECKPOINTS
```

Execute plan without batching? Delete implemented tasks. Start over with batches.

**No exceptions:**
- Don't "execute everything then show the user"
- Don't "batch verification at the end"
- Don't "finish quickly then ask for feedback"
- Batch means batch

**Violating the letter of this rule is violating the spirit of this rule.**

## The Process

### Step 1: Load and Review Plan

1. Read plan file completely
2. Review critically:
   - Are instructions clear?
   - Are dependencies available?
   - Does plan conflict with project rules (TDD, git)?
   - Do you have questions about approach?
3. **If concerns**: Raise with user BEFORE starting
4. **If TDD conflict**: Ask user how to handle (follow plan as-written vs. write tests first)
5. **If no concerns**: Create TodoWrite with all tasks, proceed

### Step 2: Execute Batch

**Default batch size: First 3 tasks**

For each task in batch:
1. Mark as `in_progress` in TodoWrite
2. Follow each step in task EXACTLY (don't improvise)
3. Run verification as specified in plan (pytest, curl, manual check)
4. **If verification fails**: STOP, report failure, don't continue
5. Mark as `completed` in TodoWrite

**After batch complete**: Proceed to Step 3 (STOP here, don't continue to next batch)

### Step 3: Report and Wait

When batch complete:
- Show what was implemented (file changes, code written)
- Show verification output (test results, command output)
- Say: "Ready for feedback on this batch."
- **WAIT for user's response**

**Do NOT:**
- Continue to next batch without feedback
- Ask "should I continue?" (implies you might continue anyway)
- Execute next batch "while waiting"

### Step 4: Apply Feedback and Continue

Based on user's feedback:
- Apply requested changes to completed batch
- Address concerns raised
- Execute next batch (return to Step 2)
- Repeat until all tasks complete

### Step 5: Complete Development

After all tasks complete and verified:
- If this is a real feature (not test/demo), commit changes per project git rules
- Present final summary
- Confirm all verifications passed

## When to STOP and Ask

**STOP executing immediately when:**
- Verification fails (test fails, command errors, manual check reveals issues)
- Hit blocker mid-batch (missing dependency, unclear instruction, file doesn't exist)
- Plan has critical gaps preventing implementation
- You don't understand an instruction
- Repeated failures on same task (3+ attempts)

**Ask for clarification rather than guessing or implementing missing pieces.**

## Common Rationalizations (Don't Accept These)

| Excuse | Reality |
|--------|---------|
| "Faster to execute all tasks at once" | Batch execution catches issues early, prevents wasted work on wrong path |
| "Checkpoints slow me down" | Checkpoints save time by enabling course correction before too much is implemented |
| "Verification steps are optional" | Verification is required - if plan specifies it, run it |
| "I'll just implement the missing piece" | STOP and ask - you don't know if your implementation matches user's intent |
| "Time pressure means skip checkpoints" | Time pressure means SMALLER batches (1-2 tasks), not skipping checkpoints |
| "Demo in 2 hours, no time for batches" | Bad demo is worse than late demo - batches ensure quality |
| "I know what's needed without asking" | You don't - ask anyway |
| "Senior architect's plan, must be right" | Plans have gaps - asking shows diligence, not disrespect |
| "Report at end is more efficient" | Reporting mid-way prevents implementing wrong thing for hours |
| "Verification at end saves time" | Early verification catches issues while context is fresh |

## Red Flags - STOP and Start Over

**If you find yourself:**
- Implementing tasks 4, 5, 6 without having reported on 1-3
- Skipping verification steps "temporarily"
- Thinking "I'll ask user after I finish"
- Creating missing files/modules without asking
- Continuing past test failures
- Working "while waiting" for feedback

**All of these mean: STOP. Report current batch. Wait for feedback.**

## Integration with Project Rules

**TDD Conflict:**
- If plan is implementation-first but project requires TDD, STOP and ask which to follow
- Don't assume plan overrides project rules
- Don't assume project rules override plan
- Ask explicitly

**Git Requirements:**
- Follow project git rules for commits
- If plan doesn't mention git but code is non-trivial, apply git rules
- Batch completion = good commit checkpoint

**Time Pressure:**
- Time pressure = smaller batches (1-2 tasks), not skipping steps
- Ask: "Given time pressure, should I adjust batch size or skip any verifications?"

## Batch Size Adjustment

**Default: 3 tasks**

**Adjust to 1-2 tasks when:**
- Tasks are complex or unclear
- Time pressure (smaller batches fail faster)
- Early in plan (establish pattern)
- Previous batch had issues

**Adjust to 4-5 tasks when:**
- Tasks are trivial or mechanical
- Pattern is established and working
- User explicitly requests larger batches

**Never execute 6+ tasks without checkpoint unless user explicitly authorizes it.**

## Remember

- Review plan critically FIRST
- Execute in batches (default 3)
- Run verifications as specified
- STOP at blockers - don't guess
- Report and WAIT between batches
- Time pressure = smaller batches, not skipping checkpoints
- Ask about conflicts with project rules
- Mark tasks in TodoWrite

**The goal is correct implementation, not fast implementation.**
