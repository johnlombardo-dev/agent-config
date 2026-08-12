#!/usr/bin/env bash

set -Eeuo pipefail

target_home="${AGENT_CONFIG_TARGET_HOME:-$HOME}"
script_source="${BASH_SOURCE[0]:-}"

if [[ -n "$script_source" ]] && [[ -f "$script_source" ]]; then
  repo_dir="$(cd -- "$(dirname -- "$script_source")" && pwd -P)"
else
  repo_dir=""
fi

if [[ ! -f "$repo_dir/AGENTS.md" || ! -d "$repo_dir/skills" ]]; then
  install_dir="${AGENT_CONFIG_INSTALL_DIR:-$target_home/.local/share/agent-config}"
  archive_url="${AGENT_CONFIG_ARCHIVE_URL:-https://api.github.com/repos/johnlombardo-dev/agent-config/tarball/main}"
  checkout_backup_base="$target_home/.local/state/agent-config/checkouts"
  download_dir="$(mktemp -d "${TMPDIR:-/tmp}/agent-config.XXXXXX")"

  cleanup_download() {
    rm -rf -- "$download_dir"
  }
  trap cleanup_download EXIT

  if [[ "$archive_url" == https://api.github.com/* ]] && [[ -z "${GITHUB_TOKEN:-}" ]]; then
    printf 'GITHUB_TOKEN is required when running this installer through a pipe.\n' >&2
    exit 1
  fi

  curl_args=(-fsSL)
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    curl_args+=(-H "Authorization: Bearer $GITHUB_TOKEN")
  fi

  curl "${curl_args[@]}" "$archive_url" |
    tar -xzf - -C "$download_dir" --strip-components=1

  mkdir -p -- "$(dirname -- "$install_dir")"
  if [[ -e "$install_dir" || -L "$install_dir" ]]; then
    mkdir -p -- "$checkout_backup_base"
    checkout_backup="$(mktemp -d "$checkout_backup_base/$(date +%Y%m%dT%H%M%S).XXXXXX")"
    mv -- "$install_dir" "$checkout_backup/repository"
    printf 'Backed up previous checkout: %s\n' "$checkout_backup/repository"
  fi

  mv -- "$download_dir" "$install_dir"
  trap - EXIT
  exec "$install_dir/install.sh"
fi

codex_dir="$target_home/.codex"
agent_skills_dir="$target_home/.agents/skills"
backup_base="$target_home/.local/state/agent-config/backups"
backup_dir=""

ensure_backup_dir() {
  if [[ -n "$backup_dir" ]]; then
    return
  fi

  mkdir -p -- "$backup_base"
  backup_dir="$(mktemp -d "$backup_base/$(date +%Y%m%dT%H%M%S).XXXXXX")"
}

link_path() {
  local source_path="$1"
  local destination_path="$2"
  local backup_relative_path="$3"

  mkdir -p -- "$(dirname -- "$destination_path")"

  if [[ -L "$destination_path" ]] && [[ "$(readlink "$destination_path")" == "$source_path" ]]; then
    printf 'Already linked: %s -> %s\n' "$destination_path" "$source_path"
    return
  fi

  if [[ -e "$destination_path" || -L "$destination_path" ]]; then
    ensure_backup_dir

    local backup_path="$backup_dir/$backup_relative_path"
    mkdir -p -- "$(dirname -- "$backup_path")"
    mv -- "$destination_path" "$backup_path"
    printf 'Backed up: %s -> %s\n' "$destination_path" "$backup_path"
  fi

  ln -s -- "$source_path" "$destination_path"
  printf 'Linked: %s -> %s\n' "$destination_path" "$source_path"
}

clean_broken_skill_links() {
  local installed_skill
  local link_target
  local resolved_target
  local target_parent
  local resolved_parent
  local skill_name
  local backup_path

  mkdir -p -- "$agent_skills_dir"

  while IFS= read -r -d '' installed_skill; do
    if [[ -e "$installed_skill" ]]; then
      continue
    fi

    link_target="$(readlink "$installed_skill")"
    if [[ "$link_target" = /* ]]; then
      resolved_target="$link_target"
    else
      resolved_target="$(dirname -- "$installed_skill")/$link_target"
    fi

    target_parent="$(dirname -- "$resolved_target")"
    if resolved_parent="$(cd -- "$target_parent" 2>/dev/null && pwd -P)"; then
      resolved_target="$resolved_parent/$(basename -- "$resolved_target")"
    fi

    if [[ "$resolved_target" != "$skills_source_dir/"* ]]; then
      continue
    fi

    ensure_backup_dir
    skill_name="$(basename -- "$installed_skill")"
    backup_path="$backup_dir/agents/skills/$skill_name"
    mkdir -p -- "$(dirname -- "$backup_path")"
    mv -- "$installed_skill" "$backup_path"
    printf 'Backed up broken skill link: %s -> %s\n' "$installed_skill" "$backup_path"
  done < <(find "$agent_skills_dir" -mindepth 1 -maxdepth 1 -type l -print0)
}

agents_source="$repo_dir/AGENTS.md"
skills_source_dir="$repo_dir/skills"

if [[ ! -f "$agents_source" ]]; then
  printf 'Missing required file: %s\n' "$agents_source" >&2
  exit 1
fi

if [[ ! -d "$skills_source_dir" ]]; then
  printf 'Missing required directory: %s\n' "$skills_source_dir" >&2
  exit 1
fi

clean_broken_skill_links
link_path "$agents_source" "$codex_dir/AGENTS.md" "codex/AGENTS.md"

skill_count=0
for skill_source in "$skills_source_dir"/*; do
  if [[ ! -d "$skill_source" || ! -f "$skill_source/SKILL.md" ]]; then
    continue
  fi

  skill_name="$(basename -- "$skill_source")"
  link_path \
    "$skill_source" \
    "$agent_skills_dir/$skill_name" \
    "agents/skills/$skill_name"
  ((skill_count += 1))
done

if ((skill_count == 0)); then
  printf 'No skill directories containing SKILL.md found in %s\n' "$skills_source_dir" >&2
  exit 1
fi

if [[ -n "$backup_dir" ]]; then
  printf 'Backups saved outside agent discovery paths: %s\n' "$backup_dir"
fi
