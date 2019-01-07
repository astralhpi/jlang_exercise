#!/usr/bin/env python3
import os
import subprocess
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('dirname', nargs=1)
def gen_output(dirname):
    with open(os.path.join(dirname, "input.txt")) as f,\
            open(os.path.join(dirname, "output.txt"), 'w') as of:
        for line in f.readlines():
            line = line.strip()
            srcpath = os.path.join(dirname, dirname) + ".coco"
            args = line.split(' ')
            proc = subprocess.Popen(
                    ['coconut-run', srcpath] + args,
                    stdout=subprocess.PIPE)
            of.write(proc.stdout.read().decode('utf-8'))


def run_python(dirname, input):
    srcpath = os.path.join(dirname, dirname) + ".py"
    proc = subprocess.Popen(
            ['python', srcpath] + input.split(' '),
            stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    return output


def run_ijs(dirname, input):
    srcpath = os.path.join(dirname, dirname) + ".ijs"
    code = '''
        load'{}'
        result =: {} {}
        echo result
    '''.format(srcpath, dirname, input)
    proc = subprocess.Popen(
            ['jc'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
    stdout = proc.communicate(input=code.encode('utf-8'))[0]
    return stdout.decode('utf-8')[12:-6]


def mark_space(s):
    return s.replace(' ', '_').replace('\n', '\\n')


@cli.command()
@click.argument('lang', nargs=1)
@click.argument('dirname', nargs=1)
def test(lang, dirname):
    with open(os.path.join(dirname, "input.txt")) as inputfile, \
            open(os.path.join(dirname, 'output.txt')) as outputfile:
        inlines, outlines = inputfile.readlines(), outputfile.readlines()
        for input, expected in zip(inlines, outlines):
            input = input.strip()

            if lang in ['py', 'python', 'py3', 'python3']:
                actual = run_python(dirname, input)
            elif lang in ['j', 'ijs']:
                actual = run_ijs(dirname, input)

            if actual == expected:
                print('PASS: ' + input)
            else:
                print('FAIL: ' + input)
                print("\texpected: ", mark_space(expected))
                print("\tactual: ", mark_space(actual))



if __name__ == "__main__":
    cli()
