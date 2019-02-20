workflow "New workflow" {
  on = "push"
  resolves = [
    "GitHub Action for Flake8",
    "GitHub Action for pylint",
  ]
}

action "GitHub Action for Flake8" {
  uses = "cclauss/GitHub-Action-for-Flake8@0.0.1"
}

action "GitHub Action for pylint" {
  uses = "cclauss/GitHub-Action-for-pylint@0.0.1"
}
