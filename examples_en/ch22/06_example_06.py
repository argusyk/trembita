# Chapter 22. Computer Use and Browser Agents – example 6 (manuscript: 22-computer-use.md, line 307)
def ask_human(action: str, args: dict, why: str) -> bool:
    """Shows the action to the broker; without an explicit "yes" the action is not executed."""
    print(f"The agent wants to perform: {action} {args}\nWhy confirmation is needed: {why}")
    return input("Allow? [yes/no] ").strip().lower() == "yes"


strict_tool = types.Tool(computer_use=types.ComputerUse(
    environment=types.Environment.ENVIRONMENT_BROWSER,
    excluded_predefined_functions=UNSUPPORTED,   # from Section 22.3, including search
    enable_prompt_injection_detection=True,      # check the screen for injections
))
