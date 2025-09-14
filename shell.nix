{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    buildInputs = [
        pkgs.python3
        pkgs.python3Packages.wxpython 
        pkgs.python3Packages.pypubsub
    ];
}