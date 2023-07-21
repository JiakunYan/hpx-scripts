#!/usr/bin/env bash

function mkdir_s() {
  if [[ -d "$1" ]]; then
    read -p "$1 directory exists. Are you sure to remove it | continue with it | or abort? [r|c|A]" -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Rr]$ ]]; then
      echo "Remove $1"
      rm -rf $1
    elif [[ $REPLY =~ ^[Cc]$ ]]; then
      echo "Continue with previous work"
    else
      echo "Abort"
      exit 1
    fi
  fi
  mkdir -p $1
}

function record_env() {
  env > init-env.log 2>&1
  if command -v module >/dev/null ; then
    module list > init-module.log 2>&1
  fi
}

function summarize() {
  # exit when any command fails
  set -e

  mkdir_s ./summary

  if [[ -d "./run" ]]; then
  #  find ./run -name 'slurm_output.*' -exec cp --parents \{\} ./summary \;
    cp -r run ./summary
  fi
  if [[ -d "./data" ]]; then
    cp -r data ./summary
  fi
  if [[ -d "./draw" ]]; then
    cp -r draw ./summary
  fi
  if [[ -d "./draw" ]]; then
    cp -r draw ./summary
  fi
  if compgen -G "*.sh" > /dev/null; then
    cp *.sh ./summary
  fi
  if compgen -G "*.py" > /dev/null; then
    cp *.py ./summary
  fi

  tar -czf summary.tar.gz summary
  rm -rf summary
}

"$@"