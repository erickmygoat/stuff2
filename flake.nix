{
  description = "A development environment for the 'My Son' AI agent.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          name = "my-son-dev-env";
          buildInputs = with pkgs; [
            # Core development environment
            python3
            poetry
            nodejs

            # Build tools
            gcc
            gnumake

            # Modern CLI tools
            ripgrep
            fd
            fzf
            bat
            eza
            jq
            yq

            # Version control
            git
          ];

          shellHook = ''
            echo "Entering 'My Son' development environment..."
            export PYTHONPATH=$PWD
          '';
        };
      }
    );
}
