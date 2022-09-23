{
  description = "Scrap API V3";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/master";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    let
    my-python = pkgs.python310;
    automation = my-python.withPackages (p: with p; [
      virtualenv
      requests
      html5lib
      beautifulsoup4
      fastapi
      uvicorn["standard"]
      selenium
    ]);
    in
    {
      devShell = pkgs.mkShell {
        nativeBuildInputs = [ pkgs.bashInteractive ];
        buildInputs = with pkgs; [
        virtualenv
        automation
        nodePackages.pyright
        chromedriver
        ];
        shellHook = with pkgs; ''
          PYTHONPATH=${automation}/${automation.sitePackages}
          export PIP_PREFIX=$(pwd)/_build/pip_packages
          export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
          export PATH="$PIP_PREFIX/bin:$PATH"
          unset SOURCE_DATE_EPOCH
        '';
      };
    });
}
