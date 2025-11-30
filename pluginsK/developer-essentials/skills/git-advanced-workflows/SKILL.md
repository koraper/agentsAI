---
name: git-advanced-workflows
description: 마스터 고급 Git 워크플로우 포함하여 rebasing, cherry-picking, bisect, worktrees, 및 reflog 에 maintain clean history 및 recover 에서 어떤 상황. Use 때 managing 복잡한 Git histories, collaborating 에 기능 branches, 또는 문제 해결 저장소 이슈.
---

# Git 고급 워크플로우

마스터 고급 Git techniques 에 maintain clean history, collaborate effectively, 및 recover 에서 어떤 상황 와 함께 confidence.

## 때 에 Use This Skill

- 정리 up 커밋 history 이전 병합하는
- Applying 특정 commits 전반에 걸쳐 branches
- 찾는 commits 것 introduced 버그
- 작업 에 여러 기능 동시에
- Recovering 에서 Git mistakes 또는 lost commits
- Managing 복잡한 branch 워크플로우
- Preparing clean PRs 위한 review
- Synchronizing diverged branches

## 핵심 개념

### 1. Interactive Rebase

Interactive rebase is the Swiss Army knife of Git history editing.

**일반적인 작업:**
- `pick`: Keep 커밋 처럼-is
- `reword`: 변경 커밋 메시지
- `edit`: Amend 커밋 콘텐츠
- `squash`: Combine 와 함께 이전 커밋
- `fixup`: 같은 squash 그러나 discard 메시지
- `drop`: Remove 커밋 전적으로

**기본 Usage:**
```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Rebase all commits on current branch
git rebase -i $(git merge-base HEAD main)

# Rebase onto specific commit
git rebase -i abc123
```

### 2. Cherry-Picking

Apply 특정 commits 에서 one branch 에 another 없이 병합하는 entire branches.

```bash
# Cherry-pick single commit
git cherry-pick abc123

# Cherry-pick range of commits (exclusive start)
git cherry-pick abc123..def456

# Cherry-pick without committing (stage changes only)
git cherry-pick -n abc123

# Cherry-pick and edit commit message
git cherry-pick -e abc123
```

### 3. Git Bisect

바이너리 search 통해 커밋 history 에 find the 커밋 것 introduced a 버그.

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v1.0.0

# Git will checkout middle commit - test it
# Then mark as good or bad
git bisect good  # or: git bisect bad

# Continue until bug found
# When done
git bisect reset
```

**자동화된 Bisect:**
```bash
# Use script to test automatically
git bisect start HEAD v1.0.0
git bisect run ./test.sh

# test.sh should exit 0 for good, 1-127 (except 125) for bad
```

### 4. Worktrees

Work 에 여러 branches 동시에 없이 stashing 또는 switching.

```bash
# List existing worktrees
git worktree list

# Add new worktree for feature branch
git worktree add ../project-feature feature/new-feature

# Add worktree and create new branch
git worktree add -b bugfix/urgent ../project-hotfix main

# Remove worktree
git worktree remove ../project-feature

# Prune stale worktrees
git worktree prune
```

### 5. Reflog

Your safety net - 추적합니다 모든 ref movements, 심지어 deleted commits.

```bash
# View reflog
git reflog

# View reflog for specific branch
git reflog show feature/branch

# Restore deleted commit
git reflog
# Find commit hash
git checkout abc123
git branch recovered-branch

# Restore deleted branch
git reflog
git branch deleted-branch abc123
```

## Practical 워크플로우

### 워크플로우 1: Clean Up 기능 Branch 이전 PR

```bash
# Start with feature branch
git checkout feature/user-auth

# Interactive rebase to clean history
git rebase -i main

# Example rebase operations:
# - Squash "fix typo" commits
# - Reword commit messages for clarity
# - Reorder commits logically
# - Drop unnecessary commits

# Force push cleaned branch (safe if no one else is using it)
git push --force-with-lease origin feature/user-auth
```

### 워크플로우 2: Apply Hotfix 에 여러 릴리스

```bash
# Create fix on main
git checkout main
git commit -m "fix: critical security patch"

# Apply to release branches
git checkout release/2.0
git cherry-pick abc123

git checkout release/1.9
git cherry-pick abc123

# Handle conflicts if they arise
git cherry-pick --continue
# or
git cherry-pick --abort
```

### 워크플로우 3: Find 버그 Introduction

```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good v2.1.0

# Git checks out middle commit - run tests
npm test

# If tests fail
git bisect bad

# If tests pass
git bisect good

# Git will automatically checkout next commit to test
# Repeat until bug found

# Automated version
git bisect start HEAD v2.1.0
git bisect run npm test
```

### 워크플로우 4: Multi-Branch 개발

```bash
# Main project directory
cd ~/projects/myapp

# Create worktree for urgent bugfix
git worktree add ../myapp-hotfix hotfix/critical-bug

