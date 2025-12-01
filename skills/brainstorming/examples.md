# Brainstorming Examples

Complete examples of the brainstorming workflow in action.

## Example 1: Adding Authentication to Web App

### Context
User request: "I want to add user authentication to my web app"

### Phase 1: Understanding

**Agent:** I am using the brainstorming skill to refine your idea into a design.

Let me start by understanding your requirements. First question:

*Uses AskUserQuestion tool:*

**Question:** "Where should the authentication data be stored?"

**Options:**
- **Session storage**: Clears on tab close, more secure, requires re-login
- **Local storage**: Persists across sessions, more convenient, stays logged in
- **Cookies**: Works with SSR, compatible with existing approach, flexible expiry

**User selects:** Local storage

**Agent:** Got it. Next question - what authentication method?

*Uses AskUserQuestion tool:*

**Question:** "Which authentication method should we implement?"

**Options:**
- **Email/password**: Simple, familiar, need password reset flow
- **OAuth (Google/GitHub)**: Third-party, less maintenance, better UX
- **Magic links**: Passwordless, modern, email-dependent
- **Multi-factor**: Most secure, more complex, additional step

**User selects:** OAuth (Google/GitHub)

**Agent:** Understood. One more question about your current setup.

**Agent:** What backend framework are you currently using? (open-ended)

**User:** Express.js with MongoDB

**Summary gathered:**
- Purpose: Add user authentication
- Storage: Local storage
- Method: OAuth (Google/GitHub)
- Backend: Express.js with MongoDB
- Success criteria: Users can sign in and stay logged in

### Phase 2: Exploration

**Agent:** I'll propose three architectural approaches for implementing OAuth authentication:

*Uses AskUserQuestion tool:*

**Question:** "Which architectural approach should we use?"

**Options:**

- **Passport.js with OAuth strategies**
  - Pros: Mature library, many strategies, well-documented
  - Cons: Middleware-heavy, some boilerplate
  - Complexity: Medium

- **NextAuth.js (if using Next.js) or custom OAuth flow**
  - Pros: Modern, minimal config, supports multiple providers
  - Cons: Opinionated, less customization
  - Complexity: Low

- **Auth0 / Firebase Auth (managed service)**
  - Pros: Fully managed, handles everything, scales easily
  - Cons: External dependency, costs at scale, vendor lock-in
  - Complexity: Very Low

**User selects:** Passport.js with OAuth strategies

### Phase 3: Design Presentation

**Agent:** Here's the architecture design for Passport.js OAuth authentication:

**Section 1: Core Architecture**

We'll use Passport.js with passport-google-oauth20 and passport-github2 strategies. The auth flow:
1. User clicks "Sign in with Google/GitHub"
2. Backend redirects to OAuth provider
3. Provider redirects back with authorization code
4. Backend exchanges code for user profile
5. Store user in MongoDB, create session
6. Return JWT token to frontend
7. Frontend stores token in localStorage

Frontend makes authenticated requests with Authorization: Bearer <token> header.

Does this look right so far?

**User:** Yes, continue.

**Section 2: Components**

**Backend components:**
- `auth/strategies/google.js` - Google OAuth strategy config
- `auth/strategies/github.js` - GitHub OAuth strategy config
- `auth/controller.js` - Auth routes and callbacks
- `middleware/authenticate.js` - JWT verification middleware
- `models/User.js` - User schema with provider info

**Frontend components:**
- `components/LoginButton.js` - OAuth provider buttons
- `services/auth.js` - Token management, API calls
- `hooks/useAuth.js` - Authentication state hook
- `contexts/AuthContext.js` - Global auth state

Does this component breakdown make sense?

**User:** Yes, looks good.

**Section 3: Data Flow & Error Handling**

**Data stored:**
- User: `{ providerId, provider, email, name, avatar, createdAt }`
- JWT payload: `{ userId, email, iat, exp }`

**Error handling:**
- OAuth failure → Redirect to /login?error=auth_failed
- Token expired → 401, trigger refresh or re-login
- Invalid token → 401, clear localStorage, redirect to login
- Missing user → Create new user in DB

**Testing approach:**
- Unit: Test JWT generation/verification
- Integration: Test OAuth callbacks with mock providers
- E2E: Test full auth flow with test Google/GitHub accounts

