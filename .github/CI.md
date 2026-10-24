# CI coverage

Linux quality jobs use `kalana-ci`. Native Apple checks and
releases use `[self-hosted, kalana-macos-ci, macOS]`. Windows checks/builds keep
their GitHub-hosted Windows runners: the repository owner explicitly requested
preserving Windows coverage because no self-hosted Windows runner is available.

Every trusted pull request and push to main runs:

- TypeScript checks, critical Biome correctness rules, and production builds of
  the web app, desktop frontend, and landing site with Bun 1.3.8 and its frozen lock.
- The deterministic Python backend suite with CPU PyTorch, offline model access,
  hash-locked dependencies, per-test timeouts, and JUnit artifacts.
- Native Rust desktop compilation, including integration-test targets, on macOS
  and Windows. The macOS code also exercises the Swift/ScreenCaptureKit build path.

Backend dependency installation uses uv's package-scoped `--torch-backend cpu`:
PyTorch packages come from the CPU wheel repository, while general dependencies
come from PyPI. The lock retains exact versions and hashes; neither compilation
nor installation enables unsafe cross-index matching. To refresh it, use the
command recorded at the top of `backend/requirements-ci.txt`.

Six scripts under backend/tests are interactive model/server evaluation harnesses;
CI excludes those scripts rather than downloading models or assuming a running
backend. GPU, native audio-capture runtime permissions, model quality, signing,
and notarization remain separate integration/release concerns. The audio-capture
integration test is compiled but not executed because it needs real system audio.

The full existing Biome policy currently reports 46 errors on the unchanged
application. CI enforces clean critical correctness rules without weakening the
existing local lint configuration or folding a broad UI refactor into this rollout.

Mac release workers need Xcode (including actool and Swift), Homebrew/LLVM as
already required by the release build, and Rosetta 2 for the preserved Intel Mac
artifact. Architecture-matched Python environments build the right sidecar; Rust
receives the same target explicitly. Runner-list APIs return HTTP 403 with the
current integration, so labels and repository access must be provisioned externally.

Unreviewed fork PRs do not execute on self-hosted workers. A maintainer can copy a
reviewed contribution to a branch in this repository to run the trusted checks.
Do not use pull_request_target to execute untrusted source.
