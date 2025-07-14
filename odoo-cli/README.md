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

    Choose option `2. Initialize configuration`, then follow the prompts to complete setup.
