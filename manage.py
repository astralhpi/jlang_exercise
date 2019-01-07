#!/usr/bin/env python3
import os
import subprocess
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('dirname', nargs=1)
def gen_input(dirname):
    with open(os.path.join(dirname, "input.txt")) as f,\
            open(os.path.join(dirname, "output.txt"), 'w') as fw:
        for line in f.readlines():
            line = line.strip()
            srcpath = os.path.join(dirname, dirname) + ".coco"
            args = line.split(' ')
            proc = subprocess.Popen(
                    ['coconut', '-q', '-r', srcpath, "--argv"] + args,
                    stdout=subprocess.PIPE)
            fw.write(proc.stdout.read().decode('utf-8'))


if __name__ == "__main__":
    cli()
