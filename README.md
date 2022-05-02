# SKI Combinator Parser

This project implements a simple parser and evaluator for SKI combinator expressions.

## Usage

```
$ ./parse_expr --help
Usage: ./parse_expr ski [--help|-h] [--silent|-s] [--noextensions|-n]
```

`--silent` disables printing the evaluation steps. `--noextensions` disables anything but the S, K, and I combinators.

## Examples

### Self-application
```
$./parse_expr '(S I I a)'
Parsed expression:
(S I I a)

Evaluation:
.. (S I I a)
>> (I a (I a))
>> (a (I a))
>>    (a)

~~ (a a)
```

### Y-combinator

```
$ ./parse_expr '(Y a b c)'
Parsed expression:
(Y a b c)

Evaluation:
.. (Y a b c)
>> (a (Y a) b c)
.. (a (Y a) b c)
.. (a (Y a) b c)

~~ (a (Y a) b c)

$ ./parse_expr -n -s '(Y a b c)'
(Y a b c)
```

### Number support and addition

```
./parse_expr -s '((+ 1 2) a b)'
(a (a (a b))) 
```

### Booleans
```
$ ./parse_expr -s '(T a b)'
a

$ ./parse_expr -s '(F a b)'
b

$ ./parse_expr -s '((and F F) a b)'
b
$ ./parse_expr -s '((and F T) a b)'

b
$ ./parse_expr -s '((and T F) a b)'
b

$ ./parse_expr -s '((and T T) a b)'
a

$ ./parse_expr -s '((or T F) a b)'
a

$ ./parse_expr -s '((not T) a b)'
b
```