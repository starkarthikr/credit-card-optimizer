# 🔒 Branch Protection Configuration Template

**Purpose**: Secure your `main` branch against unauthorized changes  
**Difficulty**: Easy  
**Time Required**: 15 minutes per repository  
**Impact**: HIGH - Prevents force pushes, requires code review

---

## 🎯 Why Branch Protection?

**Without protection:**
- ❌ Anyone with write access can force push
- ❌ No code review requirements
- ❌ Failed CI checks can be ignored
- ❌ Accidental deletions possible
- ❌ Commit history can be rewritten

**With protection:**
- ✅ Requires pull request reviews
- ✅ CI must pass before merge
- ✅ Prevents force pushes
- ✅ Prevents branch deletion
- ✅ Enforces for administrators too

---

## 🛠️ Configuration Steps

### Step 1: Access Branch Settings

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Click **Branches** (left sidebar)
4. Click **Add branch protection rule**

**Direct Links:**
- [credit-card-optimizer](https://github.com/starkarthikr/credit-card-optimizer/settings/branches)
- [General-cybersecurity-news](https://github.com/starkarthikr/General-cybersecurity-news/settings/branches)
- [crowdstrike-latest-news](https://github.com/starkarthikr/crowdstrike-latest-news/settings/branches)

---

### Step 2: Branch Name Pattern

**Field**: Branch name pattern  
**Value**: `main`

*This applies the rule to your main branch*

---

### Step 3: Protect Matching Branches

#### ✅ **REQUIRED**: Enable These Settings

##### 1. Require a pull request before merging
- [x] **Require a pull request before merging**
  - [x] **Require approvals**: 1 (minimum)
  - [x] **Dismiss stale pull request approvals when new commits are pushed**
  - [x] **Require review from Code Owners** (if CODEOWNERS file exists)

**Why**: Ensures code review before changes reach main

##### 2. Require status checks to pass before merging
- [x] **Require status checks to pass before merging**
  - [x] **Require branches to be up to date before merging**
  - Select checks to require:
    - [x] CodeQL
    - [x] Dependency Review
    - [x] Security Scan (if applicable)
    - [x] Main workflow (card-optimizer, security-monitor, etc.)

**Why**: Ensures CI/CD passes and code is tested

##### 3. Require conversation resolution before merging
- [x] **Require conversation resolution before merging**

**Why**: All review comments must be addressed

##### 4. Require signed commits (Optional but Recommended)
- [ ] **Require signed commits**

**Why**: Verifies commit author authenticity  
**Note**: Requires GPG setup (see SECURITY.md)

##### 5. Require linear history (Optional)
- [ ] **Require linear history**

**Why**: Prevents merge commits, enforces rebase  
**Note**: May complicate workflows, enable if you prefer rebase

##### 6. Include administrators
- [x] **Include administrators**

**Why**: Rules apply to everyone, even repository owners  
**Critical**: Prevents accidental force pushes by admins

##### 7. Restrict who can push to matching branches (Optional)
- [ ] **Restrict who can push to matching branches**

**Why**: Limits who can push directly  
**Note**: For team repos, specify allowed users/teams

##### 8. Allow force pushes
- [ ] **Allow force pushes** (KEEP UNCHECKED)

**Why**: Force pushes can rewrite history and cause data loss

##### 9. Allow deletions
- [ ] **Allow deletions** (KEEP UNCHECKED)

**Why**: Prevents accidental branch deletion

---

### Step 4: Rules Applied to Everyone

#### ✅ Additional Protection

##### 1. Require deployments to succeed before merging (Optional)
- [ ] **Require deployments to succeed before merging**

**Why**: If you have deployment workflows, ensure they succeed  
**Note**: Only enable if you have deployment environments configured

##### 2. Lock branch (Use with Caution)
- [ ] **Lock branch**

**Why**: Makes branch read-only, prevents all changes  
**Note**: Only use for archived/frozen branches

---

### Step 5: Save Configuration

1. Scroll to bottom
2. Click **Create** button
3. Verify green checkmark appears
4. Test by attempting a direct push (should fail)

---

## ✅ Recommended Configuration Summary

**For Solo Developer (You):**
```yaml
Branch: main

Required:
☑️ Require pull request reviews (1 approval)
☑️ Require status checks to pass
☑️ Require conversation resolution
☑️ Include administrators
☐ Allow force pushes (DISABLED)
☐ Allow deletions (DISABLED)

Optional:
☐ Require signed commits (enable after GPG setup)
☐ Require linear history (if you prefer rebase workflow)
```

**For Team Repositories:**
```yaml
Branch: main

Required:
☑️ Require pull request reviews (2+ approvals)
☑️ Dismiss stale reviews on new commits
☑️ Require status checks to pass
☑️ Require branches up to date
☑️ Require conversation resolution
☑️ Include administrators
☑️ Restrict who can push (specify team)
☑️ Require signed commits
☐ Allow force pushes (DISABLED)
☐ Allow deletions (DISABLED)
```

---

## 🧪 Testing Your Configuration

### Test 1: Direct Push Should Fail

```bash
# Try to push directly to main (should fail)
echo "test" >> README.md
git add README.md
git commit -m "test: direct push"
git push origin main

# Expected output:
remote: error: GH006: Protected branch update failed for refs/heads/main.
```

### Test 2: PR Workflow Should Work

```bash
# Create feature branch
git checkout -b feature/test-branch-protection
echo "test" >> README.md
git add README.md
git commit -m "test: branch protection"
git push origin feature/test-branch-protection

# Create PR via GitHub UI
# Merge should be blocked until:
# - CI passes
# - 1 approval received
# - Conversations resolved
```

---

## 👥 Working with Branch Protection (Solo Developer)

### Workflow for Making Changes:

```bash
# 1. Create feature branch
git checkout -b feature/my-new-feature

# 2. Make changes
# ... edit files ...

# 3. Commit changes
git add .
git commit -m "feat: add new feature"

# 4. Push feature branch
git push origin feature/my-new-feature

# 5. Create Pull Request via GitHub
# - Go to repository
# - Click "Compare & pull request"
# - Add description
# - Click "Create pull request"

# 6. Wait for CI checks to pass
# - CodeQL scan
# - Dependency review
# - Any other configured checks

# 7. Self-review (or get teammate review)
# - Review the code
# - Click "Review changes" → "Approve"

# 8. Merge via GitHub UI
# - Click "Merge pull request"
# - Choose merge type (merge commit, squash, rebase)
# - Click "Confirm merge"

# 9. Pull updated main
git checkout main
git pull origin main

# 10. Delete feature branch
git branch -d feature/my-new-feature
git push origin --delete feature/my-new-feature
```

---

## ⚠️ Bypassing Protection (Emergency Only)

### When You Might Need to Bypass:
- Critical security hotfix
- Repository corruption recovery
- CI system is down

### How to Temporarily Bypass:

1. Go to Settings → Branches
2. Click **Edit** on your branch protection rule
3. Temporarily uncheck "Include administrators"
4. Make your emergency push
5. **IMMEDIATELY** re-enable "Include administrators"

**⚠️ WARNING**: Only use in genuine emergencies. Document why you bypassed.

---

## 📊 Benefits You'll See

### Security Benefits:
- ✅ No accidental force pushes
- ✅ All code is reviewed
- ✅ CI must pass before merge
- ✅ Audit trail of all changes
- ✅ Protection against account compromise

### Quality Benefits:
- ✅ Catch bugs before merge
- ✅ Knowledge sharing through reviews
- ✅ Consistent code quality
- ✅ Documentation through PR discussions

### Compliance Benefits:
- ✅ Meets security audit requirements
- ✅ Required for SOC 2, ISO 27001
- ✅ Demonstrates due diligence
- ✅ Traceable change history

---

## 📝 Configuration Checklist

### Per Repository:

- [ ] Accessed branch protection settings
- [ ] Created rule for `main` branch
- [ ] Enabled PR requirement (1 approval)
- [ ] Enabled status check requirement
- [ ] Selected required status checks
- [ ] Enabled conversation resolution
- [ ] Enabled "Include administrators"
- [ ] Disabled force pushes
- [ ] Disabled deletions
- [ ] Clicked "Create"
- [ ] Tested with dummy PR
- [ ] Documented configuration

### All Repositories:

- [ ] credit-card-optimizer configured
- [ ] General-cybersecurity-news configured
- [ ] crowdstrike-latest-news configured

---

## 🔗 Additional Resources

- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Best Practices for Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [Required Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)

---

**Created**: February 10, 2026  
**Owner**: @starkarthikr  
**Status**: Ready to implement  
**Priority**: HIGH - Complete within 1 week
