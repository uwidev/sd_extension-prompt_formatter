import launch

if not launch.is_installed("regex"):
    print("Installing requirements for Prompt Formatter")
    launch.run_pip("install regex", "support for variable lookbehind")