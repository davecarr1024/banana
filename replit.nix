{pkgs}: {
  deps = [
    pkgs.python312Packages.pytest-cov
    pkgs.python312Packages.pytest-subtests
    pkgs.python312Packages.pytest
    pkgs.pyright
    pkgs.ruff
    pkgs.black
    pkgs.python313
    pkgs.poethepoet
  ];
}