Does this cover the important details?

**User:** Yes, this looks complete.

### Phase 4: Design Documentation

**Agent:** I'll write this design to `docs/plans/2025-10-23-oauth-authentication-design.md`.

*Agent uses writing-clearly-and-concisely skill to create clear documentation*

*Agent commits the design document*

### Phase 5: Worktree Setup

**Agent:** Ready to set up the implementation workspace?

**User:** Yes

**Agent:** I'm using the using-git-worktrees skill to set up an isolated workspace.

*Agent creates worktree, switches to it*

### Phase 6: Planning Handoff

**Agent:** Ready to create the implementation plan?

**User:** Yes

**Agent:** I'm using the writing-plans skill to create the implementation plan.

*Agent creates detailed implementation plan with task breakdown*

---

## Example 2: Going Backward When New Constraint Emerges

### Phase 2 in Progress

**Agent:** I've proposed three approaches for implementing real-time notifications...

**User:** Wait, I should mention - we're already using Socket.io for another feature.

**Agent:** That's an important constraint I didn't know about. Let me go back to Phase 1 to understand your existing setup.

*Returns to Phase 1*

**Agent:** What are you currently using Socket.io for?

**User:** Live chat feature

**Agent:** Got it. Do you want to reuse the same Socket.io connection for notifications?

*Uses AskUserQuestion tool...*

This pattern shows **flexibility over rigidity** - going backward when new information emerges.

---

## Example 3: Question Pattern Decision Flow

### Phase 1 Question - Use AskUserQuestion

**Situation:** Need to decide on data storage approach

**Why AskUserQuestion:**
- 3-4 distinct options
- Clear trade-offs for each
- Mutually exclusive choices

**Agent uses AskUserQuestion:**
```
Question: "How should we store the user preferences?"
Options:
  - "Database": Persistent, survives reinstall, requires backend
  - "Local files": Fast access, works offline, tied to device
  - "Cloud sync": Available everywhere, requires account, complexity
```

### Phase 3 Validation - Use Open-Ended

**Situation:** Validating data flow design

**Why open-ended:**
- Need detailed feedback
- User might have concerns not in structured options
- Validation, not decision

**Agent asks open-ended:**
"Does this data flow handle your use cases correctly? Any edge cases I'm missing?"

---

## Example 4: Using AskUserQuestion Effectively

### Good Example

```
Question: "Which testing framework should we use?"
Options:
  - "Jest": Most popular, great DX, snapshot testing
  - "Vitest": Fastest, Vite-native, ESM-first
  - "Mocha + Chai": Flexible, modular, more setup
```

**Why good:**
- Clear distinct options
- Concrete trade-offs
- Relevant to decision

### Bad Example

```
Question: "How should we test?"
Options:
  - "Thoroughly": Test everything
  - "Minimally": Test critical paths only
  - "Moderately": Balance coverage and time
```

**Why bad:**
- Vague options without concrete meaning
- No real architectural difference
- Doesn't help user make informed choice

---

## Example 5: When NOT to Use This Skill

### Bad: Trivial Implementation

**User:** "Can you add a console.log to this function?"

**Don't:** Launch brainstorming skill for trivial changes.

**Do:** Just add the console.log.

### Bad: User Has Complete Spec

**User:** "Implement user authentication using Passport.js with Google OAuth. Here's the exact flow: [detailed spec]"

**Don't:** Ask questions when requirements are crystal clear.

**Do:** Confirm you understand and proceed to implementation.

### Good: Rough Idea Needs Refinement

**User:** "I want users to be able to save their stuff"

**Do:** Launch brainstorming skill to refine into design.

---

## Example 6: Announcing Skill Usage

### Start of Session

**Agent:** I am using the brainstorming skill to refine your idea into a design.

**Why:** Sets expectations for the user that we'll be doing structured questioning and design before implementation.

### Transitioning to Sub-Skills

**Agent:** I'm using the writing-clearly-and-concisely skill for documentation quality.

**Agent:** I'm using the using-git-worktrees skill to set up an isolated workspace.

**Why:** Transparency about which process is being followed.

---

## See Also

- [SKILL.md](./SKILL.md) - Core workflow and principles
- [templates/progress-checklist.md](./templates/progress-checklist.md) - Track progress
