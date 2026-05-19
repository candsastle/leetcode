{
  description = "Generic Template Flake For Python Projects";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };
  outputs = {self, ...} @ inputs: let
    pkgs = inputs.nixpkgs.legacyPackages."x86_64-linux";
  in {
    devShells = {
      "x86_64-linux".default = pkgs.mkShell {
        buildInputs = with pkgs; [uv];

        shellHook =
          /*
          bash
          */
          ''
            if [ ! -f .init ]; then
              uv sync && echo "This file indicates that you have already run uv sync in this directory" > .init
            fi
            source .venv/bin/activate
          '';
      };
    };
  };
}
