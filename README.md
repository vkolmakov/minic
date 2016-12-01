# minic

A front-end for a compiler for a small subset of C. Written in [Python 3.5.2](https://www.python.org) with [rply](https://github.com/alex/rply)

## Project description

TODO

## Usage

__run.py__ script is provided.

Usage:

```bash
$ python3 run.py /path/to/source_file  # will log all results to stdout

$ python3 run.py /path/to/source_file --output /path/to/out_file  # will log results to specified file
```

__run.py__ will log output from lexer, parser and typechecker.

### Sample run

Given file `./source.c`

```c
int x;
if (x) {
  x = 1.0;
} else {
  x = 0;
}
```

```bash
$ python3 run.py ./source.c --output ./out
```

Will produce file `out`:

```
**********************************
[2016-11-26 17:54:52.623765]-START
**********************************

**********************************
[2016-11-26 17:54:52.711003]-LEXER
**********************************
Token('INT_TYPE', 'int')
Token('ID', 'x')
Token('SEMI', ';')
Token('IF', 'if')
Token('LPAREN', '(')
Token('ID', 'x')
Token('RPAREN', ')')
Token('LCURLY', '{')
Token('ID', 'x')
Token('EQUAL', '=')
Token('FLOAT', '1.0')
Token('SEMI', ';')
Token('RCURLY', '}')
Token('ELSE', 'else')
Token('LCURLY', '{')
Token('ID', 'x')
Token('EQUAL', '=')
Token('INTEGER', '0')
Token('SEMI', ';')
Token('RCURLY', '}')
***********************************
[2016-11-26 17:54:52.712483]-PARSER
***********************************
Block(
  Declaration(type=int, ids=[ID(name=x)])
  IfStatement(otherwise=Block(
  Assignment(id=ID(name=x), expr=Integer(value=0))
), then=Block(
  Assignment(id=ID(name=x), expr=Float(value=1.0))
), cond=ID(name=x))
)
****************************************
[2016-11-26 17:54:52.712749]-TYPECHECKER
****************************************
ErrorReport(
  TypeError(Assignment(id=ID(name=x), expr=Float(value=1.0)))
)

*********************************
[2016-11-26 17:54:52.712850]-DONE
*********************************
```

## Running and Developing

```bash
$ make watch  # watch directory for changes and run tests on changes

$ make test  # run the test suite

$ make clean  # remove all .pyc files
```

All of the test files will be in the same directory with the tested modules and end with `_test.py`