# Work on hotfix in separate directory
cd ../myapp-hotfix
# Make changes, commit
git commit -m "fix: resolve critical bug"
git push origin hotfix/critical-bug

# Return to main work without interruption
cd ~/projects/myapp
git fetch origin
git cherry-pick hotfix/critical-bug

# Clean up when done
git worktree remove ../myapp-hotfix
```

### 워크플로우 5: Recover 에서 Mistakes

```bash
# Accidentally reset to wrong commit
git reset --hard HEAD~5  # Oh no!

# Use reflog to find lost commits
git reflog
# Output shows:
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: my important changes

# Recover lost commits
git reset --hard def456

# Or create branch from lost commit
git branch recovery def456
```

## 고급 Techniques

### Rebase vs Merge 전략

**때 에 Rebase:**
- 정리 up 로컬 commits 이전 pushing
- Keeping 기능 branch 최신 와 함께 main
- 생성하는 linear history 위한 easier review

**때 에 Merge:**
- Integrating 완료됨 기능 into main
- Preserving exact history of collaboration
- 공개 branches used 에 의해 others

```bash
# Update feature branch with main changes (rebase)
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# Handle conflicts
git status
# Fix conflicts in files
git add .
git rebase --continue

# Or merge instead
git merge origin/main
```

### Autosquash 워크플로우

Automatically squash fixup commits 동안 rebase.

```bash
# Make initial commit
git commit -m "feat: add user authentication"

# Later, fix something in that commit
# Stage changes
git commit --fixup HEAD  # or specify commit hash

# Make more changes
git commit --fixup abc123

# Rebase with autosquash
git rebase -i --autosquash main

# Git automatically marks fixup commits
```

### 분할된 커밋

Break one 커밋 into 여러 논리적인 commits.

```bash
# Start interactive rebase
git rebase -i HEAD~3

# Mark commit to split with 'edit'
# Git will stop at that commit

# Reset commit but keep changes
git reset HEAD^

# Stage and commit in logical chunks
git add file1.py
git commit -m "feat: add validation"

git add file2.py
git commit -m "feat: add error handling"

# Continue rebase
git rebase --continue
```

### 부분 Cherry-Pick

Cherry-pick 오직 특정 파일 에서 a 커밋.

```bash
# Show files in commit
git show --name-only abc123

# Checkout specific files from commit
git checkout abc123 -- path/to/file1.py path/to/file2.py

# Stage and commit
git commit -m "cherry-pick: apply specific changes from abc123"
```

## 최선의 관행

1. **항상 Use --force-와 함께-lease**: Safer 보다 --force, 방지합니다 overwriting others' work
2. **Rebase 오직 로컬 Commits**: Don't rebase commits 것 have been pushed 및 shared
3. **Descriptive 커밋 메시지**: 미래 you will thank 현재 you
4. **원자적 Commits**: 각 커밋 should be a single 논리적인 변경
5. **Test 이전 Force Push**: Ensure history rewrite didn't break anything
6. **Keep Reflog Aware**: Remember reflog is your safety net 위한 90 days
7. **Branch 이전 Risky 작업**: Create 백업 branch 이전 복잡한 rebases

```bash
# Safe force push
git push --force-with-lease origin feature/branch

# Create backup before risky operation
git branch backup-branch
git rebase -i main
# If something goes wrong
git reset --hard backup-branch
```

## 일반적인 Pitfalls

- **Rebasing 공개 Branches**: Causes history conflicts 위한 collaborators
- **Force Pushing 없이 Lease**: Can overwrite teammate's work
- **Losing Work 에서 Rebase**: Resolve conflicts 신중하게, test 이후 rebase
- **Forgetting Worktree Cleanup**: Orphaned worktrees consume 디스크 공간
- **Not Backing Up 이전 Experiment**: 항상 create safety branch
- **Bisect 에 Dirty 작업 디렉터리**: 커밋 또는 stash 이전 bisecting

## 복구 명령

```bash
# Abort operations in progress
git rebase --abort
git merge --abort
git cherry-pick --abort
git bisect reset

# Restore file to version from specific commit
git restore --source=abc123 path/to/file

# Undo last commit but keep changes
git reset --soft HEAD^

# Undo last commit and discard changes
git reset --hard HEAD^

# Recover deleted branch (within 90 days)
git reflog
git branch recovered-branch abc123
```

## 리소스

- **참조/git-rebase-가이드.md**: Deep dive into interactive rebase
- **참조/git-conflict-해결.md**: 고급 conflict 해결 strategies
- **참조/git-history-rewriting.md**: Safely rewriting Git history
- **자산/git-워크플로우-checklist.md**: Pre-PR cleanup checklist
- **자산/git-aliases.md**: Useful Git aliases 위한 고급 워크플로우
- **스크립트/git-clean-branches.sh**: Clean up 병합됨 및 stale branches
