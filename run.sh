#!/bin/sh

DOCKERHUB_USER=mrrain345

function help() {
  echo "Usage: $(basename $0) [run [cmd]|build|rebuild [cmd]|publish [user]|help]"
  echo "  run [cmd]:      Run the container."
  echo "  build:          Build the container."
  echo "  rebuild [cmd]:  Build and run the container."
  echo "  publish [user]: Publish the container to Docker Hub. (user defaults to $DOCKERHUB_USER)"
  echo "  help:           Print this help."
}

function run() {
  docker run --rm --gpus all \
    --name voice-server \
    -v ./data:/data \
    -it voice-server "$@"
}

function build() {
  docker build . -t voice-server
}

function rebuild() {
  build && run "$@"
}

function publish() {
  local user=${1:-$DOCKERHUB_USER}
  docker build . -t voice-server
  docker tag voice-server $user/voice-server
  docker push $user/voice-server
}


pushd $(dirname $0) > /dev/null
ACTION=${1:-help}
shift 2> /dev/null

case $ACTION in
  run) run "$@";;
  build) build;;
  rebuild) rebuild "$@";;
  publish) publish "$@";;
  help) help;;
  *) echo "Unknown action: $ACTION"; help; exit 1;;
esac

popd > /dev/null