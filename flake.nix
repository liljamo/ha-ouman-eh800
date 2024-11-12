{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };

    pre-commit-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    pre-commit-hooks,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];
      perSystem = {
        config,
        lib,
        pkgs,
        system,
        ...
      }: {
        checks.pre-commit-check = pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            # Nix formatting
            alejandra.enable = true;

            # Python linting and formatting
            pylint = {
              enable = true;
              args = [
                "--disable=import-error"
                "--disable=missing-class-docstring"
                "--disable=missing-function-docstring"
                "--disable=missing-module-docstring"
              ];
            };
            black.enable = true;

            # Spell checking
            typos = {
              enable = true;
              settings.ignored-words = ["hass"];
            };
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs;
            [
              python312
              python312Packages.pip

              just
            ]
            ++ [
              self.checks.${system}.pre-commit-check.enabledPackages
            ];
          shellHook = ''
            ${self.checks.${system}.pre-commit-check.shellHook}

            python -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.dev.txt
          '';
        };
      };
    };
}
