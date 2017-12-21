"""
@author Gerard van Helden <drm@melp.nl>
@license DBAD, see <http://www.dbad-license.org/>

Simple j2 linter, useful for checking jinja2 template syntax
"""
import click
import jinja2
import os.path
from functools import reduce


class AbsolutePathLoader(jinja2.BaseLoader):
    def get_source(self, environment, path):
        if not os.path.exists(path):
            raise jinja2.TemplateNotFound(path)
        mtime = os.path.getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == os.path.getmtime(path)


def check(template, out, err, env=jinja2.Environment(loader=AbsolutePathLoader())):
    try:
        env.get_template(template)

        out.write("{}: {}\n".format(
            template,
            click.style('Syntax OK', fg='green'),
        ))
        return 0
    except jinja2.TemplateNotFound:
        err.write("{}: {}\n".format(
            template,
            click.style('File not found', fg='yellow'),
        ))
        return 2
    except jinja2.exceptions.TemplateSyntaxError as e:
        err.write(
            "{}: {}\n".format(
                template,
                click.style('Syntax check failed: {} in {} at {}'.format(
                    e.message,
                    e.filename,
                    e.lineno
                ), fg='red')
            )
        )
        return 1


def main(**kwargs):
    import sys
    try:
        sys.exit(reduce(lambda r, fn: r + check(fn, sys.stdout, sys.stderr, **kwargs), sys.argv[1:], 0))
    except IndexError:
        sys.stdout.write("Usage: j2lint.py filename [filename ...]\n")


if __name__ == "__main__":
    main()
