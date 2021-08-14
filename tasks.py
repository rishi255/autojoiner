import platform
from invoke import task


@task
def clean(c):
    if platform.system() == "Windows":
        c.run(
            "for %f in (dist build autojoiner.egg-info) do if exist %f rmdir /s /q %f",
            hide=True,
        )
    else:
        c.run("rm -rf dist build autojoiner.egg-info")
    return


@task
def make(c):
    clean(c)
    if platform.system() == "Windows":
        c.run("py setup.py sdist bdist_wheel")
    else:
        c.run("python3 setup.py sdist bdist_wheel")


@task
def upload(c, actual=False):
    if actual:
        print("ACTUAL CALLED!")
        c.run("twine upload dist/*")
    else:
        print("Test upload.")
        c.run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")


@task
def bump(c, part="patch", actual=False):
    if actual:
        c.run(f"bumpversion {part} --allow-dirty --verbose")
        print("**** NOT A DRY RUN! Version actually bumped. **** ")
    else:
        c.run(f"bumpversion {part} --allow-dirty --verbose --dry-run")
