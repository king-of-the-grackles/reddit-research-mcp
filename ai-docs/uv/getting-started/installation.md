# Installing uv

## Installation methods

Install uv with our standalone installers or your package manager of choice.

### Standalone installer

uv provides a standalone installer to download and install uv:

#### macOS and Linux

Use `curl` to download the script and execute it with `sh`:

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have `curl`, you can use `wget`:

```bash
$ wget -qO- https://astral.sh/uv/install.sh | sh
```

Request a specific version by including it in the URL:

```bash
$ curl -LsSf https://astral.sh/uv/0.8.11/install.sh | sh
```

#### Windows

Use `irm` to download the script and execute it with `iex`:

```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Changing the execution policy allows running a script from the internet.

Request a specific version by including it in the URL:

```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.8.11/install.ps1 | iex"
```

> **Tip**: The installation script may be inspected before use:
> 
> macOS and Linux:
> ```bash
> $ curl -LsSf https://astral.sh/uv/install.sh | less
> ```
> 
> Windows:
> ```powershell
> PS> powershell -c "irm https://astral.sh/uv/install.ps1 | more"
> ```

Alternatively, the installer or binaries can be downloaded directly from GitHub.

See the reference documentation on the installer for details on customizing your uv installation.

### PyPI

For convenience, uv is published to [PyPI](https://pypi.org/project/uv/).

If installing from PyPI, we recommend installing uv into an isolated environment, e.g., with `pipx`:

```bash
$ pipx install uv
```

However, `pip` can also be used:

```bash
$ pip install uv
```

> **Note**: uv ships with prebuilt distributions (wheels) for many platforms; if a wheel is not available for a given platform, uv will be built from source, which requires a Rust toolchain. See the contributing setup guide for details on building uv from source.

### Homebrew

uv is available in the core Homebrew packages.

```bash
$ brew install uv
```

### WinGet

uv is available via [WinGet](https://winstall.app/apps/astral-sh.uv).

```powershell
$ winget install --id=astral-sh.uv  -e
```

### Scoop

uv is available via [Scoop](https://scoop.sh/#/apps?q=uv).

```powershell
$ scoop install main/uv
```

### Docker

uv provides a Docker image at [`ghcr.io/astral-sh/uv`](https://github.com/astral-sh/uv/pkgs/container/uv).

See our guide on using uv in Docker for more details.

### GitHub Releases

uv release artifacts can be downloaded directly from [GitHub Releases](https://github.com/astral-sh/uv/releases).

Each release page includes binaries for all supported platforms as well as instructions for using the standalone installer via `github.com` instead of `astral.sh`.

### Cargo

uv is available via Cargo, but must be built from Git rather than crates.io due to its dependency on unpublished crates.

```bash
$ cargo install --git https://github.com/astral-sh/uv uv
```

> **Note**: This method builds uv from source, which requires a compatible Rust toolchain.

## Upgrading uv

When uv is installed via the standalone installer, it can update itself on-demand:

```bash
$ uv self update
```

> **Tip**: Updating uv will re-run the installer and can modify your shell profiles. To disable this behavior, set `UV_NO_MODIFY_PATH=1`.

When another installation method is used, self-updates are disabled. Use the package manager's upgrade method instead. For example, with `pip`:

```bash
$ pip install --upgrade uv
```

## Shell autocompletion

> **Tip**: You can run `echo $SHELL` to help you determine your shell.

To enable shell autocompletion for uv commands, run one of the following:

### Bash
```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
```

### Zsh
```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
```

### fish
```bash
echo 'uv generate-shell-completion fish | source' > ~/.config/fish/completions/uv.fish
```

### Elvish
```bash
echo 'eval (uv generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv
```

### PowerShell / pwsh
```powershell
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

To enable shell autocompletion for uvx, run one of the following:

### Bash
```bash
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
```

### Zsh
```bash
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc
```

### fish
```bash
echo 'uvx --generate-shell-completion fish | source' > ~/.config/fish/completions/uvx.fish
```

### Elvish
```bash
echo 'eval (uvx --generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv
```

### PowerShell / pwsh
```powershell
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
Add-Content -Path $PROFILE -Value '(& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

Then restart the shell or source the shell config file.

## Uninstallation

If you need to remove uv from your system, follow these steps:

1. **Clean up stored data (optional):**

```bash
$ uv cache clean
$ rm -r "$(uv python dir)"
$ rm -r "$(uv tool dir)"
```

> **Tip**: Before removing the binaries, you may want to remove any data that uv has stored.

2. **Remove the uv and uvx binaries:**

macOS and Linux:
```bash
$ rm ~/.local/bin/uv ~/.local/bin/uvx
```

Windows:
```powershell
PS> rm $HOME\.local\bin\uv.exe
PS> rm $HOME\.local\bin\uvx.exe
```

> **Note**: Prior to 0.5.0, uv was installed into `~/.cargo/bin`. The binaries can be removed from there to uninstall. Upgrading from an older version will not automatically remove the binaries from `~/.cargo/bin`.

## Next steps

See the first steps or jump straight to the guides to start using uv.