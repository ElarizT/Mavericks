import re
from jinja2 import Environment, FileSystemLoader
from src.schemas import AgentSchema
from src.log import render_error, render_success, render_warning
import pathlib
import sys

if getattr(sys, "frozen", False):
    jinja_folder_path = pathlib.Path(sys._MEIPASS) / "src" / "jinja" / "templates"
else:
    jinja_folder_path = pathlib.Path(__file__).resolve().parent / "templates"

parent_exec_folder = pathlib.Path.cwd()


def generate_uv_pyproject_toml(env: Environment, folder: pathlib.Path):
    template = "pyproject_toml.j2"
    uv_pyproject = env.get_template(template)
    pyproject_render = uv_pyproject.render()

    fp = folder / "pyproject.toml"
    if fp.is_file():
        return

    with open(fp, "w+") as f:
        f.write(pyproject_render)
        render_success("Added pyproject.toml successfully")


def generate_agent_file(agent_body: AgentSchema) -> None:
    env = Environment(loader=FileSystemLoader(f"{jinja_folder_path}"))
    template = env.get_template("agent_template.j2")
    agent_name = re.sub(
        r"[^a-zA-Z0-9_]", "", agent_body.agent_name.replace(" ", "_").lower()
    )
    rendered = template.render(
        agent_token=agent_body.agent_jwt,
        agent_name=agent_name,
        agent_description=agent_body.agent_description,
        # default_docstring="Detailed description of the agent could be specified here",
    )

    agents_folder = parent_exec_folder / "agents"
    try:
        agents_folder.mkdir(parents=True, exist_ok=True)
        agent_personal_folder = agents_folder / agent_name
        agent_personal_folder.mkdir(parents=True, exist_ok=True)

        py_fp = agent_personal_folder / f"{agent_name}.py"
        if py_fp.is_file():
            render_warning(f"Agent {py_fp} already exists.")
            return

        with open(py_fp, "w+") as f:
            f.write(rendered)
            render_success(f"Created {agent_name} agent successfully at: {str(py_fp)}")
        generate_uv_pyproject_toml(env=env, folder=agent_personal_folder)
    except OSError as e:
        render_error(
            f"Error: Could not create 'agents/' folder file at {parent_exec_folder}: {str(e)}"
        )
