"""Exercise Git command contracts in disposable repositories, never the caller's repo."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class GitContracts(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="git-contracts-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()
        self.repo = self.root / "repo with spaces"
        self.repo.mkdir()
        # Isolate configuration/identity/protocols for synthetic fixture commits.
        # No existing repository config, hooks, credentials or external remotes run.
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_ALLOW_PROTOCOL": "file",
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
                "GIT_EDITOR": "true",
                "GIT_MERGE_AUTOEDIT": "no",
            }
        )
        self.git("init", "--initial-branch=main", "--template=", str(self.repo))
        self.git("config", "core.autocrlf", "false")
        self.write(".gitignore", "private/\n")
        self.write("task.txt", "base\n")
        self.write("other.txt", "base\n")
        self.git("add", "--", ".gitignore", "task.txt", "other.txt")
        self.git("commit", "-m", "chore: initialize fixture")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *args, cwd=None, ok=True):
        result = subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            env=self.env,
            text=True,
            encoding="utf-8",
            errors="strict",
            capture_output=True,
            timeout=30,
            check=False,
        )
        if ok and result.returncode:
            self.fail(f"git {args!r} failed: {result.stderr}")
        if not ok:
            self.assertNotEqual(result.returncode, 0, args)
        return result

    def write(self, name, value, root=None):
        path = (root or self.repo) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8", newline="\n")

    def commit(self, name, value):
        self.write(name, value)
        self.git("add", "--", name)
        self.git("commit", "-m", "fix: change fixture behavior")
        return self.git("rev-parse", "HEAD").stdout.strip()

    def test_scoped_commit_preserves_excluded_index_and_worktree(self):
        self.git("switch", "--no-track", "-c", "fix/scoped")
        self.write("other.txt", "user staged\n")
        self.git("add", "--", "other.txt")
        self.write("other.txt", "user staged plus unstaged\n")
        staged = self.git("show", ":other.txt").stdout
        staged_oid = self.git("rev-parse", ":other.txt").stdout
        working = (self.repo / "other.txt").read_bytes()
        self.write("task.txt", "verified fix\n")
        self.git("add", "--", "task.txt")
        # Explicit add does not make the whole index safe for a plain commit.
        self.assertEqual(
            set(self.git("diff", "--cached", "--name-only").stdout.splitlines()),
            {"task.txt", "other.txt"},
        )
        # A path-only commit is valid here because task.txt has no excluded hunks.
        self.git(
            "commit", "--only", "-m", "fix: preserve scoped changes", "--", "task.txt"
        )
        self.assertEqual(
            self.git(
                "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
            ).stdout.strip(),
            "task.txt",
        )
        self.assertEqual(self.git("show", ":other.txt").stdout, staged)
        self.assertEqual(self.git("rev-parse", ":other.txt").stdout, staged_oid)
        self.assertEqual((self.repo / "other.txt").read_bytes(), working)
        self.assertEqual(self.git("show", "HEAD:other.txt").stdout, "base\n")

    def test_branch_delete_success_does_not_prove_trunk_integration(self):
        remote = self.root / "remote.git"
        self.git("init", "--bare", "--initial-branch=main", "--template=", str(remote))
        self.git("remote", "add", "origin", str(remote))
        self.git("switch", "--no-track", "-c", "fix/unmerged")
        tip = self.commit("task.txt", "not on main\n")
        self.git("push", "-u", "origin", "HEAD:refs/heads/fix/unmerged")
        self.git("switch", "main")
        self.git("merge-base", "--is-ancestor", tip, "main", ok=False)
        self.git("branch", "-d", "fix/unmerged")
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)

    def test_fast_forward_refuses_divergence_without_changing_head(self):
        self.git("switch", "-c", "fix/incoming")
        self.commit("task.txt", "incoming\n")
        self.git("switch", "main")
        local = self.commit("other.txt", "local\n")
        self.git("merge", "--ff-only", "fix/incoming", ok=False)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), local)
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    def test_worktree_shares_refs_and_requires_ignored_data_inspection(self):
        path = self.root / "linked tree"
        self.git(
            "worktree", "add", "--no-track", "-b", "fix/isolated", str(path), "main"
        )
        self.git("branch", "--list", "fix/isolated")
        self.git("branch", "-d", "fix/isolated", ok=False)
        self.write("private/local.txt", "valuable ignored data\n", root=path)
        self.assertEqual(self.git("status", "--porcelain", cwd=path).stdout, "")
        self.assertIn(
            "!! private/", self.git("status", "--short", "--ignored", cwd=path).stdout
        )
        # Preserve the data before even normal removal; this is not a force test.
        saved = self.root / "preserved.txt"
        saved.write_bytes((path / "private/local.txt").read_bytes())
        self.git("worktree", "remove", str(path))
        self.assertFalse(path.exists())
        self.assertEqual(saved.read_text(), "valuable ignored data\n")
        self.git("branch", "-d", "fix/isolated")

    def test_annotated_tag_publishes_only_selected_ref_and_cannot_overwrite(self):
        remote = self.root / "remote.git"
        self.git("init", "--bare", "--initial-branch=main", "--template=", str(remote))
        self.git("remote", "add", "origin", str(remote))
        self.git("tag", "-a", "v1.0.0", self.base, "-m", "Release 1.0.0")
        self.git("tag", "-a", "v2.0.0", self.base, "-m", "Unpublished fixture tag")
        self.git("config", "push.followTags", "true")
        self.assertEqual(
            self.git("cat-file", "-t", "refs/tags/v1.0.0").stdout.strip(), "tag"
        )
        tag_object = self.git("rev-parse", "refs/tags/v1.0.0").stdout.strip()
        self.assertEqual(
            self.git("rev-parse", "v1.0.0^{commit}").stdout.strip(), self.base
        )
        self.git(
            "push", "--no-follow-tags", "origin", "refs/tags/v1.0.0:refs/tags/v1.0.0"
        )
        refs = self.git("ls-remote", "--tags", "origin").stdout
        self.assertEqual(
            set(refs.splitlines()),
            {
                f"{tag_object}\trefs/tags/v1.0.0",
                f"{self.base}\trefs/tags/v1.0.0^{{}}",
            },
        )
        self.git("tag", "-a", "v1.0.0", self.base, "-m", "Conflict", ok=False)

    def test_rejected_push_integrates_remote_topic_without_rewriting(self):
        remote = self.root / "remote.git"
        self.git("init", "--bare", "--initial-branch=main", "--template=", str(remote))
        self.git("remote", "add", "origin", str(remote))
        self.git("switch", "-c", "fix/topic")
        self.git(
            "push", "--no-follow-tags", "-u", "origin", "HEAD:refs/heads/fix/topic"
        )
        local = self.commit("task.txt", "local fix\n")
        self.git("switch", "-c", "fix/peer", self.base)
        incoming = self.commit("other.txt", "remote fix\n")
        self.git("push", "--no-follow-tags", "origin", "HEAD:refs/heads/fix/topic")
        self.git("switch", "fix/topic")
        self.git(
            "push", "--no-follow-tags", "origin", "HEAD:refs/heads/fix/topic", ok=False
        )
        self.git(
            "fetch", "origin", "refs/heads/fix/topic:refs/remotes/origin/fix/topic"
        )
        self.git("merge", "--no-edit", "origin/fix/topic")
        for tip in (local, incoming):
            self.git("merge-base", "--is-ancestor", tip, "HEAD")
        self.assertEqual((self.repo / "task.txt").read_text(), "local fix\n")
        self.assertEqual((self.repo / "other.txt").read_text(), "remote fix\n")
        self.git("push", "--no-follow-tags", "origin", "HEAD:refs/heads/fix/topic")
        head = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertEqual(
            self.git("ls-remote", "origin", "refs/heads/fix/topic").stdout.strip(),
            f"{head}\trefs/heads/fix/topic",
        )

    def test_backport_and_revert_preserve_history(self):
        self.git("switch", "-c", "fix/source")
        fix = self.commit("task.txt", "fixed\n")
        self.git("switch", "--no-track", "-c", "fix/backport", self.base)
        self.git("cherry-pick", "-x", fix)
        self.assertIn(
            f"cherry picked from commit {fix}",
            self.git("log", "-1", "--format=%B").stdout,
        )
        before_revert = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("revert", "--no-commit", before_revert)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before_revert)
        self.assertEqual((self.repo / "task.txt").read_text(), "base\n")
        self.assertIn("task.txt", self.git("diff", "--cached", "--name-only").stdout)

    def test_bisect_reset_restores_starting_branch_and_head(self):
        self.commit("task.txt", "middle\n")
        tip = self.commit("task.txt", "bad\n")
        self.git("bisect", "start", tip, self.base)
        self.git("bisect", "reset")
        self.assertEqual(self.git("branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), tip)
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    def test_hard_reset_overwrites_obstructing_untracked_data(self):
        self.git("switch", "-c", "fix/with-file")
        target = self.commit("obstacle.txt", "tracked target\n")
        self.git("switch", "main")
        self.write("obstacle.txt", "untracked valuable bytes\n")
        self.assertEqual(self.git("diff", "HEAD").stdout, "")
        # Intentional destructive command against this synthetic fixture only.
        # It proves why a clean tracked diff does not satisfy discard safeguards.
        self.git("reset", "--hard", target)
        self.assertEqual((self.repo / "obstacle.txt").read_text(), "tracked target\n")

    def test_conflicting_merge_abort_restores_owned_start(self):
        self.git("switch", "-c", "fix/incoming")
        self.commit("task.txt", "incoming\n")
        self.git("switch", "main")
        tip = self.commit("task.txt", "local\n")
        self.git("merge", "--no-edit", "fix/incoming", ok=False)
        self.assertIn("UU task.txt", self.git("status", "--short").stdout)
        self.git("merge", "--abort")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), tip)
        self.assertEqual((self.repo / "task.txt").read_text(), "local\n")
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    def test_resolved_merge_finishes_original_operation(self):
        self.git("switch", "-c", "fix/incoming")
        incoming = self.commit("task.txt", "incoming\n")
        self.git("switch", "main")
        local = self.commit("task.txt", "local\n")
        self.git("merge", "--no-edit", "fix/incoming", ok=False)
        self.write("task.txt", "combined resolution\n")
        self.git("add", "--", "task.txt")
        self.git("commit", "--no-edit")
        parents = self.git("show", "-s", "--format=%P", "HEAD").stdout.split()
        self.assertEqual(parents, [local, incoming])
        self.assertEqual((self.repo / "task.txt").read_text(), "combined resolution\n")
        self.assertEqual(self.git("status", "--porcelain").stdout, "")


if __name__ == "__main__":
    print(
        subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        flush=True,
    )
    unittest.main(verbosity=2)
