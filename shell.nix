{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    terraform
  ];

  shellHook = ''
    echo "Terraform version: $(terraform version | head -n 1)"
    echo "Working directory: $PWD"
  '';
}