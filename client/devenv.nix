{ pkgs, lib, config, inputs, ... }:
let
  buildInputs = with pkgs; [
    stdenv.cc.cc
    libuv
    zlib
  ];
  pkgs-unstable = import inputs.nixpkgs-unstable { system = pkgs.stdenv.system; };
in 
{
  # https://devenv.sh/basics/
  env.GREET = "devenv";
  env.ELECTRON_PATH = "$(which electron)";
  #env = {
  #  LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [
  #    fontconfig
  #    libGL
  #    libxkbcommon
  #    freetype
  #    libdbusmenu
  #  ];
  #};
  # https://devenv.sh/packages/
  packages = [ 
    pkgs.git 
    pkgs-unstable.electron
    pkgs.autoPatchelfHook
    pkgs-unstable.python312Packages.pyqt6
    pkgs-unstable.python312Packages.pyside6
    pkgs-unstable.libsForQt5.qt5.qtwayland
  ];
  languages.python = {
    enable = true;
    package = pkgs-unstable.python312Full;
  };
  languages.python.uv = {
    enable = true;
    package = pkgs-unstable.uv;
  };
  languages.python.venv.enable = true;
  # https://devenv.sh/languages/
  # languages.rust.enable = true;

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';
  #export LD_LIBRARY_PATH=${pkgs.libGL}/lib/
  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
