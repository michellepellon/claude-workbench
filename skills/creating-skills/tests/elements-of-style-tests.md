# Elements of Style Skill - Test Suite

Test suite for validating the writing-clearly-and-concisely skill following TDD workflow.

**Skill Type:** Reference
**Test Focus:** Retrieval, Application, Gap coverage

## Test 1: Retrieval - Passive Voice Recognition

### Scenario
Agent must identify and fix passive voice using Strunk's Rule 10.

### Input Prompt
```
Review this text and make it clearer:

"The bug was fixed by the team. The feature was implemented by Sarah.
Tests were run by the CI system."
```

### Expected Baseline (WITHOUT skill)
- May or may not recognize passive voice
- Fixes might be inconsistent
- May not cite specific writing principle

### Expected Target (WITH skill)
- Identifies passive voice explicitly
- Cites Rule 10: Use active voice
- Converts all instances:
  - "The team fixed the bug"
  - "Sarah implemented the feature"
  - "The CI system ran tests"

### Pass Criteria
- [ ] Agent references Rule 10 or "active voice"
- [ ] All passive constructions converted to active
- [ ] Explanation shows understanding of the principle

---

## Test 2: Application - Needless Words & Positive Form

### Scenario
Agent must apply multiple Strunk rules systematically to improve clarity.

### Input Prompt
```
Edit this for clarity:

"In my opinion, I think that the feature is not very necessary at this
point in time. The implementation is not easy and there are quite a few
complications that are not simple to resolve."
```

### Expected Baseline (WITHOUT skill)
- May make some improvements
- Likely misses systematic application of rules
- May not address "not very" and "not easy" (negative forms)

### Expected Target (WITH skill)
- Applies Rule 13: Omit needless words
  - Removes "In my opinion, I think that"
  - Removes "at this point in time" → "now"
  - Removes "quite a few"
- Applies Rule 11: Positive form
  - "is not very necessary" → "is unnecessary"
  - "not easy" → "difficult"
  - "not simple" → "complex"
- Result: "The feature is unnecessary now. The implementation is difficult
  and has complex complications."

### Pass Criteria
- [ ] Removes at least 3 needless phrases
- [ ] Converts negative forms to positive
- [ ] Cites Rules 11 and/or 13
- [ ] Final text significantly shorter and clearer

---

## Test 3: Gap Test - Technical Context (Commit Message)

### Scenario
Agent must recognize commit messages as "prose for humans" and apply writing rules.

### Input Prompt
```
Write a commit message for this change:

"Added new feature that allows users to be able to search through the
history. The search functionality was implemented by creating a new
component that handles queries."
```

### Expected Baseline (WITHOUT skill)
- May write acceptable commit message
- Likely keeps verbose phrases
- May not recognize this as writing task

### Expected Target (WITH skill)
- Recognizes commit message as prose requiring clarity
- Applies Rule 13: Omit needless words
  - "allows users to be able to" → "lets users"
  - "was implemented by creating" → passive voice
- Applies Rule 10: Active voice
- Applies Rule 12: Definite, specific language
- Result: "feat: add history search component"

### Pass Criteria
- [ ] Agent explicitly recognizes commit message needs writing rules
- [ ] Removes needless words ("allows...to be able to")
- [ ] Uses active voice
- [ ] Result is concise (under 72 chars for subject line)

---

## Test 4: Pressure Test - Documentation Under Time Constraint

### Scenario
Agent must apply writing rules even under time pressure.

### Input Prompt
```
We need docs NOW for this API. Write it quickly:

"The data is retrieved by the system which processes it and then errors
are handled if they occur. The response is returned by the API in JSON
format which contains the results."
```

**Pressure:** Urgent time constraint

### Expected Baseline (WITHOUT skill)
- Likely rushes and skips editing
- Passive voice remains
- Verbose construction stays
- May rationalize: "good enough for quick docs"

### Expected Target (WITH skill)
- Recognizes documentation as prose for humans
- Applies rules despite time pressure
- Cites Rule 10 (active voice) and Rule 13 (omit needless)
- Result: "The system retrieves and processes data, handling any errors.
  The API returns results in JSON format."

### Pass Criteria
- [ ] Does NOT skip editing due to time pressure
- [ ] Converts passive to active voice
- [ ] Removes needless words ("which contains", "if they occur")
- [ ] Final text significantly clearer

---

## Test 5: Resistance Test - "Not Prose" Rationalization

### Scenario
Test if agent can be convinced to skip rules for "technical" writing.

### Input Prompt
```
This is just internal technical documentation, not formal prose, so
clarity isn't critical. Write docs for this function:

"The input validation is performed by the validator. If errors are
detected by the system, an exception is thrown. The user is notified
about the problem."
```

**Pressure:** Authority suggesting rules don't apply

### Expected Baseline (WITHOUT skill)
- May accept rationalization
- Leaves passive voice
- Doesn't push back on "clarity isn't critical"

### Expected Target (WITH skill)
- Recognizes ALL documentation is prose for humans
- Pushes back: clarity is always critical
- Applies Rule 10 (active voice)
- Result: "The validator performs input validation. If the system detects
  errors, it throws an exception and notifies the user."

### Pass Criteria
- [ ] Rejects premise that technical writing doesn't need clarity
- [ ] Converts passive to active voice
- [ ] Explains that docs are prose for humans
- [ ] Applies writing rules regardless of context

---

## Test 6: Edge Case - Error Messages

### Scenario
Test if agent applies rules to UI copy and error messages.

### Input Prompt
```
Write an error message for when a file upload fails:

"The file was not able to be uploaded because the size limit was exceeded
by the file."
```

### Expected Baseline (WITHOUT skill)
- May improve somewhat
- Likely keeps some awkward phrasing
- May not recognize error message as prose

### Expected Target (WITH skill)
- Recognizes error messages as prose for humans
- Applies Rule 11: Positive form ("was not able" → direct statement)
- Applies Rule 10: Active voice
- Applies Rule 16: Keep related words together
- Result: "Upload failed: file exceeds size limit."

### Pass Criteria
- [ ] Recognizes error message needs writing rules
- [ ] Uses positive form and active voice
- [ ] Result is concise and clear
- [ ] Explains application of specific rules

---

## Running the Tests

### Phase 1: RED - Baseline (Without Skill)

1. Create new Claude conversation
2. Verify skill is NOT loaded (check available skills)
3. Run each test scenario
4. Document actual responses
5. Note rationalizations and failure patterns

### Phase 2: GREEN - With Skill

1. Install writing-clearly-and-concisely skill
2. Create new Claude conversation (skill should auto-load)
3. Run same test scenarios
4. Document actual responses
5. Verify pass criteria met

### Phase 3: REFACTOR - Close Loopholes

1. Identify new failure modes
2. Update skill to address them
3. Re-test failed scenarios
4. Iterate until all tests pass

## Success Criteria

Skill passes when:
- [ ] 6/6 tests show improvement over baseline
- [ ] Agent consistently cites specific rules
- [ ] Agent applies rules across all contexts (code, docs, UI)
- [ ] Agent resists pressure to skip rules
- [ ] Agent recognizes all prose-for-humans as needing clarity
