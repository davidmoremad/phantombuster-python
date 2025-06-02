# Command Line Interface

The Command Line Interface (CLI) allows users to interact with the system through a terminal or command prompt. It provides a way to execute commands, manage files, and perform various tasks without a graphical user interface.

# Installation
To install the CLI, follow these steps:
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to install the CLI.
3. Run the following command:
   ```bash
   pip install phantombuster-cli
   ```
4. Verify the installation by running:
   ```bash
    phantombuster --version
    ```

# Usage & Commands

To use the CLI, you can execute commands directly in your terminal. Here are some common commands:

All available commands can be listed by running:
```bash
phantombuster --help
```

> [!TIP]
> You can use `-d` or `--debug` to enable debug mode for more detailed output in JSON format.

| Command | Description |
|---------|-------------|
| `phantombuster --help` | Show help information for the CLI. |
| `phantombuster org info` | Display information about the organization. |
| `phantombuster org usage` | Show usage statistics for the organization. |
| `phantombuster agent list` | List all agents in the organization. |
| `phantombuster agent show <agent_id>` | Show details of a specific agent by ID. |
| `phantombuster agent create --name "<name>" --script "<script_id>" --org "<org_slug>" --args "<key=value>"` | Create a new agent with specified parameters. |
| `phantombuster agent delete <agent_id>` | Delete a specific agent by ID. |
| `phantombuster agent run <agent_id> --args "<key=value>"` | Run a specific agent with provided arguments. |
| `phantombuster script list` | List all scripts available in the organization. |
| `phantombuster script show <script_id>` | Show details of a specific script by ID. |
| `phantombuster container list` | List all containers in the organization. |
| `phantombuster container show <container_id>` | Show details of a specific container by ID. |
| `phantombuster container results <container_id>` | Show results of a specific container by ID. |
| `phantombuster container output <container_id>` | Show output of a specific container by ID. |
