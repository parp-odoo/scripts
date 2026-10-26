# Odoo CLI

Configure your Odoo workspace, start the server, switch versions, and run selected
Odoo tests from the terminal.

## Watch the demo

https://github.com/user-attachments/assets/5b66baff-0572-415b-9bf5-58a591507cad

[Watch the 30-second demo with audio](docs/odoo-cli-demo.mp4).
It covers aliases, configuration, starting the server, VS Code debugging, and
running a selected test. Live terminal footage is sped up, with short instruction
cards for aliases and VS Code.

## Get started

Activate the Python environment you normally use for Odoo. From the root of this
repository, install the CLI requirements:

```bash
python3 -m pip install -r odoo-cli/requirements.txt
```

Then open the menu:

```bash
bash odoo-cli/run.sh
```

Use the arrow keys to choose an option and press **Enter**. Press **Q** or
**Esc** to leave the menu.

## Add shortcuts

Use aliases to open the CLI and run tests from any directory:

```bash
alias odoo='bash /full/path/to/tools/odoo-cli/run.sh'
alias odoo-test='bash /full/path/to/tools/odoo-cli/test.sh'
```

Replace `/full/path/to/tools` with this repository's location. To keep the
shortcuts, add those lines to `~/.bashrc` for Bash or `~/.zshrc` for Zsh, then open
a new terminal.

Now use `odoo` to open the menu, or `odoo-test ':TestClass'` to run selected tests.

## Configure your workspace

Choose **Initialize configuration** and enter:

- The path to your Odoo Enterprise folder.
- The path to your Odoo Community folder.
- The port to use, such as `8069`.
- The path to your `odoo.conf` file.

The CLI remembers these details. Choose the same option whenever you need to
change them.

## Start the server

Open the menu and choose **Run Odoo server**:

```bash
bash odoo-cli/run.sh
```

Once startup finishes, open [localhost:8069](http://localhost:8069) in your browser.
If you chose another port, use that port instead. Keep the terminal open while
using Odoo, and press **Ctrl+C** when you want to stop the server.

## Run selected tests

Use an existing Odoo database with the modules you want to test already installed.
Pass a test name, class, or module to the test launcher:

```bash
bash odoo-cli/test.sh '.test_some_code'
bash odoo-cli/test.sh ':TestClass'
bash odoo-cli/test.sh '/point_of_sale'
```

The video uses `:TestIrHttpConverters`, an existing Odoo test class.

The CLI remembers the last selector. To run it again:

```bash
bash odoo-cli/test.sh
```

On your first run, omitting the selector prompts you to enter one. Passing a new
selector replaces the saved choice. Tests stop automatically when they finish;
check the terminal for the results.

For a selector beginning with a minus sign, add `--` before it:

```bash
bash odoo-cli/test.sh -- '-slow,/point_of_sale'
```

## Debug with VS Code

1. Install the **Python Debugger** extension in VS Code.
2. Add the configuration from [`vscode/launch.json`](../vscode/launch.json) to
   `.vscode/launch.json` in your Odoo workspace. If that file already exists, add
   the supplied entry to its list of configurations.
3. Set a breakpoint in your Python code, then start the server with `odoo` and
   choose **Run Odoo server**.
4. Open **Run and Debug**, choose **Odoo: Attach to odoo-cli**, and press **F5**.
   Use Odoo to trigger the code with your breakpoint.

Debugging is enabled automatically. After changing Python code, stop the server
with **Ctrl+C**, start it again, and reattach. You can also attach during a test
run while the tests are still running.

## Other menu options

- **Change version** — select an Odoo version, update your repositories, and
  choose whether to start the server afterward.
- **Drop database & run server** — delete the current version's database and
  start again. This permanently removes that database's data. Starting the server
  after changing versions also drops the selected version's database.
