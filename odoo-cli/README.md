# Odoo CLI: Simplified Server Management and Version Control

The Odoo CLI streamlines common development tasks, allowing you to:

- Start the Odoo server quickly.
- Initialize and manage configuration files.
- Switch between Odoo versions with ease.
- Pull the latest code updates.
- Drop and recreate the database as needed.

This tool is designed to make your Odoo development workflow faster and more efficient.

## 🚀 Setup Instructions
1. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

2. Add an alias to make the CLI accessible from anywhere:

    ```bash
    echo 'alias alias-name="bash /home/odoo/odoo/tools/odoo-cli/run.sh"' >> ~/.bashrc
    source ~/.bashrc
    ```
    > **Note:** Adjust the alias name and path as needed for your environment or shell.

3. If you use the Fish shell, add a alias to your Fish configuration:
    Open your fish config file:
    ```bash
    nano ~/.config/fish/config.fish
    ```

    Add the following to `config.fish`:
    ```fish
    function alias-name
        bash /home/odoo/odoo/tools/odoo-cli/run.sh $argv
    end
    ```

    Reload the config:
    Then reload your Fish configuration:

    ```bash
    source ~/.config/fish/config.fish
    ```
4. Initialize the configuration file:
    Run the CLI:
    ```bash
    alias-name
    ```

    Choose `Initialize configuration`, then follow the prompts to complete setup.

## Run selected tests

Use the dedicated launcher with an Odoo test selector:

```bash
bash odoo-cli/test.sh '.test_some_code'
bash odoo-cli/test.sh ':TestClass'
bash odoo-cli/test.sh 'test_pos_module'
```

The launcher saves the last selector in `odoo-cli/.cache/odoo-cli.json`.
Omit the argument to reuse it; the first run prompts for tags if none are saved:

```bash
bash odoo-cli/test.sh
```

Pass a new selector to replace the saved value. Odoo selectors are passed through
unchanged, including comma-separated combinations and module selectors such as
`/point_of_sale`. Use `--` before a selector starting with a minus sign:

```bash
bash odoo-cli/test.sh -- '-slow,/point_of_sale'
```

Test mode uses the current version's existing `testdb-<version>` database and runs
tests against installed modules without requesting module updates or
initialization. It does not request demo or test-data installation. Prepare the
database and install any required modules before running tests. Tests run with
`--workers=0`, without development reloads, and with `--stop-after-init`.
The launcher exits with Odoo's exit code, including failures.

The test launcher enables debugpy on `127.0.0.1:5678` automatically and starts
tests immediately. Attach VS Code while the tests are still running; the
debugger port closes when they finish. Install debugpy in the active Python
environment as described below. No additional launcher arguments are needed.

## Debug Python with VS Code

1. Activate the Python environment you use for Odoo and install the debugger:

    ```bash
    python3 -m pip install debugpy
    ```

2. Install the **Python Debugger** extension in VS Code. Copy
   [`vscode/launch.json`](../vscode/launch.json) into `.vscode/launch.json` in
   your Odoo workspace, or add its configuration to your existing file.
   Open the same Community, Enterprise, or custom addon source files that the
   CLI runs. With VS Code Remote SSH, open the workspace on the server.

3. Start the regular launcher from this repository:

    ```bash
    bash odoo-cli/run.sh
    ```

    Choose **Run Odoo server**. Odoo starts with debugging enabled, without
    waiting for VS Code. You can attach while the server is running. Server
    starts after dropping the database or changing versions also enable
    debugging automatically. No additional launcher arguments are needed.

4. Set a breakpoint directly in your Python file. In VS Code's **Run and Debug**
   view, select **Odoo: Attach to odoo-cli** and press **F5**. Then use Odoo to
   trigger the code containing the breakpoint.

The debugger listens on `127.0.0.1:5678`.
Debug mode uses the CLI's active Python interpreter, disables worker processes,
and keeps XML/QWeb development features while disabling automatic Python reloads.
After editing Python code, stop the server with **Ctrl+C**, run the command
again, and reattach VS Code.

If VS Code runs locally and Odoo runs on another machine, `127.0.0.1` in the
attach configuration points at your local computer. Open an SSH tunnel in a
separate local terminal and keep it running:

```bash
ssh -N -L 5678:127.0.0.1:5678 your-user@your-server
```

Replace `your-user@your-server` with your SSH login. Start `run.sh` or `test.sh`
on the server, then attach using the existing VS Code configuration. A VS Code
Remote SSH window connected to the server is another option. Both launchers
enable debugging without waiting. A refused connection means the debugger is
not reachable at that address; check the launcher's terminal for startup errors
and keep the Odoo process running while attaching.

See the [VS Code Python debugging guide](https://code.visualstudio.com/docs/python/debugging)
for more about attaching and breakpoints.
