from invoke import Collection, task

#################################################################
# running the pipeline
#################################################################

@task
def copy_sample_files(context):
    """
    Run the pipeline
    """
    context.run("cp data/samples/* data/data_files/incoming/")

@task
def run_ingestion(context):
    """
    Run the pipeline
    """
    context.run("poetry run python src/main.py")

#################################################################
# cleaning
#################################################################


@task
def clean_build(context):
    """
    Remove build artifacts
    """
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc(context):
    """
    Remove Python artifacts
    """
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")
    context.run("find . -name '.pytest_cache' -exec rm -fr {} +")


@task
def clean_test(context):
    """
    Remove test and coverage artifacts
    """
    context.run("rm -fr .tox/")
    context.run("rm -f .coverage")
    context.run("rm -fr htmlcov/")


@task(clean_build, clean_pyc, clean_test)
def clean(context):
    """
    Remove all build, test, coverage and Python artifacts
    """
    pass


@task
def clean_venv(context):
    """
    Remove virtual environment
    """
    # poetry env remove might not to work if `virtualenvs.in-project = true`
    # (see https://github.com/python-poetry/poetry/issues/2124)
    # so if not, remove whole `.venv` directory using https://unix.stackexchange.com/questions/153763  # noqa
    context.run(
        "poetry env remove $$(poetry env info -p)/bin/python && ([ $$? -eq 0 ]) "
        "|| rm -rf $$(poetry env info -p)"
    )


#################################################################
# all tests and checks
#################################################################


@task
def tox(context):
    """
    Run tox default targets, usually all tests and BDD tests (see tox.ini)
    """
    context.run("poetry run tox")


@task()
def tox_p(context):
    """
    Same as 'tox', but with parallel runs
    """
    context.run("poetry run tox -p auto")


#################################################################
# linting
#################################################################


@task
def lint(context):
    """
    Check style with flake8
    """
    context.run(f"poetry run ruff check src tests")


#################################################################
# formatting
#################################################################


@task
def isort(context):
    context.run(f"poetry run isort src tests")


@task
def black(context):
    context.run(f"poetry run black src tests")


@task(isort, black)
def format(context):
    """
    Enforce correct format with isort and black
    """
    pass


@task
def format_check(context):
    """
    Check format for compliance with black and isort
    """
    context.run(f"poetry run isort -c src tests")
    context.run(f"poetry run black --check src tests")


#################################################################
# typing
#################################################################


@task
def type(context):
    context.run(f"poetry run mypy src tests")


#################################################################
# unit testing
#################################################################


@task
def test(context):
    """
    Run unit tests
    """
    context.run("poetry run pytest")


@task(aliases=["tox-test-default-version", "tox-py"])
def tox_test(context):
    """
    Run unit tests with the default Python
    """
    context.run("poetry run tox -e py")


@task(aliases=["tox-py311"])
def tox_test_py311(context):
    """
    Run unit tests with Python 3.11
    """
    context.run("poetry run tox -e py311")


@task(aliases=["tox-py310"])
def tox_test_py310(context):
    """
    Run unit tests with Python 3.10
    """
    context.run("poetry run tox -e py310")


@task(aliases=["tox-py39"])
def tox_test_py39(context):
    """
    Run unit tests with Python 3.9
    """
    context.run("poetry run tox -e py39")


@task(aliases=["tox-py38"])
def tox_test_py38(context):
    """
    Run unit tests with Python 3.8
    """
    context.run("poetry run tox -e py38")


@task(aliases=["tox-test-all-versions"])
def tox_test_all(context):
    """
    Run unit tests on each Python version declared
    """
    context.run("poetry run tox -e py311,py310,py39,py38,py37")


#################################################################
# git targets
#################################################################


@task
def prune_branches(context):
    """
    Prune obsolete local tracking branches and local branches
    """
    context.run("git remote prune origin")
    context.run(
        "git branch -vv | "
        "grep ': gone]'| "
        "grep -v '\\*' | "
        "awk '{ print $1; }' | "
        "xargs git branch -d"
    )


@task(aliases=["pbf"])
def prune_branches_force(context):
    """
    Same as prune-branches but force delete local branches
    """
    context.run("git remote prune origin")
    context.run(
        "git branch -vv | "
        "grep ': gone]'| "
        "grep -v '\\*' | "
        "awk '{ print $1; }' | "
        "xargs git branch -D"
    )


@task(post=[prune_branches_force], aliases=["pms"])
def post_pr_merge_sync(context):
    """
    Switch to dev, pull and run prune-branches-force task
    """
    context.run("git switch dev")
    context.run("git pull")


#################################################################
# Run all local tests and checks
#################################################################


@task(format, lint)
def all_checks(context):
    """
    Run all checks
    """
    pass


@task(test, all_checks)
def all_locals(context):
    """
    Run all local tests and checks
    """
    pass


#################################################################
# Tasks organization in namespaces
#################################################################


namespace = Collection()
namespace.add_task(run_ingestion)
namespace.add_task(copy_sample_files)

namespace_tox = Collection("tox_")
namespace_tox.add_task(tox_test, name="test")
namespace_tox.add_task(tox_test_all, name="test_all")
namespace_tox.add_task(tox_test_py311, name="test_py311")
namespace_tox.add_task(tox_test_py310, name="test_py310")
namespace_tox.add_task(tox_test_py39, name="test_py39")
namespace_tox.add_task(tox_test_py38, name="test_py38")

namespace_git = Collection("git")
namespace_git.add_task(prune_branches)
namespace_git.add_task(prune_branches_force)
namespace_git.add_task(post_pr_merge_sync)

namespace.add_collection(namespace_git)

namespace.add_task(clean)
namespace.add_task(clean_venv)
namespace.add_task(all_checks)
namespace.add_task(all_locals)
namespace.add_task(test)
namespace.add_task(isort)
namespace.add_task(black)
namespace.add_task(format)
namespace.add_task(format_check)
namespace.add_task(lint)
namespace.add_task(type)
namespace.add_task(tox)
namespace.add_task(tox_p)
